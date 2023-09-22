import csv

from PySide6.QtGui import QAction, QStandardItemModel
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QVBoxLayout, \
    QListWidget, QWidget

from Book import Book
from EditBookDialog import EditBookDialog
from BookInfo import BookInfo


class MainWindow(QMainWindow):
    def __init__(self):  # Инициализация главного окна
        super().__init__()

        self.setWindowTitle("Лист книг")
        self.setMinimumWidth(900)
        self.setMinimumHeight(600)

        # Создание главных элементов
        self.books = []
        self.filtered_books = []
        self.genres = []
        self.books_by_year_window = None
        self.genre_charts_window = None
        self.books_info = None

        self.model = QStandardItemModel()

        # Создание меню
        self.menu_bar = self.menuBar()

        file_menu = self.menu_bar.addMenu("Файл")  # Отдельная вкладка  в меню

        load_action = QAction("Обновить данные", self)  # Кнопка во вкладке
        load_action.triggered.connect(self.load_data)
        file_menu.addAction(load_action)

        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_data)
        file_menu.addAction(save_action)

        exit_action = QAction("Выйти из приложения", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = self.menu_bar.addMenu("Редактирование")

        add_action = QAction("Добавить новую книгу", self)
        add_action.triggered.connect(self.add_book)
        edit_menu.addAction(add_action)

        edit_action = QAction("Редактировать выбранную книгу", self)
        edit_action.triggered.connect(self.edit_book)
        edit_menu.addAction(edit_action)

        delete_action = QAction("Удалить выбранную книгу", self)
        delete_action.triggered.connect(self.delete_book)
        edit_menu.addAction(delete_action)

        filter_menu = self.menu_bar.addMenu("Фильтрация списка")

        by_genre_action = QAction("Фильтрация по жанру", self)
        by_genre_action.triggered.connect(self.filter_by_genre)
        filter_menu.addAction(by_genre_action)

        reset_filter_action = QAction("Сбросить фильтр", self)
        reset_filter_action.triggered.connect(self.reset_filter)
        filter_menu.addAction(reset_filter_action)

        additionally_menu = self.menu_bar.addMenu("Дополнительно")

        books_by_year_action = QAction("Открыть списки книг по годам", self)
        books_by_year_action.triggered.connect(self.books_by_year)
        additionally_menu.addAction(books_by_year_action)

        genre_charts_action = QAction("Сформировать гистограммы для издательств", self)
        genre_charts_action.triggered.connect(self.genre_charts)
        additionally_menu.addAction(genre_charts_action)

        # Создание в окне списка
        self.list = QListWidget()
        self.list.itemClicked.connect(self.book_info)
        self.load_data()  # Загрузка данных в список

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.list)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_data(self):  # Загрузка данных
        #  Очищение массивов с данными
        self.books.clear()
        self.filtered_books.clear()
        # Построчное чтение файла
        with open("data_books.csv", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # Проверка строки на корректность и заполнение массивов
                if len(row) == 7:
                    book = Book(*row)
                    self.books.append(book)
                    self.filtered_books.append(book)
                    if row[2] not in self.genres:
                        self.genres.append(row[2])
        self.update_model()  # Обновление таблицы

    def save_data(self):  # Сохранение изменений (Перезапись исходного файла)
        with open("data_books.csv", "w", encoding="utf-8") as file:
            for book in self.books:
                file.write(f"{book.title},{book.author},{book.genre},{book.publisher},{book.year},"
                           f"{book.pages},{book.price}\n")

    def book_info(self):  # Полная информация
        selected_row = self.list.currentRow()
        if selected_row >= 0:
            book = self.filtered_books[selected_row]
            self.books_info = BookInfo(book)
            self.books_info.show()

    def add_book(self):  # Добавление новой книги
        dialog = EditBookDialog()
        dialog.setWindowTitle("Добавление")
        if dialog.exec() == QDialog.Accepted:  # Запуск окна и проверка подтверждения
            book = dialog.get_book_data()
            self.books.append(book)
            if book.genre not in self.genres:
                self.genres.append(book.genre)
            self.reset_filter()  # Сброс фильтров, иначе книга отобразится в отфильтрованном списке

    def edit_book(self):  # Редактирование книги
        selected_row = self.list.currentRow()  # Номер выбранной строки

        if selected_row >= 0:
            book = self.filtered_books[selected_row]  # Берет книгу из этой строки

            dialog = EditBookDialog()
            dialog.setWindowTitle("Редактирование")

            # Заполнение форм данными книги
            dialog.title_input.setText(book.title)
            dialog.author_input.setText(book.author)
            dialog.genre_input.setText(book.genre)
            dialog.publisher_input.setText(book.publisher)
            dialog.year_input.setText(book.year)
            dialog.pages_input.setText(book.pages)
            dialog.price_input.setText(book.price)

            if dialog.exec() == QDialog.Accepted:  # Запуск окна и проверка подтверждения
                editedBook = dialog.get_book_data()

                # Обновление данных книги
                book.title = editedBook.title
                book.author = editedBook.author
                book.genre = editedBook.genre
                book.publisher = editedBook.publisher
                book.year = editedBook.year
                book.pages = editedBook.pages
                book.price = editedBook.price

                self.update_model()  # Обновление таблицы

    def delete_book(self):
        selected_row = self.list.currentRow()  # Номер выбранной строки
        if selected_row >= 0:
            book = self.filtered_books[selected_row]  # Берет книгу из этой строки
            self.books.pop(self.books.index(book))  # Удаление книги
            self.filtered_books.pop(self.filtered_books.index(book))
            self.update_model()  # Обновление таблицы

    def filter_by_genre(self):  # Фильтрация по жанру
        # Выбор жанра в окошке
        genre, ok = QInputDialog.getItem(self, "Фильтрация по жанру", "Выберите жанр:", self.genres, 0, False)

        if ok:
            self.filtered_books.clear()  # Очищение массива отфильтрованных книг
            # Заполнение новыми данными
            for i in range(len(self.books)):
                if self.books[i].genre == genre:
                    self.filtered_books.append(self.books[i])
            self.update_model()  # Обновление таблицы

    def reset_filter(self):  # Сброс фильтров
        self.filtered_books.clear()  # Очищение массива отфильтрованных книг
        # Заполнение всеми книгами
        for book in self.books:
            self.filtered_books.append(book)
        self.update_model()  # Обновление таблицы

    def update_model(self):  # Обновление списка
        self.list.clear()  # Очищение списка
        # Заполнение
        for book in self.filtered_books:
            self.list.addItem(book.title + " (" + book.author + ")")

    def books_by_year(self):  # Открытие окна с книгами по годам
        try:
            module = __import__("BooksByYear")
            module_class = getattr(module, "BooksByYear")
            self.books_by_year_window = module_class()
            self.books_by_year_window.show()
        except ImportError as e:
            print(f"Ошибка импорта модуля: {e}")

    def genre_charts(self):  # Открытие окна с гистограммами
        try:
            module = __import__("GenreCharts")
            module_class = getattr(module, "GenreCharts")
            self.genre_charts_window = module_class()
            self.genre_charts_window.show()
        except ImportError as e:
            print(f"Ошибка импорта модуля: {e}")


if __name__ == "__main__":  # Запуск приложения
    app = QApplication()
    main_window = MainWindow()
    main_window.show()
    app.exec()
