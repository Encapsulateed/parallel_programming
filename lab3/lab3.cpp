#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

#define N 1024 // Размерность матрицы

// Умножение матрицы на вектор
double* mult_m_v(double** m, double* v) {
    double* res;
    res = (double*)malloc(sizeof(double) * N);
    int i;

    // Параллельный цикл для умножения матрицы на вектор
#pragma omp parallel for shared(m, v, res) private(i)
    for (i = 0; i < N; i++) {
        res[i] = 0;

        for (int j = 0; j < N; j++) {
            res[i] += (m[i][j] * v[j]);
        }
    }
    return res;
}

// Умножение вектора на скаляр
void mult_v_s(double* v, double s) {
    int i;

    // Параллельный цикл для умножения вектора на скаляр
#pragma omp parallel for shared(v) private(i)
    for (i = 0; i < N; i++) {
        v[i] *= s;
    }
}

// Вычитание векторов
void difference(double* v1, double* v2) {
    int i;

    // Параллельный цикл для вычитания векторов
#pragma omp parallel for shared(v1, v2) private(i)
    for (i = 0; i < N; i++) {
        v1[i] -= v2[i];
    }
}

// Норма вектора
double norm(double* v) {
    int i;
    int len = 0;

    // Параллельный цикл для вычисления квадрата нормы вектора
#pragma omp parallel for shared(v) private(i) reduction(+:len)
    for (i = 0; i < N; i++) {
        len += (v[i] * v[i]);
    }

    len = sqrt(len);
    return len;
}

// Скалярное произведение векторов
double scalar_product(double* v1, double* v2) {
    int i;
    double len = 0;

    // Параллельный цикл для вычисления скалярного произведения векторов
#pragma omp parallel for shared(v1, v2) private(i) reduction(+:len)
    for (i = 0; i < N; i++) {
        len += (v1[i] * v2[i]);
    }

    return len;
}

int main() {
#ifdef _OPENMP
    printf("OpenMP is supported!\n");
#endif

    double eps = 0.0000001;
    double tao;

    // Выделение памяти для матрицы A
    double **A;
    A = (double**)malloc(sizeof(double*) * N);

    // Инициализация матрицы A
    for (int i = 0; i < N; i++) {
        A[i] = (double*)malloc(sizeof(double) * N);

        for (int j = 0; j < N; j++) {
            if (i == j) {
                A[i][j] = 2.0;
            } else {
                A[i][j] = 1.0;
            }
        }
    }

    // Выделение памяти для векторов x и b
    double* x;
    double* b;
    x = (double*)malloc(sizeof(double) * N);
    b = (double*)malloc(sizeof(double) * N);

    // Инициализация векторов x и b
    for (int i = 0; i < N; i ++) {
        x[i] = 0;
        b[i] = N + 1;
    }

    double* y;
    double* ay;

    while (1) {
        // y = Ax-b
        y = mult_m_v(A, x);
        difference(y, b);

        // Нормировка до достижения сходимости
        if ((norm(x) / norm(y)) < eps) {
            printf("Similar!");
            free(y);
            break;
        }

        // ay = A * y
        ay = mult_m_v(A, y);

        tao = scalar_product(y, ay) / scalar_product(ay, ay);
        // x = x - tao*y
        mult_v_s(y, tao);
        difference(x, y);

        free(y);
        free(ay);
    }

    // Освобождение памяти
    free(x);
    free(b);

    for (int i = 0; i < N; i++) {
        free(A[i]);
    }

    free(A);

    return 0;
}
