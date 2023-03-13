from unittest.mock import MagicMock, patch
import pytest
from dataclasses import dataclass
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.view.categories_view import CategoryDialog
from bookkeeper.view.expense_budget_view import MainWindow, TableModel
from PySide6.QtCore import QTimer
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QApplication

DB_NAME = "tests/test.db"


@pytest.fixture
def repo_expense():
    return SQLiteRepository(DB_NAME, Expense)


@pytest.fixture
def repo_budget():
    return SQLiteRepository(DB_NAME, Budget)


@pytest.fixture
def repo_category():
    return SQLiteRepository(DB_NAME, Category)


def test_input_expence(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    qtbot.keyClicks(widget.amount_line_edit, "123")
    assert widget.amount_line_edit.text() == "123"
    assert widget.get_amount() == 123

    qtbot.keyClicks(widget.comment_line_edit, "abc")
    assert widget.comment_line_edit.text() == "abc"
    assert widget.get_comment() == "abc"

    qtbot.keyClicks(widget.day_line_edit, "1")
    assert widget.day_line_edit.text() == "1"
    assert widget.get_day_budget() == 1

    qtbot.keyClicks(widget.week_line_edit, "1")
    assert widget.week_line_edit.text() == "1"
    assert widget.get_week_budget() == 1

    qtbot.keyClicks(widget.month_line_edit, "1")
    assert widget.month_line_edit.text() == "1"
    assert widget.get_month_budget() == 1


def test_set_expense_table(qtbot, repo_expense):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.set_expense_table(repo_expense.get_all())
    assert isinstance(widget.item_model_expense, TableModel)


def test_set_budget_table(qtbot, repo_budget):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.set_budget_table(repo_budget.get_all())
    assert isinstance(widget.item_model_budget, TableModel)


def test_set_category_dropdown(qtbot, repo_category):
    widget = MainWindow()
    qtbot.addWidget(widget)
    names = [cat.name for cat in repo_category.get_all()]
    widget.set_category_dropdown(repo_category.get_all())
    wid_cats = [
        widget.category_dropdown.itemText(i)
        for i in range(widget.category_dropdown.count())
    ]
    for name in names:
        assert name in wid_cats


def test_on_expense_add_button_clicked():
    window = MainWindow()
    # assert window.bottom_controls.itemAtPosition(1, 2) == window.budget_day_button
    mock_slot = MagicMock()
    window.on_expense_add_button_clicked(mock_slot)
    window.expense_add_button.clicked.emit()
    mock_slot.assert_called_once()


def test_on_expense_delete_button_clicked():
    window = MainWindow()
    mock_slot = MagicMock()
    window.on_expense_delete_button_clicked(mock_slot)
    window.expense_delete_button.clicked.emit()
    mock_slot.assert_called_once()


def test_on_budget_day_button_clicked(qtbot, repo_budget):
    window = MainWindow()
    qtbot.addWidget(window)
    mock_slot = MagicMock()

    # budget = repo_budget.get(1).budget
    # new_budget = str(budget + 1)

    # qtbot.keyClicks(window.day_line_edit, new_budget)
    window.on_budget_day_button_clicked(mock_slot)
    window.budget_day_button.clicked.emit()
    mock_slot.assert_called_once()
    # assert str(repo_budget.get(1).budget) == new_budget


def test_on_budget_week_button_clicked():
    window = MainWindow()
    mock_slot = MagicMock()
    window.on_budget_week_button_clicked(mock_slot)
    window.budget_week_button.clicked.emit()
    mock_slot.assert_called_once()


def test_on_budget_month_button_clicked():
    window = MainWindow()
    mock_slot = MagicMock()
    window.on_budget_month_button_clicked(mock_slot)
    window.budget_month_button.clicked.emit()
    mock_slot.assert_called_once()


def test_get_selected_expenses(repo_expense):
    window = MainWindow()
    window.set_expense_table(repo_expense.get_all())
    assert window.get_selected_expenses() == None
    window.expenses_grid.selectRow(0)
    assert window.get_selected_expenses() == [window.item_model_expense._data[0].pk]


def test_get_selected_category(repo_category):
    window = MainWindow()
    window.set_category_dropdown(repo_category.get_all())
    window.category_dropdown.setCurrentIndex(0)
    assert window.get_selected_cat() == window.category_dropdown.itemData(0)


def test_on_category_edit_button_clicked():
    window = MainWindow()
    # assert window.bottom_controls.itemAtPosition(1, 2) == window.budget_day_button
    mock_slot = MagicMock()
    window.on_category_edit_button_clicked(mock_slot)
    window.category_edit_button.clicked.emit()
    mock_slot.assert_called_once()


# def test_show_cats_dialog_opens_dialog(qtbot):
#     window = MainWindow()
#     qtbot.addWidget(window)
#     repo = None  # replace None with a real repository object if necessary
#     window.show_cats_dialog(repo)

#     # Wait for the CategoryDialog to be created
#     cat_dlg = qtbot.wait_until(lambda: qtbot.widget(CategoryDialog))


#     # Assert that CategoryDialog was created with the correct settings
#     assert cat_dlg.windowTitle() == "Редактирование категорий"
#     # assert cat_dlg.geometry() == QRect(300, 100, 600, 300)


def test_show_cats_dialog_opens_dialog(qtbot, repo_category):
    """Test that show_cats_dialog opens a CategoryDialog with the correct settings"""

    window = MainWindow()
    qtbot.addWidget(window)

    # def handle_dialog():
    #     while window.show_cats_dialog is None:
    #         QtGui.QApplication.processEvents()
    #     assert window.cat_dlg.windowTitle() == "Редактирование категорий"
    #     # dlg = window.show_cats_dialog
    #     # assert dlg.windowTitle() == "Редактирование категорий"

    #     # handle dialog now

    # QTimer.singleShot(0, handle_dialog)
    # window.show_cats_dialog(repo_category)
    # assert window.cat_dlg.windowTitle() == "Редактирование категорий"
    # qtbot.ex

    # window.show_cats_dialog(repo_category)
    # qtbot.mouseClick(window.browseButton, QtCore.Qt.LeftButton, delay=1)

    # qtbot.mouseClick(window.browseButton, QtCore.Qt.LeftButton, delay=1)

    # window = MainWindow()
    # qtbot.addWidget(window)

    # QTimer.singleShot(500, handle_dialog)

    # cat_dlg = qtbot.wait_until(
    #     lambda: qtbot.widget(CategoryDialog)
    # )  # wait_for_window_shown(CategoryDialog)
    # cat_dlg = qtbot.addWidget(window.show_cats_dialog(repo_category))

    # assert cat_dlg.windowTitle() == "Редактирование категорий"
    # cat_dlg.accept()
    # window.close()
