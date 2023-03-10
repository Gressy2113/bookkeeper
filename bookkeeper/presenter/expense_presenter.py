from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget


# from bookkeeper.view.categories_view import EditCategoryWindow


class ExpensePresenter:
    def __init__(self, model, view, cat_repo, exp_repo, bud_repo):
        self.model = model
        self.view = view
        self.exp_data = None
        self.cat_data = (
            cat_repo.get_all()
        )  # TODO: implement update_cat_data() similar to update_expense_data()
        self.exp_repo = exp_repo
        self.bud_repo = bud_repo

        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked
        )

    def update_expense_data(self):
        self.exp_data = self.exp_repo.get_all()
        for e in self.exp_data:
            # TODO: "TypeError: 'NoneType' object is not iterable" on empty DB
            for c in self.cat_data:
                if c.pk == e.category:
                    e.category = c.name
                    break
        self.view.set_expense_table(self.exp_data)

    def update_budget_data(self):
        self.bud_data = self.bud_repo.get_all()
        # print(self.bud_data)
        self.view.set_budget_table(self.bud_data)

    def show(self):
        self.view.show()
        self.update_expense_data()
        self.update_budget_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        exp = Expense(int(amount), cat_pk)
        self.exp_repo.add(exp)
        self.bud_repo.create_update_budget_table()
        self.update_expense_data()
        self.update_budget_data()

    def handle_category_edit_button_clicked(self):
        self.view.show_cats_dialog(self.cat_data)
