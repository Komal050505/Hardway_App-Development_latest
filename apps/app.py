from profile_management.utils.user_utils import *
from profile_management.apps.constants import *
from profile_management.email_setup.email_operations import send_email, new_record_email_content
from profile_management.authentication_authorisation.aunthentic_authorised import *
from profile_management.logging_activity.logging_utils import log_info, log_warning, log_error, log_debug
from flask import jsonify
"""
This module contains the main code to be executed 
"""


# POST METHOD
@authenticate_decorator
def new_record(admin_name, record):
    """
        This method inserts new record.
        :param admin_name: str
        :param record:  dictionary
        :return: dict
    """
    log_info(f"--------------New Record function Entered  -----------------\n")

    try:
        if admin_name not in DATA['users'] and admin_name not in DATA['admins']:
            log_warning(f"External user '{admin_name}' ")
            email_subject = f"Red Alert: External User '{admin_name}' attempted to Insert New Users Record"
            email_body = f"External user '{admin_name}' attempted attempted to Insert New Users {record} Record ."
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for external user '{admin_name}' attempt")
            return jsonify({"error": f"External user '{admin_name}' "
                                     f"is not authorized to Insert New Users {record} Record"}), 403
        # validates admin_operations(name) function (authentic_authorised.py)
        if admin_operations(admin_name):

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
            email_subject, email_body = new_record_email_content(admin_name, record)
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email has been sent to the users ")

            log_debug(f"Record inserted successfully. New record added to AVAILABLE_RECORDS: {AVAILABLE_RECORDS}")

            log_info(f"Record successfully inserted using POST METHOD: {record}")
            return jsonify({"message": "Successfully inserted into the record", "record": record}), 200
        else:
            log_error(f"Unauthorized access: {admin_name} does not have permission to create new records.")
            email_subject = f"Unauthorized Access Attempt by '{admin_name}'"
            email_body = f"User '{admin_name}' attempted to add a new record but lacks the necessary permissions."
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            return jsonify({"error": "No user details found"}), 403
    except KeyError as error:
        error_message = f"KeyError: {error}. Please check the structure of the record."
        log_error(error_message)
        email_subject = f"Error Inserting Record by '{admin_name}'"
        email_body = f"KeyError occurred while '{admin_name}' was inserting a record: {error_message}"
        send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
        return jsonify({"message": error_message, "status": "Failed"}), 400

    except ValueError as error:
        error_message = str(error)
        log_error(f"Error inserting record: {error_message} using POST METHOD")
        email_subject = f"Error Inserting Record by '{admin_name}'"
        email_body = f"ValueError occurred while '{admin_name}' was inserting a record: {error_message}"
        send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
        return jsonify({"message": error_message, "status": "Failed"}), 400
    except Exception as error:
        error_message = f"Unexpected error: {str(error)}"
        log_error(f"Error inserting record: {error_message} using POST METHOD")
        email_subject = f"Unexpected Error Inserting Record by '{admin_name}'"
        email_body = f"An unexpected error occurred while '{admin_name}' was inserting a record: {error_message}"
        send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
        return jsonify({"message": error_message, "status": "Failed"}), 500


log_info(f"----------------------New Record function Ended---------------------------\n")


# GET METHOD SINGLE USER DETAILS

