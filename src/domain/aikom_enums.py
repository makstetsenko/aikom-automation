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
