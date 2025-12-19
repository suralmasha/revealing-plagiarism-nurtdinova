import logging
from pathlib import Path

from database.db_utils import create_database, load_synonyms_dict_from_db
from src.plagiarism_detector import PlagiarismRevealer, TextImprover, TextProcessor
from src.report_maker import Reporter
from src.utils.data_loader import SynonymLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    Implement main logic.
    """
    base_dir = Path(__file__).resolve().parent.parent
    corpus_dir = base_dir / 'src' / 'assets' / 'corpus'
    json_path = base_dir / 'src' / 'assets' / 'synonyms.json'

    path_to_check = base_dir / 'assets' / 'corpus_plagiarized' / 'eco_3_pl.txt'

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
        print(f'\nНайдено сходство с документом: {best_match["filename"]}')
        print(reporter.generate_plagiarism_report(best_match['data']))

        syn_map = load_synonyms_dict_from_db()
        improver = TextImprover(syn_map)
        improved_text = improver.rewrite_text(text_to_check)

        new_res = revealer.find_plagiarism(best_match['content'], improved_text, processor)

        print(
            '\n'
            + reporter.generate_rewrite_report(
                rewritten=improved_text,
                old_sim=best_match['score'],
                new_sim=new_res['similarity'],
            )
        )
    else:
        print('\nТекст прошел проверку. Совпадений в корпусе не обнаружено.')


if __name__ == '__main__':
    main()
