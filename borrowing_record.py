from datetime import date


class BorrowingRecord:
    def __init__(self, user_id, isbn, borrow_date, due_date):
        self.user_id = user_id
        self.isbn = isbn
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None

    def is_overdue(self):
        return (
            self.return_date is None
            and date.today() > self.due_date
        )

    def get_overdue_days(self):
        if not self.is_overdue():
            return 0

        return (date.today() - self.due_date).days
