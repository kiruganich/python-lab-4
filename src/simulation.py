import random
import logging
from typing import List, Callable
from src.models import Library, Book
from src.constants import GENRES, AUTHORS, BOOK_TITLES, MIN_YEAR, MAX_YEAR

logger = logging.getLogger(__name__)


class LibrarySimulator:
    
    def __init__(self, library: Library):
        self.library = library
        self.event_counter = 0
        self._isbn_counter = 1000  # Для генерации уникальных ISBN
        
        # Список событий
        self.events: List[Callable] = [
            self.event_add_book,
            self.event_remove_book,
            self.event_search_by_author,
            self.event_search_by_year,
            self.event_search_invalid_isbn,
            self.event_search_by_genre,
        ]
        
        logger.info(f"Simulator initialized with {len(self.events)} event types")
    
    def _generate_isbn(self) -> str:
        isbn = f"ISBN-{self._isbn_counter:06d}"
        self._isbn_counter += 1
        return isbn
    
    def event_add_book(self) -> str:
        title = random.choice(BOOK_TITLES)
        author = random.choice(AUTHORS)
        year = random.randint(MIN_YEAR, MAX_YEAR)
        genre = random.choice(GENRES)
        isbn = self._generate_isbn()
        
        book = Book(title, author, year, genre, isbn)
        self.library.add_book(book)
        
        return f"Added new book: {book}"
    
    def event_remove_book(self) -> str:
        if len(self.library.books) == 0:
            return "Cannot remove: library is empty"
        
        # Получить случайную книгу
        random_index = random.randint(0, len(self.library.books) - 1)
        book_to_remove = self.library.books[random_index]
        
        self.library.remove_book(book_to_remove.isbn)
        return f"Removed book: {book_to_remove}"
    
    def event_search_by_author(self) -> str:
        if len(self.library.books) == 0:
            return "Cannot search: library is empty"
        
        # Выбрать автора из существующих
        author = random.choice(AUTHORS)
        results = self.library.search_by_author(author)
        
        count = len(results)
        return f"Search by author '{author}': found {count} book(s)"
    
    def event_search_by_year(self) -> str:
        year = random.randint(MIN_YEAR, MAX_YEAR)
        results = self.library.search_by_year(year)
        
        count = len(results)
        return f"Search by year {year}: found {count} book(s)"
    
    def event_search_invalid_isbn(self) -> str:
        fake_isbn = f"ISBN-{random.randint(1, 10000):06d}"
        result = self.library.search_by_isbn(fake_isbn)
        
        if result is None:
            return f"Search by ISBN '{fake_isbn}': NOT FOUND (expected behavior)"
        else:
            return f"Search by ISBN '{fake_isbn}': found unexpected book"
    
    def event_search_by_genre(self) -> str:
        genre = random.choice(GENRES)
        results = self.library.search_by_genre(genre)
        
        count = len(results)
        return f"Search by genre '{genre}': found {count} book(s)"
    
    def run_step(self) -> str:
        self.event_counter += 1
        event_func = random.choice(self.events)
        result = event_func()
        
        formatted = f"[Step {self.event_counter}] {result}"
        logger.info(formatted)
        return formatted
    
    def run_simulation(self, steps: int = 20, seed: int = None) -> None:
        if seed is not None:
            random.seed(seed)
            logger.info(f"Simulation started with seed={seed}")
        else:
            logger.info("Simulation started with random seed")
        
        print("\n" + "="*70)
        print(f"LIBRARY SIMULATION: {steps} steps")
        print("="*70 + "\n")
        
        for _ in range(steps):
            event_output = self.run_step()
            print(event_output)
        
        # Вывести итоговую статистику
        print("\n" + "="*70)
        print("FINAL STATISTICS:")
        print("="*70)
        stats = self.library.get_statistics()
        print(f"Total books: {stats['total_books']}")
        print(f"Unique authors: {stats['unique_authors']}")
        if stats['year_range']:
            print(f"Year range: {stats['year_range'][0]} - {stats['year_range'][1]}")
        print(f"Genres: {', '.join(stats['genres'])}")
        print("="*70 + "\n")
        
        logger.info("Simulation completed")


def run_simulation(steps: int = 20, seed: int = None) -> None:

    # Создать библиотеку
    library = Library("Central Library")
    
    # Добавить несколько начальных книг
    initial_books = [
        Book("Foundation", "Isaac Asimov", 1951, "Science", "ISBN-0001"),
        Book("Cosmos", "Carl Sagan", 1980, "Science", "ISBN-0002"),
        Book("2001: A Space Odyssey", "Arthur C. Clarke", 1968, "Fiction", "ISBN-0003"),
    ]
    
    for book in initial_books:
        library.add_book(book)
    
    # Создать симулятор и запустить
    simulator = LibrarySimulator(library)
    simulator.run_simulation(steps=steps, seed=seed)
