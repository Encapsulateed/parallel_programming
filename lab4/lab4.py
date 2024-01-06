import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork, stop_event):
        super().__init__(name=name)
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.stop_event = stop_event


    '''
    Метод run представляет действия философа, выполняемые в отдельном потоке.
    Философ поочередно размышляет и обедает, пока не поступит сигнал остановки.
    '''
    def run(self):
        while not self.stop_event.is_set():
            self.think()
            self.dine()

    # Пауза
    '''
    Метод think представляет процесс размышления философа. 
    Выводится сообщение и выполняется случайная пауза.
    '''
    def think(self):
        print(f"{self.name} Размышляет.")
        time.sleep(random.uniform(1, 3))

    # Обед. Берем левую и правую вилку, а потом кладем на место
    '''
      Метод dine представляет процесс обеда философа.
      Философ пытается взять левую вилку и, если успешно, пытается взять правую. 
      Если обе вилки взяты, философ ест, а затем кладет вилки на место.
    '''
    def dine(self):
        print(f"{self.name} голоден и пытается взять вилки")
        acquired_left = False
        acquired_right = False

        while not acquired_left and not self.stop_event.is_set():
            acquired_left = self.left_fork.acquire(timeout=random.randint(1, 3))

        if acquired_left:
            print(f"{self.name} взял левую вилку.")
            # Попытка взять правую вилку
            while not acquired_right and not self.stop_event.is_set():
                acquired_right = self.right_fork.acquire(timeout=1)

            if acquired_right:
                print(f"{self.name} взял правую вилку и ест.")
                time.sleep(random.uniform(1, 3))
                print(f"{self.name} опустить правую вилку.")
                self.right_fork.release()

            print(f"{self.name} опустить левую вилку.")
            self.left_fork.release()


def main():
    num_philosophers = 10
    forks = [threading.Lock() for _ in range(num_philosophers)] # Список мьютексов
    stop_event = threading.Event()

    philosophers = [Philosopher(f"Философ {i}", forks[i], forks[(i + 1) % num_philosophers], stop_event) for i in
                    range(num_philosophers)] # Потоки

    try:
        for philosopher in philosophers:
            philosopher.start()

        time.sleep(10)  # Программа работает 10 секунд

    finally:
        stop_event.set()
        for philosopher in philosophers:
            philosopher.join()


if __name__ == "__main__":
    main()
