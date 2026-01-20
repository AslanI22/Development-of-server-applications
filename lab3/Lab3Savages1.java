package lab3;
import java.io.PrintStream;
import java.io.UnsupportedEncodingException;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Lab3Savages1 {
    private static final int POT_CAPACITY = 5;
    private static int portionsInPot = POT_CAPACITY;
    
    private static final Lock lock = new ReentrantLock();
    private static final Condition potNotEmpty = lock.newCondition();
    private static final Condition potEmpty = lock.newCondition();
    
    public static void main(String[] args) throws InterruptedException {
        setupEncoding();
        
        int numberOfSavages = 8;
        
        Thread cook = new Thread(new Cook());
        Thread[] savages = new Thread[numberOfSavages];
        
        for (int i = 0; i < numberOfSavages; i++) {
            savages[i] = new Thread(new Savage(i));
        }
        
        System.out.println("Начинается обед дикарей!");
        System.out.println("Кастрюля вмещает " + POT_CAPACITY + " порций");
        System.out.println("Дикарей: " + numberOfSavages);

        
        cook.start();
        for (Thread savage : savages) {
            savage.start();
        }
        
        for (Thread savage : savages) {
            savage.join();
        }
        
        cook.interrupt();
        

        System.out.println("Все дикари поели! Обед окончен.");
    }
    
    private static void setupEncoding() {
        try {
            System.setOut(new PrintStream(System.out, true, "UTF-8"));
        } catch (UnsupportedEncodingException e) {
            System.out.println("UTF-8 not supported, using default encoding");
        }
    }
    
    static class Cook implements Runnable {
        @Override
        public void run() {
            try {
                while (!Thread.currentThread().isInterrupted()) {
                    lock.lock();
                    try {
                        while (portionsInPot > 0) {
                            potEmpty.await();
                        }
                        
                        portionsInPot = POT_CAPACITY;
                        System.out.println("Повар наполнил кастрюлю! Порций: " + portionsInPot);
                        
                        potNotEmpty.signalAll();
                    } finally {
                        lock.unlock();
                    }
                }
            } catch (InterruptedException e) {
                System.out.println("🍳 Повар закончил работу");
            }
        }
    }
    
    static class Savage implements Runnable {
        private final int id;
        
        public Savage(int id) {
            this.id = id;
        }
        
        @Override
        public void run() {
            try {
                lock.lock();
                try {
                    while (portionsInPot == 0) {
                        System.out.println("Дикарь " + id + " ждет пока наполнят кастрюлю");
                        potNotEmpty.await();
                    }
                    
                    portionsInPot--;
                    System.out.println("Дикарь " + id + " взял порцию. Осталось: " + portionsInPot);
                    
                    if (portionsInPot == 0) {
                        System.out.println("Кастрюля пуста! Зовем повара...");
                        potEmpty.signal();
                    }
                } finally {
                    lock.unlock();
                }
                
                Thread.sleep(100);
                
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}