@authenticate_decorator
def get_single_user_details(username, record):
    log_info("-----------GET Single User METHOD Entered----------------\n")

    try:
        if username not in DATA['users'] and username not in DATA['admins']:
            log_warning(f"External user '{username}' attempted to access user details")
            email_subject = f"Unauthorized Access Attempt by External User '{username}'"
            email_body = f"Red Alert: External User '{username}' Attempted to Access single User info"
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for external user '{username}' attempt")
            return jsonify({"error": f"User '{username}' is not authorized to access these details"}), 403

        if "mobile" not in record or "employee_id" not in record or "name" not in record:
            log_warning(f'Missing "mobile", "employee_id", or "name" keys in record')
            email_subject = f"Missing Keys in Record Access Attempt by '{username}'"
            email_body = f"User '{username}' attempted to access details with missing keys in record."
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for missing keys in record by '{username}'")
            return jsonify({"error": "Missing 'mobile', 'employee_id', or 'name' keys in record"}), 403

        name = record["name"].lower()
        mobile = str(record["mobile"])  # Ensure mobile number is converted to string
        employee_id = record["employee_id"]

        log_debug(f"Name extracted: {name}")
        log_debug(f"Mobile number extracted: {mobile}")
        log_debug(f"Employee ID extracted: {employee_id}")

        if not is_valid_mobile(mobile):
            log_error(f"Invalid mobile number {mobile} or employee ID {employee_id}")
            email_subject = f"Invalid Credentials by '{username}'"
            email_body = f"User '{username}' attempted to access details with invalid mobile number or employee ID."
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for invalid credentials by '{username}'")
            return jsonify({"error": "Invalid mobile number or employee ID"}), 400

        user_found = None

        log_debug(f"Admin Check: Is '{username}' an admin? {'Yes' if username in DATA['admins'] else 'No'}")

        if username in DATA['admins']:
            log_debug(f"'{username}' is an admin. Looking up user details for any user.")
            for user in DATA['records']:
                log_debug(f"Checking user record: {user}")
                if (user["name"].lower() == name and str(user["mobile"]) == mobile and
                        user["employee_id"] == employee_id):
                    user_found = user
                    break
        else:
            log_debug(f"'{username}' is not an admin. Checking user record for '{username}' only.")
            if username.lower() == name:
                for user in DATA['records']:
                    log_debug(f"Checking user record: {user}")
                    if (user["name"].lower() == name and str(user["mobile"]) == mobile and
                            user["employee_id"] == employee_id):
                        user_found = user
                        break

        if not user_found:
            log_warning(f"No user details found for name {name}, mobile number {mobile}, and employee ID {employee_id}")
            email_subject = f"User {username} is checking Other Users info"
            email_body = f"User {username} is trying to check other users' information"
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for user details not found for '{username}'")
            return jsonify({"error": f"User details not found for {username}"}), 404

        if username in DATA['admins']:
            log_info(f"Admin '{username}' accessed details for '{name}': {user_found}")
            email_subject = f"Admin Access: User '{username}' accessed details for '{name}'"
            email_body = f"Admin '{username}' has accessed details:\n{user_found}"
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for admin access by '{username}'")
            return jsonify(user_found), 200

        elif username.lower() == name:
            log_info(f"User '{username}' accessed their own details: {user_found}")
            email_subject = f"Access: User '{username}' accessed their own details"
            email_body = f"User '{username}' has accessed their details:\n{user_found}"
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for user accessing their own details '{username}'")
            return jsonify(user_found), 200

        else:
            log_warning(
                f"Unauthorized access attempt by '{username}' for '{name}',"
                f" mobile: {mobile}, employee ID: {employee_id}")
            email_subject = f"Unauthorized Access Attempt by '{username}'"
            email_body = f"User '{username}' attempted to check others' record but lacks the necessary permissions."
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for unauthorized access attempt by '{username}'")
            return jsonify({'error': 'Normal users only have permission to view their own records'}), 403

    except ValueError as error:
        log_error(f"Error in GET SINGLE USER DETAILS METHOD: {error}")
        email_subject = f"Error Checking Record by '{username}'"
        email_body = f"ValueError occurred while '{username}' was checking for details of single user"
        send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
        log_debug(f"Email sent for error during record checking by '{username}'")
        return jsonify({"error": str(error)}), 400

    finally:
        log_info("-----------------GET Single User METHOD Ended-----------------\n")


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
        if name not in DATA['users'] and name not in DATA['admins']:
            log_warning(f"External user '{name}' attempted to access all user details")
            email_subject = f"Red Alert: External User '{name}' Attempted to Access User Data"
            email_body = f"External user '{name}' attempted to access all user details."
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for external user '{name}' attempt")
            return jsonify({"error": f"External user '{name}' is not authorized to access these details"}), 403

        # Checks if not satisfies is admin(name) function and returns error if False 
        if not is_admin(name):
            log_warning("Not an Admin so Invalid access to view all users information.")
            email_subject = f"Not an Admin : User '{name}' is trying to get all users info"
            email_body = f"User '{name}' has no access to view all users details"
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for user accessing their own details '{name}'")
            return jsonify({"error": "Not an Admin user so getting all records information failed"}), 403

        log_info(f"User details found: {name}")
        log_debug(f"All User details are  -->> {DATA['records']}")

        try:
            email_subject = f"Admin Access: User '{name}' accessed details for '{name}'"
            email_body = f"Admin '{name}' has accessed details:\n{DATA['records']}"
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for admin access by '{name}'")
        except Exception as error:
            log_error(f"Failed to send email: {error}")
            email_subject = f"Error Checking Record by '{name}'"
            email_body = (f"Exception Error occurred while '{name}' "
                          f"was checking for details of all users '{DATA['records']}'")
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for error during record checking by '{name}'")

        # Returns list of dictionaries 
        return jsonify(['records']), 200

    except ValueError as error:
        log_error(f"Error in GET METHOD: {error}")
        email_subject = f"Error Checking Record by '{name}'"
        email_body = f"ValueError occurred while '{name}' was checking for details of all users '{DATA['records']}'"
        send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
        log_debug(f"Email sent for error during record checking by '{name}'")
        return jsonify({"error": str(error)}), 400
    finally:
        log_info("-----------------GET All User Details METHOD Ended-----------------\n")


