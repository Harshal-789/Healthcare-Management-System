import ValidationModule as valid
from LoggerModule import logger


def find_patient_by_id(patients, patient_id):
    """Return the matching patient record if the ID exists."""
    for patient in patients:
        if patient["patient_id"].lower() == patient_id.lower():
            return patient
    return None


def show_patient_details(patient):
    """Print the details of one patient in a simple, easy-to-read format."""
    print("-" * 30)
    print(f"Patient ID  : {patient['patient_id']}")
    print(f"Name        : {patient['name']}")
    print(f"Age         : {patient['age']}")
    print(f"Gender      : {patient['gender']}")
    print(f"Contact     : {patient['contact_number']}")
    print(f"City        : {patient['city']}")
    print(f"Blood Group : {patient['blood_group']}")
    print(f"Disease     : {patient['disease']}")


def register_patient(patients):
    """Ask the user for patient details and add a new record."""
    print("\n--- Register New Patient ---")

    try:
        patient_id = input("Enter Patient ID: ").strip()

        if not patient_id:
            print("Patient ID cannot be empty.")
            return

        existing_patient = find_patient_by_id(patients, patient_id)
        if existing_patient is not None:
            print(f"Patient ID {patient_id} already exists.")
            logger.warning(f"Duplicate Patient ID {patient_id} entered")
            return

        patient_name = input("Enter patient name: ").strip()
        if not valid.validate_name(patient_name):
            print("Invalid name. Please use letters only.")
            return

        age_text = input("Enter age: ").strip()
        if not valid.validate_age(age_text):
            print("Invalid age. Please enter a number between 1 and 120.")
            return

        gender = input("Enter gender (Male/Female/Other): ").strip()
        if not valid.validate_gender(gender):
            print("Invalid gender. Must be Male, Female or Other.")
            return

        contact_number = input("Enter 10 digit contact number: ").strip()
        if not valid.validate_contact_number(contact_number):
            print("Invalid contact number. It must have exactly 10 digits.")
            return

        city = input("Enter city: ").strip()
        if not valid.validate_not_empty(city):
            print("City cannot be empty.")
            return

        blood_group = input("Enter blood group (e.g. O+): ").strip()
        if not valid.validate_blood_group(blood_group):
            print("Invalid blood group.")
            return

        disease = input("Enter disease / health problem: ").strip()
        if not valid.validate_not_empty(disease):
            print("Disease field cannot be empty.")
            return

        new_patient = {
            "patient_id": patient_id,
            "name": patient_name,
            "age": int(age_text),
            "gender": gender.capitalize(),
            "contact_number": contact_number,
            "city": city,
            "blood_group": blood_group.upper(),
            "disease": disease,
        }

        patients.append(new_patient)
        print(f"Patient {patient_id} registered successfully.")
        logger.info(f"Patient {patient_id} registered successfully")

    except Exception:
        print("Something went wrong while registering the patient.")
        logger.exception("Unexpected error while registering patient")


def view_all_patients(patients):
    """Print every patient currently in the list."""
    print("\n--- All Patients ---")

    if not patients:
        print("No patients found.")
        return

    for patient in patients:
        show_patient_details(patient)


def search_patient(patients):
    """Let the user search patients by different fields."""
    print("\n--- Search Patient ---")
    print("1. Patient ID")
    print("2. Patient Name")
    print("3. Contact Number")
    print("4. City")
    print("5. Disease")
    print("6. Blood Group")

    choice = input("Choose a search option: ").strip()
    search_value = input("Enter search value: ").strip().lower()

    matching_patients = []

    try:
        if choice == "1":
            matching_patients = [patient for patient in patients if patient["patient_id"].lower() == search_value]
        elif choice == "2":
            matching_patients = [patient for patient in patients if search_value in patient["name"].lower()]
        elif choice == "3":
            matching_patients = [patient for patient in patients if patient["contact_number"] == search_value]
        elif choice == "4":
            matching_patients = [patient for patient in patients if search_value in patient["city"].lower()]
        elif choice == "5":
            matching_patients = [patient for patient in patients if search_value in patient["disease"].lower()]
        elif choice == "6":
            matching_patients = [patient for patient in patients if patient["blood_group"].lower() == search_value]
        else:
            print("Invalid search option.")
            return
    except KeyError:
        print("Some patient records seem to be incomplete.")
        logger.error("KeyError while searching patients")
        return

    if not matching_patients:
        print("No matching patient found.")
        return

    for patient in matching_patients:
        show_patient_details(patient)


def update_patient(patients):
    """Update details of an existing patient. Patient ID stays the same."""
    print("\n--- Update Patient ---")
    patient_id = input("Enter Patient ID to update: ").strip()

    found_patient = find_patient_by_id(patients, patient_id)
    if found_patient is None:
        print("Patient ID does not exist.")
        logger.warning(f"Update failed, Patient ID {patient_id} not found")
        return

    print("Leave a field blank to keep the current value.")

    try:
        new_name = input(f"Name [{found_patient['name']}]: ").strip()
        if new_name:
            if valid.validate_name(new_name):
                found_patient["name"] = new_name
            else:
                print("Invalid name, keeping old value.")

        new_age = input(f"Age [{found_patient['age']}]: ").strip()
        if new_age:
            if valid.validate_age(new_age):
                found_patient["age"] = int(new_age)
            else:
                print("Invalid age, keeping old value.")

        new_contact_number = input(f"Contact number [{found_patient['contact_number']}]: ").strip()
        if new_contact_number:
            if valid.validate_contact_number(new_contact_number):
                found_patient["contact_number"] = new_contact_number
            else:
                print("Invalid contact number, keeping old value.")

        new_city = input(f"City [{found_patient['city']}]: ").strip()
        if new_city:
            found_patient["city"] = new_city

        new_blood_group = input(f"Blood group [{found_patient['blood_group']}]: ").strip()
        if new_blood_group:
            if valid.validate_blood_group(new_blood_group):
                found_patient["blood_group"] = new_blood_group.upper()
            else:
                print("Invalid blood group, keeping old value.")

        new_disease = input(f"Disease [{found_patient['disease']}]: ").strip()
        if new_disease:
            found_patient["disease"] = new_disease

        print(f"Patient {patient_id} updated successfully.")
        logger.info(f"Patient {patient_id} updated successfully")

    except Exception:
        print("Something went wrong while updating the patient.")
        logger.exception(f"Unexpected error while updating patient {patient_id}")


def delete_patient(patients, appointments):
    """Delete a patient, but only if they don't have a scheduled appointment."""
    print("\n--- Delete Patient ---")
    patient_id = input("Enter Patient ID to delete: ").strip()

    found_patient = find_patient_by_id(patients, patient_id)
    if found_patient is None:
        print("Patient ID does not exist.")
        return

    has_scheduled_appointment = any(
        appointment["patient_id"].lower() == patient_id.lower() and appointment["status"] == "Scheduled"
        for appointment in appointments
    )
    if has_scheduled_appointment:
        print("This patient has a scheduled appointment and cannot be deleted.")
        logger.warning(f"Delete blocked, Patient {patient_id} has a scheduled appointment")
        return

    confirm = input(f"Are you sure you want to delete {found_patient['name']}? (yes/no): ").strip().lower()
    if confirm == "yes":
        patients.remove(found_patient)
        print(f"Patient {patient_id} deleted successfully.")
        logger.info(f"Patient {patient_id} deleted successfully")
    else:
        print("Delete cancelled.")
