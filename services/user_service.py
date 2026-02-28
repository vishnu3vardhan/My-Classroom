# services/user_service.py

from database.user_repo import insert_user, find_by_username
from utils.helpers import build_linkedin_url, normalize_username


def add_user(name: str, username: str):
    """
    Validate and add a new user.
    Returns (success: bool, message: str)
    """

    if not name or not username:
        return False, "Name and LinkedIn username are required."

    username = normalize_username(username)

    # check duplicate
    if find_by_username(username):
        return False, "This LinkedIn username is already added."

    # build linkedin url
    linkedin_url = build_linkedin_url(username)

    # insert into DB
    insert_user(name=name.strip(), username=username, linkedin_url=linkedin_url)

    return True, "User added successfully."