log_info(f"-----------------GET All User Details METHOD Ended----------------- \n")


@authenticate_decorator
def patch_user_details(name, raw_DATA, record):
    """
            This method inserts new record.
            :param raw_DATA: dict
            :param name: str
            :param record: list of dicts
            :return:  dict
    """
    log_info(f"----------------PATCH METHOD Entered---------------- \n")

    try:
        # Extract details from the record
        employee_id = record.get("employee_id")
        mobile = record.get("mobile")

        log_info(f"Record to update: {record}")

        # Validate mobile number format
        if not is_valid_mobile(mobile):
            raise ValueError(f"Invalid mobile number format: {mobile}")

        user_found = False
        if is_admin(name):
            # Admin can modify any user details
            for user in raw_DATA['records']:
                log_info(f"Checking user: {user}")
                log_debug(
                    f"Comparing mobile: {user['mobile']} (type: {type(user['mobile'])}) "
                    f"with {mobile} (type: {type(mobile)})")
                log_debug(
                    f"Comparing employee_id: {user['employee_id']} (type: {type(user['employee_id'])})"
                    f"with {employee_id} (type: {type(employee_id)})")
                if str(user["mobile"]) == str(mobile) and str(user["employee_id"]) == str(employee_id):
                    # Update user details, except mobile and employee_id (K for keys and V for values in dict)
                    user.update({k: v for k, v in record.items() if k not in ["mobile", "employee_id"]})
                    log_info(f"User details updated for '{user['name']}': {user}")
                    email_subject = f"Admin '{name}' updated details for '{user['name']}'"
                    email_body = f"Admin '{name}' has updated user details:\n{user}"
                    send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
                    user_found = True
                    break
        else:
            # Normal user can only modify their own record
            for user in raw_DATA['records']:
                log_info(f"Checking user: {user}")
                log_debug(
                    f"Comparing mobile: {user['mobile']} (type: {type(user['mobile'])}) "
                    f"with {mobile} (type: {type(mobile)})")
                log_debug(
                    f"Comparing employee_id: {user['employee_id']} (type: {type(user['employee_id'])}) "
                    f"with {employee_id} (type: {type(employee_id)})")
                if (str(user["mobile"]) == str(mobile) and str(user["employee_id"]) == str(employee_id) and
                        user["name"] == name):
                    # Update user details, except mobile and employee_id (K for keys and V for values in dict)
                    user.update({k: v for k, v in record.items() if k not in ["mobile", "employee_id"]})
                    log_info(f"User '{name}' updated his own record: {user}")
                    email_subject = f"User '{name}' updated his own record"
                    email_body = f"User '{name}' has updated his own record:\n{user}"
                    send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
                    user_found = True
                    break

        if not user_found:
            log_warning(f"No user details found for mobile number: {mobile} and employee ID: {employee_id}")
            return jsonify({"error": "User details not found"}), 403

        return jsonify({"success": "User details updated successfully"}), 200

    except ValueError as error:
        log_error(f"Error in PATCH METHOD for '{name}': {error}")
        return jsonify({"error": str(error)}), 400

    except Exception as error:
        log_error(f"Unexpected error in PATCH METHOD for '{name}': {error}")
        return jsonify({"error": str(error)}), 500

    finally:
        log_info("-----------------PATCH METHOD Ended----------------\n")


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
        if name not in DATA['users'] and name not in DATA['admins']:
            log_warning(f"External user '{name}' attempted to delete user details")
            email_subject = f"Red Alert: External User '{name}' Attempted to Delete User Data"
            email_body = f"External user '{name}' attempted to delete user details."
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for external user '{name}' attempt")
            return jsonify({"error": f"External user '{name}' is not authorized to delete these details"}), 403

        employee_id = record.get("employee_id")
        mobile = record.get("mobile")

        if not employee_id or not mobile:
            log_error(f"Employee ID {employee_id} and mobile number {mobile} are required for deletion")
            email_subject = (f"Not matching employee id and/or mobile number: Employee_id: '{employee_id}'"
                             f" Mobile: {mobile}")
            email_body = (f"Please check and provide employee id and/or mobile number: Employee_id: '{employee_id}' "
                          f"Mobile: {mobile}.")
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for employee id, mobile mismatched '{name}' attempt")
            raise ValueError("Employee ID and mobile number are required for deletion.")

        if not is_valid_mobile(mobile):
            log_error(f"Invalid mobile number {mobile}")
            email_subject = (f"Mobile number mismatched for Employee_id: '{employee_id}'"
                             f" Mobile: {mobile}")
            email_body = (f"Please check and provide valid mobile number for Employee_id: '{employee_id}' "
                          f"Mobile: {mobile}.")
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for mobile mismatched '{name}' attempt")
            return jsonify({"error": "Invalid mobile number."}), 400

        if admin_operations(name) and name in DATA['admins']:
            log_info(f"Delete user details function started for {name}")

            for x, user in enumerate(DATA['records']):
                log_debug(f"Comparing record: {user}")
                log_debug(
                    f"Comparing mobile: {user['mobile']} (type: {type(user['mobile'])})"
                    f" with {mobile} (type: {type(mobile)})")
                log_debug(
                    f"Comparing employee_id: {user['employee_id']} (type: {type(user['employee_id'])}) "
                    f"with {employee_id} (type: {type(employee_id)})")
                if str(user["mobile"]) == str(mobile) and str(user["employee_id"]) == str(employee_id):
                    email_subject = f"Admin '{name}' Delete Access details for '{user}'"
                    email_body = f"Admin '{name}' has Deleted user details:\n{user}"
                    send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
                    log_debug(f"Email sent for admin delete access by '{name}'")

                    deleted_user = DATA['records'].pop(x)

                    log_info(f"User deleted successfully: {deleted_user}")
                    return jsonify(deleted_user), 200

            log_warning(f"No user details found for mobile number {mobile} and employee id {employee_id} "
                        f"so Deletion not possible.")
            return jsonify({"error": "User details not found."}), 404

        else:
            log_error(f"Unauthorized access: {name} does not have permission to delete users.")
            email_subject = f"Normal User: Normal User '{name}' Attempted to Delete User Details"
            email_body = f"Normal User '{name}' attempted to delete user details."
            send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
            log_debug(f"Email sent for Normal user '{name}' attempt")
            return jsonify({"error": "Unauthorized access."}), 403

    except ValueError as error:
        log_error(f"Error in delete_user_details: {error}")
        email_subject = f"Value Error: while '{name}' Attempted to Delete User Data"
        email_body = f"Value Error occurred for user '{name}' attempted to delete user details."
        send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
        log_debug(f"Email sent for Value Error for user '{name}' attempt")
        return jsonify({"error": str(error)}), 400
    except Exception as error:
        log_error(f"Unexpected error in delete_user_details: {error}")
        email_subject = f"Exception Error: while '{name}' Attempted to Delete User Details"
        email_body = f"Exception occurred for user '{name}' attempted to delete user details."
        send_email(["komalsaikiran05@gmail.com"], email_subject, email_body)
        log_debug(f"Email sent for exceptional error for user '{name}' attempt")
        return jsonify({"error": str(error)}), 500
    finally:
        log_info("-----------------Delete User Details METHOD Ended----------------- \n")


