"""
Описание главного окна программы с таблицами расходов и бюждета
"""

from typing import Any, Callable
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.abstract_repository import T
from bookkeeper.view.categories_view import CategoryDialog


class TableModel(QtCore.QAbstractTableModel):
    """
    Общая модель таблицы в основном окне
    """

    def __init__(self, data: list[T], *args):
        super(TableModel, self).__init__()
        self._data = data
        self.header_names = list(data[0].__dataclass_fields__.keys())

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """
        возвращает названия столбцов
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        """
        возвращает данные
        """
        if role == QtCore.Qt.DisplayRole:
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])

    def rowCount(self, index=None) -> int:
        """возвращает количество строк"""
        return len(self._data)

    def columnCount(self, index=None) -> int:
        """
        возвращает количество столбцов
        """
        return len(self._data[0].__dataclass_fields__)


class QPushButtonWithSignals(QtWidgets.QPushButton):
    """Remove attributes below once Signal typing issues are fixed upstream"""

    clicked: Signal
    # Add other missing Signals here if used


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Программа для ведения бюджета")

        self.layout = QtWidgets.QVBoxLayout()

        self.layout.addWidget(QtWidgets.QLabel("Последние расходы"))
        self.expenses_grid = QtWidgets.QTableView()
        self.item_model_expense = None
        self.layout.addWidget(self.expenses_grid)

        self.layout.addWidget(QtWidgets.QLabel("Бюджет"))
        self.budget_grid = QtWidgets.QTableView()
        self.item_model_budget = None
        self.layout.addWidget(self.budget_grid)

        self.layout.addWidget(QtWidgets.QLabel("Изменение расходов"))

        self.width = 0
        fixedwidth0 = 350

        self.middle_controls = QtWidgets.QGridLayout()
        self.middle_controls.addWidget(QtWidgets.QLabel("Сумма"), 1, 0)
        self.amount_line_edit = QtWidgets.QLineEdit()
        self.amount_line_edit.setFixedWidth(fixedwidth0)

        self.middle_controls.addWidget(self.amount_line_edit, 1, 1)

        self.middle_controls.addWidget(QtWidgets.QLabel("Категория"), 0, 0)
        self.category_dropdown = QtWidgets.QComboBox()
        self.middle_controls.addWidget(self.category_dropdown, 0, 1)

        self.middle_controls.addWidget(QtWidgets.QLabel("Комментарий"), 2, 0)
        self.comment_line_edit = QtWidgets.QLineEdit()
        self.comment_line_edit.setFixedWidth(fixedwidth0)
        self.middle_controls.addWidget(self.comment_line_edit, 2, 1)

        self.category_edit_button = QPushButtonWithSignals(
            "Редактировать категории"
        )  # QtWidgets.QPushButton("Редактировать категории")
        self.middle_controls.addWidget(self.category_edit_button, 0, 2)
        self.category_edit_button.clicked.connect(self.show_cats_dialog)

        self.expense_add_button = QPushButtonWithSignals("Добавить расход")
        self.middle_controls.addWidget(self.expense_add_button, 3, 0, 3, 2)

        self.expense_delete_button = QPushButtonWithSignals("Удалить выбранный\nрасход")
        self.middle_controls.addWidget(self.expense_delete_button, 1, 2, 3, 1)

        self.middle_widget = QtWidgets.QWidget()
        self.middle_widget.setLayout(self.middle_controls)

        self.layout.addWidget(self.middle_widget)
        #####

        self.layout.addWidget(QtWidgets.QLabel("Изменение бюджета"))

        self.bottom_controls = QtWidgets.QGridLayout()

        self.bottom_controls.addWidget(QtWidgets.QLabel("На день"), 1, 0)
        self.day_line_edit = QtWidgets.QLineEdit()
        self.day_line_edit.setFixedWidth(fixedwidth0)
        self.bottom_controls.addWidget(self.day_line_edit, 1, 1)
        self.budget_day_button = QPushButtonWithSignals("Принять")
        self.bottom_controls.addWidget(self.budget_day_button, 1, 2)

        self.bottom_controls.addWidget(QtWidgets.QLabel("На неделю"), 2, 0)
        self.week_line_edit = QtWidgets.QLineEdit()
        self.week_line_edit.setFixedWidth(fixedwidth0)
        self.bottom_controls.addWidget(self.week_line_edit, 2, 1)
        self.budget_week_button = QPushButtonWithSignals("Принять")
        self.bottom_controls.addWidget(self.budget_week_button, 2, 2)

        self.bottom_controls.addWidget(QtWidgets.QLabel("На месяц"), 3, 0)
        self.month_line_edit = QtWidgets.QLineEdit()
        self.month_line_edit.setFixedWidth(fixedwidth0)
        self.bottom_controls.addWidget(self.month_line_edit, 3, 1)
        self.budget_month_button = QPushButtonWithSignals("Принять")
        self.bottom_controls.addWidget(self.budget_month_button, 3, 2)

        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

        self.cat_dlg = None

    def set_expense_table(self, data: list[Expense]) -> None:
        """
        описание представления таблицы расходов
        """
        if data:
            self.item_model_expense = TableModel(data)
            self.expenses_grid.setModel(self.item_model_expense)
            self.expenses_grid.hideColumn(
                self.item_model_expense.header_names.index("pk")
            )
            self.expenses_grid.resizeColumnsToContents()
            grid_width = sum(
                [
                    self.expenses_grid.columnWidth(x)
                    for x in range(0, self.item_model_expense.columnCount(0) + 1)
                ]
            )
            self.expenses_grid.horizontalHeader().setSectionResizeMode(
                4, QtWidgets.QHeaderView.Stretch
            )
            self.width = grid_width + 60
            self.setFixedSize(grid_width + 60, 800)

    def set_budget_table(self, data: list[Budget]) -> None:
        """
        описание представления таблицы бюджета
        """
        if data:
            self.item_model_budget = TableModel(data)
            self.budget_grid.setModel(self.item_model_budget)
            self.budget_grid.hideColumn(self.item_model_budget.header_names.index("pk"))
            for i in range(self.item_model_budget.columnCount() - 1):
                self.budget_grid.horizontalHeader().setSectionResizeMode(
                    i, QtWidgets.QHeaderView.Stretch
                )
                self.budget_grid.verticalHeader().setSectionResizeMode(
                    i, QtWidgets.QHeaderView.Stretch
                )
        self.budget_grid.setFixedHeight(100)

    def set_category_dropdown(self, data: list[Category]) -> None:
        """
        описание представления выпадающего списка категорий
        для выбора при добавлении расхода
        """

        self.category_dropdown.clear()
        for i in data:
            self.category_dropdown.addItem(i.name, i.pk)

    def on_expense_add_button_clicked(self, slot: Callable[[], None]) -> None:
        """нажали на кнопку добавления расхода"""
        self.expense_add_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot: Callable[[], None]) -> None:
        """нажали на кнопку удаления расхода"""
        self.expense_delete_button.clicked.connect(slot)

    def on_budget_day_button_clicked(self, slot: Callable[[], None]) -> None:
        """нажали на кнопку изменения бюждета на день"""
        self.budget_day_button.clicked.connect(slot)

    def on_budget_week_button_clicked(self, slot: Callable[[], None]) -> None:
        """нажали на кнопку изменения бюждета на неделю"""

        self.budget_week_button.clicked.connect(slot)

    def on_budget_month_button_clicked(self, slot: Callable[[], None]) -> None:
        """нажали на кнопку изменения бюждета на месяц"""

        self.budget_month_button.clicked.connect(slot)

    def get_amount(self) -> float:
        """возвращает введенную сумму расхода при его добавлении"""

        return float(self.amount_line_edit.text())

    def get_day_budget(self) -> float:
        """возвращает введенную сумму бюждета на день при его изменении"""

        return float(self.day_line_edit.text())

    def get_week_budget(self) -> float:
        """возвращает введенную сумму бюждета на недею при его изменении"""

        return float(self.week_line_edit.text())

    def get_month_budget(self) -> float:
        """возвращает введенную сумму бюждета на месяц при его изменении"""

        return float(self.month_line_edit.text())

    def get_comment(self) -> str:
        """возвращает комментарий к расходу при его добавлении"""

        return self.comment_line_edit.text()

    def __get_selected_row_indices(self) -> list[int]:
        """возвращает выбранные индексы строк для их удаления"""

        return list(
            set(
                [
                    qmi.row()
                    for qmi in self.expenses_grid.selectionModel().selection().indexes()
                ]
            )
        )

    def get_selected_expenses(self) -> list[int] | None:
        """возвращает выбранные расходы для удаления"""

        idx = self.__get_selected_row_indices()
        if not idx:
            return None
        assert isinstance(self.item_model_expense, TableModel)
        return [self.item_model_expense._data[i].pk for i in idx]

    def get_selected_cat(self) -> int | Any:
        """возвращает выбранную в выпадающем списке категорию"""

        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def on_category_edit_button_clicked(self, slot: Callable[[], None]) -> None:
        """нажали на кнопку изменения списка категорий"""

        self.category_edit_button.clicked.connect(slot)

    def show_cats_dialog(self, repo: SQLiteRepository[Any]) -> None:
        """открывает новое окно изменения списка категорий"""

        if repo:
            self.cat_dlg = CategoryDialog(repo)
            self.cat_dlg.setWindowTitle("Редактирование категорий")
            self.cat_dlg.setGeometry(300, 100, 600, 300)
            self.cat_dlg.exec()
