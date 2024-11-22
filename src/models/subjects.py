from enum import Enum, auto


class Subjects(Enum):
    MATH = auto()
    PHYSICS = auto()
    ASTRONOMY = auto()
    COMPUTER_SCIENCE = auto()
    GEOGRAPHY = auto()
    ECOLOGY = auto()

    def get_localized_name(self):
        match self:
            case Subjects.MATH:
                return 'Математика'
            case Subjects.PHYSICS:
                return 'Физика'
            case Subjects.ASTRONOMY:
                return 'Астрономия'
            case Subjects.COMPUTER_SCIENCE:
                return 'Информатика'
            case Subjects.GEOGRAPHY:
                return 'География'
            case Subjects.ECOLOGY:
                return 'Экология'

    def get_db_name(self):
        match self:
            case Subjects.MATH:
                return 'math'
            case Subjects.PHYSICS:
                return 'physics'
            case Subjects.ASTRONOMY:
                return 'astronomy'
            case Subjects.COMPUTER_SCIENCE:
                return 'computer_science'
            case Subjects.GEOGRAPHY:
                return 'geography'
            case Subjects.ECOLOGY:
                return 'ecology'

def get_subjects_string(subs):
    k = []
    if subs.math:
        k.append(Subjects.get_localized_name(Subjects.MATH))
    if subs.physics:
        k.append(Subjects.get_localized_name(Subjects.PHYSICS))
    if subs.astronomy:
        k.append(Subjects.get_localized_name(Subjects.ASTRONOMY))
    if subs.computer_science:
        k.append(Subjects.get_localized_name(Subjects.COMPUTER_SCIENCE))
    if subs.geography:
        k.append(Subjects.get_localized_name(Subjects.GEOGRAPHY))
    if subs.ecology:
        k.append(Subjects.get_localized_name(Subjects.ECOLOGY))
    return ', '.join(k)

def subjects_dict_to_model(sub_dict):
    ret = {}
    for i in sub_dict:
        ret[Subjects.get_db_name(Subjects(i))] = sub_dict[i]
    return ret
