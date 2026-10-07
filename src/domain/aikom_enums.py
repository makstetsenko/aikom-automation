from enum import StrEnum


class StudyingForm(StrEnum):
    ON_CAMPUS = "Очна (денна)"
    FAMILY = "Сімейна (домашня)"
    PEDAGOGICAL_SUPPORT = "Педагогічний патронаж"
    EXTERNAL_EDUCATION = "Екстернатна"


class DocumentType(StrEnum):
    BIRTH_CERTIFICATE = "Свідоцтво про народження українського зразка"


class RelationshipToStudentType(StrEnum):
    MOTHER = "Мати"
    FATHER = "Батько"
    GUARDIAN = "Опікун"


class StudentTransferOrderType(StrEnum):
    TRANSFER_TO_NEXT_GRADE = "Переведення учнів до наступного класу"
    REPEAT_GRADE = "Залишення на повторний курс навчання"
    TRANSFER_WITHIN_GRADE = "Переведення з класу в клас в межах паралелі"
    TRANSFER_TO_INDIVIDUAL_STUDY = "Переведення на індивідуальну форму навчання"
