from library import Library


class LibraryConsole:
    def __init__(self, library):
        self.library = library

    def run(self):
        while True:
            self.show_menu()

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.remove_book()
            elif choice == "3":
                self.search_books()
            elif choice == "4":
                self.register_user()
            elif choice == "5":
                self.show_users()
            elif choice == "6":
                self.borrow_book()
            elif choice == "7":
                self.return_book()
            elif choice == "8":
                self.show_overdue_books()
            elif choice == "9":
                self.show_all_books()
            elif choice == "0":
                print("Программа завершена.")
                break
            else:
                print("Некорректный пункт меню.")

    def show_menu(self):
        print("\n===== LIBRARY MANAGEMENT =====")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Найти книгу")
        print("4. Зарегистрировать пользователя")
        print("5. Показать пользователей")
        print("6. Выдать книгу")
        print("7. Вернуть книгу")
        print("8. Просроченные книги")
        print("9. Все книги")
        print("0. Выход")

    def add_book(self):
        title = input("Название: ").strip()
        author = input("Автор: ").strip()
        isbn = input("ISBN: ").strip()
        genre = input("Жанр: ").strip()

        if not all([title, author, isbn, genre]):
            print("Все поля обязательны.")
            return

        if self.library.add_book(title, author, isbn, genre):
            print("Книга добавлена.")
        else:
            print("Книга с таким ISBN уже существует.")

    def remove_book(self):
        isbn = input("Введите ISBN: ").strip()

        if self.library.remove_book(isbn):
            print("Книга удалена.")
        else:
            print("Не удалось удалить книгу.")

    def search_books(self):
        query = input(
            "Введите название, автора или ISBN: "
        ).strip()

        books = self.library.search_books(query)

        if not books:
            print("Книги не найдены.")
            return

        for book in books:
            self.print_book(book)

    def register_user(self):
        name = input("Имя: ").strip()
        user_id = input("ID пользователя: ").strip()
        email = input("Email: ").strip()
        user_type = input(
            "Тип (student/faculty/guest): "
        ).strip()

        if not all([name, user_id, email]):
            print("Все поля обязательны.")
            return

        if self.library.register_user(
            name,
            user_id,
            email,
            user_type
        ):
            print("Пользователь зарегистрирован.")
        else:
            print("Не удалось зарегистрировать пользователя.")

    def show_users(self):
        users = self.library.get_all_users()

        if not users:
            print("Пользователей нет.")
            return

        for user in users:
            print(
                f"{user.name} | "
                f"ID: {user.user_id} | "
                f"Тип: {user.__class__.__name__} | "
                f"Книг: {len(user.borrowed_books)}/"
                f"{user.get_max_books()}"
            )

    def borrow_book(self):
        user_id = input("ID пользователя: ").strip()
        isbn = input("ISBN книги: ").strip()

        print(self.library.borrow_book(user_id, isbn))

    def return_book(self):
        user_id = input("ID пользователя: ").strip()
        isbn = input("ISBN книги: ").strip()

        print(self.library.return_book(user_id, isbn))

    def show_overdue_books(self):
        records = self.library.get_overdue_books()

        if not records:
            print("Просроченных книг нет.")
            return

        for record in records:
            book = self.library.find_book(record.isbn)

            print(
                f"Книга: {book.title if book else record.isbn} | "
                f"Пользователь: {record.user_id} | "
                f"Срок возврата: {record.due_date} | "
                f"Просрочка: {record.get_overdue_days()} дней"
            )

    def show_all_books(self):
        books = self.library.get_all_books()

        if not books:
            print("Книг нет.")
            return

        for book in books:
            self.print_book(book)

    def print_book(self, book):
        status = "доступна" if book.is_available else "выдана"

        print(
            f"{book.title} | "
            f"{book.author} | "
            f"ISBN: {book.isbn} | "
            f"Жанр: {book.genre} | "
            f"{status}"
        )
