import threading
import time
import random

class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork, stop_flag):
        super().__init__()
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.stop_flag = stop_flag

    # Метод, описывающий действия философа во время выполнения потока
    def run(self):
        while not self.stop_flag.is_set():
            self.think()
            self.dine()
    # Метод, представляющий размышления философа

    def think(self):
        print(f"{self.name} размышляет.")
        time.sleep(random.uniform(1, 5))  # митируем время для размышления

    # Метод, представляющий прием пищи философа

    def dine(self):
        with self.left_fork:
            print(f"{self.name} взял левую вилку.")
            with self.right_fork:
                print(f"{self.name} взял правую вилку и обедает.")
                # Имитация времени приема пищи
                time.sleep(random.uniform(1, 5))  
            print(f"{self.name} положил правую вилку.")
        print(f"{self.name} положил левую вилку.")

if __name__ == "__main__":

    num_philosophers = 4

    forks = [threading.Lock() for _ in range(num_philosophers)]  # Создание вилок
    stop_flag = threading.Event()  # Флаг для остановки симуляции

    # Создание философов с использованием созданных вилок и флага
    philosophers = [Philosopher(f"Философ {i}", forks[i], forks[(i + 1) % num_philosophers], stop_flag)
                    for i in range(num_philosophers)]

    # Запуск потоков для каждого философа
    for philosopher in philosophers:
        philosopher.start()

    time.sleep(30)  # Запустить симуляцию на 30 секунд

    stop_flag.set()  # Остановить симуляцию

    # Дождаться завершения всех потоков
    for philosopher in philosophers:
        philosopher.join()