"""
Лабораторная работа №1
Осипова Анна, вариант 17.

Итерационные методы:
- квадратный корень: метод Ньютона;
- кубический корень: метод Ньютона;
- натуральный логарифм: степенной ряд.

Дополнительное требование Д6:
проверка корректности входных данных и понятные сообщения
при ошибочном вводе.
"""
import math
from typing import Callable, Tuple


EPS = 1e-6
N_MAX = 100


def validate_number(value, name: str) -> float:
    """Проверяет, что значение является конечным числом."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name}: требуется ввести число.")
    if not math.isfinite(value):
        raise ValueError(f"{name}: число должно быть конечным.")
    return value


def sqrt_newton(a: float, eps: float = EPS, n_max: int = N_MAX) -> Tuple[float, int]:
    """Вычисляет sqrt(a) методом Ньютона с критерием по невязке."""
    a = validate_number(a, "a")
    if a < 0:
        raise ValueError("a < 0: квадратный корень из отрицательного числа не определён.")
    if eps <= 0:
        raise ValueError("eps должна быть положительной.")
    if a == 0:
        return 0.0, 0

    x = 1.0  # x0 по варианту 17
    for n in range(1, n_max + 1):
        x_new = 0.5 * (x + a / x)
        if abs(x_new * x_new - a) < eps:
            return x_new, n
        x = x_new
    raise RuntimeError(f"Точность не достигнута за {n_max} итераций.")


def cbrt_newton(b: float, eps: float = EPS, n_max: int = N_MAX) -> Tuple[float, int]:
    """Вычисляет кубический корень методом Ньютона с критерием по невязке."""
    b = validate_number(b, "b")
    if eps <= 0:
        raise ValueError("eps должна быть положительной.")
    if b == 0:
        return 0.0, 0

    sign = -1.0 if b < 0 else 1.0
    value = abs(b)
    x = 1.0  # x0 по варианту 17

    for n in range(1, n_max + 1):
        x_new = (2.0 * x + value / (x * x)) / 3.0
        result = sign * x_new
        if abs(result ** 3 - b) < eps:
            return result, n
        x = x_new
    raise RuntimeError(f"Точность не достигнута за {n_max} итераций.")


def ln_series(c: float, eps: float = EPS, n_max: int = 100000) -> Tuple[float, int]:
    """Вычисляет ln(c) рядом 2*sum(y^(2k+1)/(2k+1)), y=(c-1)/(c+1)."""
    c = validate_number(c, "c")
    if c <= 0:
        raise ValueError("c <= 0: аргумент натурального логарифма должен быть положительным.")
    if eps <= 0:
        raise ValueError("eps должна быть положительной.")

    y = (c - 1.0) / (c + 1.0)
    y2 = y * y
    power = y
    total = 0.0

    for k in range(n_max):
        term = 2.0 * power / (2 * k + 1)
        if abs(term) < eps:
            return total, k
        total += term
        power *= y2

    raise RuntimeError(f"Точность не достигнута за {n_max} итераций.")


def iterations_table(func: Callable, value: float, eps: float = EPS, n_max: int = N_MAX):
    """Возвращает строки таблицы итераций для метода Ньютона."""
    rows = []
    if func is sqrt_newton:
        x = 1.0
        for n in range(1, n_max + 1):
            x_new = 0.5 * (x + value / x)
            diff = abs(x_new - x)
            rows.append((n, x_new, diff, abs(x_new * x_new - value)))
            if abs(x_new * x_new - value) < eps:
                break
            x = x_new
    elif func is cbrt_newton:
        sign = -1.0 if value < 0 else 1.0
        b = abs(value)
        x = 1.0
        for n in range(1, n_max + 1):
            x_new_abs = (2.0 * x + b / (x * x)) / 3.0
            x_new = sign * x_new_abs
            diff = abs(x_new - sign * x)
            rows.append((n, x_new, diff, abs(x_new ** 3 - value)))
            if abs(x_new ** 3 - value) < eps:
                break
            x = x_new_abs
    return rows


def demonstrate_invalid_input():
    """Демонстрация требования Д6."""
    tests = [
        ("sqrt(-1)", lambda: sqrt_newton(-1)),
        ("ln(0)", lambda: ln_series(0)),
        ("sqrt('abc')", lambda: sqrt_newton("abc")),
        ("ln(-5)", lambda: ln_series(-5)),
    ]
    print("\nДемонстрация проверки ошибочных данных:")
    for title, action in tests:
        try:
            action()
        except (ValueError, RuntimeError) as exc:
            print(f"  {title:14} -> Ошибка: {exc}")


def main():
    a, b, c = 0.8, -216.0, 0.05

    print("Лабораторная работа №1")
    print("Осипова Анна, вариант 17")
    print(f"Параметры: a={a}, b={b}, c={c}, eps={EPS:g}, критерий: по невязке, x0=1\n")

    calculations = [
        ("sqrt(a)", sqrt_newton, a, math.sqrt(a)),
        ("cbrt(b)", cbrt_newton, b, math.copysign(abs(b) ** (1 / 3), b)),
        ("ln(c)", ln_series, c, math.log(c)),
    ]

    print(f"{'Функция':<10} {'Результат':>18} {'Эталон':>18} {'Погрешность':>16} {'Итерации':>10}")
    print("-" * 78)
    for name, func, arg, reference in calculations:
        result, count = func(arg)
        error = abs(result - reference)
        print(f"{name:<10} {result:>18.12f} {reference:>18.12f} {error:>16.3e} {count:>10}")

    print("\nТаблица итераций для корней (Д6 + контроль процесса):")
    for name, func, arg, _ in calculations[:2]:
        print(f"\n{name}:")
        print(f"{'n':>3} {'x_n':>18} {'|x_n-x_(n-1)|':>20} {'невязка':>16}")
        for n, x, diff, residual in iterations_table(func, arg):
            print(f"{n:>3} {x:>18.12f} {diff:>20.6e} {residual:>16.6e}")

    demonstrate_invalid_input()


if __name__ == "__main__":
    main()
