import csv

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QTabWidget, QTableView, QHeaderView

from Book import Book


class BooksByYear(QTabWidget):
    def __init__(self):  # Инициализация окна с книгами по годам
        super().__init__()

        self.books = []
        self.load_data()
        self.setWindowTitle("Книги по годам")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        years = set(book.year for book in self.books)  # Создание списка годов без повторений

        # Для каждого года создается таблица с книгами
        for year in sorted(years):
            table_view = QTableView()
            model = QStandardItemModel()
            model.setColumnCount(7)
            model.setHorizontalHeaderLabels(["Название", "Автор", "Жанр", "Издательство", "Год", "Количество страниц",
                                             "Цена"])

            for book in self.books:
                if book.year == year:
                    row = [book.title, book.author, book.genre, book.publisher, book.year, book.pages, book.price]
                    model.appendRow([QStandardItem(item) for item in row])

            table_view.setModel(model)
            table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            self.addTab(table_view, str(year))  # Таблица добавляется в отдельную вкладку

    def load_data(self):
        with open("data_books.csv", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) == 7:
                    book = Book(*row)
                    self.books.append(book)
