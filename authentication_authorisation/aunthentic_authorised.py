from app_development.app.constants import USERS, ADMINS
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
    if name in USERS or name in ADMINS:
        log_debug(f"User {name} authenticated successfully - meaning basic info verified")
        return True
    log_info(f"authenticate function ended")
    return False


@authenticate_decorator
def for_create_delete_user_conditions(name):
    """
    This function is used for giving permission to only Admin user for create, delete
    :param name: str
    :return: bool
    """

    # Authorisation

    role = input(f"Options are n, a:")

    if role == 'n':
        log_error(f"Normal User {name}... so, doesn't have permission to create new record or to delete record")
        raise PermissionError(f"Normal User {name}..."
                              f" so, doesn't have permission to create new record or to delete record")
    elif role == 'a':
        log_debug(f"Admin User {name}... so, have permission to "
                  f"create new record or to delete record")
        return True
    else:
        log_error(f"Incorrect role chosen - available options are 'n' and 'a' only")
        raise ValueError(f"Incorrect role chosen - available options are 'n' and 'a' only")


@authenticate_decorator
def for_update_read_user_conditions(name):
    """
        This function is used for giving permission to user for update, read
        :param name: str
        :return: bool
    """
    role = input(f"Options are n, a:")

    if role in ['n', 'a']:
        log_debug(f"check if user selected either n or a ")
        return f"  Cool.....Authorised user only..... "
    else:
        log_error(f"Incorrect role chosen - available options are 'n' and 'a' only")
        raise ValueError(f"Incorrect role chosen - available options are 'n' and 'a' only")


@authenticate_decorator
def create_admin_normaluser_info(role, employee_id):
    """
    This function is used to create/add new admins as well as new normal users into ADMINS , USERS lists
    :param employee_id: str
    :param role: str
    :return: dict
    """
    try:
        log_info(f"create admin normal user info function entered\n")
        user = input(f"Enter username:")
        if not user:
            log_error(f"Username cannot be empty.")
            raise ValueError("Username cannot be empty.")
        # Mandatory
        firstname = input(f"Enter First name:")
        if not firstname:
            log_error(f"First name cannot be empty.")
            raise ValueError("First name cannot be empty.")
        middlename = input(f"Enter middle name:")  # Optional
        lastname = input(f"Enter last name:")  # Optional
        dept = input("Enter the department: ")
        if not dept:
            log_error(f"Department cannot be empty.")
            raise ValueError("Department cannot be empty.")
        dob = input(f"Enter the DOB:")
        if not dob:
            log_error(f"DOB cannot be empty.")
            raise ValueError("DOB cannot be empty.")

        if role == "n":
            admin = False
            USERS.append(user)
        elif role == "a":
            admin = True
            ADMINS.append(user)
        else:
            log_error(f"Invalid role. Use 'n' for normal user or 'a' for admin.")
            raise ValueError("Invalid role. Use 'n' for normal user or 'a' for admin.")
        log_info(f"{user} created in create_admin_normaluser_info function")
        return {"username": user, "name": firstname + middlename + lastname, "dept": dept,
                "dob": dob, "isadmin": admin, "employee_id": employee_id}
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
