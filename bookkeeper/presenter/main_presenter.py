from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.sqlite_repository import BudgetTable, SQLiteRepository
from bookkeeper.view.expense_budget_view import MainWindow


class MainPresenter:
    def __init__(
        self,
        view: MainWindow,
        cat_repo: SQLiteRepository[Category],
        exp_repo: SQLiteRepository[Expense],
        bud_repo: BudgetTable,
    ) -> None:
        # self.model = model
        self.view = view
        self.exp_data = None
        self.cat_data = (
            cat_repo.get_all()
        )  # TODO: implement update_cat_data() similar to update_expense_data()
        self.exp_repo = exp_repo
        self.bud_repo = bud_repo
        self.cat_repo = cat_repo

        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_expense_delete_button_clicked(
            self.handle_expense_delete_button_clicked
        )

        self.view.on_budget_day_button_clicked(self.handle_budget_day_button_clicked)
        self.view.on_budget_week_button_clicked(self.handle_budget_week_button_clicked)
        self.view.on_budget_month_button_clicked(
            self.handle_budget_month_button_clicked
        )

        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked
        )

    def update_expense_data(self) -> None:
        self.exp_data = self.exp_repo.get_all()
        if self.exp_data:
            for e in self.exp_data:
                # TODO: "TypeError: 'NoneType' object is not iterable" on empty DB
                for c in self.cat_data:
                    if c.pk == e.category:
                        e.category = c.name
                        break
        self.view.set_expense_table(self.exp_data)

    def update_budget_data(self) -> None:
        self.bud_data = self.bud_repo.get_all()
        self.view.set_budget_table(self.bud_data)

    def update_cat_data(self) -> None:
        self.cat_data = self.cat_repo.get_all()
        self.view.set_category_dropdown(self.cat_data)

    def show(self) -> None:
        self.update_expense_data()
        self.update_budget_data()
        self.update_cat_data()
        self.view.show()

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        comment = self.view.get_comment()
        exp = Expense(int(amount), cat_pk, comment=comment)
        self.exp_repo.add(exp)
        self.bud_repo.create_update_budget_table()
        self.update_expense_data()
        self.update_budget_data()

    def handle_expense_delete_button_clicked(self) -> None:
        selected = self.view.get_selected_expenses()
        if selected:
            for e in selected:
                self.exp_repo.delete(e)
            self.bud_repo.create_update_budget_table()
            self.update_expense_data()
            self.update_budget_data()

    def handle_budget_day_button_clicked(self) -> None:
        value = self.view.get_day_budget()
        self.bud_repo.update_budget(0, value)
        self.update_budget_data()

    def handle_budget_week_button_clicked(self) -> None:
        value = self.view.get_week_budget()
        self.bud_repo.update_budget(1, value)
        self.update_budget_data()

    def handle_budget_month_button_clicked(self) -> None:
        value = self.view.get_month_budget()
        self.bud_repo.update_budget(2, value)
        self.update_budget_data()

    def handle_category_edit_button_clicked(self) -> None:
        self.view.show_cats_dialog(self.cat_repo)
        self.update_cat_data()
