from collections import deque
from PySide6.QtWidgets import QTreeView, QVBoxLayout
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QDialogButtonBox


class CategoryDialog(QDialog):
    def __init__(self, data):
        super().__init__()
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QDialogButtonBox.Ok)

        self.tree = QTreeView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        layout.addWidget(self.buttonBox)

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Категория"])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        data = [
            {"unique_id": c.pk, "category_name": c.name, "parent_id": c.parent}
            for c in data
        ]
        self.importData(data)
        self.tree.expandAll()

    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}  # List of  QStandardItem
        values = deque(data)
        while values:
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
            parent.appendRow([QStandardItem(value["category_name"])])
            seen[unique_id] = parent.child(parent.rowCount() - 1)


# class EditCategoryWindow(QWidget):
#     def __init__(self, data):
#         super(EditCategoryWindow, self).__init__()
#         self.data = data

#         self.setWindowTitle("Редактирование категорий")
#         self.tree = QTreeView(self)
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.tree)
#         self.model = QStandardItemModel()
#         self.model.setHorizontalHeaderLabels(["Name"])
#         self.tree.header().setDefaultSectionSize(180)
#         self.tree.setModel(self.model)
#         self.importData(data)

#         self.tree.collapseAll()
#         self.tree.doubleClicked.connect(self.editItem)

#     def importData(self, data, root=None):
#         self.model.setRowCount(0)
#         if root is None:
#             root = self.model.invisibleRootItem()
#         seen = {}
#         data1 = [
#             {
#                 "unique_id": pk,
#                 "short_name": name,
#                 "parent_id": pid,
#             }
#             for pk, name, pid in data
#         ]
#         values = deque(data1)
#         while values:
#             value = values.popleft()
#             if value["unique_id"] == 1 or value["parent_id"] is None:
#                 parent = root
#             else:
#                 pid = value["parent_id"]
#                 if pid not in seen:
#                     values.append(value)
#                     continue
#                 parent = seen[pid]
#             unique_id = value["unique_id"]
#             parent.appendRow(
#                 [QStandardItem(value["short_name"])]  # QStandardItem(str(unique_id)),
#             )
#             seen[unique_id] = parent.child(parent.rowCount() - 1)

#     def editItem(self):
#         itm = self.tree.itemFromIndex(self.tree.selectedIndexes()[0])
#         column = self.tree.currentColumn()
#         edit = QtWidgets.QLineEdit()
#         edit.returnPressed.connect(
#             lambda *_: self.project.setData(column, edit.text(), itm, column, self.tree)
#         )
#         edit.returnPressed.connect(lambda *_: self.update())
#         self.tree.setItemWidget(itm, column, edit)


# if __name__ == "__main__":
#     cat_repo = SQLiteRepository[Category]("test.db", Category)

#     data = cat_repo.get_all()
#     app = QApplication(sys.argv)
#     view_ = EditCategoryWindow(data)
#     view_.setGeometry(300, 100, 600, 300)
#     view_.setWindowTitle("QTreeview Example")
#     view_.show()
#     sys.exit(app.exec_())
