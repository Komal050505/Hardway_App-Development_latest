import os

SMTP_PORT = 587  # For starttls
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "komalsaikiran05@gmail.com"
RECEIVER_EMAIL = ["komalsaikiran05@gmail.com"]
PASSWORD = "qlqgqoyzaynbogra"
MESSAGE = f"""\
Subject: Hi there

New User  has been Posted successfully in your table ."""
DELETE_MESSAGE = """
User has been deleted successfully from your table 

"""
UPDATE_MESSAGE = """
User has been updated successfully

"""
GET_ALL_MESSAGE = """
Some one is checking all users information from the table
"""
GET_SINGLE_MESSAGE = """
Some one is checking single user information from the table
"""
GET_USER_RANGE = """
Some one is checking User Range information from the table
"""
#print("This is smtp_port---", SMTP_PORT)
#print("This is email_password", PASSWORD)
