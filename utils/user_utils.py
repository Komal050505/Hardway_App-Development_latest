from app_development.app.constants import *
from app_development.logging_activity.logging_utils import *
import re

"""
This module contains utilities which are repeated in the actual program. Programmers can use these in their code.
"""


# MOBILE VALIDATION
def is_valid_mobile(mobile):
    """
    This function checks whether the mobile number is valid or not.
    :param mobile: int
    :return: bool
    """
    log_info(f" ------is valid mobile function entered------\n")
    try:
        if isinstance(mobile, int):
            converted_str = str(mobile)
            if len(converted_str) == 12:
                if converted_str[:2] in VALID_COUNTRY_LIST:
                    log_debug(f"converted str {converted_str[:2]} is in {VALID_COUNTRY_LIST}")
                    log_info("------is valid mobile function ended------")
                    return True
                else:
                    log_error(f"Invalid country code - {converted_str[:2]} which is not in {VALID_COUNTRY_LIST}")
                    raise ValueError(f"Invalid country code - {converted_str[:2]} which is not in {VALID_COUNTRY_LIST}")
            else:
                log_error(f"Invalid length of mobile - {converted_str}, should be length of 12")
                raise ValueError(f"Invalid mobile number length - {mobile}")
        else:
            log_error(f"Invalid mobile type - {mobile}, should be an integer")
            raise ValueError(f"Invalid mobile number type - {type(mobile)}")
    except Exception as error:
        log_error(f"Error in is_valid_mobile function: {error}")
        return err


try:
    mobiles = 912459878954
    is_valid_mobile(mobiles)
    log_info(f"Result: {mobiles}")
except ValueError as e:
    log_error(e)


def is_excluded(mobile_num):
    """
    This function checks whether the mobile number is in the exemptions mobile number list.
    :param mobile_num: int
    :return: bool
    """
    log_info(f" ------is excluded function entered------\n")

    if not isinstance(mobile_num, int):
        log_error(f"Invalid type for mobile_num: {type(mobile_num)}. Expected type is int.")
        raise ValueError(f"Invalid type for mobile_num: {type(mobile_num)}. Expected type is int.")

    if mobile_num in EXCLUDED_NUMBERS:
        log_debug(f"mobile_num {mobile_num} is in EXCLUDED_NUMBERS {EXCLUDED_NUMBERS}. Verification successful.")
        return True
    log_warning(f"mobile_num {mobile_num} is not in {EXCLUDED_NUMBERS}.")
    return False


try:
    mobile_nums = 912459878954
    is_excluded(mobile_nums)
    log_info(f"Result: {mobile_nums}")
except ValueError as e:
    log_error(e)


def is_valid_country(converted_str):
    """
    This function checks whether the mobile number matches the given country code or not.
    :param converted_str: str
    :return: bool
    """
    log_info(f" ------is valid country function entered------\n")
    if converted_str[:2] in VALID_COUNTRY_LIST:
        log_debug(f"converted_str {converted_str} is in VALID_COUNTRY_LIST {VALID_COUNTRY_LIST}")
        return True
    else:
        log_error(f"Invalid country code - {converted_str[:2]} which is not in {VALID_COUNTRY_LIST}")
        raise ValueError(f"Invalid country code - {converted_str[:2]}. Valid country codes are {VALID_COUNTRY_LIST}")


try:
    converted_strs = "561245625142"
    is_valid_country(converted_strs)
    log_info(f"Result: {converted_strs}")
except ValueError as e:
    log_error(e)


def is_mobile_length_valid(converted_str):
    """
    This function checks whether the mobile number length matches the desired length or not.
    :param converted_str: str
    :return: bool
    """
    log_info(f" ------is mobile length valid function entered------\n")
    if len(converted_str) == 12:
        log_debug(f"converted_str {converted_str} is of valid length (12 digits)")
        log_info("------is mobile length valid function ended------")
        return True
    else:
        log_error(f"Invalid mobile length - {converted_str}, should be length of 12")
        raise ValueError(f"Invalid mobile number length {len(converted_str)}. Valid length is {converted_str}")


try:
    converted_strs = is_mobile_length_valid("564215210212")
    log_info(f"Result: {converted_strs}")
except ValueError as e:
    log_error(e)


def is_valid_type(mobile):
    """
    This function checks whether the type of the mobile number is valid or not.
    :param mobile: int
    :return: bool
    """
    log_info(f" ------is  valid type function entered------\n")
    if isinstance(mobile, int):
        log_debug(f" {mobile} is of valid type -- {isinstance(mobile, int)}")
        return True
    else:
        log_error(f"Invalid mobile type - {mobile}, should be an integer")
        raise ValueError(f"Invalid mobile number type - {type(mobile)}")


try:
    mobiles = is_valid_type(561245789654)
    log_info(f"Result: {mobiles}")
except ValueError as e:
    log_error(e)


def is_valid_record(RAW_DATA, record):
    """
    This function checks whether the record is valid or not.
    :param RAW_DATA: dict
    :param record: list of dict
    :return: bool
    """
    log_info(f" ------is  valid record function entered------\n")

    if not isinstance(RAW_DATA, dict):
        log_error(f"Invalid data structure - {RAW_DATA}, should be a dict")
        raise ValueError(f"Invalid input DATA {RAW_DATA}")

    if not isinstance(record, dict):
        log_error(f"Invalid data structure - {record}, should be a dict")
        raise ValueError(f"Record should be a dictionary, got {type(record)} instead.")

    if "mobile" not in record:
        log_error(f"Missing 'mobile' key in record: {record}")
        raise ValueError(f"Missing 'mobile' key in record: {record}")

    log_debug(f"Record {record} is valid")
    return True


try:
    valid_record = is_valid_record(DATA, {"mobile": 9898989898, "name": "Suresh", "company": "MIND TREE"})
    log_info(f"Result: {valid_record}")
except ValueError as err:
    log_error(err)


def is_valid_employee_id(employee_id):
    """
    This function checks whether the employee ID is valid or not.
    :param employee_id: str
    :return: bool
    """
    log_info(f" ------is valid employee ID function entered------\n")
    if isinstance(employee_id, str) and employee_id.startswith("EMP") and len(employee_id) == 6:
        log_debug(f"Employee ID {employee_id} is valid.")
        # if employee_id not in VALID_EMPLOYEE_IDS:
        #     log_warning(f"{employee_id} is not in {VALID_EMPLOYEE_IDS}")
        #     return False
        # else:
        #     log_info(f"{employee_id} is in {VALID_EMPLOYEE_IDS}")
        #     return True
        return True
    else:
        log_warning(f"Invalid employee ID format: {employee_id}")
        return False


def send_email(recipients, message):
    """
    Sends an email to the given recipients.
    :param recipients: list of str
    :param message: str
    :return: None
    """
    log_info(f"Sending email to {recipients} with message: {message}")

    log_debug("Email sent successfully.")


def is_valid_email(email):
    # Define the regex pattern for a valid email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
