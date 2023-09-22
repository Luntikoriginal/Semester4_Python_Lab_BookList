from PySide6.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QLabel, QDialogButtonBox

from Book import Book


class EditBookDialog(QDialog):
    def __init__(self):
        super().__init__()  # Инициализация окна
        self.setModal(True)

        layout = QVBoxLayout()  # Вертикальный блок
        # Создание форм
        layout.addWidget(QLabel("Название:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("Автор:"))
        self.author_input = QLineEdit()
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel("Жанр:"))
        self.genre_input = QLineEdit()
        layout.addWidget(self.genre_input)
        layout.addWidget(QLabel("Издательство:"))
        self.publisher_input = QLineEdit()
        layout.addWidget(self.publisher_input)
        layout.addWidget(QLabel("Год:"))
        self.year_input = QLineEdit()
        layout.addWidget(self.year_input)
        layout.addWidget(QLabel("Количество страниц:"))
        self.pages_input = QLineEdit()
        layout.addWidget(self.pages_input)
        layout.addWidget(QLabel("Цена:"))
        self.price_input = QLineEdit()
        layout.addWidget(self.price_input)

        # Создание кнопок
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_book_data(self):  # Возвращает отредактированную книгу
        # Присваивание переменным содержимого форм
        title = self.title_input.text()
        author = self.author_input.text()
        genre = self.genre_input.text()
        publisher = self.publisher_input.text()
        year = self.year_input.text()
        pages = self.pages_input.text()
        price = self.price_input.text()

        return Book(title, author, genre, publisher, year, pages, price)
