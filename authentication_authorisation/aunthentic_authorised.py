from app_development.app.constants import ADMINS, DATA
from app_development.logging_activity.logging_utils import *


def authenticate_decorator(fun):
    """
    This is decorator func
    :param fun: function
    :return: bool
    """

    def wrapper(name, *args, **kwargs):
        log_info(f"Decorator Function Entered")
        try:

            log_info(f"Authenticate decorator: Entered for {name}")
            if authenticate_user(name):
                log_info(f"{name} authenticated successfully.")
                return fun(name, *args, **kwargs)
            else:
                log_error(f"Unauthorized access for {name}.")
                return {"error": "Unauthorized access"}
        except Exception as err:
            log_error(f"Exception in authentication decorator: {err}")
            return {"error": str(err)}

    return wrapper


def authenticate_user(name):
    """
    Checks who is the person
    :param name: str
    :return: bool
    """
    log_info(f"authenticate_user Function Entered")
    if name in DATA['users'] or name in DATA['admins']:
        log_debug(f"User {name} authenticated successfully - meaning basic info verified")
        return True
    log_info(f"authenticate function ended")
    return False


def is_normal_user(user_name):
    """
    Check if the user is a normal user.
    :param user_name: str
    :return: bool
    """
    if user_name in DATA['users']:
        log_debug(f"{user_name} found in DATA['users'] list")
        return True
    if user_name in [item["name"] for item in DATA["records"]]:
        log_debug(f"{user_name} found in DATA['records']")
        return True
    return False


def is_admin(user_name):
    """
        Check if the user is an admin.
        :param user_name: str
        :return: bool
        """
    if user_name in DATA['admins']:
        log_debug(f"{user_name} found in DATA['admins'] list")
        return True
    if user_name in [item["name"] for item in DATA["records"]]:
        log_debug(f"{user_name} found in DATA['records']")
        return True
    return False


@authenticate_decorator
def admin_operations(name):
    """
    This function is used for giving permission to only Admin user for create, delete
    :param name: str
    :return: bool
    """

    # Authorisation

    role = input(f"Options are n, a:")
    try:
        if role == 'n':
            log_debug(f"selected option is 'n' and user is {name} ")
            # log_error(f"Normal User {name}... so, doesn't have permission ")
            raise PermissionError(f"Normal User {name}..."
                                  f" so, doesn't have permission ")
        elif role == 'a':
            log_debug(f"selected option is 'a' and user is {name} ")
            if name in ADMINS:
                log_debug(f"Admin User {name}... so, has permission")
                return True
            else:
                return False
            # log_debug(f"Admin User {name}... so, have permission")
        else:
            log_error(f"Incorrect role {role} chosen - available options are 'n' and 'a' only")
            raise ValueError(f"Incorrect role chosen - available options are 'n' and 'a' only")
    except PermissionError as p_err:
        log_error(p_err)
        return False
    except ValueError as v_err:
        log_error(v_err)
        return False
    except Exception as err:
        log_error(err)
        return False


@authenticate_decorator
def normal_user_operations(name):
    """
        This function is used for giving permission to user for update, read
        :param name: str
        :return: bool
    """
    role = input(f"Options are n, a:")
    try:

        if role in ['n', 'a']:
            log_debug(f"check if user selected either n or a ")
            return f"  Cool.....Authorised user only..... "

        # if role == 'a':
        #     pass

        else:
            log_error(f"Incorrect role chosen - available options are 'n' and 'a' only")
            raise ValueError(f"Incorrect role chosen - available options are 'n' and 'a' only")

    except Exception as err:
        log_error(err)
        return {"error": str(err)}


@authenticate_decorator
def create_admin_normaluser_info(role, employee_id):
    """
    This function is used to create/add new admins as well as new normal users into ADMINS, USERS lists
    :param employee_id: str
    :param role: str
    :return: dict
    """
    try:
        log_info("create admin normal user info function entered\n")
        user = input("Enter username:")
        if not user:
            log_error("Username cannot be empty.")
            raise ValueError("Username cannot be empty.")

        # Mandatory
        firstname = input("Enter First name:")
        if not firstname:
            log_error("First name cannot be empty.")
            raise ValueError("First name cannot be empty.")

        middlename = input("Enter middle name:")  # Optional
        lastname = input("Enter last name:")  # Optional
        dept = input("Enter the department:")
        if not dept:
            log_error("Department cannot be empty.")
            raise ValueError("Department cannot be empty.")

        dob = input("Enter the DOB:")
        if not dob:
            log_error("DOB cannot be empty.")
            raise ValueError("DOB cannot be empty.")

        new_user = {
            "username": user,
            "name": f"{firstname} {middlename} {lastname}",
            "dept": dept,
            "dob": dob,
            "isadmin": (role == "a"),  # True if role is admin, False otherwise
            "employee_id": employee_id
        }

        if role == "n":
            DATA['users'].append(new_user)
        elif role == "a":
            DATA['admins'].append(new_user)
        else:
            log_error("Invalid role. Use 'n' for normal user or 'a' for admin.")
            raise ValueError("Invalid role. Use 'n' for normal user or 'a' for admin.")

        log_info(f"{user} created in create_admin_normaluser_info function")
        return new_user

    except ValueError as e:
        log_error(e)
        return {"error": str(e)}


'''
@authenticate_decorator
def create_user_conditions(name):
    # Authorisation
    if name in ADMINS:
        
        role = input(f"Options are n, a:")

        # if role == 'n':
        #     print(f'(" Normal USER Role ")')
        # elif role == 'a':
        #     print(f'(" ADMIN Role ")')
        # else:
        #     raise ValueError(f"Incorrect role chosen - available options are n and a only")
        #
        print(f"Admin User {name}... so, have permission to create new record")
    else:
        print(f"Normal User {name} does not have permission to create new record")
        raise PermissionError(f"Normal User {name} does not have permission to create new record")

#create_user_conditions("jdoe")
#print(f"Present users normal -{USERS} admins-{ADMINS}")
'''
