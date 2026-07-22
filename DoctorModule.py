import ValidationModule as valid
from LoggerModule import logger


def find_doctor_by_id(doctors, doctor_id):
    """Return the matching doctor record if the ID exists."""
    for doctor in doctors:
        if doctor["doctor_id"].lower() == doctor_id.lower():
            return doctor
    return None


def show_doctor_details(doctor):
    """Print the details of one doctor in a clear format."""
    print("-" * 30)
    print(f"Doctor ID    : {doctor['doctor_id']}")
    print(f"Name         : {doctor['doctor_name']}")
    print(f"Department   : {doctor['department']}")
    print(f"Fee          : {doctor['consultation_fee']}")
    print(f"Availability : {doctor['availability_status']}")


def add_doctor(doctors):
    """Ask for doctor details and add a new doctor record."""
    print("\n--- Add New Doctor ---")

    try:
        doctor_id = input("Enter Doctor ID: ").strip()

        if not doctor_id:
            print("Doctor ID cannot be empty.")
            return

        existing_doctor = find_doctor_by_id(doctors, doctor_id)
        if existing_doctor is not None:
            print(f"Doctor ID {doctor_id} already exists.")
            logger.warning(f"Duplicate Doctor ID {doctor_id} entered")
            return

        doctor_name = input("Enter doctor name: ").strip()
        if not valid.validate_not_empty(doctor_name):
            print("Doctor name cannot be empty.")
            return

        department = input("Enter department: ").strip()
        if not valid.validate_not_empty(department):
            print("Department cannot be empty.")
            return

        consultation_fee_text = input("Enter consultation fee: ").strip()
        if not valid.validate_amount(consultation_fee_text) or float(consultation_fee_text) <= 0:
            print("Invalid consultation fee. It must be greater than zero.")
            logger.error("Invalid consultation fee entered")
            return

        availability_status = input("Availability (Available/Unavailable/On Leave): ").strip()
        if not valid.validate_status(availability_status, valid.VALID_AVAILABILITY):
            print("Invalid availability status.")
            return

        new_doctor = {
            "doctor_id": doctor_id,
            "doctor_name": doctor_name,
            "department": department,
            "consultation_fee": float(consultation_fee_text),
            "availability_status": availability_status.strip().title(),
        }

        doctors.append(new_doctor)
        print(f"Doctor {doctor_id} added successfully.")
        logger.info(f"Doctor {doctor_id} registered successfully")

    except Exception:
        print("Something went wrong while adding the doctor.")
        logger.exception("Unexpected error while adding doctor")


def view_all_doctors(doctors):
    """Print every doctor currently in the list."""
    print("\n--- All Doctors ---")

    if not doctors:
        print("No doctors available.")
        return

    for doctor in doctors:
        show_doctor_details(doctor)


def search_doctor(doctors):
    """Search doctors by ID, name, department or availability status."""
    print("\n--- Search Doctor ---")
    print("1. Doctor ID")
    print("2. Doctor Name")
    print("3. Department")
    print("4. Availability Status")

    choice = input("Choose a search option: ").strip()
    search_value = input("Enter search value: ").strip().lower()

    matching_doctors = []

    if choice == "1":
        matching_doctors = [doctor for doctor in doctors if doctor["doctor_id"].lower() == search_value]
    elif choice == "2":
        matching_doctors = [doctor for doctor in doctors if search_value in doctor["doctor_name"].lower()]
    elif choice == "3":
        matching_doctors = [doctor for doctor in doctors if search_value in doctor["department"].lower()]
    elif choice == "4":
        matching_doctors = [doctor for doctor in doctors if doctor["availability_status"].lower() == search_value]
    else:
        print("Invalid search option.")
        return

    if not matching_doctors:
        print("No matching doctor found.")
        return

    for doctor in matching_doctors:
        show_doctor_details(doctor)
