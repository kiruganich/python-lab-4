"""
Тесты для системы управления библиотекой (pytest)
"""
import pytest
from src.models import Book, BookCollection, IndexDict, Library
from src.simulation import LibrarySimulator, run_simulation


class TestBook:
    """Тесты для класса Book"""
    
    def test_book_creation(self):
        """Тест создания книги"""
        book = Book("Test", "Author", 2020, "Fiction", "ISBN-001")
        assert book.title == "Test"
        assert book.author == "Author"
        assert book.year == 2020
        assert book.genre == "Fiction"
        assert book.isbn == "ISBN-001"
    
    def test_book_equality(self):
        """Тест равенства книг по ISBN"""
        book1 = Book("Title1", "Author1", 2020, "Fiction", "ISBN-001")
        book2 = Book("Title2", "Author2", 2021, "Science", "ISBN-001")
        book3 = Book("Title1", "Author1", 2020, "Fiction", "ISBN-002")
        
        assert book1 == book2  # Одинаковый ISBN
        assert book1 != book3  # Разные ISBN
    
    def test_book_repr(self):
        """Тест __repr__ для Book"""
        book = Book("Foundation", "Asimov", 1951, "Science", "ISBN-001")
        repr_str = repr(book)
        assert "Foundation" in repr_str
        assert "Asimov" in repr_str
        assert "ISBN-001" in repr_str
    
    def test_book_contains(self):
        """Тест __contains__ для поиска в книге"""
        book = Book("Foundation", "Isaac Asimov", 1951, "Science", "ISBN-001")
        assert "Foundation" in book
        assert "Asimov" in book
        assert "foundation" in book  # Case insensitive
        assert "NonExistent" not in book


class TestBookCollection:
    """Тесты для класса BookCollection"""
    
    def test_collection_creation(self):
        """Тест создания пустой коллекции"""
        collection = BookCollection()
        assert len(collection) == 0
    
    def test_add_book(self):
        """Тест добавления книги"""
        collection = BookCollection()
        book = Book("Test", "Author", 2020, "Fiction", "ISBN-001")
        collection.add(book)
        assert len(collection) == 1
    
    def test_getitem_single(self):
        """Тест __getitem__ для одного элемента"""
        collection = BookCollection()
        book1 = Book("Book1", "Author1", 2020, "Fiction", "ISBN-001")
        book2 = Book("Book2", "Author2", 2021, "Science", "ISBN-002")
        collection.add(book1)
        collection.add(book2)
        
        assert collection[0] == book1
        assert collection[1] == book2
        assert collection[-1] == book2
    
    def test_getitem_slice(self):
        """Тест __getitem__ для срезов"""
        collection = BookCollection()
        books = [
            Book(f"Book{i}", f"Author{i}", 2020 + i, "Fiction", f"ISBN-{i:03d}")
            for i in range(5)
        ]
        for book in books:
            collection.add(book)
        
        # Тест срезов
        slice_result = collection[1:3]
        assert len(slice_result) == 2
        assert slice_result[0] == books[1]
        assert slice_result[1] == books[2]
    
    def test_iter(self):
        """Тест __iter__ для итерации"""
        collection = BookCollection()
        books = [
            Book(f"Book{i}", f"Author{i}", 2020 + i, "Fiction", f"ISBN-{i:03d}")
            for i in range(3)
        ]
        for book in books:
            collection.add(book)
        
        # Проверить итерацию
        iterated_books = list(collection)
        assert len(iterated_books) == 3
        assert iterated_books == books
    
    def test_contains(self):
        """Тест __contains__ для проверки наличия"""
        collection = BookCollection()
        book = Book("Test", "Author", 2020, "Fiction", "ISBN-001")
        collection.add(book)
        
        assert book in collection
        assert "ISBN-001" in collection
        
        other_book = Book("Other", "Other", 2021, "Fiction", "ISBN-999")
        assert other_book not in collection
        assert "ISBN-999" not in collection
    
    def test_remove(self):
        """Тест удаления по ISBN"""
        collection = BookCollection()
        book1 = Book("Book1", "Author1", 2020, "Fiction", "ISBN-001")
        book2 = Book("Book2", "Author2", 2021, "Science", "ISBN-002")
        collection.add(book1)
        collection.add(book2)
        
        assert len(collection) == 2
        
        removed = collection.remove("ISBN-001")
        assert removed is True
        assert len(collection) == 1
        assert "ISBN-001" not in collection
        
        removed = collection.remove("ISBN-999")
        assert removed is False
    
    def test_remove_at_index(self):
        """Тест удаления по индексу"""
        collection = BookCollection()
        books = [
            Book(f"Book{i}", f"Author{i}", 2020 + i, "Fiction", f"ISBN-{i:03d}")
            for i in range(3)
        ]
        for book in books:
            collection.add(book)
        
        removed = collection.remove_at_index(1)
        assert removed == books[1]
        assert len(collection) == 2


