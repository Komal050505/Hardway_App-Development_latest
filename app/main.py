from app_development.utils.user_utils import *
from app_development.app.constants import *
from app_development.email_setup.email_constants import *
from app_development.authentication_authorisation.aunthentic_authorised import (
    authenticate_decorator, admin_operations, is_admin, is_normal_user, normal_user_operations)
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
        :param record:  dictionary
        :return: dict
    """
    log_info(f"--------------New Record function Entered  -----------------\n")

    try:
        # validates admin_operations(name) function (authentic_authorised.py)
        if admin_operations(name):

            # Check if 'mobile' key exists in record and is valid
            if "mobile" not in record:
                log_error(f"Missing mobile key in the record {record}")
                raise ValueError("Missing 'mobile' key in record")

            # Check if 'employee_id' key exists in record and is valid
            if "employee_id" not in record:
                log_error(f"Missing employee_id key in the record {record}")
                raise ValueError("Missing 'employee_id' key in record")

            # assigns dict record having key mobile (record["mobile"]) to mobile_number
            mobile_number = record["mobile"]
            log_debug(f" mobile number is extracted - {mobile_number}")

            # assigns dict record having key employee id (record["employee_id"]) to employee_id
            employee_id = record["employee_id"]
            log_debug(f"Employee ID is extracted - {employee_id}")

            # checks if employee id, if it is not valid  then exits... which is in user_utils.py
            if not is_valid_employee_id(employee_id):
                log_error(f"Invalid employee ID - {employee_id}")
                raise ValueError("Invalid 'employee_id' format")

            # Check if mobile number already exists in AVAILABLE_RECORDS list which is in constants.py
            if mobile_number in AVAILABLE_RECORDS:
                log_warning(f"Record with mobile number {mobile_number} already exists. Please enter new details.")
                return "Duplicate Record Found"

            # Insert record into DATA and update AVAILABLE_RECORDS list
            DATA["records"].append(record)
            AVAILABLE_RECORDS.append(mobile_number)

            # This email will not display anything because there is no database linked .
            send_email(["komalsaikiran05@gmail.com"], f"Admin -'{name}]- added a new record {record}.")
            log_debug(f"Email has been sent to the users ")

            log_debug(f"Record inserted successfully. New record added to AVAILABLE_RECORDS: {AVAILABLE_RECORDS}")

            log_info(f"Record successfully inserted using POST METHOD: {record}")
            return {"message": "Successfully inserted into the record", "record": record}
        else:
            log_error(f"Unauthorized access: {name} does not have permission to create new records.")
            return {"error": "No user details found"}
    except KeyError as error:
        error_message = f"KeyError: {error}. Please check the structure of the record."
        log_error(error_message)
        return {"message": error_message, "status": "Failed"}

    except ValueError as error:
        error_message = str(error)
        log_error(f"Error inserting record: {error_message} using POST METHOD")
        return {"message": error_message, "status": "Failed"}
    except Exception as error:
        error_message = f"Unexpected error: {str(error)}"
        log_error(f"Error inserting record: {error_message} using POST METHOD")
        return {"message": error_message, "status": "Failed"}


# Only Admin users should create new record so name should be in admin list.
inserted_record = new_record("komal", {"mobile": 935620002028, "name": "Julie",
                                       "company": "Platinum", "employee_id": "EMP009"})
log_info(
    f" {inserted_record} has been inserted using mobile number \n")
log_info(f"----------------------New Record function Ended---------------------------\n")


# GET METHOD SINGLE USER DETAILS
@authenticate_decorator
def get_single_user_details(username, name, record):
    """
        This method gets single record.
        :param username: str
        :param name: str
        :param record:  dictionary
        :return: dict
    """
    log_info(f"-----------GET Single User METHOD Entered  ----------------\n")

    try:
        # Checks if mobile key is not in record or employee id key not in record
        if "mobile" not in record or "employee_id" not in record:
            log_warning(f'"error": "Missing "mobile" or "employee_id" key in record"')
            return {"error": "Missing 'mobile' or 'employee_id' key in record"}

        # Assigns dict record having key mobile (record["mobile"]) to mobile
        mobile = record["mobile"]
        # assigns dict record having key employee id (record["employee_id"]) to employee_id
        employee_id = record["employee_id"]
        log_debug(f"Mobile number extracted: {mobile}")
        log_debug(f"Employee ID extracted: {employee_id}")

        # Checks if it is not valid mobile number and is valid employee id then returns error
        if not (is_valid_mobile(mobile) and is_valid_employee_id(employee_id)):
            log_error(f"'error': 'Invalid mobile number {mobile} or employee ID {employee_id}'")
            return {"error": "Invalid mobile number or employee ID"}

        # taking user found  initial value  None
        user_found = None

        # looping user in dict DATA having records key (DATA['records'])
        for user in DATA['records']:

            # Checks if provided user name matches with name in our data and also checks mobile,employee id
            if user["name"] == name and user["mobile"] == mobile and user["employee_id"] == employee_id:
                user_found = user
                break

        # if user not found then returns error 
        if not user_found:
            log_warning(f"No user details found for mobile number {mobile} and employee ID {employee_id}")
            return {"error": f"User details not found for {name}"}

        # Checks is admin(username) , is normal user(username) functions and assigns name to username 
        if is_admin(username) or (is_normal_user(username) and username == name):
            log_info(f"User details found: {user_found}")
            try:
                send_email(["komalsaikiran05@gmail.com"], f"User {username} -- is viewing single user details {record}")
                log_debug("Email has been sent to the user")
            except Exception as error:
                log_error(f"Failed to send email: {error}")

            return user_found

        # Checks if conditions fails in previous steps, 
        # is normal user(username) and username is not equal to name then return error
        elif is_normal_user(username) and username != name:
            return {'error': 'Normal users only have permission to view their own records'}

        log_warning(f"Unauthorized access for {username}.")
        return {"error": "Unauthorized access"}

    except ValueError as error:
        log_error(f"Error in GET METHOD: {error}")
        return {"error": str(err)}
    finally:
        log_info("-----------------GET Single User METHOD Ended-----------------\n")


# # Admin user can view any user details but normal user can view only their details only.
single_user_details = get_single_user_details("Kumar Makala", "Kumar Makala",
                                              {"mobile": 914234234245, "employee_id": "EMP001"})
log_info(
    f" {single_user_details} has been viewed successfully using mobile number {mobiles}  \n")

logging.info(f"-----------------GET Single User METHOD Ended----------------- \n")


# GET ALL USER DETAILS
@authenticate_decorator
def get_all_user_details(name):
    """
        This method inserts new record.
        :param name: str
        :return: list of dict
    """
    log_info(f"-----------GET All User Details METHOD Entered  --------- \n")
    try:
        # Checks if not satisfies is admin(name) function and returns error if False 
        if not is_admin(name):
            log_warning("Invalid access to view all users information.")
            return {"error": "Not an Admin user so getting all records information failed"}

        log_info(f"User details found: {name}")
        log_debug(f"All User details are  -->> {DATA['records']}")

        try:
            send_email(["komalsaikiran05@gmail.com"], f"User {name} is viewing all user details")
            log_debug("Email has been sent to the users")
        except Exception as error:
            log_error(f"Failed to send email: {error}")

        # Returns list of dictionaries 
        return DATA['records']

    except ValueError as error:
        log_error(f"Error in GET METHOD: {error}")
        return {"error": str(err)}
    finally:
        log_info("-----------------GET All User Details METHOD Ended-----------------\n")


# Admin has privilege to view all user details but not normal users
all_users = get_all_user_details("Mahesh")
log_info(
    f" {all_users} has been displayed here \n")
log_info(f"-----------------GET All User Details METHOD Ended----------------- \n")


# DELETE METHOD
@authenticate_decorator
def delete_user_details(name, record):
    """
            This method inserts new record.
            :param name: str
            :param record: dictionary
            :return:  dict
    """
    log_info(f"-----------------Delete User Details METHOD Entered----------------- \n")
    try:
        # Retrieves employee id and mobile details from record
        employee_id = record.get("employee_id")
        mobile = record.get("mobile")

        # Checks if not employee id or not mobile if True then raise error
        if not employee_id or not mobile:
            log_error(f"Employee ID {employee_id} and mobile number {mobile} are required for deletion")
            raise ValueError("Employee ID and mobile number are required for deletion.")

        # Checks if not is valid mobile(mobile) function if True then return error
        if not is_valid_mobile(mobile):
            log_error(f"Invalid mobile number {mobile}")
            return {"error": "Invalid mobile number."}

        # Check if user is authorized to delete
        if admin_operations(name) and name in DATA['admins']:
            log_info(f"Delete user details function started for {name}")

            # Iterates and Find the user in DATA['records'] and delete if found
            for x, user in enumerate(DATA['records']):
                if user["mobile"] == mobile and user.get("employee_id") == employee_id:
                    deleted_user = DATA['records'].pop(x)

                    # Send email notification
                    send_email(["komalsaikiran05@gmail.com"], f"Admin '{name}' deleted record of {record}")
                    log_info(f"Email sent to users regarding deletion.")

                    log_info(f"User deleted successfully: {deleted_user}")
                    return deleted_user

            log_warning(f"No user details found for mobile number {mobile}. Deletion not possible.")
            return {"error": "User details not found."}

        else:
            log_error(f"Unauthorized access: {name} does not have permission to delete users.")
            return {"error": "Unauthorized access."}

    except ValueError as error:
        log_error(f"Error in delete_user_details: {error}")
        return {"error": str(err)}
    except Exception as error:
        log_error(f"Unexpected error in delete_user_details: {error}")
        return {"error": str(error)}
    finally:
        log_info("-----------------Delete User Details METHOD Ended----------------- \n")


# If only Admin user then only deletes the record
deleted_user_details = delete_user_details("Kumar Makala", {"mobile": 913020022100, "employee_id": "EMP003"})
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
        # Check if user is an admin and have admin privileges
        if admin_operations(name):
            # Admin can modify any user details
            employee_id = record.get("employee_id")
            log_debug(f"Employee ID extracted: {employee_id}")
            mobile = record.get("mobile")
            log_debug(f"Mobile number extracted: {mobile}")

            # Checks valid mobile or not and iterates user in raw DATA if True
            if is_valid_mobile(mobile):
                for user in raw_DATA['records']:
                    if user["mobile"] == mobile:
                        log_info(f"User found for updating -->> {user}")

                        # Update user details
                        user.update(record)
                        log_info(f"User details updated to -->> {user}")

                        send_email(["komalsaikiran05@gmail.com"], f"Admin '{name}' updated record of {record}")
                        log_debug(f"Email has been sent to the users ")

                        return user

                log_warning(f"No user details found for mobile number in PATCH METHOD {mobile}")
                return {"error": "User details not found"}

            else:
                log_error(f"Invalid details found for mobile number in PATCH METHOD {mobile}")
                raise ValueError("Invalid mobile number format")

        # Check if user is a normal user and can only update their own record
        elif normal_user_operations(name):
            # Normal user can only modify their own record
            employee_id = record.get("employee_id")
            log_debug(f"Employee ID extracted: {employee_id}")
            mobile = record.get("mobile")
            log_debug(f"Mobile number extracted: {mobile}")

            if is_valid_mobile(mobile):
                for user in raw_DATA['records']:
                    if user["mobile"] == mobile and user["employee_id"] == employee_id:
                        log_info(f"User found for updating -->> {user}")

                        # Update user details
                        user.update(record)
                        log_info(f"User details updated to -->> {user}")

                        send_email(["komalsaikiran05@gmail.com"], f"User '{name}' updated their own record {record}")
                        log_debug(f"Email has been sent to the users ")

                        return user

                log_warning(f"No user details found for mobile number in PATCH METHOD {mobile}")
                return {"error": "User details not found"}

            else:
                log_error(f"Invalid details found for mobile number in PATCH METHOD {mobile}")
                raise ValueError("Invalid mobile number format")

        else:
            return {"error": "Unauthorized access"}

    except ValueError as error:
        log_error(f"Error in PATCH METHOD: {error}")
        return {"error": str(err)}


#
record_to_update = {"mobile": 914111111111, "name": "vicky", "employee_id": "EMP009"}
updated_user = patch_user_details("komal", DATA, record_to_update)
log_info(
    f"User partial updation done successfully in PATCH METHOD: {updated_user}, updated record is -{record_to_update}")
log_info(f"-----------------Patch User Details METHOD Ended----------------- \n")


@authenticate_decorator
def reset_user_password(admin_name, user_to_reset, new_password):
    """
    This method resets the password for a user if the requester is an admin.
    :param admin_name: str
    :param user_to_reset: str
    :param new_password: str
    :return: dict
    """
    log_info(f"-----------Reset User Password METHOD Entered  --------- \n")
    try:
        # Checks if admin or not function if not then return error
        if not is_admin(admin_name):
            log_warning("Unauthorized access to reset user password.")
            return {"error": "Only admins are authorized to reset user passwords."}

        # Checks if user whose password is to be reset not in DATA if True returns error
        if user_to_reset not in DATA['users']:
            log_warning(f"User '{user_to_reset}' not found in the list of users.")
            return {"error": f"User '{user_to_reset}' not found."}

        # Sets password and sends email
        log_info(f"Resetting password for user '{user_to_reset}' to '{new_password}'.")
        send_email(["komalsaikiran05@gmail.com"],
                   f"Admin -'{admin_name}'- is resetting User {user_to_reset}'s password")
        log_debug(f"Email has been sent to the users ")
        log_info(f"Password reset successful for user '{user_to_reset}'.")

        return {"message": f"Password reset successful for user '{user_to_reset}'."}

    except Exception as error:
        log_error(f"Error resetting password: {error}")
        return {"error": f"Error resetting password: {error}"}
    finally:
        log_info("-----------------Reset User Password METHOD Ended-----------------\n")


# Only Admin can set Password
reset_result = reset_user_password("komal", "kmakala", "newpassword123")
log_info(f"Reset result: {reset_result}")
