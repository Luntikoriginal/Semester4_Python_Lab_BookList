import csv

from PySide6 import QtCharts
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QTabWidget

from Book import Book


class GenreCharts(QTabWidget):
    def __init__(self):  # Инициализация окна с гистограммами
        super().__init__()
        self.setWindowTitle("Гистограммы по жанрам для издательств")
        self.books = []
        self.load_data()

        publishers = set(book.publisher for book in self.books)  # Создание массива издательств без повторений
        publishers.remove("Издательство")  # Лишнее

        for publisher in publishers:  # Для каждого издательства:

            # Создание списка книг издательства
            publisher_books = []
            for book in self.books:
                if book.publisher == publisher:
                    publisher_books.append(book)

            chart_view = QtCharts.QChartView()
            chart = QtCharts.QChart()
            series = QtCharts.QBarSeries()

            genre_counts = {}
            for p_book in publisher_books:
                genre = p_book.genre
                if genre in genre_counts:
                    genre_counts[genre] += 1
                else:
                    genre_counts[genre] = 1

            for genre, count in genre_counts.items():
                bar_set = QtCharts.QBarSet(genre)
                bar_set.append(count)
                series.append(bar_set)

            chart.addSeries(series)
            chart.createDefaultAxes()
            chart_view.setChart(chart)
            chart_view.setRenderHint(QPainter.Antialiasing)
            chart_view.setMinimumSize(500, 500)

            self.addTab(chart_view, publisher)

    def load_data(self):
        with open("data_books.csv", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) == 7:
                    book = Book(*row)
                    self.books.append(book)
