"""Расширенные эксперименты для лабораторной работы, вариант 17."""
import math
from main import sqrt_newton, cbrt_newton, ln_series

A, B, C = 0.8, -216.0, 0.05


def show_accuracy():
    print("Проверка точности для eps = 1e-6")
    items = [
        ("sqrt(0.8)", sqrt_newton, A, math.sqrt(A)),
        ("cbrt(-216)", cbrt_newton, B, math.copysign(abs(B) ** (1/3), B)),
        ("ln(0.05)", ln_series, C, math.log(C)),
    ]
    for name, func, arg, ref in items:
        value, n = func(arg)
        print(f"{name:14} value={value:.12f}, reference={ref:.12f}, "
              f"error={abs(value-ref):.3e}, iterations={n}")


def compare_eps():
    print("\nЗависимость числа итераций от eps")
    print(f"{'eps':>12} {'sqrt':>8} {'cbrt':>8} {'ln':>8}")
    for power in range(1, 11):
        eps = 10 ** (-power)
        counts = []
        for func, arg in [(sqrt_newton, A), (cbrt_newton, B), (ln_series, C)]:
            try:
                _, n = func(arg, eps)
            except RuntimeError:
                n = None
            counts.append(n)
        print(f"{eps:12.0e} {str(counts[0]):>8} {str(counts[1]):>8} {str(counts[2]):>8}")


if __name__ == "__main__":
    show_accuracy()
    compare_eps()
