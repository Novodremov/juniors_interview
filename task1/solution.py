def strict(func):
    """
    Декоратор, проверяющий соответствие поданных на вход функции аргументов
    аннотациям в теле функции.
    """
    def wrapper(*args, **kwargs):
        # Получаем общий список величин из args и kwargs.
        all_values = list(args)
        all_values.extend(kwargs.values())
        # Получаем аннотации типов всех аргументов.
        annotations = func.__annotations__
        annotations.pop('return', None)
        # Пользуясь тем, что словарь с аннотациями упорядочен, можем сразу
        # проверить и позиционные, и именованные аргументы.
        for arg_name, arg_value in zip(annotations.keys(), all_values):
            expected_type = annotations[arg_name]
            # Вместо isinstance используем type для более строгой проверки.
            if type(arg_value) is not expected_type:
                raise TypeError(
                    f"Argument '{arg_name}' must be {expected_type.__name__}, "
                    f"got {type(arg_value).__name__}"
                )
        return func(*args, **kwargs)
    return wrapper


# Объявляем несколько функций, проводим тесты.
@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def greet(name: str) -> str:
    return f"Hello, {name}!"


@strict
def divide(x: float, y: float) -> float:
    return x / y


@strict
def is_even(n: int) -> bool:
    return n % 2 == 0


assert sum_two(1, 2) == 3
try:
    sum_two(1, 2.4)
except TypeError as e:
    assert str(e) == "Argument 'b' must be int, got float"

assert greet("Alice") == "Hello, Alice!"
try:
    greet(123)
except TypeError as e:
    assert str(e) == "Argument 'name' must be str, got int"

assert divide(10.0, 2.0) == 5.0
try:
    divide(10.0, "2")
except TypeError as e:
    assert str(e) == "Argument 'y' must be float, got str"

assert is_even(4) is True
assert is_even(5) is False
try:
    is_even("4")
except TypeError as e:
    assert str(e) == "Argument 'n' must be int, got str"

print("Все тесты пройдены успешно!")
