import csv
import datetime
import pathlib

from pydantic import BaseModel, ConfigDict, Field, field_validator


class WithdrawalStudent(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    name: str = Field(alias="Ім'я")
    surname: str = Field(alias="Прізвище")
    parent_full_name: str = Field(alias="ПІБ Одного з батьків")
    parent_phone_number: str = Field(alias="Номер телефону одного з батьків")
    parent_relationship_to_student: str = Field(alias="Відношення до дитини")
    withdrawal_date: datetime.date = Field(alias="Дата Відрахування ")
    withdrawal_order_number: str = Field(alias="Номер наказу")
    withdrawal_order_reason: str = Field(alias="Підстава наказу")
    withdrawal_type: str = Field(alias="Причина відрахування")
    was_withdrawal_done: bool = Field(alias="Виконано?")


    @field_validator("withdrawal_date", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, datetime.date):
            return value

        return datetime.datetime.strptime(value, "%d.%m.%Y").date()
    
    @field_validator("was_withdrawal_done", mode="before")
    @classmethod
    def parse_bool(cls, value):
        if isinstance(value, bool):
            return value

        if value is None or str(value) == "":
            return False

        return str(value).lower() == "так"

def read_students_from_csv(path: pathlib.Path) -> list[WithdrawalStudent]:
    with open(path.as_posix(), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        result = [WithdrawalStudent.model_validate(row) for row in reader]

    return result
