import csv
import pathlib

from pydantic import BaseModel, ConfigDict, Field


class StudentWithOOP(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    name: str = Field(alias="І'мя")
    surname: str = Field(alias="Прізвише")
    oop_level: int = Field(alias="Рівень ІРЦ")


def read_students_from_csv(path: pathlib.Path) -> list[StudentWithOOP]:
    with open(path.as_posix(), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        result = [StudentWithOOP.model_validate(row) for row in reader]

    return result
