from bookkeeper.view.expense_budget_view import MainWindow


def test_input_expence(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    qtbot.keyClicks(widget.amount_line_edit, "123")
    assert widget.amount_line_edit.text() == "123"
    assert widget.get_amount() == 123
