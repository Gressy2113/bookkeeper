"""
Модуль описывает репозиторий, работающий в базе данных sqlite
"""

import sqlite3
from inspect import get_annotations
from typing import Any
from bookkeeper.repository.abstract_repository import AbstractRepository, T


class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в базе данных sqlite. Хранит данные в базе данных.
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop("pk")

    def add(self, obj: T) -> int:
        """Добавить объект"""
        names = ", ".join(self.fields.keys())
        p = ", ".join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(f"INSERT INTO {self.table_name} ({names}) VALUES ({p})", values)

            pk = cur.lastrowid
            assert isinstance(pk, int)
            obj.pk = pk

        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        """Получить объект по id"""
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM {self.table_name} WHERE pk=({pk})")
            res = cur.fetchone()
        con.close()
        return res

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
        return res

    def update(self, obj: T) -> None:
        """Обновить данные об объекте. Объект должен содержать поле pk."""
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute(f"UPDATE * FROM {self.table_name}")
            # res = cur.fetchall()
        con.close()

    def delete(self, pk: int) -> None:
        """Удалить запись"""
        with sqlite3.connect(self.db_file) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(f"DELETE FROM {self.table_name} WHERE pk={pk}")
        # cur.rowcount
        con.close()