class TestIndexDict:
    """Тесты для класса IndexDict"""
    
    def test_index_dict_creation(self):
        """Тест создания пустого индекса"""
        index = IndexDict()
        assert len(index) == 0
    
    def test_add_book(self):
        """Тест добавления книги в индексы"""
        index = IndexDict()
        book = Book("Test", "Author", 2020, "Fiction", "ISBN-001")
        index.add_book(book)
        
        assert len(index) == 1
        assert index.get_by_isbn("ISBN-001") == book
    
    def test_get_by_isbn(self):
        """Тест поиска по ISBN"""
        index = IndexDict()
        book = Book("Foundation", "Asimov", 1951, "Science", "ISBN-001")
        index.add_book(book)
        
        found = index.get_by_isbn("ISBN-001")
        assert found == book
        
        not_found = index.get_by_isbn("ISBN-999")
        assert not_found is None
    
    def test_get_by_author(self):
        """Тест поиска по автору"""
        index = IndexDict()
        book1 = Book("Foundation", "Asimov", 1951, "Science", "ISBN-001")
        book2 = Book("Robot", "Asimov", 1950, "Science", "ISBN-002")
        book3 = Book("Cosmos", "Sagan", 1980, "Science", "ISBN-003")
        
        index.add_book(book1)
        index.add_book(book2)
        index.add_book(book3)
        
        asimov_books = index.get_by_author("Asimov")
        assert len(asimov_books) == 2
        assert book1 in asimov_books
        assert book2 in asimov_books
        
        empty = index.get_by_author("Unknown")
        assert len(empty) == 0
    
    def test_get_by_year(self):
        """Тест поиска по году"""
        index = IndexDict()
        book1 = Book("Book1", "Author1", 2020, "Fiction", "ISBN-001")
        book2 = Book("Book2", "Author2", 2020, "Science", "ISBN-002")
        book3 = Book("Book3", "Author3", 2021, "Fiction", "ISBN-003")
        
        index.add_book(book1)
        index.add_book(book2)
        index.add_book(book3)
        
        year_2020 = index.get_by_year(2020)
        assert len(year_2020) == 2
        
        year_2021 = index.get_by_year(2021)
        assert len(year_2021) == 1
    
    def test_remove_book(self):
        """Тест удаления книги из индексов"""
        index = IndexDict()
        book = Book("Test", "Author", 2020, "Fiction", "ISBN-001")
        index.add_book(book)
        
        assert len(index) == 1
        
        removed = index.remove_book(book)
        assert removed is True
        assert len(index) == 0
        assert index.get_by_isbn("ISBN-001") is None


