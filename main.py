import sys
import logging
from src.logger_config import setup_logging
from src.simulation import run_simulation


def main():
    setup_logging(log_level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    logger.info("="*70)
    logger.info("LIBRARY MANAGEMENT SYSTEM - SIMULATION")
    logger.info("="*70)

    steps = 20
    seed = None
    
    if len(sys.argv) > 1:
        try:
            if sys.argv[1] in ['-h', '--help']:
                print_help()
                return
 
            steps = int(sys.argv[1])

            if len(sys.argv) > 2:
                seed = int(sys.argv[2])
        except ValueError:
            print("Ошибка: аргументы должны быть целыми числами")
            print_help()
            return
    
    # Запуск симуляции
    try:
        run_simulation(steps=steps, seed=seed)
        logger.info("Simulation completed successfully")
    except Exception as e:
        logger.error(f"Simulation failed: {e}", exc_info=True)
        sys.exit(1)


def print_help():
    help_text = """
Library Management System - Simulation

ИСПОЛЬЗОВАНИЕ:
    python main.py [steps] [seed]

АРГУМЕНТЫ:
    steps    - количество шагов симуляции (по умолчанию: 20)
    seed     - seed для воспроизводимости (по умолчанию: случайный)
    -h, --help - показать эту справку

ПРИМЕРЫ:
    python main.py                  # Запустить 20 шагов со случайным seed
    python main.py 50               # Запустить 50 шагов
    python main.py 30 42            # Запустить 30 шагов с seed=42
    python main.py --help           # Показать эту справку

СОБЫТИЯ СИМУЛЯЦИИ:
    - Добавление новой книги
    - Удаление случайной книги
    - Поиск по автору/году/жанру
    - Попытка получить несуществующую книгу

ТЕСТЫ:
    pytest tests/test.py            # Запустить все тесты
    pytest tests/test.py -v         # С подробным выводом
"""
    print(help_text)


if __name__ == "__main__":
    main()
