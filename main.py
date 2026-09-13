from library import Library
from library_console import LibraryConsole


def main():
    library = Library()
    console = LibraryConsole(library)

    console.run()


if __name__ == "__main__":
    main()
