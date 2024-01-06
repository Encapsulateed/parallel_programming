import time
import numpy as np
from numpy.linalg import norm, det
import sys
from mpi4py import MPI

# Установка начального значения для генерации случайных чисел
np.random.seed(42)

# Инициализация MPI (Message Passing Interface)
comm = MPI.COMM_WORLD
rank = comm.Get_rank()  # Номер текущего процесса
size = comm.Get_size()  # Общее количество процессов

# Размер матрицы и размер блока берутся из аргументов командной строки
MATRIX_SIZE = 2 ** 13
MATRIX_SPLIT = int(sys.argv[1])

# Создание симметричной положительно определенной матрицы 'a'
a = np.zeros((MATRIX_SIZE, MATRIX_SIZE), dtype=np.double)
for i in range(MATRIX_SIZE):
    for j in range(MATRIX_SIZE):
        if i == j:
            a[i, j] = 2
        else:
            a[i, j] = 1

# Выбор тестового случая в зависимости от аргумента командной строки
if sys.argv[2] == "1":
    # Тест 1: установка значений векторов b и x
    b = np.ones(MATRIX_SIZE, dtype=np.double) * (2 ** 13 + 1)
    x = np.zeros(MATRIX_SIZE, dtype=np.double)
elif sys.argv[2] == "2":
    # Тест 2: генерация случайного вектора u и вычисление вектора b
    u = np.zeros(MATRIX_SIZE, dtype=np.double)
    for i in range(MATRIX_SIZE):
        u[i] = np.random.random()
    b = np.matmul(a, u[:, None]).T[0]
    x = np.zeros(MATRIX_SIZE, dtype=np.double)


# Установка значения epsilon для оценки точности вычислений
epsilon = 1e-5

# Функция для умножения матрицы на вектор
def mult_matrix_by_vector(m, v):
    v = v[:, None]
    # Буфер для вычислений
    part_a = np.empty(shape=(MATRIX_SIZE // MATRIX_SPLIT, MATRIX_SIZE), dtype=np.double)
  
    comm.Scatter(m, part_a, root=0)
    # Умножение части матрицы на в  ектор
    part_a = part_a @ v
    # Выделение места под результат
    res = None
    if rank == 0:
        res = np.empty(shape=(MATRIX_SIZE, 1), dtype=np.double)
    # Сбор результатов на процессе с rank=0
    comm.Gather(part_a, res, root=0)

    return comm.bcast(res, root=0).T[0]

# Основная функция программы
def main():
    global x

    old_crit = 0  # Значение критерия на предыдущей итерации
    i = 0  # Счетчик итераций
    while True:
        i += 1
        y = mult_matrix_by_vector(a, x) - b
        ay = mult_matrix_by_vector(a, y)
        flag = False
        if rank == 0:
            crit = norm(y) / norm(b)
            if crit < epsilon or crit == old_crit:
                flag = True
            else:
                old_crit = crit
                tao = (y.dot(ay)) / (ay.dot(ay))
                x = x - tao * y

        # Рассылка флага о завершении и проверка условия выхода
        if comm.bcast(flag, root=0):
            break
        x = comm.bcast(x, root=0)

# Запуск основной функции при выполнении скрипта
if __name__ == '__main__':
    t = time.time()
    main()
    # Вывод результата времени выполнения для процесса с rank=0
    if rank == 0:
        print(MATRIX_SPLIT, time.time() - t)
