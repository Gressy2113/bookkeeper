"""
Модуль описывает репозиторий, работающий в базе данных sqlite
"""

import sqlite3
from inspect import get_annotations
from typing import Any, Tuple
from bookkeeper.models.budget import Budget
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в базе данных sqlite. Хранит данные в базе данных.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.cls = cls
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop("pk")
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            res = cur.execute("SELECT name FROM sqlite_master")
            db_tables = [t[0].lower() for t in res.fetchall()]
            if self.table_name not in db_tables:
                col_names = ", ".join(self.fields.keys())
                request = (
                    f"CREATE TABLE {self.table_name} ("
                    f'"pk" INTEGER PRIMARY KEY AUTOINCREMENT, {col_names})'
                )
                cur.execute(request)
        con.close()
        # self.create_update_budget_table()

    def add(self, obj: T) -> int:
        """Добавить объект"""
        names = ", ".join(self.fields.keys())
        sep = ", ".join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = 0")
            cur.execute(
                f"INSERT INTO {self.table_name} ({names}) VALUES ({sep})", values
            )
            pk = cur.lastrowid
            assert isinstance(pk, int)
            obj.pk = pk
        con.close()
        return obj.pk

    def __generate_object(self, db_row: Tuple[Any, ...]) -> T | Any:
        obj = self.cls(self.fields)
        for field, value in zip(self.fields, db_row[1:]):
            setattr(obj, field, value)
        obj.pk = db_row[0]
        return obj

    def get(self, pk: int) -> T | None:
        """Получить объект по id"""
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.table_name} WHERE pk=({pk})")
            res = cur.fetchone()
        con.close()

        if res is None:
            return None

        return self.__generate_object(res)

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            request = ""
            if where is None:
                request += f"SELECT * FROM {self.table_name}"
            else:
                request += f"SELECT * FROM {self.table_name} WHERE ("
                i = 0
                for col, val in where.items():
                    request += col + " = '" + str(val) + "'"
                    i += 1
                    if 0 < i < len(where):
                        request += " AND "
                request += ")"

            cur.execute(request)

            res = cur.fetchall()
        con.close()

        if not res:
            return []

        return [self.__generate_object(row) for row in res]

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError("attempt to update object with unknown primary key")

        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            names = list(self.fields.keys())
            values = [getattr(obj, x) for x in self.fields]
            update_command = (
                f"UPDATE {self.table_name} SET "
                + ", ".join([f"{name} = ?" for name in names])
                + " WHERE pk = ?"
            )
            cur.execute(update_command, values + [obj.pk])
        con.close()

    def delete(self, pk: int) -> None:
        """Удалить запись"""
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM {self.table_name} WHERE pk={pk}")
        con.close()


class BudgetTable(SQLiteRepository[Budget]):
    """
    Репозиторий для создания и обновления таблицы бюджета в базе данных
    """

    intervals: list[str] = ["День", "Неделя", "Месяц"]
    patterns: list[str] = [
        "datetime('now', 'start of day')",
        "date('now', 'Weekday 1', '-7 days')",
        "datetime('now', 'start of month')",
    ]

    def __init__(self, db_file: str, cls: type):
        super().__init__(db_file, cls)
        self.create_update_budget_table()

    def create_update_budget_table(self) -> None:
        """
        Создание и обновление расходов в таблице бюджета.
        День - расходы за сегодня
        Неделя - расходы за эту неделю (начиная с последнего пн)
        Месяц - расходы с 1 числа текущего месяца

        """

        for interval, pattern in zip(self.intervals, self.patterns):
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute(f"SELECT * FROM budget WHERE interval='{interval}'")
                ispresent = cur.fetchone()
                cur.execute(
                    f"SELECT amount FROM Expense WHERE expense_date >= {pattern}"
                )
                ams = cur.fetchall()
                summ = sum((float(am[0]) for am in ams))
                if ispresent is None:
                    self.add(Budget(interval=interval, summ=summ, budget=0, pk=0))
                else:
                    cur.execute(
                        f"UPDATE budget SET summ={summ} WHERE interval='{interval}'"
                    )
            con.close()

    def update_budget(self, ind: int, value: float) -> None:
        """Обновление ограничения бюджета"""
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(
                f"UPDATE budget SET budget={value} WHERE interval='{self.intervals[ind]}'"
            )
        con.close()
