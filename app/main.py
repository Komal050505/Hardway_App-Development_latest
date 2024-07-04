from app_development.utils.user_utils import *
from app_development.app.constants import *
from app_development.email_setup.email_constants import *
from app_development.authentication_authorisation.aunthentic_authorised import (
    authenticate_decorator, for_create_delete_user_conditions, for_update_read_user_conditions)
from app_development.logging_activity.logging_utils import *

"""
This module contains the main code to be executed 
"""


@authenticate_decorator
# POST METHOD
def new_record(name, record):
    """
        This method inserts new record.
        :param name: str
        :param record: list of dictionary
        :return: dict
    """
    log_info(f"--------------New Record function Entered  -----------------\n")

    try:

        if for_create_delete_user_conditions(name):

            # Check if 'mobile' key exists in record and is valid
            if "mobile" not in record:
                log_error(f"Missing mobile key in the record {record}")
                raise ValueError("Missing 'mobile' key in record")

            if "employee_id" not in record:
                log_error(f"Missing employee_id key in the record {record}")
                raise ValueError("Missing 'employee_id' key in record")

            mobile_number = record["mobile"]
            log_debug(f" mobile number is extracted - {mobile_number}")
            employee_id = record["employee_id"]
            log_debug(f"Employee ID is extracted - {employee_id}")

            if not is_valid_employee_id(employee_id):
                log_error(f"Invalid employee ID - {employee_id}")
                raise ValueError("Invalid 'employee_id' format")

            # Check if mobile number already exists in AVAILABLE_RECORDS list
            if mobile_number in AVAILABLE_RECORDS or mobile_number in EXCLUDED_NUMBERS:
                log_warning(f"Record with mobile number {mobile_number} already exists. Please enter new details.")
                return "Duplicate Record Found"

            # Insert record into DATA and update AVAILABLE_RECORDS list
            DATA["records"].append(record)
            AVAILABLE_RECORDS.append(mobile_number)

            send_email(["komalsaikiran05@gmail.com"], MESSAGE)
            log_debug(f"Email has been sent to the users ")

            log_debug(f"Record inserted successfully. New record added to AVAILABLE_RECORDS: {AVAILABLE_RECORDS}")

            log_info(f"Record successfully inserted using POST METHOD: {record}")
            return {"message": "Successfully inserted into the record", "record": record}
        else:
            return {"error": "No user details found"}
    except KeyError as err:
        error_message = f"KeyError: {err}. Please check the structure of the record."
        log_error(error_message)
        return {"message": error_message, "status": "Failed"}

    except ValueError as err:
        error_message = str(err)
        log_error(f"Error inserting record: {error_message} using POST METHOD")
        return {"message": error_message, "status": "Failed"}


inserted_record = new_record("komal", {"mobile": 935620002028, "name": "Julie",
                                       "company": "Platinum", "employee_id": "EMP009"})
log_info(
    f" {inserted_record} has been inserted using mobile number \n")
log_info(f"----------------------New Record function Ended---------------------------\n")


# GET METHOD SINGLE USER DETAILS
@authenticate_decorator
def get_single_user_details(name, record):
    """
        This method gets single record.
        :param name: str
        :param record: list of dictionary
        :return: dict
    """
    log_info(f"-----------GET Single User METHOD Entered  ----------------\n")

    try:

        if for_update_read_user_conditions(name):
            if "mobile" in record and "employee_id" in record:
                mobile = record["mobile"]
                employee_id = record["employee_id"]
                log_debug(f"Mobile number extracted: {mobile}")
                log_debug(f"Employee ID extracted: {employee_id}")

                if is_valid_mobile(mobile) and is_valid_employee_id(employee_id):
                    for user in DATA['records']:
                        if user["mobile"] == mobile and user["employee_id"] == employee_id:
                            log_info(f"User details found: {user}")
                            try:
                                send_email(["komalsaikiran05@gmail.com"], GET_SINGLE_MESSAGE)
                                log_debug("Email has been sent to the user")
                            except Exception as err:
                                log_error(f"Failed to send email: {err}")

                            return user

                    log_warning(f"No user details found for mobile number in GET METHOD {mobile}"
                                f" so GET METHOD will return nothing.")

                    return {"error": "User details not found "}
                else:
                    return {"error": "Invalid mobile number or Invalid employee id entered"}
            else:
                return {"error": "Missing 'mobile' key in record"}
        else:
            return {"error": "Access denied"}
    except ValueError as err:
        log_error(f"Error in GET METHOD: {err}")
        return {"error": str(err)}


single_user_details = get_single_user_details("kmakala", {"mobile": 914111111111, "employee_id": "EMP005"})
log_info(
    f" {single_user_details} has been viewed successfully using mobile number {mobiles}  \n")

logging.info(f"-----------------GET Single User METHOD Ended----------------- \n")


