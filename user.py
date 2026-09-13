class User:
    def __init__(self, name, user_id, email):
        self.name = name
        self.user_id = user_id
        self.email = email
        self.borrowed_books = []

    def get_max_books(self):
        raise NotImplementedError

    def get_borrow_days(self):
        raise NotImplementedError

    def get_fine_per_day(self):
        raise NotImplementedError

    def can_borrow(self):
        return len(self.borrowed_books) < self.get_max_books()

    def borrow_book(self, isbn):
        self.borrowed_books.append(isbn)

    def return_book(self, isbn):
        if isbn in self.borrowed_books:
            self.borrowed_books.remove(isbn)


class Student(User):
    def get_max_books(self):
        return 3

    def get_borrow_days(self):
        return 14

    def get_fine_per_day(self):
        return 0.50


class Faculty(User):
    def get_max_books(self):
        return 10

    def get_borrow_days(self):
        return 30

    def get_fine_per_day(self):
        return 1.00


class Guest(User):
    def get_max_books(self):
        return 1

    def get_borrow_days(self):
        return 7

    def get_fine_per_day(self):
        return 1.50
