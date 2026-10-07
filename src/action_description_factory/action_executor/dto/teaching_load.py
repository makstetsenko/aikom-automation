import csv
import ast
import pathlib

from pydantic import BaseModel, ConfigDict, Field


class SubjectConfigDto(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    name: str
    hours_per_week: float
    classes: list[str]
    is_main: bool


class SubjectConfig(BaseModel):
    name: str
    hours_per_week: float
    classes: list[str]
    is_main: bool


class TeachingLoadConfig(BaseModel):
    staff_name: str
    staff_surname: str
    job_title: str

    subjects: list[SubjectConfig]


def read_from_directory(path: pathlib.Path) -> list[TeachingLoadConfig]:

    result = []

    for d in path.glob("*.csv"):
        with open(d.as_posix(), encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            subjects = []

            for row in reader:
                row["classes"] = ast.literal_eval(row["classes"])

                subject = SubjectConfigDto.model_validate(row)
                subjects.append(subject)

        staff_full_name = d.stem.split("-")[0]
        job_title = d.stem.split("-")[1]

        result.append(
            TeachingLoadConfig(
                staff_name=staff_full_name.split()[1],
                staff_surname=staff_full_name.split()[0],
                job_title=job_title,
                subjects=[
                    SubjectConfig(name=c.name, hours_per_week=c.hours_per_week, classes=c.classes, is_main=c.is_main)
                    for c in subjects
                ],
            )
        )

    return result
