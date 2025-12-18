import logging
from typing import List, Optional, Union
from src.constants import GENRES, AUTHORS, BOOK_TITLES, MIN_YEAR, MAX_YEAR

logger = logging.getLogger(__name__)


class Book:
    
    def __init__(self, title: str, author: str, year: int, genre: str, isbn: str):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isbn = isbn
    
    def __repr__(self) -> str:
        return f"Book(title='{self.title}', author='{self.author}', isbn='{self.isbn}')"
    
    def __str__(self) -> str:
        return f"{self.title} by {self.author} ({self.year}) - {self.genre} [ISBN: {self.isbn}]"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Book):
            return False
        return self.isbn == other.isbn
    
    def __contains__(self, keyword: str) -> bool:
        keyword_lower = keyword.lower()
        return (keyword_lower in self.title.lower() or 
                keyword_lower in self.author.lower())


class BookCollection:

    def __init__(self):
        self._books: List[Book] = []
    
    def add(self, book: Book) -> None:
        if not isinstance(book, Book):
            raise TypeError("Можно добавлять только объекты Book")
        self._books.append(book)
        logger.debug(f"Added book: {book}")
    
    def remove(self, isbn: str) -> bool:
        for i, book in enumerate(self._books):
            if book.isbn == isbn:
                removed_book = self._books.pop(i)
                logger.debug(f"Removed book: {removed_book}")
                return True
        logger.warning(f"Book with ISBN {isbn} not found")
        return False
    
    def remove_at_index(self, index: int) -> Optional[Book]:
        if 0 <= index < len(self._books):
            removed_book = self._books.pop(index)
            logger.debug(f"Removed book at index {index}: {removed_book}")
            return removed_book
        return None
    
    def clear(self) -> None:
        self._books.clear()
        logger.debug("Collection cleared")
    
    def __getitem__(self, key: Union[int, slice]) -> Union[Book, List[Book]]:
        return self._books[key]
    
    def __iter__(self):
        return iter(self._books)
    
    def __len__(self) -> int:
        return len(self._books)
    
    def __contains__(self, item: Union[Book, str]) -> bool:
        if isinstance(item, Book):
            return item in self._books
        elif isinstance(item, str):
            # Поиск по ISBN
            return any(book.isbn == item for book in self._books)
        return False
    
    def __repr__(self) -> str:
        return f"BookCollection(size={len(self._books)})"


class IndexDict:

    def __init__(self):
        self._by_isbn: dict = {}      # ISBN -> Book
        self._by_author: dict = {}    # Author -> [Books]
        self._by_year: dict = {}      # Year -> [Books]
    
    def add_book(self, book: Book) -> None:
        # Индекс по ISBN
        self._by_isbn[book.isbn] = book
        
        # Индекс по автору
        if book.author not in self._by_author:
            self._by_author[book.author] = []
        self._by_author[book.author].append(book)
        
        # Индекс по году
        if book.year not in self._by_year:
            self._by_year[book.year] = []
        self._by_year[book.year].append(book)
        
        logger.debug(f"Indexed book: {book}")
    
    def remove_book(self, book: Book) -> bool:
        removed = False
        
        # Удалить из ISBN индекса
        if book.isbn in self._by_isbn:
            del self._by_isbn[book.isbn]
            removed = True
        
        # Удалить из автора индекса
        if book.author in self._by_author:
            if book in self._by_author[book.author]:
                self._by_author[book.author].remove(book)
                if not self._by_author[book.author]:
                    del self._by_author[book.author]
        
        # Удалить из года индекса
        if book.year in self._by_year:
            if book in self._by_year[book.year]:
                self._by_year[book.year].remove(book)
                if not self._by_year[book.year]:
                    del self._by_year[book.year]
        
        return removed
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self._by_isbn.get(isbn)
    
    def get_by_author(self, author: str) -> List[Book]:
        return self._by_author.get(author, [])
    
    def get_by_year(self, year: int) -> List[Book]:
        return self._by_year.get(year, [])
    
    def __getitem__(self, key: str):
        return self._by_isbn.get(key)
    
    def __contains__(self, key: str) -> bool:
        return key in self._by_isbn
    
    def __len__(self) -> int:
        return len(self._by_isbn)
    
    def __repr__(self) -> str:
        return (f"IndexDict(by_isbn={len(self._by_isbn)}, "
                f"by_author={len(self._by_author)}, "
                f"by_year={len(self._by_year)})")


class Library:
    
    def __init__(self, name: str = "Main Library"):
        self.name = name
        self.books = BookCollection()
        self.indexes = IndexDict()
        logger.info(f"Library '{name}' initialized")
    
    def add_book(self, book: Book) -> None:
        self.books.add(book)
        self.indexes.add_book(book)
        logger.info(f"Book added to library: {book}")
    
    def remove_book(self, isbn: str) -> bool:
        # Найти книгу
        book = self.indexes.get_by_isbn(isbn)
        if book:
            self.books.remove(isbn)
            self.indexes.remove_book(book)
            logger.info(f"Book removed from library: {book}")
            return True
        logger.warning(f"Book with ISBN {isbn} not found in library")
        return False
    
    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.indexes.get_by_isbn(isbn)
    
    def search_by_author(self, author: str) -> List[Book]:
        return self.indexes.get_by_author(author)
    
    def search_by_year(self, year: int) -> List[Book]:
        return self.indexes.get_by_year(year)
    
    def search_by_genre(self, genre: str) -> List[Book]:
        results = []
        for book in self.books:
            if book.genre == genre:
                results.append(book)
        return results
    
    def get_all_books(self) -> BookCollection:
        return self.books
    
    def get_statistics(self) -> dict:
        authors = set()
        years = set()
        genres = set()
        
        for book in self.books:
            authors.add(book.author)
            years.add(book.year)
            genres.add(book.genre)
        
        return {
            'total_books': len(self.books),
            'unique_authors': len(authors),
            'year_range': (min(years), max(years)) if years else None,
            'genres': list(genres)
        }
    
    def __repr__(self) -> str:
        return f"Library(name='{self.name}', books={len(self.books)}, indexes={self.indexes})"
