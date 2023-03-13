import pytest
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.presenter.main_presenter import MainPresenter
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.view.expense_budget_view import MainWindow

DB_NAME = "tests/test.db"


@pytest.fixture
def exp_repo():
    return SQLiteRepository(DB_NAME, Expense)


@pytest.fixture
def bud_repo():
    return SQLiteRepository(DB_NAME, Budget)


@pytest.fixture
def cat_repo():
    return SQLiteRepository(DB_NAME, Category)


def test_init_presenter(qtbot, cat_repo, exp_repo, bud_repo):
    """
    Should update expense data in the view's table
    """
    view = MainWindow()
    main_presenter = MainPresenter(view, cat_repo, exp_repo, bud_repo)
    qtbot.addWidget(main_presenter.view)
    assert isinstance(main_presenter.view, MainWindow)
    assert main_presenter.exp_repo == exp_repo
    assert main_presenter.cat_repo == cat_repo
    assert main_presenter.bud_repo == bud_repo


def test_update_expense_data(qtbot, cat_repo, exp_repo, bud_repo):
    """
    Should update expense data in the view's table
    """
    view = MainWindow()
    main_presenter = MainPresenter(view, cat_repo, exp_repo, bud_repo)
    qtbot.addWidget(main_presenter.view)
    obj = Expense()
    lenth = len(main_presenter.exp_repo.get_all())
    main_presenter.exp_repo.add(obj)
    main_presenter.update_expense_data()
    assert len(main_presenter.exp_repo.get_all()) == lenth + 1


# def test_update_budget_data(qtbot, cat_repo, exp_repo, bud_repo):
#     """
#     Should update expense data in the view's table
#     """
#     view = MainWindow()
#     main_presenter = MainPresenter(view, cat_repo, exp_repo, bud_repo)
#     qtbot.addWidget(main_presenter.view)
#     main_presenter.bud_repo.add(obj)
#     main_presenter.update_expense_data()
#     assert len(main_presenter.exp_repo.get_all()) == lenth + 1
