def f(x: float) -> float:
    return x ** 2


def df(x: float) -> float:
    return 2 * x


def g(x: float) -> float:
    return x + 2


def dg(x: float) -> float:
    return 1.0


def h(x: float) -> float:
    return f(x) * g(x)


def product_rule_dh(x: float) -> float:
    return df(x) * g(x) + f(x) * dg(x)


def expanded_dh(x: float) -> float:
    # h(x) = x^3 + 2x^2  =>  h'(x) = 3x^2 + 4x
    return 3 * (x ** 2) + 4 * x


def central_difference_dh(x: float, eps: float = 1e-6) -> float:
    return (h(x + eps) - h(x - eps)) / (2 * eps)


if __name__ == "__main__":
    for x_val in [0.0, 1.0, 2.0, -3.5]:
        pr = product_rule_dh(x_val)
        ex = expanded_dh(x_val)
        fd = central_difference_dh(x_val)
        assert abs(pr - ex) < 1e-12, f"Algebra mismatch at x={x_val}"
        assert abs(pr - fd) < 1e-6, f"Numerical mismatch at x={x_val}"
        print(f"x={x_val:>4}: ProductRule={pr:>8.4f} | Expanded={ex:>8.4f} | FiniteDiff={fd:>8.4f} [OK]")