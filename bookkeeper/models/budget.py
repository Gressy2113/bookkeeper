"""
Модель бюджета
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Budget:
    """
    interval - День/Неделя/Месяц
    summ - сколько потратили в промежутке
    budget - сколько можно потратить в промежутке
    pk - id записи в базе данных
    """

    interval: str
    summ: float = 0
    budget: float = 0
    pk: int = 0
