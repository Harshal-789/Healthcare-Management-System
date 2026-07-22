import ValidationModule as valid

from LoggerModule import logger

from database_connection import (
    get_database_connection,
    close_database_connection
)


def find_doctor_by_id(doctor_id):

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            return None

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM doctors
        WHERE doctor_id=%s
        """

        cursor.execute(query, (doctor_id,))

        return cursor.fetchone()

    except Exception as error:
        logger.exception(error)
        return None

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)


def show_doctor_details(doctor):

    print("-" * 40)
    print(f"Doctor ID        : {doctor['doctor_id']}")
    print(f"Doctor Name      : {doctor['doctor_name']}")
    print(f"Department       : {doctor['department']}")
    print(f"Consultation Fee : {doctor['consultation_fee']}")
    print(f"Availability     : {doctor['availability_status']}")


def add_doctor():

    print("\n--- Add New Doctor ---")

    connection = None
    cursor = None

    try:

        doctor_name = input("Enter Doctor Name: ").strip()

        if not valid.validate_not_empty(doctor_name):
            print("Doctor name cannot be empty.")
            return

        department = input("Enter Department: ").strip()

        if not valid.validate_not_empty(department):
            print("Department cannot be empty.")
            return

        consultation_fee = input("Enter Consultation Fee: ").strip()

        if not valid.validate_amount(consultation_fee):
            print("Invalid consultation fee.")
            return

        availability = input(
            "Availability (Available/Unavailable/On Leave): "
        ).strip()

        if not valid.validate_status(
            availability,
            valid.VALID_AVAILABILITY
        ):
            print("Invalid availability.")
            return

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor()

        query = """
        INSERT INTO doctors
        (
            doctor_name,
            department,
            consultation_fee,
            availability_status
        )
        VALUES
        (%s,%s,%s,%s)
        """

        values = (
            doctor_name,
            department,
            float(consultation_fee),
            availability.title()
        )

        cursor.execute(query, values)

        connection.commit()

        print(
            f"Doctor added successfully. Doctor ID : {cursor.lastrowid}"
        )

        logger.info(
            f"Doctor {cursor.lastrowid} added successfully."
        )

    except Exception as error:

        print("Something went wrong.")

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)


def view_all_doctors():

    print("\n--- All Doctors ---")

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
        FROM doctors
        ORDER BY doctor_id
        """

        cursor.execute(query)

        doctors = cursor.fetchall()

        if not doctors:
            print("No doctors available.")
            return

        for doctor in doctors:
            show_doctor_details(doctor)

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)


def search_doctor():

    print("\n--- Search Doctor ---")
    print("1. Doctor ID")
    print("2. Doctor Name")
    print("3. Department")
    print("4. Availability Status")

    choice = input("Choose a search option: ").strip()
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
            FROM doctors
            WHERE doctor_id=%s
            """

            cursor.execute(query, (search_value,))

        elif choice == "2":

            query = """
            SELECT *
            FROM doctors
            WHERE doctor_name LIKE %s
            """

            cursor.execute(query, ("%" + search_value + "%",))

        elif choice == "3":

            query = """
            SELECT *
            FROM doctors
            WHERE department LIKE %s
            """

            cursor.execute(query, ("%" + search_value + "%",))

        elif choice == "4":

            query = """
            SELECT *
            FROM doctors
            WHERE availability_status=%s
            """

            cursor.execute(query, (search_value.title(),))

        else:
            print("Invalid search option.")
            return

        doctors = cursor.fetchall()

        if not doctors:
            print("No matching doctor found.")
            return

        for doctor in doctors:
            show_doctor_details(doctor)

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)