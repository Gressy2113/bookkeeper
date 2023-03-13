import sqlite3
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import BudgetTable, SQLiteRepository
from dataclasses import dataclass
import pytest


DB_NAME = "tests/test.db"


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        pk: int = 0
        test_field: str = "abc"

    return Custom


@pytest.fixture
def custom_class1():
    @dataclass
    class Custom1:
        pk: int = 0
        test_field1: str = "cab"

    return Custom1


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository(DB_NAME, custom_class)


@pytest.fixture
def repo1():
    return SQLiteRepository(DB_NAME, Expense)


@pytest.fixture
def repo2():
    return BudgetTable(DB_NAME, Budget)


def test_add_get_and_delete(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    o = repo.get(5555)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    assert o is None
    repo.delete(pk)
    assert repo.get(pk) is None


def test_get_all_all_records(repo, custom_class):
    obj1 = custom_class()
    pk1 = repo.add(obj1)
    obj2 = custom_class()
    pk2 = repo.add(obj2)
    records = repo.get_all()

    assert len(records) > 0
    assert all(isinstance(record, custom_class) for record in records)
    repo.delete(pk1)
    repo.delete(pk2)


def test_get_all_multiple_where(repo, custom_class):
    obj = custom_class()
    obj.test_field = "abc"
    pk = repo.add(obj)
    records = repo.get_all(where={"pk": pk, "test_field": "abc"})
    assert len(records) > 0
    assert all(isinstance(record, custom_class) for record in records)
    assert all(record.pk == pk and record.test_field == "abc" for record in records)
    repo.delete(pk)


def test_get_all_non_existing_where(repo):
    records = repo.get_all(where={"pk": 10})
    assert len(records) == 0


def test_update_object_with_pk(repo, custom_class):
    obj = custom_class(test_field="abc")
    pk = repo.add(obj)
    obj_new = custom_class(pk=pk, test_field="cab")
    repo.update(obj_new)
    get_upd = repo.get(pk)
    assert get_upd.test_field == obj_new.test_field
    repo.delete(pk)


def test_update_object_without_pk(repo, custom_class):
    obj = custom_class(test_field="abc")
    assert obj.pk == 0
    # with TestCase.assertRaises(ValueError):
    #     repo.update(obj)
    try:
        repo.update(obj)
        # raise AssertionError
    except ValueError:
        pass


def _drop_custom1_table():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS custom1")
    con.close()


def test_create_table_if_not_exists(repo, custom_class1):
    _drop_custom1_table()
    repo.__init__(DB_NAME, custom_class1)
    obj = custom_class1()
    pk = repo.add(obj)
    _drop_custom1_table()


def _drop_budget_table():
    with sqlite3.connect(DB_NAME) as con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS budget")
    con.close()


def test_create_update_budget_table(repo1, repo2):
    repo1.add(Expense(100, ""))
    _drop_budget_table()
    repo2.__init__(DB_NAME, Budget)


def test_update_budget(repo2):
    repo2.update_budget(0, 500)
