from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QWidget,
    QGridLayout,
    QComboBox,
    QLineEdit,
    QPushButton,
)
from PySide6 import QtCore, QtWidgets


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.item_model = None
        self.setWindowTitle("Программа для ведения бюджета")

        self.layout = QVBoxLayout()

        ###########################################################
        self.layout.addWidget(QLabel("Последние расходы"))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        ##########################################################
        self.layout.addWidget(QLabel("Бюджет"))

        self.budget_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.budget_grid)
        # QLabel("<TODO: таблица бюджета>\n\n\n\n\n\n\n\n"))

        ############################################################
        self.bottom_controls = QGridLayout()

        self.bottom_controls.addWidget(QLabel("Сумма"), 0, 0)

        self.amount_line_edit = QLineEdit()

        self.bottom_controls.addWidget(
            self.amount_line_edit, 0, 1
        )  # TODO: добавить валидатор
        self.bottom_controls.addWidget(QLabel("Категория"), 1, 0)

        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 1, 1)

        self.category_edit_button = QPushButton("Редактировать")
        self.bottom_controls.addWidget(self.category_edit_button, 1, 2)

        self.expense_add_button = QPushButton("Добавить")
        self.bottom_controls.addWidget(self.expense_add_button, 2, 1)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data):
        self.item_model = TableModel(data)
        self.expenses_grid.setModel(self.item_model)
        self.expenses_grid.resizeColumnsToContents()
        grid_width = sum(
            [
                self.expenses_grid.columnWidth(x)
                for x in range(0, self.item_model.columnCount(0) + 1)
            ]
        )
        self.setFixedSize(grid_width + 80, 600)

    def set_budget_table(self, data):
        self.item_model = TableModel(data)
        self.budget_grid.setModel(self.item_model)
        self.budget_grid.resizeColumnsToContents()
        grid_width = sum(
            [
                self.budget_grid.columnWidth(x)
                for x in range(0, self.item_model.columnCount(0) + 1)
            ]
        )
        self.setFixedSize(grid_width + 80, 600)

    def set_category_dropdown(self, data):
        for tup in data:
            self.category_dropdown.addItem(tup[1], tup[0])

    def on_expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)

    def get_amount(self) -> float:
        return float(self.amount_line_edit.text())  # TODO: обработка исключений

    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())
