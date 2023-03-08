from bookkeeper.models.expense import Expense
from bookkeeper.view.category import EditCategoryWindow


class ExpensePresenter:
    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.exp_data = None
        self.cat_data = (
            cat_repo.get_all()
        )  # TODO: implement update_cat_data() similar to update_expense_data()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_category_edit_button_clicked(
            self.handle_category_edit_button_clicked
        )

    def update_expense_data(self):
        self.exp_data = self.exp_repo.get_all()
        data = []
        for tup in self.exp_data:
            row = list(tup)
            for cat_tup in self.cat_data:
                if cat_tup[0] == row[2]:
                    row[2] = cat_tup[1]
                    break
            data.append(row)
        self.view.set_expense_table(data)

    # def update_category_data(self):
    #     # print(self.cat_data)# = self.cat_data.get_all()
    #     # data = []
    #     for tup in self.cat_data:
    #         print(tup)
    #         # row = list(tup)
    #         # for cat_tup in self.cat_data:
    #         #     if cat_tup[0] == row[2]:
    #         #         row[2] = cat_tup[1]
    #         #         break
    #         # data.append(row)
    #     # self.view.set_category_dropdown(data)

    def show(self):
        self.view.show()
        self.update_expense_data()
        # self.update_cat_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        exp = Expense(int(amount), cat_pk)
        self.exp_repo.add(exp)
        self.update_expense_data()

    def handle_category_edit_button_clicked(self) -> None:
        self.w = EditCategoryWindow(self.cat_data)
        self.w.show()
