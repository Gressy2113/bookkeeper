from PySide6 import QtCore, QtWidgets
from bookkeeper.view.categories_view import CategoryDialog


class TableModel(QtCore.QAbstractTableModel):
    """
    Общая модель таблицы в основном окне
    """

    def __init__(self, data, *args):
        super(TableModel, self).__init__()
        self._data = data
        self.header_names = list(data[0].__dataclass_fields__.keys())

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])

    def rowCount(self, index=None):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index=None):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0].__dataclass_fields__)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # self.item_model = None
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

        self.width = None
        fixedwidth0 = 350

        self.middle_controls = QtWidgets.QGridLayout()
        self.middle_controls.addWidget(QtWidgets.QLabel("Сумма"), 1, 0)
        self.amount_line_edit = QtWidgets.QLineEdit()
        self.amount_line_edit.setFixedWidth(fixedwidth0)

        self.middle_controls.addWidget(
            self.amount_line_edit, 1, 1
        )  # TODO: добавить валидатор

        self.middle_controls.addWidget(QtWidgets.QLabel("Категория"), 0, 0)
        self.category_dropdown = QtWidgets.QComboBox()
        self.middle_controls.addWidget(self.category_dropdown, 0, 1)

        self.middle_controls.addWidget(QtWidgets.QLabel("Комментарий"), 2, 0)
        self.comment_line_edit = QtWidgets.QLineEdit()
        self.comment_line_edit.setFixedWidth(fixedwidth0)
        self.middle_controls.addWidget(self.comment_line_edit, 2, 1)

        self.category_edit_button = QtWidgets.QPushButton("Редактировать категории")
        self.middle_controls.addWidget(self.category_edit_button, 0, 2)
        self.category_edit_button.clicked.connect(self.show_cats_dialog)

        self.expense_add_button = QtWidgets.QPushButton("Добавить расход")
        self.middle_controls.addWidget(self.expense_add_button, 3, 0, 3, 2)

        self.expense_delete_button = QtWidgets.QPushButton("Удалить выбранный\nрасход")
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
        self.budget_day_button = QtWidgets.QPushButton("Принять")
        self.bottom_controls.addWidget(self.budget_day_button, 1, 2)

        self.bottom_controls.addWidget(QtWidgets.QLabel("На неделю"), 2, 0)
        self.week_line_edit = QtWidgets.QLineEdit()
        self.week_line_edit.setFixedWidth(fixedwidth0)
        self.bottom_controls.addWidget(self.week_line_edit, 2, 1)
        self.budget_week_button = QtWidgets.QPushButton("Принять")
        self.bottom_controls.addWidget(self.budget_week_button, 2, 2)

        self.bottom_controls.addWidget(QtWidgets.QLabel("На месяц"), 3, 0)
        self.month_line_edit = QtWidgets.QLineEdit()
        self.month_line_edit.setFixedWidth(fixedwidth0)
        self.bottom_controls.addWidget(self.month_line_edit, 3, 1)
        self.budget_month_button = QtWidgets.QPushButton("Принять")
        self.bottom_controls.addWidget(self.budget_month_button, 3, 2)

        self.bottom_widget = QtWidgets.QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data):
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

    def set_budget_table(self, data):
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

    def set_category_dropdown(self, data):
        self.category_dropdown.clear()
        for c in data:
            self.category_dropdown.addItem(c.name, c.pk)

    def on_expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot):
        self.expense_delete_button.clicked.connect(slot)

    def on_budget_day_button_clicked(self, slot):
        self.budget_day_button.clicked.connect(slot)

    def on_budget_week_button_clicked(self, slot):
        self.budget_week_button.clicked.connect(slot)

    def on_budget_month_button_clicked(self, slot):
        self.budget_month_button.clicked.connect(slot)

    def get_amount(self) -> float:
        return float(self.amount_line_edit.text())  # TODO: обработка исключений

    def get_day_budget(self) -> float:
        return float(self.day_line_edit.text())

    def get_week_budget(self) -> float:
        return float(self.week_line_edit.text())  # TODO: обработка исключений

    def get_month_budget(self) -> float:
        return float(self.month_line_edit.text())  # TODO: обработка исключений

    def get_comment(self) -> float:
        return self.comment_line_edit.text()

    def __get_selected_row_indices(self) -> list[int]:
        return list(
            set(
                [
                    qmi.row()
                    for qmi in self.expenses_grid.selectionModel().selection().indexes()
                ]
            )
        )

    def get_selected_expenses(self) -> list[int] | None:
        idx = self.__get_selected_row_indices()
        if not idx:
            return None
        return [self.item_model_expense._data[i].pk for i in idx]

    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def on_category_edit_button_clicked(self, slot):
        self.category_edit_button.clicked.connect(slot)

    def show_cats_dialog(self, repo):
        if repo:
            cat_dlg = CategoryDialog(repo)
            cat_dlg.setWindowTitle("Редактирование категорий")
            cat_dlg.setGeometry(300, 100, 600, 300)
            cat_dlg.exec()
