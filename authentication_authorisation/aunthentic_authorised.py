from profile_management.apps.constants import DATA, ADMINS
from profile_management.logging_activity.logging_utils import (
    log_info, log_error, log_debug
)
from profile_management.utils.user_utils import is_valid_mobile


def authenticate_decorator(fun):
    """
    This is decorator func
    :param fun: function
    :return: bool
    """

    def wrapper(*args, **kwargs):
        log_info(f"Decorator Function Entered")
        try:
            log_info(f"Authenticating user '{args[0]}'")
            return fun(*args, **kwargs)

        except Exception as error:
            log_error(f"Exception in authentication decorator: {error}")
            return {"error": str(error)}

    return wrapper




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
    if user_name.lower() in [admin.lower() for admin in DATA['admins']]:
        log_debug(f"{user_name} found in DATA['admins'] list")
        return True


@authenticate_decorator
def admin_operations(name):
    """
    This function is used for giving permission to only Admin user for create, delete
    :param name: str
    :return: bool
    """

    # Authorisation

    role = input(f"Options For Admin operations are n, a:")
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
    role = input(f"Options for Normal User are n, a:")
    try:

        if role in ['n', 'a']:
            log_debug(f"check if user selected either n or a ")
            return f"  Cool.....Authorised user only..... "

        # if role == 'a':
        #     pass

        else:
            log_error(f"Incorrect role chosen - available options are 'n' and 'a' only")
            raise ValueError(f"Incorrect role chosen - available options are 'n' and 'a' only")

    except Exception as error:
        log_error(error)
        return {"error": str(error)}



