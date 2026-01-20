package lab3;
public class lab3nosync {
    private static int counter = 0;
    
    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Usage: java Lab3NoSync <n> <m>");
            System.out.println("where n - number of increment threads, m - number of decrement threads");
            return;
        }
        
        int n = Integer.parseInt(args[0]); 
        int m = Integer.parseInt(args[1]); 
        
        Thread[] incrementThreads = new Thread[n];
        Thread[] decrementThreads = new Thread[m];
        
        long startTime = System.currentTimeMillis();
        
        for (int i = 0; i < n; i++) {
            incrementThreads[i] = new Thread(new IncrementTask());
            incrementThreads[i].start();
        }
        
        for (int i = 0; i < m; i++) {
            decrementThreads[i] = new Thread(new DecrementTask());
            decrementThreads[i].start();
        }
        
        try {
            for (int i = 0; i < n; i++) {
                incrementThreads[i].join();
            }
            for (int i = 0; i < m; i++) {
                decrementThreads[i].join();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        long endTime = System.currentTimeMillis();
        long executionTime = endTime - startTime;
        
        System.out.println("Final counter value: " + counter);
        System.out.println("Execution time: " + executionTime + " ms");
    }
    
    static class IncrementTask implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < 100000; i++) {
                int local = counter;
                local++;
                counter = local;
            }
        }
    }
    
    static class DecrementTask implements Runnable {
        @Override
        public void run() {
            for (int i = 0; i < 100000; i++) {
                int local = counter;
                local--;
                counter = local;
            }
        }
    }
}