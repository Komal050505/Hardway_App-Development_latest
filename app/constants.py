"""

This module is for constants which contains DATA Base related DATA

"""
# DATABASE RECORD
DATA = {"records": [{"mobile": 914234234245, "name": "Kumar Makala", "company": "KXN", "employee_id": "EMP001"},
                    {"mobile": 915421215452, "name": "Komal", "company": "APPLE", "employee_id": "EMP002"},
                    {"mobile": 913020022100, "name": "Mahesh", "company": "MICROSOFT", "employee_id": "EMP003"},
                    {"mobile": 910000000000, "name": "Rajesh", "company": "WIPRO", "employee_id": "EMP004"},
                    {"mobile": 914111111111, "name": "Suresh", "company": "MIND TREE", "employee_id": "EMP005"}]}
"""
914111111111 in DATA
"records" in DATA
"""

AVAILABLE_RECORDS = [item["mobile"] for item in DATA["records"]]
# print(f"available records are --- {AVAILABLE_RECORDS}")


# FILTERS TO BE APPLIED
VALID_COUNTRY_LIST = ["91", "45", "67", "56"]
EXCLUDED_NUMBERS = [9898989898, 9999999999, 8888888888]
VALID_EMPLOYEE_IDS = ["EMP001", "EMP002", "EMP003", "EMP004", "EMP005"]
USERS = ['kmakala', 'dinesh', 'kmahesh']
ADMINS = ['komal']

LOG_SWITCH = True
