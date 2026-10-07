import csv
import datetime
import pathlib

from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.domain.aikom_enums import StudentTransferOrderType, StudyingForm


class TransferStudent(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    student_name: str = Field(alias="Ім'я учня")
    student_surname: str = Field(alias="Прізвище учня")
    transfer_type: StudentTransferOrderType = Field(alias="Тип переведення")
    order_number: str = Field(alias="Номер наказу")
    order_date: datetime.date = Field(alias="Дата наказу")

    from_academic_year: str = Field(alias="Перевести з навчального року")
    from_studying_form: StudyingForm = Field(alias="Перевести з форми навчання")
    from_class_year: int = Field(alias="Перевести з паралелі")
    from_class_name: str | None = Field(alias="Перевести з класу")

    to_academic_year: str = Field(alias="Перевести в навчальний рік")
    to_studying_form: StudyingForm = Field(alias="Перевести на форму навчання")
    to_class_year: int = Field(alias="Перевести в паралель")
    to_class_name: str | None = Field(alias="Перевести в клас")

    was_done: bool = Field(alias="Виконано?")

    @field_validator("order_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, datetime.date):
            return value

        return datetime.datetime.strptime(value, "%d.%m.%Y").date()

    @field_validator("was_done", mode="before")
    @classmethod
    def parse_bool(cls, value):
        if isinstance(value, bool):
            return value

        if value is None or str(value) == "":
            return False

        return str(value).lower() == "так"


def read_students_from_csv(path: pathlib.Path) -> list[TransferStudent]:
    with open(path.as_posix(), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        result = [TransferStudent.model_validate(row) for row in reader]

    return result
