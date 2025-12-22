import logging
from pathlib import Path

from database.db_utils import create_database, load_synonyms_dict_from_db  # from database import ...
from src.plagiarism_detector import PlagiarismRevealer, TextImprover, TextProcessor  # from .plagiarism_detector import ...
from src.report_maker import Reporter  # from .report_maker import Reporter
from src.utils.data_loader import SynonymLoader  # from .utils import SynonymLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    Implement main logic.
    """
    base_dir = Path(__file__).resolve().parent.parent
    corpus_dir = base_dir / 'src' / 'assets' / 'corpus'
    json_path = base_dir / 'src' / 'assets' / 'synonyms.json'

    path_to_check = base_dir / 'src' / 'assets' / 'corpus_plagiarised' / 'eco_3_pl.txt'
    # Советую "собирать" путь вот так: Path(base_dir, 'src', 'assets', 'corpus_plagiarised', 'eco_3_pl.txt')
    # Это абсолютный аналог вашего варианта, но зато так вы избежите путаницы из-за неоднозначности символа `/`.

    create_database()
    SynonymLoader.load_from_json(json_path)

    processor = TextProcessor()
    revealer = PlagiarismRevealer()
    reporter = Reporter()

    if not path_to_check.exists():
        logger.error(f'Файл для проверки не найден по пути: {path_to_check}')
        return

    text_to_check = path_to_check.read_text(encoding='utf-8')
    logger.info(f'Загружен текст для проверки: {path_to_check.name}')

    best_match = {'filename': None, 'score': -1, 'data': None, 'content': None}

    corpus_files = list(corpus_dir.glob('*.txt'))
    if not corpus_files:
        logger.warning('Корпус пуст! Положите оригиналы в src/assets/corpus/')
        return

    for file_path in corpus_files:
        original_content = file_path.read_text(encoding='utf-8')
        res = revealer.find_plagiarism(original_content, text_to_check, processor)

        if res['similarity'] > best_match['score']:
            best_match = {
                'filename': file_path.name,
                'score': res['similarity'],
                'data': res,
                'content': original_content,
            }

    bound = 0.15
    if best_match['filename'] and best_match['score'] > bound:
        logger.info(f'\nНайдено сходство с документом: {best_match["filename"]}')
        print(reporter.generate_plagiarism_report(best_match['data']))  # Expected type 'dict', got 'int | None' instead

        synonyms = load_synonyms_dict_from_db()
        improver = TextImprover(synonyms)
        improved_text = improver.rewrite_text(text_to_check)

        new_res = revealer.find_plagiarism(best_match['content'], improved_text, processor)  # Expected type 'str', got 'int | None' instead

        print(
            '\n'
            + reporter.generate_rewrite_report(
                rewritten=improved_text,
                old_sim=best_match['score'],
                new_sim=new_res['similarity'],
            )
        )
    else:
        logger.info('\nТекст прошел проверку на плагиат. Совпадений в корпусе не обнаружено.')


if __name__ == '__main__':
    main()
