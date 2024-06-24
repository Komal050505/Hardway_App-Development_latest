from Http_Methods.utils.user_utils import *
from Http_Methods.app.constants import *
import logging

"""
This module contains the main code to be executed 
"""
# LOGGING MODULES
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='a', filename='main.log')


# POST METHOD
def new_record(record):
    """
        This method inserts new record.
        :param record: list of dictionary
        :return: dict
    """
    logging.debug(f"POST METHOD entered with record {record}")

    try:

        if (record["mobile"]) not in available_records:
            data["records"].append(record)
            response = {"message": "Successfully inserted into the record ", "record": record}
            logging.info(f"Record successfully inserted using POST METHOD: {record}")
            return response
        else:
            logging.warning(f"{record} Record already exists, please enter new record details using POST METHOD")
            return f"Duplicate Record Found "
    except ValueError as err:
        response = {"message": str(err), "status": "Failed"}
        logging.error(f"Error inserting record: {err} using POST METHOD")
        return response


# print(new_record([1,2,3]))


print(new_record({"mobile": 914111111111, "name": "Suresh", "company": "MIND TREE"}))
print(data)


# GET METHOD SINGLE USER DETAILS
def get_single_user_details(record):
    """
        This method gets single record.
        :param record: list of dictionary
        :return: dict
    """
    logging.debug(f"GET METHOD entered with record {record}")

    try:
        mobile = record["mobile"]
        if is_valid_mobile(record["mobile"]):
            for user in data['records']:
                if user["mobile"] == mobile:
                    logging.info(f"User details found -->> {user}")
                    # print(f"User details found -->> {user}")
                    return user
            logging.warning(f"No user details found for mobile number in GET METHOD {mobile}"
                            f" so GET METHOD will return nothing.")
            # print(f"No user details found for mobile number {mobile}.")
            return {"error": "User details not found "}
    except ValueError as err:
        logging.error(f"Error in GET METHOD: {err}")
        return {"error": str(err)}


single_user_details = get_single_user_details({"mobile": 915421215452})
print(f'single user details is --->> {single_user_details}')


# GET ALL USER DETAILS
def get_all_user_details(raw_data):
    """
        This method inserts new record.
        :param raw_data: dictionary
        :return: list of dict
    """
    logging.debug(f"GET METHOD entered")
    try:
        # Assuming 'data' is a dictionary containing a key 'records' which is a list of user records
        if 'records' in raw_data:

            logging.info(f"All User details are  -->> {raw_data['records']}")
            return raw_data['records']
        else:
            logging.warning(f"No user details found in GET METHOD.")
            return {"error": "No user details found "}
    except ValueError as err:
        logging.error(f"Error in GET METHOD: {err}")
        return {"error": str(err)}


all_users = get_all_user_details(data)
print(all_users)


# DELETE METHOD
def delete_user_details(record):
    """
            This method inserts new record.
            :param record: list of dictionaries
            :return:  dict
    """
    try:
        mobile = record["mobile"]
        if is_valid_mobile(record["mobile"]):
            for x, user in enumerate(data['records']):
                if user["mobile"] == mobile:
                    logging.info(f"User details found -->> {user}")
                    # print(f"User details found -->> {user}")
                    delete_user = data['records'].pop(x)
                    logging.info(f"User deleted successfully in DELETE METHOD: {delete_user}")
                    return delete_user

            logging.warning(f"No user details found for mobile number {mobile} so DELETION is not possible.")
            # print(f"No user details found for mobile number {mobile}.")
            return {"error": "User details not found "}
    except ValueError as err:
        logging.error(f"Error: {err}")
        return {"error": str(err)}


print(delete_user_details({"mobile": 915421215451}))
print(f"Users are -->> {data}")


def patch_user_details(raw_data, record):
    """
            This method inserts new record.
            :param record: list of dicts
            :param raw_data: dictionary
            :return:  dict
    """
    logging.debug(f"PATCH METHOD entered with record {record}")

    try:

        mobile = record["mobile"]

        if is_valid_mobile(mobile):
            for user in raw_data['records']:
                if user["mobile"] == mobile:
                    logging.info(f"User found for updating -->> {user}")

                    # Update user details
                    user.update(record)
                    logging.info(f"User details updated to -->> {user}")
                    return user

            logging.warning(f"No user details found for mobile number in PATCH METHOD {mobile}")
            return {"error": "User details not found"}

        else:
            raise ValueError("Invalid mobile number format")

    except ValueError as err:
        logging.error(f"Error in PATCH METHOD: {err}")
        return {"error": str(err)}


record_to_update = {"mobile": 914111111111, "name": "Johnathan Doe"}
updated_user = patch_user_details(data, record_to_update)
print(updated_user)
