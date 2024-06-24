import logging
from Http_Methods.app.constants import *

"""
This module contains utilities which are repeated in actual program. Programmer can use these in his code

"""


# POST
# User1
# User sign up - Insert the new record in the database

# MOBILE VALIDATION
def is_valid_mobile(mobile):
    """
    This function checks whether mobile number is valid or not.
    :param mobile: int
    :return: bool
    """
    if isinstance(mobile, int):
        converted_str = str(mobile)
        if len(converted_str) == 12:
            if converted_str[:2] in VALID_COUNTRY_LIST:
                logging.info("Mobile verification is successful")
                # print("Mobile verification is successful")
                return True
            else:
                raise ValueError(f"Invalid country code - {converted_str[:2]} which is not in {VALID_COUNTRY_LIST}")
        else:
            raise ValueError(f"Invalid mobile number - {mobile}")


def is_excluded(mobile_num):
    """
        This function checks whether mobile number is in the exemptions mobile number list.
        :param mobile_num:
        :return: bool
    """
    if mobile_num in EXCLUDED_NUMBERS:
        print(f"{mobile_num} in excluded list")
        print("Mobile verification is successful")
        return True
    return False


def is_valid_country(converted_str):
    """
        This function checks whether mobile number is matched with the given country code or not.
        :param converted_str:
        :return: bool
    """
    if converted_str[:2] in VALID_COUNTRY_LIST:

        print("Mobile verification is successful")
        return True
    else:
        raise ValueError(f"Invalid country code - {converted_str[:2]}. Valid country codes are -> {VALID_COUNTRY_LIST}")


def is_mobile_length_valid(converted_str):
    """
        This function checks whether mobile number length matches with the desired length  or not.
        :param converted_str: str
        :return: bool
    """
    # Mobile length must be 12 digits
    if len(converted_str) == 12:
        return True
    else:
        raise ValueError(f"Invalid Mobile number length {len(converted_str)}. Valid length is -> {converted_str} ")


def is_valid_type(mobile):
    """
          This function checks whether type of the mobile number is valid or not.
          :param mobile: int
          :return: bool
    """

    if isinstance(mobile, int):
        return True
    else:
        raise ValueError(f"Invalid mobile number type - {type(mobile)}")


def is_valid_record(raw_data, record):
    """
          This function checks whether record is valid or not.
          :param raw_data: dict
          :param record: list of dict
          :return: bool
    """
    if isinstance(record, dict) or "mobile" in record:
        if not isinstance(raw_data, dict):
            raise ValueError(f"Invalid input data {raw_data}")

        if not isinstance(record, list):
            raise ValueError(f"Record should be a list of dictionaries, got {type(record)} instead.")

        for item in record:
            if not isinstance(item, dict):
                raise ValueError(f"Invalid item in record: {item}. Each item should be a dictionary.")
            if "mobile" not in item:
                raise ValueError(f"Missing 'mobile' key in record item: {item}")

        return True


"""
def is_valid_mobile(mobile):
    '''
        This function checks whether mobile number is valid or not.
        :param mobile: int
        :return: bool
    '''
    converted_str = str(mobile)  # e.g., "674545454545"
    mobile_num = int(converted_str[2:])  # int("4545454545") => 4545454545
    if is_valid_type(mobile) and is_mobile_length_valid(converted_str):
        # Excluded persons no further validation required
        if is_excluded(mobile_num):
            return True
        if is_valid_country(converted_str):
            return True
        return False
"""