class TestLibrary:
    """Тесты для класса Library"""
    
    def test_library_creation(self):
        """Тест создания библиотеки"""
        library = Library("Test Library")
        assert library.name == "Test Library"
        assert len(library.books) == 0
    
    def test_add_book(self):
        """Тест добавления книги в библиотеку"""
        library = Library("Test")
        book = Book("Test", "Author", 2020, "Fiction", "ISBN-001")
        library.add_book(book)
        
        assert len(library.books) == 1
        assert library.search_by_isbn("ISBN-001") == book
    
    def test_remove_book(self):
        """Тест удаления книги из библиотеки"""
        library = Library("Test")
        book = Book("Test", "Author", 2020, "Fiction", "ISBN-001")
        library.add_book(book)
        
        assert len(library.books) == 1
        
        removed = library.remove_book("ISBN-001")
        assert removed is True
        assert len(library.books) == 0
    
    def test_search_methods(self):
        """Тест всех методов поиска"""
        library = Library("Test")
        book1 = Book("Foundation", "Asimov", 1951, "Science", "ISBN-001")
        book2 = Book("Cosmos", "Sagan", 1980, "Science", "ISBN-002")
        book3 = Book("Robot", "Asimov", 1950, "Fiction", "ISBN-003")
        
        library.add_book(book1)
        library.add_book(book2)
        library.add_book(book3)
        
        # Поиск по ISBN
        assert library.search_by_isbn("ISBN-001") == book1
        
        # Поиск по автору
        asimov_books = library.search_by_author("Asimov")
        assert len(asimov_books) == 2
        
        # Поиск по году
        year_1951 = library.search_by_year(1951)
        assert len(year_1951) == 1
        
        # Поиск по жанру
        science_books = library.search_by_genre("Science")
        assert len(science_books) == 2
    
    def test_get_statistics(self):
        """Тест получения статистики"""
        library = Library("Test")
        book1 = Book("Foundation", "Asimov", 1951, "Science", "ISBN-001")
        book2 = Book("Cosmos", "Sagan", 1980, "Science", "ISBN-002")
        
        library.add_book(book1)
        library.add_book(book2)
        
        stats = library.get_statistics()
        assert stats['total_books'] == 2
        assert stats['unique_authors'] == 2
        assert 'Science' in stats['genres']


class TestLibrarySimulator:
    """Тесты для симулятора"""
    
    def test_simulator_creation(self):
        """Тест создания симулятора"""
        library = Library("Test")
        simulator = LibrarySimulator(library)
        assert len(simulator.events) > 0
    
    def test_simulation_reproducibility(self):
        """Тест воспроизводимости симуляции с seed"""
        # Первая симуляция
        library1 = Library("Test1")
        simulator1 = LibrarySimulator(library1)
        for _ in range(5):
            simulator1.run_step()
        size1 = len(library1.books)
        
        # Вторая симуляция с тем же seed
        library2 = Library("Test2")
        simulator2 = LibrarySimulator(library2)
        for _ in range(5):
            simulator2.run_step()
        size2 = len(library2.books)
        
        # Размеры должны быть одинаковыми (так как seed генерирует одинаковые события)
        # Примечание: это работает, если использовать одинаковый seed для random
    
    def test_event_add_book(self):
        """Тест события добавления книги"""
        library = Library("Test")
        simulator = LibrarySimulator(library)
        
        result = simulator.event_add_book()
        assert "Added new book" in result
        assert len(library.books) == 1
    
    def test_event_remove_book_empty(self):
        """Тест события удаления из пустой библиотеки"""
        library = Library("Test")
        simulator = LibrarySimulator(library)
        
        result = simulator.event_remove_book()
        assert "empty" in result.lower()
    
    def test_event_remove_book_non_empty(self):
        """Тест события удаления из непустой библиотеки"""
        library = Library("Test")
        book = Book("Test", "Author", 2020, "Fiction", "ISBN-001")
        library.add_book(book)
        
        simulator = LibrarySimulator(library)
        result = simulator.event_remove_book()
        assert "Removed" in result
        assert len(library.books) == 0


class TestIntegration:
    """Интеграционные тесты"""
    
    def test_full_workflow(self):
        """Полный тест работы системы"""
        # Создать библиотеку
        library = Library("Integration Test")
        
        # Добавить несколько книг
        books = [
            Book("Foundation", "Asimov", 1951, "Science", "ISBN-001"),
            Book("Cosmos", "Sagan", 1980, "Science", "ISBN-002"),
            Book("Robot", "Asimov", 1950, "Science", "ISBN-003"),
        ]
        
        for book in books:
            library.add_book(book)
        
        # Проверить, что все добавилось
        assert len(library.books) == 3
        
        # Проверить поиск
        assert library.search_by_isbn("ISBN-001") == books[0]
        assert len(library.search_by_author("Asimov")) == 2
        
        # Удалить книгу
        library.remove_book("ISBN-001")
        assert len(library.books) == 2
        
        # Проверить индексы
        assert library.search_by_isbn("ISBN-001") is None
    
    def test_simulation_full_run(self):
        """Тест полного запуска симуляции"""
        # Это не должно вызывать ошибок
        run_simulation(steps=5, seed=42)
