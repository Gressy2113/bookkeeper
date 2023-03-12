from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_budget_view import MainWindow
from bookkeeper.presenter.main_presenter import MainPresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository, BudgetTable
import sys

DB_NAME = "test.db"

if __name__ == "__main__":
    app = QApplication(sys.argv)

    view = MainWindow()
    model = None  # TODO: здесь должна быть модель

    cat_repo = SQLiteRepository[Category](DB_NAME, Category)
    exp_repo = SQLiteRepository[Expense](DB_NAME, Expense)
    budget_repo = BudgetTable(DB_NAME, Budget)
    window = MainPresenter(model, view, cat_repo, exp_repo, budget_repo)
    window.show()
    app.exec()
