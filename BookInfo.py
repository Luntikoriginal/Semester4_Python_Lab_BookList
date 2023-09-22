from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class BookInfo(QWidget):  # Окно для вывода полной информации
    def __init__(self, book):
        super().__init__()
        self.setWindowTitle("Информация о человеке")
        self.setFixedSize(400, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel(f"Название: {book.title}"))
        layout.addWidget(QLabel(f"Автор: {book.author}"))
        layout.addWidget(QLabel(f"Жанр: {book.genre}"))
        layout.addWidget(QLabel(f"Издательство: {book.publisher}"))
        layout.addWidget(QLabel(f"Количество страниц: {book.year}"))
        layout.addWidget(QLabel(f"Цена: {book.price}"))
        self.setLayout(layout)
