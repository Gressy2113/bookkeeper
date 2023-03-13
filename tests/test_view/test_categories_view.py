import pytest
from bookkeeper.models.category import Category
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.view.categories_view import CategoryDialog
from bookkeeper.view.expense_budget_view import MainWindow, TableModel
from bookkeeper.presenter.main_presenter import MainPresenter
from pytestqt.qt_compat import qt_api
from PySide6.QtWidgets import QApplication, QDialog

DB_NAME = "tests/test.db"


@pytest.fixture
def cat_repo():
    return SQLiteRepository(DB_NAME, Category)


# def test_init_CategoryDialog(qtbot, cat_repo):
#     # assert 1 == 0
#     app = QApplication([])
#     dialog = CategoryDialog(cat_repo)

#     assert isinstance(dialog, QDialog)
#     assert dialog.windowTitle() == "Редактирование категорий"
#     app.quit()
# self.assertIsInstance(self.dialog.treeView, QTreeView)
# self.assertIsInstance(self.dialog.model, QStandardItemModel)
# self.assertIsInstance(self.dialog.button_add, QPushButton)
# self.assertIsInstance(self.dialog.button_delete, QPushButton)
# self.assertEqual(self.dialog.button_ok, QDialog.Accepted)
# assert dlg is not None
# qtbot.addWidget(dlg)
# assert 1 == 0
# qtbot.mouseClick(dlg.cancel_button, Qt.LeftButton)  # click the cancel button
# assert not dlg.isVisible()  # check that the dialog is no longer visible


# def test_add_category(qtbot, view, cat_repo):
#     # Set up the test case
#     category_name = "Test Category"
#     view.edit_category.setText(category_name)

#     # Simulate a button click and wait for the signal to be emitted
#     with qtbot.waitSignal(view.button_categories.clicked):
#         view.button_categories.click()

#     # Check that the category was added to the repository
#     categories = cat_repo.get_all()
#     assert len(categories) == 1
#     assert categories[0].name == category_name

# class TestCategoryDialog(unittest.TestCase):
#     def setUp(self):
#         self.app = QApplication([])
#         self.cat_repo = Mock()
#         self.dialog = CategoryDialog(self.cat_repo)

#     def tearDown(self):
#         self.app.quit()

#     def test_init(self):
#         self.assertIsInstance(self.dialog, QDialog)
#         self.assertEqual(self.dialog.windowTitle(), "Редактирование категорий")
#         self.assertIsInstance(self.dialog.treeView, QTreeView)
#         self.assertIsInstance(self.dialog.model, QStandardItemModel)
#         self.assertIsInstance(self.dialog.button_add, QPushButton)
#         self.assertIsInstance(self.dialog.button_delete, QPushButton)
#         self.assertEqual(self.dialog.button_ok, QDialog.Accepted)

#     def test_add_category(self):
#         category_name = "Test Category"
#         parent_pk = 1
#         new_category = Mock(pk=2, name=category_name, parent=parent_pk)
#         self.cat_repo.add.return_value = new_category
#         category = self.dialog.add_category(category_name, parent_pk)
#         self.assertEqual(category, new_category)
#         self.cat_repo.add.assert_called_once_with(Mock(name=category_name, parent=parent_pk))

#     def test_remove_category(self):
#         category_pk = 1
#         category = Mock(pk=category_pk, name="Test Category", parent=None)
#         subcategory1 = Mock(pk=2, name="Subcategory 1", parent=category_pk)
#         subcategory2 = Mock(pk=3, name="Subcategory 2", parent=subcategory1.pk)
#         self.cat_repo.get.return_value = category
#         self.cat_repo.delete.return_value = None
#         self.cat_repo.get_all.return_value = [category, subcategory1, subcategory2]
#         deleted_category = self.dialog.remove_category(category_pk)
#         self.assertEqual(deleted_category, category)
#         self.cat_repo.get.assert_called_once_with(category_pk)
#         self.cat_repo.delete.assert_called_once_with(category_pk)
#         self.cat_repo.get_all.assert_called_once()

#     def test_on_add_button_clicked(self):
#         # TODO: write test for on_add_button_clicked method
#         pass

#     def test_on_delete_button_clicked(self):
#         # TODO: write test for on_delete_button_clicked method
#         pass
