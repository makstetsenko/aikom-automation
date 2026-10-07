import logging

from playwright.sync_api import Page

from src.action_description_factory.action_executor import student_enrolment_executor
from src.action_description_factory.action_executor import student_meal_setup_executor
from src.action_description_factory.action_executor import student_sen_level_executor
from src.action_description_factory.action_executor import student_transfer_executor
from src.action_description_factory.action_executor import student_withdrawal_executor
from src.action_description_factory.action_executor import teaching_load_setup_executor
from src.action_description_factory.action_executor import update_classes_type_executor
from src.action_description_factory.action_executor import go_home_executor

from src.action_description_factory.action_descriptor import ActionDescriptor
from src.action_description_factory.action_descriptor import ActionName

logger = logging.getLogger(__name__)

EXECUTION_MAP = {
    ActionName.GO_HOME: go_home_executor.execute,
    ActionName.STUDENT_ENROLMENT: student_enrolment_executor.execute,
    ActionName.STUDENT_MEAL_SETUP: student_meal_setup_executor.execute,
    ActionName.STUDENT_SEN_LEVEL: student_sen_level_executor.execute,
    ActionName.STUDENT_TRANSFER: student_transfer_executor.execute,
    ActionName.STUDENT_WITHDRAWAL: student_withdrawal_executor.execute,
    ActionName.TEACHING_LOAD_SETUP: teaching_load_setup_executor.execute,
    ActionName.UPDATE_CLASSES_TYPE: update_classes_type_executor.execute,
}


def execute(descriptor: ActionDescriptor, page: Page):
    logger.info(f"Executing {descriptor.name.value}")
    action = EXECUTION_MAP[descriptor.name]
    action(descriptor.data_source, page)
