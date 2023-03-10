from PySide6 import QtCore, QtWidgets
from bookkeeper.view.categories_view import CategoryDialog


class TableModel(QtCore.QAbstractTableModel):
    """
    Общая модель таблицы в основном окне
    """

    def __init__(self, data):
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


# class BugdetTableModel(TableModel):
#     # def setData(self, index, value, role):
#     #     if role == QtCore.Qt.EditRole:
#     #         print(self._data)
#     #         self._data.update_budget(index.row(), value)
#     #         # print(index.row(), index.column(), value)

#     #         # self._data.add()
#     #         # self._data[index.row()][index.column()] = value
#     #         # self.dataChanged.emit(index, index)

#     #         return True

#     #     return False

#     def flags(self, index):
#         fl = QtCore.QAbstractTableModel.flags(self, index)
#         if index.column() == 2:
#             fl |= (
#                 QtCore.Qt.ItemIsEditable
#                 | QtCore.Qt.ItemIsEnabled
#                 | QtCore.Qt.ItemIsSelectable
#             )
#         return fl


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
        self.width = None
        fixedwidth0 = 350
        self.bottom_controls = QtWidgets.QGridLayout()
        self.bottom_controls.addWidget(QtWidgets.QLabel("Сумма"), 1, 0)
        self.amount_line_edit = QtWidgets.QLineEdit()
        self.amount_line_edit.setFixedWidth(fixedwidth0)

        self.bottom_controls.addWidget(
            self.amount_line_edit, 1, 1
        )  # TODO: добавить валидатор

        self.bottom_controls.addWidget(QtWidgets.QLabel("Категория"), 0, 0)
        self.category_dropdown = QtWidgets.QComboBox()
        self.bottom_controls.addWidget(self.category_dropdown, 0, 1)

        # self.bottom_controls = QtWidgets.QGridLayout()
        self.bottom_controls.addWidget(QtWidgets.QLabel("Комментарий"), 2, 0)
        self.comment_line_edit = QtWidgets.QLineEdit()
        self.comment_line_edit.setFixedWidth(fixedwidth0)
        self.bottom_controls.addWidget(self.comment_line_edit, 2, 1)

        self.category_edit_button = QtWidgets.QPushButton("Редактировать категории")
        self.bottom_controls.addWidget(self.category_edit_button, 0, 2)
        self.category_edit_button.clicked.connect(self.show_cats_dialog)

        self.expense_add_button = QtWidgets.QPushButton("Добавить расход")
        self.bottom_controls.addWidget(self.expense_add_button, 3, 0, 3, 2)

        self.expense_delete_button = QtWidgets.QPushButton("Удалить выбранный\nрасход")
        self.bottom_controls.addWidget(self.expense_delete_button, 1, 2, 3, 1)

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
            self.width = grid_width + 60
            self.setFixedSize(grid_width + 60, 600)

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
        for c in data:
            self.category_dropdown.addItem(c.name, c.pk)

    def on_expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)

    def on_expense_delete_button_clicked(self, slot):
        self.expense_delete_button.clicked.connect(slot)

    def get_amount(self) -> float:
        return float(self.amount_line_edit.text())  # TODO: обработка исключений

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

    # def renameSection(self, index):
    #     oldTitle = self.model.headerData(
    #         index, QtCore.Qt.Horizontal, QtCore.Qt.DisplayRole)

    #     newTitle, accepted = QtWidgets.QInputDialog.getText(
    #         self, 'Change column title', oldTitle)

    #     if accepted and oldTitle != newTitle:
    #         self.model.setHeaderData(
    #             index, QtCore.Qt.Horizontal, newTitle, QtCore.Qt.DisplayRole)

    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def on_category_edit_button_clicked(self, slot):
        self.category_edit_button.clicked.connect(slot)

    def show_cats_dialog(self, data):
        if data:
            cat_dlg = CategoryDialog(data)
            cat_dlg.setWindowTitle("Редактирование категорий")
            cat_dlg.setGeometry(300, 100, 600, 300)
            cat_dlg.exec_()