log_info(f"-----------------Delete User Details METHOD Ended----------------- \n")


@authenticate_decorator
def reset_user_password(admin_name, user_mobile, user_employee_id, new_password):
    log_info("-----------Reset User Password METHOD Entered ---------")

    try:
        # Check if admin is authorized
        if not is_admin(admin_name):
            log_warning(f"Unauthorized attempt to reset password by '{admin_name}'")
            send_email(["komalsaikiran05@gmail.com"], f"Unauthorized Attempt to Reset Password by '{admin_name}'",
                       f"{admin_name} attempted to reset a user's password without authorization.")
            return jsonify({"error": f"Unauthorized access by '{admin_name}'. Only admins can reset passwords."}), 403

        logging.debug(f"User mobile: {user_mobile}, Employee ID: {user_employee_id}")
        # Find user in DATA['records']
        user_found = None
        for record in DATA['records']:
            if str(record['mobile']) == str(user_mobile) and record['employee_id'] == user_employee_id:
                user_found = record
                break

        if not user_found:
            log_warning(f"User with mobile '{user_mobile}' and employee ID '{user_employee_id}' not found.")
            send_email(["komalsaikiran05@gmail.com"], "User Not Found for Password Reset",
                       f"User with mobile '{user_mobile}' and employee ID '{user_employee_id}' not found.")
            return jsonify({"error": f"User with mobile '{user_mobile}' and "
                                     f"employee ID '{user_employee_id}' not found."}), 400

        # Reset password
        user_found['password'] = new_password
        log_info(
            f"Password reset successful for user with mobile '{user_mobile}' and employee ID '{user_employee_id}'.")
        send_email(["komalsaikiran05@gmail.com"], "Password Reset Successful",
                   f"Admin '{admin_name}' has reset the password for user with mobile '{user_mobile}' "
                   f"and employee ID '{user_employee_id}'.")
        return jsonify({
            "message": f"Password reset successful for user with mobile '{user_mobile}' "
                       f"and employee ID '{user_employee_id}'."}), 200

    except Exception as e:
        log_error(f"Error resetting password: {e}")
        send_email(["komalsaikiran05@gmail.com"], "Error in Reset User Password Method",
                   f"Error occurred while resetting password by '{admin_name}': {e}")
        return jsonify({"error": f"Error resetting password: {e}"}), 500

    finally:
        log_info("Reset User Password METHOD Ended")


