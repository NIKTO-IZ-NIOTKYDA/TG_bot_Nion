import log.colors as colors
import log.logging as logging

class Lessons:
    log: logging.logging = None

    number_lessons: int = 0
    lessons = [
        ['algebra', 'Алгебра'],
        ['english_lang_1', 'Англ. Яз. (1 группа)'],
        ['english_lang_2', 'Англ. Яз. (2 группа)'],
        ['biology', 'Биология'],
        ['geography', 'География'],
        ['geometry', 'Геометрия'],
        ['computer_science_1', 'Информатика (1 группа)'],
        ['computer_science_2', 'Информатика (2 группа)'],
        ['story', 'История'],
        ['literature', 'Литература'],
        # ['music', 'Музыка'],
        ['OBZR', 'ОБЗР'],
        ['social_science', 'Обществознание'],
        # ['native_literature', 'Родная литература'],
        ['russian_lang', 'Русский язык'],
        # ['TBIS', 'Теория вероятностей и статистика'],
        ['technology', 'Технология'],
        ['physics', 'Физика'],
        ['chemistry', 'Химия']
    ]

    def __init__(self) -> None:
        self.log = logging.logging(Name='LESSONS', Color=colors.blue)

        for lesson in self.lessons:
            self.number_lessons += 1
            self.log.init(f'Load lesson {lesson[0]} : \'{lesson[1]}\'')
        self.log.init(f'Loaded {self.number_lessons} lessons')


    async def GetName(self, id: str) -> str | NameError:
        for id_ in self.lessons:
            if id == id_[0]: return id_[1]
            else: continue
        
        return NameError
