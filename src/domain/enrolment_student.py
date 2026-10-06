import csv
import datetime
import pathlib

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.aikom_enums import RelationshipToStudentType, StudyingForm


class EnrolmentStudent(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    student_birth_certificate_serial: str = Field(alias="Серія свідотства про народження дитини")
    student_birth_certificate_number: str = Field(alias="Номер свідотства про народження дитини")
    student_birth_date: datetime.date = Field(alias="Дата народження дитини")
    academic_year: str = Field(alias="Навчальний рік до зарахування")
    studying_form: StudyingForm = Field(alias="Форма навчання")
    class_year: int = Field(alias="Паралель")
    class_name: str = Field(alias="Клас")
    parent_name: str = Field(alias="ПІБ одного з батьків")
    parent_phone_number: str = Field(alias="Номер телефону одного з батьків")
    parent_relationship_to_student: RelationshipToStudentType = Field(alias="Тип відносин з дитиною одного з батьків")
    enrolment_date: datetime.date = Field(alias="Дата зарахування")
    enrolment_order_number: str = Field(alias="Номер наказу про зарахування")
    was_enrolment_done: bool = Field(alias="Виконано?")

    @field_validator("student_birth_date", "enrolment_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, datetime.date):
            return value

        return datetime.datetime.strptime(value, "%d.%m.%Y").date()

    @field_validator("was_enrolment_done", mode="before")
    @classmethod
    def parse_bool(cls, value):
        if isinstance(value, bool):
            return value

        if value is None or str(value) == "":
            return False

        return str(value).lower() == "так"


def read_students_from_csv(path: pathlib.Path) -> list[EnrolmentStudent]:
    with open(path.as_posix(), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        result = [EnrolmentStudent.model_validate(row) for row in reader]

    return result