# GET ALL USER DETAILS
@authenticate_decorator
def get_all_user_details(name, raw_DATA):
    """
        This method inserts new record.
        :param name: str
        :param raw_DATA: dictionary
        :return: list of dict
    """
    log_info(f"-----------GET All User Details METHOD Entered  --------- \n")
    try:
        if for_update_read_user_conditions(name):
            # Assuming 'DATA' is a dictionary containing a key 'records' which is a list of user records
            if 'records' in raw_DATA:
                log_debug(f"All User details are  -->> {raw_DATA['records']}")

                for user in raw_DATA['records']:
                    log_debug(f"Employee ID: {user.get('employee_id')} and record: {user.get('mobile')}")

                send_email(["komalsaikiran05@gmail.com"], GET_ALL_MESSAGE)
                log_debug(f"Email has been sent to the users ")
                return raw_DATA['records']
            else:
                log_warning(f"No user details found in GET METHOD.")
                return {"error": "No user details found "}
        else:
            return {"error": "Unauthorized access"}
    except ValueError as err:
        log_error(f"Error in GET METHOD: {err}")
        return {"error": str(err)}


all_users = get_all_user_details("komal", DATA)
log_info(
    f" {all_users} has been displayed here \n")
log_info(f"-----------------GET All User Details METHOD Ended----------------- \n")


# DELETE METHOD
@authenticate_decorator
def delete_user_details(name, record):
    """
            This method inserts new record.
            :param name: str
            :param record: list of dictionaries
            :return:  dict
    """
    log_info(f"-----------------Delete User Details METHOD Entered----------------- \n")
    try:
        if for_create_delete_user_conditions(name):
            log_info(f"Delete user details function started")

            employee_id = record.get("employee_id")
            log_debug(f"Employee ID extracted: {employee_id}")

            mobile = record["mobile"]
            log_debug(f"mobile number is extracted - {mobile}")

            if is_valid_mobile(mobile):
                for x, user in enumerate(DATA['records']):
                    if user["mobile"] == mobile:
                        log_debug(f"User details found -->> {user}")

                        deleted_user = DATA['records'].pop(x)

                        send_email(["komalsaikiran05@gmail.com"], DELETE_MESSAGE)
                        log_debug(f"Email has been sent to the users ")

                        log_info(f"User deleted successfully in DELETE METHOD: {deleted_user}")
                        return deleted_user

                log_warning(f"No user details found for mobile number {mobile} so DELETION is not possible.")

                return {"error": "User details not found "}
            else:
                return {"error": "Invalid mobile number"}
        else:
            log_error(f"Un Authorised Entry detected {name}")
            raise ValueError(f"Un Authorised Entry detected {name}")
    except ValueError as err:
        log_error(f"Error: {err}")
        return {"error": str(err)}


deleted_user_details = delete_user_details("kmakala", {"mobile": 914111111111, "employee_id": "EMP001"})
log_info(f"User deleted successfully in DELETE METHOD: {deleted_user_details}")
log_info(f"-----------------Delete User Details METHOD Ended----------------- \n")


@authenticate_decorator
def patch_user_details(name, raw_DATA, record):
    """
            This method inserts new record.
            :param name: str
            :param record: list of dicts
            :param raw_DATA: dictionary
            :return:  dict
    """
    log_info(f"----------------PATCH METHOD Entered---------------- \n")

    try:
        if for_update_read_user_conditions(name):
            employee_id = record.get("employee_id")
            log_debug(f"Employee ID extracted: {employee_id}")
            mobile = record["mobile"]
            log_debug(f"mobile number extracted : {mobile}")

            if is_valid_mobile(mobile):
                for user in raw_DATA['records']:
                    if user["mobile"] == mobile:
                        log_info(f"User found for updating -->> {user}")

                        # Update user details
                        user.update(record)
                        log_info(f"User details updated to -->> {user}")

                        send_email(["komalsaikiran05@gmail.com"], UPDATE_MESSAGE)
                        log_debug(f"Email has been sent to the users ")

                        return user

                log_warning(f"No user details found for mobile number in PATCH METHOD {mobile}")
                return {"error": "User details not found"}

            else:
                log_error(f"Invalid details found for mobile number in PATCH METHOD {mobile}")
                raise ValueError("Invalid mobile number format")
        else:
            return {"error": "Unauthorized access"}
    except ValueError as err:
        log_error(f"Error in PATCH METHOD: {err}")
        return {"error": str(err)}


record_to_update = {"mobile": 913020022100, "name": "John"}
updated_user = patch_user_details("kmakala", DATA, record_to_update)
log_info(
    f"User partial updation done successfully in PATCH METHOD: {updated_user}, updated record is -{record_to_update}")
log_info(f"-----------------Patch User Details METHOD Ended----------------- \n")