def menu():
    while True:
        print("Select an option between (1-7):")
        print("1. New Record")
        print("2. Get Single User Details")
        print("3. Get All User Details")
        print("4. Patch User Details")
        print("5. Delete User Details")
        print("6. Reset User Password")
        print("7. Exit")

        log_info(f"Show menu Entered")
        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            log_debug(f"Selected option is {choice}")
            name = input("Enter only Admin's name: ")
            try:
                # Input validation for Admin  name
                if not is_valid_name(name):
                    log_info(f"Invalid name {name} Entered... Please Enter name in alphabetic's only")
                    print(f"Invalid name Entered... Please Enter name in alphabetic's only")
                    continue

                if not is_admin(name):
                    log_info(f"Not an Admin name {name}... Please Enter Admin name  only")
                    print(f"Please Enter Admin name only")
                    continue

                # Input validation for new users name
                new_user_name = input("Enter the name of the new user : ")
                if not is_valid_name(new_user_name):
                    log_info(f"Invalid name {new_user_name} Entered... Please Enter name in alphabetic's only")
                    print(f"Invalid name entered... Please enter alphabetic characters only")
                    continue

                # Input validation for new users mobile number
                new_user_mobile = input("Enter the mobile number of the new user : ")
                if not (is_valid_mobile(new_user_mobile) and is_mobile_length_valid(new_user_mobile) and
                        is_valid_type(new_user_mobile)):
                    log_info(f"Invalid mobile number {new_user_mobile} entered...")
                    print(f"Invalid mobile number entered...")
                    continue

                # Input validation for new users employee ID
                new_user_employee_id = input("Enter the new user's employee ID : ")
                if not is_valid_employee_id(new_user_employee_id):
                    log_info(f"Invalid employee ID {new_user_employee_id} entered...")
                    print(f"Invalid employee ID entered...")
                    continue
                # Input  for user new users company
                new_user_company = input("Enter new user's company name: ")
                log_info(f"new users company {new_user_company} entered...")

                # Input  for new users isadmin status
                new_user_isadmin = input("Enter the user's isadmin : ")
                log_info(f"new user isadmin block {new_user_isadmin} entered...")

                # Input  for new users Password
                new_user_password = input("Enter the user's password: ")
                log_info(f"new user password block {new_user_password} entered...")

                record = {
                    "name": new_user_name,
                    "mobile": new_user_mobile,
                    "employee_id": new_user_employee_id,
                    "company": new_user_company,
                    "password": new_user_password,
                    "isadmin": new_user_isadmin
                }
                result = new_record(name, record)
                log_info(f"show menu result is {result} ")
                print(result)
                log_info(f"show menu for choice {choice} ended")
                break
            except Exception as error:
                log_error(f"Exception error {error} occured in show menu please check")
                print(f"{error}")
                return error
        elif choice == '2':
            # Input validation for admin or normal users name
            name = input("Enter Admin/User name : ")
            try:
                if not is_valid_name(name):
                    log_info(f"Invalid name {name} entered... Please enter alphabetic characters only")
                    print(f"Invalid name entered... Please enter alphabetic characters only")
                    continue

                if not (is_admin(name) or is_normal_user(name)):
                    log_info(f"{name} entered is neither an admin name nor an user name...")
                    continue

                # Input validation for user_name to retrieve
                user_name = input("Enter the name of the user to retrieve: ")
                if not is_valid_name(user_name):
                    log_info(f"Invalid name {user_name} entered... Please enter alphabetic characters only")
                    print(f"Invalid name entered... Please enter alphabetic characters only")
                    continue

                if not is_normal_user(user_name):
                    log_info(f"{user_name} entered is not a valid normal user name...")
                    continue

                # Input Validation for user mobile
                user_mobile = input("Enter the mobile number of the user to retrieve: ")
                user_found = None

                # Input validation for user employee ID
                user_employee_id = input("Enter the user's employee ID to retrieve: ")

                # Check if the entered mobile number and employee ID match any user's details
                for user_record in DATA["records"]:
                    if user_name.lower() == user_record["name"].lower() and str(user_mobile) == str(
                            user_record["mobile"]) and user_employee_id == user_record["employee_id"]:
                        user_found = user_record
                        break

                if not user_found:
                    log_info(
                        f"No user found with name '{user_name}', mobile number '{user_mobile}',"
                        f" and employee ID '{user_employee_id}'")
                    print(
                        f"No user found with name '{user_name}', mobile number '{user_mobile}',"
                        f" and employee ID '{user_employee_id}'")
                    continue
                # Construct the record dictionary with validated inputs
                record = {
                    "name": user_name,
                    "mobile": user_mobile,
                    "employee_id": user_employee_id
                }

                # Call the function to get single user details
                result = get_single_user_details(name, record)
                log_info(f"Successfully retrieved result: {result}")
                print(result)

            except Exception as error:
                log_error(f"Exception error occurred in show menu: {error}")
                print(error)
                return error

        elif choice == '3':
            # Input validation for Admin  name
            name = input("Enter Admin name only : ")

            if not is_valid_name(name):
                log_info(f"Invalid name {name} Entered... Please Enter name in alphabetic's only")
                print(f"Invalid name Entered... Please Enter name in alphabetic's only")
                continue

            if not is_admin(name):
                log_info(f"Not an Admin name {name}... Please Enter Admin name  only")
                print(f"Please Enter Admin name only")
                continue
            result = get_all_user_details(name)
            log_info(f"Successfully retrieved result: {result}")
            print(result)

        elif choice == '4':
            try:

                # Input Validation for Admin Name
                name = input("Enter Admin name only: ")

                if not is_valid_name(name):
                    log_info(f"Invalid name {name} Entered... Please Enter name in alphabetic's only")
                    print(f"Invalid name Entered... Please Enter name in alphabetic's only")

                    return

                if not is_admin(name):
                    log_info(f"Not an Admin name {name}... Please Enter Admin name only")
                    print(f"Please Enter Admin name only")

                    return

                # Input validation for Users Mobile
                user_mobile = input("Enter the mobile of the user to patch: ")

                if not (is_valid_mobile(user_mobile) and is_mobile_length_valid(user_mobile) and is_valid_type(
                        user_mobile)):
                    log_info(f"Invalid mobile number {user_mobile} entered...")
                    print(f"Invalid mobile number entered...")

                    return

                # Input validation for user employee ID
                user_employee_id = input("Enter the user's employee ID to patch: ")

                if not is_valid_employee_id(user_employee_id):
                    log_info(f"Invalid employee ID {user_employee_id} entered...")
                    print(f"Invalid employee ID entered...")

                    return

                # Optional: Input validation for Users Name
                user_name = input("Enter the name of the user to patch: ")

                if not is_valid_name(user_name):
                    log_info(f"Invalid name {user_name} entered... Please enter alphabetic characters only")
                    print(f"Invalid name entered... Please enter alphabetic characters only")

                    return

                # Optional: Input validation for user company
                user_company = input("Enter the company of the user to patch: ")
                log_info(f"{user_company} is the user's company name")

                # Optional: Input validation for user password
                user_password = input("Enter the new password: ")
                log_info(f"{user_password} is the user's password")

                # Optional: Input validation for user isadmin status
                user_isadmin = input("Enter the user's isadmin status: ")
                log_info(f"User isadmin status: {user_isadmin}")

                # Prepare the record dictionary to update
                record_to_update = {
                    "name": user_name,
                    "mobile": user_mobile,
                    "employee_id": user_employee_id,
                    "company": user_company,  # Optional
                    "password": user_password,  # Optional
                    "isadmin": user_isadmin,  # Optional

                }

                # Call the function to patch user details
                result = patch_user_details(name, DATA, record_to_update)
                log_info(f"Result from patch_user_details: {result}")
                print(result)

            except Exception as e:
                log_error(f"Exception occurred in menu option '4': {e}")
                print(f"Exception occurred: {e}. Please try again or contact support.")

        elif choice == '5':
            name = input("Enter Admin name only : ")
            if not is_valid_name(name):
                log_info(f"Invalid name {name} Entered... Please Enter name in alphabetic's only")
                print(f"Invalid name Entered... Please Enter name in alphabetic's only")
                continue

            if not is_admin(name):
                log_info(f"Not an Admin name {name}... Please Enter Admin name  only")
                print(f"Please Enter Admin name only")
                continue

            # Input Validation for Users Mobile
            user_mobile = input("Enter the mobile of the user to delete: ")
            if not (is_valid_mobile(user_mobile) and is_mobile_length_valid(user_mobile) and is_valid_type(
                    user_mobile)):
                log_info(f"Invalid mobile number {user_mobile} entered...")
                print(f"Invalid mobile number entered...")
                continue
            user_employee_id = input("Enter the employee id of the user to delete: ")
            if not is_valid_employee_id(user_employee_id):
                log_info(f"Invalid employee id  {user_employee_id} entered...")
                continue

            record = {
                "mobile": user_mobile,
                "employee_id": user_employee_id
            }
            result = delete_user_details(name, record)
            log_info(f"{result} User is Deleted")
            print(result)

        elif choice == '6':
            try:
                log_debug(f"Selected option is {choice}")
                admin_name = input("Enter Admin name only : ")

                if not is_valid_name(admin_name):
                    log_info(f"Invalid name {admin_name} Entered... Please Enter name in alphabetic's only")
                    print(f"Invalid name Entered... Please Enter name in alphabetic's only")
                    continue

                if not is_admin(admin_name):
                    log_info(f"Not an Admin name {admin_name}... Please Enter Admin name only")
                    print(f"Please Enter Admin name only")
                    continue

                user_mobile = input("Enter the mobile number of the user to reset password: ")

                if not is_valid_mobile(user_mobile):
                    log_info(f"Invalid mobile number {user_mobile} entered...")
                    print(f"Invalid mobile number entered...")
                    continue

                user_employee_id = input("Enter the employee ID of the user to reset password: ")

                if not is_valid_employee_id(user_employee_id):
                    log_info(f"Invalid employee ID {user_employee_id} entered...")
                    print(f"Invalid employee ID entered...")
                    continue

                new_password = input("Enter the new password: ")
                log_info(f"new user password block {new_password} entered...")

                result = reset_user_password(admin_name, user_mobile, user_employee_id, new_password)
                print(result)
            except Exception as error:
                log_error(f"Exception occurred during password reset: {error}")
                print(f"Error occurred: {error}")


