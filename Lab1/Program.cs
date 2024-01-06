using System;
using System.Diagnostics;
using System.Threading.Tasks;

class MatrixMultiplication
{
    static int[,] MultiplyMatrices(int[,] matrixA, int[,] matrixB)
    {
        int n = matrixA.GetLength(0); // Количество строк в матрице A
        int m = matrixB.GetLength(1); // Количество столбцов в матрице B
        int[,] result = new int[n, m]; // Создание результирующей матрицы C размерности n x m

        Parallel.For(0, n, i =>
        {

            for (int j = 0; j < m; j++)
            {
                for (int k = 0; k < matrixA.GetLength(1); k++)
                {
                    result[i, j] += matrixA[i, k] * matrixB[k, j];
                }
            }
        });

        return result;
    }

    static int[,] Fill_Matrix(int[,] matrixA)
    {
        int n = matrixA.GetLength(0); // Количество строк в матрице A
        int m = matrixA.GetLength(1); // Количество строк в матрице A

        int[,] result = new int[n, m];

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                for (int k = 0; k < matrixA.GetLength(1); k++)
                {
                    result[i, j] += new Random().Next(0, 10);
                }
            }
        }

        return result;
    }

    static void Print(int[,] Matrix)
    {
        int n = Matrix.GetLength(0); // Количество строк в матрице A
        int m = Matrix.GetLength(1); // Количество строк в матрице A

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                Console.Write(Matrix[i, j].ToString() + " ");
            }
            Console.WriteLine();
        }
    }

    static int[,] MultiplyMatrices_non_parallel(int[,] matrixA, int[,] matrixB)
    {
        int n = matrixA.GetLength(0); // Количество строк в матрице A
        int m = matrixA.GetLength(1); // Количество столбцов в матрице A (и строк в матрице B)

        int[,] result = new int[n, m]; // Результирующая матрица C размерности n x p

        if (m != matrixB.GetLength(0))
        {
            throw new ArgumentException("Несовместимые размерности матриц для умножения.");
        }

        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < m; j++)
            {
                int sum = 0;
                for (int k = 0; k < m; k++)
                {
                    sum += matrixA[i, k] * matrixB[k, j];
                }
                result[i, j] = sum;
            }
        }

        return result;
    }

    static void Main()
    {

        int n = 500; // Количество строк в матрице A
        int m = 500; // Количество столбцов в матрице B
        int[,] matrixA = new int[n, m]; // Создание матрицы A размерности n x m
        int[,] matrixB = new int[m, n]; // Создание матрицы B размерности m x n

        matrixA = Fill_Matrix(matrixA);
        matrixB = Fill_Matrix(matrixB);

        // Заполнение матриц A и B данными (ваш код)
        Console.WriteLine("start");

        Stopwatch stopwatch = new Stopwatch();
        stopwatch.Start();

        int[,] result = MultiplyMatrices(matrixA, matrixB);

        stopwatch.Stop();
        Console.WriteLine($"Время выполнения параллельного алгоритма: {stopwatch.ElapsedMilliseconds} мс");

        stopwatch.Start();

        int[,] result_non_parallel = MultiplyMatrices_non_parallel(matrixA, matrixB);
        stopwatch.Stop();
        Console.WriteLine($"Время выполнения  алгоритма: {stopwatch.ElapsedMilliseconds} мс");
      
    }
}
