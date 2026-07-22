import ValidationModule as valid

from LoggerModule import logger

from database_connection import (
    get_database_connection,
    close_database_connection
)


def find_patient_by_id(patient_id):
    """
    Return the matching patient record from the database.
    """

    connection = None
    cursor = None

    try:
        connection = get_database_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM patients
        WHERE patient_id=%s
        """

        cursor.execute(query, (patient_id,))

        return cursor.fetchone()

    except Exception as error:
        logger.exception(error)
        return None

    finally:
        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)


def show_patient_details(patient):

    print("-" * 40)
    print(f"Patient ID      : {patient['patient_id']}")
    print(f"Name            : {patient['name']}")
    print(f"Age             : {patient['age']}")
    print(f"Gender          : {patient['gender']}")
    print(f"Contact Number  : {patient['contact_number']}")
    print(f"City            : {patient['city']}")
    print(f"Blood Group     : {patient['blood_group']}")
    print(f"Disease         : {patient['disease']}")

def register_patient():
    """
    Register a new patient into the MySQL database.
    """

    print("\n--- Register New Patient ---")

    connection = None
    cursor = None

    try:
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
            print("Invalid gender.")
            return

        contact_number = input("Enter 10 digit contact number: ").strip()
        if not valid.validate_contact_number(contact_number):
            print("Invalid contact number.")
            return

        city = input("Enter city: ").strip()
        if not valid.validate_not_empty(city):
            print("City cannot be empty.")
            return

        blood_group = input("Enter blood group: ").strip()
        if not valid.validate_blood_group(blood_group):
            print("Invalid blood group.")
            return

        disease = input("Enter disease / health problem: ").strip()
        if not valid.validate_not_empty(disease):
            print("Disease cannot be empty.")
            return

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor()

        query = """
        INSERT INTO patients
        (
            name,
            age,
            gender,
            contact_number,
            city,
            blood_group,
            disease
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            patient_name,
            int(age_text),
            gender.capitalize(),
            contact_number,
            city,
            blood_group.upper(),
            disease
        )

        cursor.execute(query, values)
        connection.commit()

        print(f"\nPatient registered successfully.")
        print(f"Generated Patient ID : {cursor.lastrowid}")

        logger.info(
            f"Patient {cursor.lastrowid} registered successfully."
        )

    except Exception as error:
        print("Something went wrong while registering the patient.")
        logger.exception(error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def view_all_patients():

    print("\n--- All Patients ---")

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM patients
        ORDER BY patient_id
        """

        cursor.execute(query)

        patients = cursor.fetchall()

        if not patients:
            print("No patients found.")
            return

        for patient in patients:
            show_patient_details(patient)

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def search_patient():

    print("\n--- Search Patient ---")
    print("1. Patient ID")
    print("2. Name")
    print("3. Contact Number")

    choice = input("Choose option: ").strip()
    search_value = input("Enter search value: ").strip()

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        if choice == "1":

            query = """
            SELECT *
            FROM patients
            WHERE patient_id=%s
            """

            cursor.execute(query, (search_value,))

        elif choice == "2":

            query = """
            SELECT *
            FROM patients
            WHERE name LIKE %s
            """

            cursor.execute(query, ("%" + search_value + "%",))

        elif choice == "3":

            query = """
            SELECT *
            FROM patients
            WHERE contact_number=%s
            """

            cursor.execute(query, (search_value,))

        else:
            print("Invalid option.")
            return

        patients = cursor.fetchall()

        if not patients:
            print("No patient found.")
            return

        for patient in patients:
            show_patient_details(patient)

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def update_patient():

    patient_id = input("Enter Patient ID to update: ").strip()

    patient = find_patient_by_id(patient_id)

    if patient is None:
        print("Patient not found.")
        return

    name = input(f"Name [{patient['name']}]: ").strip() or patient["name"]
    age = input(f"Age [{patient['age']}]: ").strip() or str(patient["age"])
    gender = input(f"Gender [{patient['gender']}]: ").strip() or patient["gender"]
    contact = input(f"Contact [{patient['contact_number']}]: ").strip() or patient["contact_number"]
    city = input(f"City [{patient['city']}]: ").strip() or patient["city"]
    blood = input(f"Blood Group [{patient['blood_group']}]: ").strip() or patient["blood_group"]
    disease = input(f"Disease [{patient['disease']}]: ").strip() or patient["disease"]

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor()

        query = """
        UPDATE patients
        SET
            name=%s,
            age=%s,
            gender=%s,
            contact_number=%s,
            city=%s,
            blood_group=%s,
            disease=%s
        WHERE patient_id=%s
        """

        cursor.execute(
            query,
            (
                name,
                int(age),
                gender,
                contact,
                city,
                blood,
                disease,
                patient_id
            )
        )

        connection.commit()

        print("Patient updated successfully.")

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def delete_patient():

    patient_id = input("Enter Patient ID to delete: ").strip()

    patient = find_patient_by_id(patient_id)

    if patient is None:
        print("Patient not found.")
        return

    confirm = input("Delete this patient? (Y/N): ").upper()

    if confirm != "Y":
        print("Deletion cancelled.")
        return

    connection = None
    cursor = None

    try:

        connection = get_database_connection()
        cursor = connection.cursor()

        query = """
        DELETE FROM patients
        WHERE patient_id=%s
        """

        cursor.execute(query, (patient_id,))
        connection.commit()

        print("Patient deleted successfully.")

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)            