if __name__ == "__main__":
    menu()

# all functions calls happens here

# Only Admin users should create new record so name should be in admin list.
inserted_record = new_record("komal", {"mobile": 935620002028, "name": "Julie",
                                       "company": "Platinum", "employee_id": "EMP009",
                                       "password": "julie@123", "isadmin": False})
log_info(
    f" {inserted_record} has been inserted using mobile number \n")

# # Admin user can view any user details but normal user can view only their details only.
single_user_details = get_single_user_details("komal",
                                              {"name": "kmakala",
                                               "mobile": 914234234245,
                                               "employee_id": "EMP001",
                                               "isadmin": False})
print(single_user_details)
log_info(
    f" {single_user_details} has been viewed successfully  \n")

# Admin has privilege to view all user details but not normal users
all_users = get_all_user_details("komaljg")
log_info(
    f" {all_users} has been displayed here \n")

record_to_update = {"mobile": 914111111111, "name": "vicky", "employee_id": "EMP005"}
updated_user = patch_user_details("komak", DATA, record_to_update)
log_info(
    f"User partial updation done successfully in PATCH METHOD: {updated_user}, updated record is -{record_to_update}")

# If only Admin user then only deletes the record
deleted_user_details = delete_user_details("komal", {"mobile": 913020022100, "employee_id": "EMP003"})
log_info(f"User deleted successfully in DELETE METHOD: {deleted_user_details}")

# Only Admin can set Password
reset_result = reset_user_password("komal", "kmakala", "newpassword123")
log_info(f"Reset result: {reset_result}")
