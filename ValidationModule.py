from datetime import datetime

VALID_BLOOD_GROUPS = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
VALID_GENDERS = ["Male", "Female", "Other"]
VALID_AVAILABILITY = ["Available", "Unavailable", "On Leave"]
VALID_PAYMENT_STATUS = ["Paid", "Pending"]


def normalize_text(value):
    """Remove extra spaces around a text value and return a clean version."""
    if not value:
        return ""
    return value.strip()


def validate_name(name):
    """A name should not be empty and should only have letters, spaces or dots."""
    cleaned_name = normalize_text(name)
    if not cleaned_name:
        return False

    allowed_chars = cleaned_name.replace(" ", "").replace(".", "")
    return allowed_chars.isalpha()


def validate_age(age):
    """Age has to be a whole number between 1 and 120."""
    try:
        age_value = int(age)
    except (ValueError, TypeError):
        return False
    return 1 <= age_value <= 120


def validate_contact_number(number):
    """Contact number must be exactly 10 digits, nothing else."""
    cleaned_number = normalize_text(number)
    if not cleaned_number:
        return False
    return cleaned_number.isdigit() and len(cleaned_number) == 10


def validate_gender(gender):
    """Check whether the gender is one of the allowed values."""
    cleaned_gender = normalize_text(gender)
    if not cleaned_gender:
        return False
    return cleaned_gender.capitalize() in VALID_GENDERS


def validate_blood_group(blood_group):
    """Check whether the blood group is one of the allowed values."""
    cleaned_group = normalize_text(blood_group)
    if not cleaned_group:
        return False
    return cleaned_group.upper() in VALID_BLOOD_GROUPS


def validate_not_empty(value):
    """Generic check used for city, disease, department, etc."""
    return bool(value and value.strip())


def validate_amount(amount):
    """Charges/fees must be a number and can't be negative."""
    try:
        amount_value = float(amount)
    except (ValueError, TypeError):
        return False
    return amount_value >= 0


def validate_status(status, allowed_values):
    """Generic status checker, used for availability / payment status."""
    cleaned_status = normalize_text(status)
    if not cleaned_status:
        return False
    return cleaned_status.title() in [value.title() for value in allowed_values]


def validate_date(date_text):
    """Expecting the date in DD-MM-YYYY format, e.g. 25-07-2026."""
    try:
        datetime.strptime(normalize_text(date_text), "%d-%m-%Y")
        return True
    except (ValueError, AttributeError):
        return False


def validate_time(time_text):
    """Expecting something like '10:30 AM'."""
    try:
        datetime.strptime(normalize_text(time_text).upper(), "%I:%M %p")
        return True
    except (ValueError, AttributeError):
        return False
