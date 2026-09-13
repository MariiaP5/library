from datetime import date, timedelta

from book import Book
from user import Student, Faculty, Guest
from borrowing_record import BorrowingRecord


class Library:
    def __init__(self):
        self.books = {}
        self.users = {}
        self.borrowing_history = []

    def add_book(self, title, author, isbn, genre):
        if isbn in self.books:
            return False

        self.books[isbn] = Book(
            title,
            author,
            isbn,
            genre
        )

        return True

    def remove_book(self, isbn):
        book = self.books.get(isbn)

        if book is None or not book.is_available:
            return False

        del self.books[isbn]
        return True

    def find_book(self, isbn):
        return self.books.get(isbn)

    def search_books(self, query):
        query = query.lower()

        return [
            book for book in self.books.values()
            if (
                query in book.title.lower()
                or query in book.author.lower()
                or query in book.isbn.lower()
            )
        ]

    def get_all_books(self):
        return list(self.books.values())

    def register_user(self, name, user_id, email, user_type):
        if user_id in self.users:
            return False

        user_type = user_type.lower()

        if user_type == "student":
            user = Student(name, user_id, email)
        elif user_type == "faculty":
            user = Faculty(name, user_id, email)
        elif user_type == "guest":
            user = Guest(name, user_id, email)
        else:
            return False

        self.users[user_id] = user
        return True

    def find_user(self, user_id):
        return self.users.get(user_id)

    def get_all_users(self):
        return list(self.users.values())

    def borrow_book(self, user_id, isbn):
        user = self.users.get(user_id)

        if user is None:
            return "Пользователь не найден."

        book = self.books.get(isbn)

        if book is None:
            return "Книга не найдена."

        if not book.is_available:
            return "Книга уже выдана."

        if not user.can_borrow():
            return "Пользователь достиг лимита книг."

        borrow_date = date.today()
        due_date = borrow_date + timedelta(
            days=user.get_borrow_days()
        )

        book.is_available = False
        user.borrow_book(isbn)

        record = BorrowingRecord(
            user_id,
            isbn,
            borrow_date,
            due_date
        )

        self.borrowing_history.append(record)

        return f"Книга успешно выдана до {due_date}."

    def return_book(self, user_id, isbn):
        user = self.users.get(user_id)

        if user is None:
            return "Пользователь не найден."

        book = self.books.get(isbn)

        if book is None:
            return "Книга не найдена."

        if isbn not in user.borrowed_books:
            return "Эта книга не числится за пользователем."

        record = None

        for item in reversed(self.borrowing_history):
            if (
                item.user_id == user_id
                and item.isbn == isbn
                and item.return_date is None
            ):
                record = item
                break

        if record is None:
            return "Запись о выдаче не найдена."

        overdue_days = record.get_overdue_days()
        fine = overdue_days * user.get_fine_per_day()

        record.return_date = date.today()
        book.is_available = True
        user.return_book(isbn)

        if fine > 0:
            return (
                f"Книга возвращена. "
                f"Просрочка: {overdue_days} дней. "
                f"Штраф: {fine:.2f}"
            )

        return "Книга успешно возвращена."

    def get_overdue_books(self):
        return [
            record for record in self.borrowing_history
            if record.is_overdue()
        ]
