"""
Лабораторная работа № 1
Дисциплина: Теория алгоритмов
Направление: 38.03.05 «Бизнес-информатика»
Вариант: 0

Итерационные методы вычисления:
- квадратного корня методом Ньютона;
- кубического корня методом Ньютона;
- натурального логарифма степенным рядом.

В вычислительных функциях не используются math.sqrt(), math.log()
и **0.5. Библиотека math используется только для эталонных значений.
"""

import math


EPS = 1e-6
N_MAX = 100


def sqrt_newton(a, eps=EPS, n_max=N_MAX):
    """Вычисление sqrt(a) методом Ньютона."""
    if a < 0:
        raise ValueError(
            "Ошибка: подкоренное выражение не может быть отрицательным."
        )

    if a == 0:
        return 0.0, 0

    x = a if a >= 1 else 1.0

    for n in range(1, n_max + 1):
        x_new = 0.5 * (x + a / x)

        if abs(x_new - x) < eps:
            return x_new, n

        x = x_new

    raise RuntimeError(
        "Точность не достигнута за заданное число итераций."
    )


def cbrt_newton(b, eps=EPS, n_max=N_MAX):
    """Вычисление кубического корня методом Ньютона."""
    if b == 0:
        return 0.0, 0

    sign = -1 if b < 0 else 1
    b_abs = abs(b)

    x = b_abs if b_abs >= 1 else 1.0

    for n in range(1, n_max + 1):
        x_new = (2 * x + b_abs / (x * x)) / 3

        if abs(x_new - x) < eps:
            return sign * x_new, n

        x = x_new

    raise RuntimeError(
        "Точность не достигнута за заданное число итераций."
    )


def ln_series(c, eps=EPS, n_max=10000):
    """
    Вычисление ln(c) рядом:
    ln(c) = 2 * (y + y^3/3 + y^5/5 + ...),
    где y = (c - 1) / (c + 1).

    Возвращает (результат, число использованных итераций).
    """
    if c <= 0:
        raise ValueError(
            "Ошибка: аргумент логарифма должен быть положительным."
        )

    y = (c - 1) / (c + 1)
    y2 = y * y
    power = y
    total = 0.0

    for k in range(n_max):
        term = 2 * power / (2 * k + 1)

        if abs(term) < eps:
            return total, k

        total += term
        power *= y2

    raise RuntimeError(
        "Точность не достигнута за заданное число итераций."
    )


def print_iteration_table_sqrt(a, eps=EPS):
    """Печать таблицы итераций для квадратного корня."""
    x = a if a >= 1 else 1.0
    print("\nИтерации для sqrt(a):")
    print(f"{'n':>3} {'x_n':>18} {'|x_n-x_(n-1)|':>20}")
    print("-" * 45)
    print(f"{0:>3} {x:>18.12f} {'-':>20}")

    for n in range(1, N_MAX + 1):
        x_new = 0.5 * (x + a / x)
        difference = abs(x_new - x)
        print(f"{n:>3} {x_new:>18.12f} {difference:>20.12e}")

        if difference < eps:
            break
        x = x_new


def print_iteration_table_cbrt(b, eps=EPS):
    """Печать таблицы итераций для кубического корня."""
    sign = -1 if b < 0 else 1
    b_abs = abs(b)
    x = b_abs if b_abs >= 1 else 1.0

    print("\nИтерации для cbrt(b):")
    print(f"{'n':>3} {'x_n':>18} {'|x_n-x_(n-1)|':>20}")
    print("-" * 45)
    print(f"{0:>3} {sign * x:>18.12f} {'-':>20}")

    for n in range(1, N_MAX + 1):
        x_new = (2 * x + b_abs / (x * x)) / 3
        difference = abs(x_new - x)
        print(f"{n:>3} {sign * x_new:>18.12f} {difference:>20.12e}")

        if difference < eps:
            break
        x = x_new


def main():
    # Данные варианта 0
    a = 2
    b = 10
    c = 5
    eps = 1e-6

    sqrt_value, sqrt_iterations = sqrt_newton(a, eps)
    cbrt_value, cbrt_iterations = cbrt_newton(b, eps)
    ln_value, ln_iterations = ln_series(c, eps)

    # Эталонные значения используются только для проверки.
    sqrt_reference = math.sqrt(a)
    cbrt_reference = b ** (1 / 3)
    ln_reference = math.log(c)

    sqrt_error = abs(sqrt_value - sqrt_reference)
    cbrt_error = abs(cbrt_value - cbrt_reference)
    ln_error = abs(ln_value - ln_reference)

    print("=" * 95)
    print("ЛАБОРАТОРНАЯ РАБОТА № 1 — ВАРИАНТ 0")
    print("Итерационные методы вычисления элементарных функций")
    print("=" * 95)

    print(
        f"{'Функция':<12}"
        f"{'Аргумент':>12}"
        f"{'Результат':>20}"
        f"{'Эталон':>20}"
        f"{'Погрешность':>18}"
        f"{'Итерации':>12}"
    )
    print("-" * 95)

    print(
        f"{'sqrt':<12}"
        f"{a:>12}"
        f"{sqrt_value:>20.12f}"
        f"{sqrt_reference:>20.12f}"
        f"{sqrt_error:>18.2e}"
        f"{sqrt_iterations:>12}"
    )

    print(
        f"{'cbrt':<12}"
        f"{b:>12}"
        f"{cbrt_value:>20.12f}"
        f"{cbrt_reference:>20.12f}"
        f"{cbrt_error:>18.2e}"
        f"{cbrt_iterations:>12}"
    )

    print(
        f"{'ln':<12}"
        f"{c:>12}"
        f"{ln_value:>20.12f}"
        f"{ln_reference:>20.12f}"
        f"{ln_error:>18.2e}"
        f"{ln_iterations:>12}"
    )

    print("\nТребуемая точность:", eps)

    print_iteration_table_sqrt(a, eps)
    print_iteration_table_cbrt(b, eps)


if __name__ == "__main__":
    main()
