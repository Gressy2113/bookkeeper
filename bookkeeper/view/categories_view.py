"""
Окно редактирования категорий
"""

from collections import deque

from PySide6.QtGui import Qt, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QPushButton,
    QTreeView,
    QVBoxLayout,
    QLabel,
    QTextEdit,
)

from bookkeeper.models.category import Category


class CategoryDialog(QDialog):
    """
    Окно просмотра и редактирования категорий в иерархическом виде.
    Функции: добавить, удалить, изменить название категории
    """

    def __init__(self, cat_repo) -> None:
        super().__init__()
        self.cat_repo = cat_repo
        self.cat_data = None
        self.get_update_data()
        self.tree = QTreeView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.setWindowTitle("Редактирование категорий")

        self.model = QStandardItemModel(0, 2, self)
        self.tree.setModel(self.model)
        self.importData(self.cat_data)

        self.add_button = QPushButton("Добавить")
        self.delete_button = QPushButton("Удалить")
        self.ok_button = QDialogButtonBox.Ok

        self.buttonbox = QDialogButtonBox(Qt.Horizontal)
        self.buttonbox.addButton(self.add_button, QDialogButtonBox.ActionRole)
        self.buttonbox.addButton(self.delete_button, QDialogButtonBox.ActionRole)
        self.buttonbox.addButton(self.ok_button)
        self.buttonbox.accepted.connect(self.accept)

        layout.addWidget(self.buttonbox)

        self.model.setHorizontalHeaderLabels(["Категория", ""])
        self.tree.hideColumn(1)

        self.model.itemChanged.connect(self.on_edit_text_changed)
        self.add_button.clicked.connect(self.on_add_button_clicked)
        self.delete_button.clicked.connect(self.on_delete_button_clicked)
        self.tree.expandAll()
        self.dialog = None
        self.text_edit = None
        self.add_parent_pk = None

    def get_update_data(self) -> None:
        """
        обновление данных после изменений
        """
        self.cat_data = [
            {"unique_id": c.pk, "category_name": c.name, "parent_id": c.parent}
            for c in self.cat_repo.get_all()
        ]

    def update_category(self, new_name, pk) -> None:
        """
        обновление категории
        """
        category = self.cat_repo.get(pk)
        category.name = new_name
        self.cat_repo.update(category)

    def on_edit_text_changed(self, item) -> None:
        """
        получение имени новой категории
        """
        index = item.index()
        pk = self.model.data(item.index(), Qt.UserRole)
        new_name = index.data()
        self.update_category(new_name, int(pk))

    def on_add_button_clicked(self) -> None:
        """
        окно добавления новой категории
        """
        if self.tree.selectedIndexes():
            index = self.tree.selectedIndexes()[0]
            self.add_parent_pk = self.model.data(index, Qt.UserRole)
        else:
            self.add_parent_pk = None

        self.dialog = QDialog()
        label = QLabel("Введите название категории:")
        self.text_edit = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.dialog.setWindowTitle("Добавление категории")

        layout.addWidget(self.text_edit)

        self.dialog.setLayout(layout)
        ok_button = QDialogButtonBox.Ok
        buttonbox = QDialogButtonBox(Qt.Horizontal)
        buttonbox.addButton(ok_button)
        buttonbox.accepted.connect(self.on_accepted_)
        layout.addWidget(buttonbox)
        self.dialog.exec()

    def on_accepted_(self) -> None:
        """
        закрытие диалога в конце редактирования категорий
        """
        text = self.text_edit.toPlainText()
        self.dialog.close()
        self.add_category(text, self.add_parent_pk)

    def add_category(self, name, parent) -> None:
        """
        добавление категории
        """
        category = Category(name=name, parent=parent)
        self.cat_repo.add(category)
        self.get_update_data()
        self.importData(self.cat_data)

    def on_delete_button_clicked(self) -> None:
        """
        удаление категории, обработка запроса
        """
        if not self.tree.selectedIndexes():
            return
        index = self.tree.selectedIndexes()[0]
        pk = self.model.data(index, Qt.UserRole)
        parent = self.model.data(index.parent(), Qt.UserRole)
        name = self.model.data(index, 0)
        childs = [
            _ for _ in Category(name, parent, pk).get_subcategories(self.cat_repo)
        ]
        if len(childs) > 0:
            for cat in childs:
                self.remove_category(cat.pk)
        self.remove_category(pk)

    def remove_category(self, pk) -> None:
        """
        удаление категории из репозитория
        """
        self.cat_repo.delete(pk)
        self.get_update_data()
        self.importData(self.cat_data)

    def importData(self, data, root=None) -> None:
        """
        импорт данных из репозитория и отображение их в виде дерева
        """
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}
        values = deque(data)
        while values and len(values) > 0:
            value = values.popleft()
            if value["parent_id"] is None:
                parent = root
            else:
                pid = value["parent_id"]
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value["unique_id"]
            parentItem = QStandardItem(value["category_name"])
            parentItem.setData(value["unique_id"], Qt.UserRole)
            parent.appendRow(parentItem)
            seen[unique_id] = parent.child(parent.rowCount() - 1)
        self.tree.expandAll()


# if __name__ == "__main__":
#     cat_repo = SQLiteRepository[Category]("test.db", Category)
#     app = QApplication(sys.argv)
#     view_ = CategoryDialog(cat_repo)
#     view_.setGeometry(300, 100, 600, 300)
#     view_.setWindowTitle("QTree Example")
#     view_.show()
#     sys.exit(app.exec())
