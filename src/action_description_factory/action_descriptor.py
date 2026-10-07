from dataclasses import dataclass
from enum import StrEnum
import pathlib

from pydantic import BaseModel, field_validator


class ActionName(StrEnum):
    STUDENT_ENROLMENT = "student_enrolment"
    STUDENT_MEAL_SETUP = "student_meal_setup"
    STUDENT_SEN_LEVEL = "student_sen_level"
    STUDENT_TRANSFER = "student_transfer"
    STUDENT_WITHDRAWAL = "student_withdrawal"
    TEACHING_LOAD_SETUP = "teaching_load_setup"
    UPDATE_CLASSES_TYPE = "update_classes_type"
    GO_HOME = "go_home"


class ActionDescriptor(BaseModel):
    name: ActionName
    data_source: pathlib.Path | None = None
    next: ActionDescriptor | None = None

    @field_validator("data_source", mode="before")
    @classmethod
    def parse_date(cls, value):
        if isinstance(value, pathlib.Path):
            return value

        if value is None:
            return None

        if value.strip() == "":
            return None

        path = pathlib.Path(value.strip()).resolve()

        if not path.exists():
            raise ValueError(f"Path {value} does not exists")

        if not path.is_file():
            raise ValueError(f"Path {value} is not a file")

        if not path.suffix in [".yml", ".yaml", ".csv", ".txt"]:
            raise ValueError(f"Provided file type {path.suffix} is not allowed")

        return path


def read_from_yaml_file(file_path: pathlib.Path) -> ActionDescriptor:
    import yaml

    with open(file_path.as_posix(), "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return ActionDescriptor.model_validate(data)
