"""

This module is for constants which contains Data Base related Data

"""
# DATABASE RECORD
data = {"records": [{"mobile": 914234234245, "name": "Kumar Makala", "company": "KXN"},
                    {"mobile": 915421215452, "name": "Komal", "company": "APPLE"},
                    {"mobile": 913020022100, "name": "Mahesh", "company": "MICROSOFT"},
                    {"mobile": 910000000000, "name": "Rajesh", "company": "WIPRO"},
                    {"mobile": 914111111111, "name": "Suresh", "company": "MIND TREE"}]}
"""
914111111111 in data
"records" in data
"""

available_records = [item["mobile"] for item in data["records"]]
# print(f"available records are --- {available_records}")


# FILTERS TO BE APPLIED
VALID_COUNTRY_LIST = ["91", "45", "67", "56"]
EXCLUDED_NUMBERS = [9898989898, 9999999999, 8888888888]


