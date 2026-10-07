import csv
import pathlib

from pydantic import BaseModel, ConfigDict, Field

from src.actions.shared.school.update_class.edit_class_page import ClassType
from src.domain.aikom_enums import StudyingForm


class UpdateClassType(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    academic_year: str = Field(alias="Навчальний рік")
    class_year: int = Field(alias="Паралель")
    class_name: str = Field(alias="Назва класу")
    class_studying_form: StudyingForm = Field(alias="Форма навчання")
    class_teacher_name: str = Field(alias="Класний керівник")
    class_type: ClassType = Field(alias="Тип класу")


def read_from_csv(path: pathlib.Path) -> list[UpdateClassType]:
    with open(path.as_posix(), "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        result = [UpdateClassType.model_validate(row) for row in reader]

    return result
