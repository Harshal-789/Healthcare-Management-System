import ValidationModule as valid

from LoggerModule import logger

from PatientModule import find_patient_by_id
from DoctorModule import find_doctor_by_id

from datetime import datetime
from database_connection import (
    get_database_connection,
    close_database_connection
)


# def find_patient_by_id(patients, patient_id):
#     """Return the matching patient record if the ID exists."""
#     for patient in patients:
#         if patient["patient_id"].lower() == patient_id.lower():
#             return patient
#     return None
 

# def find_doctor_by_id(doctors, doctor_id):
#     """Return the matching doctor record if the ID exists."""
#     for doctor in doctors:
#         if doctor["doctor_id"].lower() == doctor_id.lower():
#             return doctor
#     return None


def show_appointment_details(appointment, patient_name, doctor_name, department_name):
    """Print one appointment in a simple format."""
    print("-" * 30)
    print(f"Appointment ID : {appointment['appointment_id']}")
    print(f"Patient        : {patient_name} ({appointment['patient_id']})")
    print(f"Doctor         : {doctor_name} ({appointment['doctor_id']})")
    print(f"Department     : {department_name}")
    print(f"Date           : {appointment['appointment_date']}")
    print(f"Time           : {appointment['appointment_time']}")
    print(f"Status         : {appointment['status']}")


def book_appointment():

    print("\n--- Book Appointment ---")

    connection = None
    cursor = None

    try:

        patient_id = input("Enter Patient ID: ").strip()

        patient = find_patient_by_id(patient_id)

        if patient is None:
            print("Patient not found.")
            return

        doctor_id = input("Enter Doctor ID: ").strip()

        doctor = find_doctor_by_id(doctor_id)

        if doctor is None:
            print("Doctor not found.")
            return

        if doctor["availability_status"] != "Available":
            print("Doctor is currently unavailable.")
            return

        appointment_date = input("Enter Appointment Date (DD-MM-YYYY): ").strip()

        if not valid.validate_date(appointment_date):
            print("Invalid date.")
            return
        
        appointment_date = datetime.strptime(appointment_date,"%d-%m-%Y").strftime("%Y-%m-%d")
        appointment_time = input("Enter Appointment Time (HH:MM AM/PM): ").strip()


        if not valid.validate_time(appointment_time):
            print("Invalid time.")
            return

        
        appointment_time = datetime.strptime(
            appointment_time,
            "%I:%M %p"
        ).strftime("%H:%M:%S")

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT *
        FROM appointments
        WHERE doctor_id=%s
        AND appointment_date=%s
        AND appointment_time=%s
        AND status='Scheduled'
        """

        print("DEBUG appointment_date:", appointment_date)
        print("DEBUG type:", type(appointment_date))

        cursor.execute(
            query,
            (
                doctor_id,
                appointment_date,
                appointment_time
            )
        )

        if cursor.fetchone():

            print("Appointment slot already booked.")
            return

        cursor = connection.cursor()

        query = """
        INSERT INTO appointments
        (
            patient_id,
            doctor_id,
            appointment_date,
            appointment_time,
            status
        )
        VALUES
        (%s,%s,%s,%s,%s)
        """

        cursor.execute(
            query,
            (
                patient_id,
                doctor_id,
                appointment_date,
                appointment_time,
                "Scheduled"
            )
        )

        connection.commit()

        print(
            f"Appointment booked successfully. Appointment ID : {cursor.lastrowid}"
        )

        logger.info(
            f"Appointment {cursor.lastrowid} booked successfully."
        )

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def view_all_appointments():

    print("\n--- All Appointments ---")

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
        FROM appointments
        ORDER BY appointment_id
        """

        cursor.execute(query)

        appointments = cursor.fetchall()

        if not appointments:
            print("No appointments available.")
            return

        for appointment in appointments:

            patient = find_patient_by_id(appointment["patient_id"])
            doctor = find_doctor_by_id(appointment["doctor_id"])

            patient_name = patient["name"] if patient else "Unknown"
            doctor_name = doctor["doctor_name"] if doctor else "Unknown"
            department = doctor["department"] if doctor else "Unknown"

            show_appointment_details(
                appointment,
                patient_name,
                doctor_name,
                department
            )

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)


def cancel_appointment():

    appointment_id = input("Enter Appointment ID: ").strip()

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM appointments WHERE appointment_id=%s",
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            print("Appointment not found.")
            return

        if appointment["status"] == "Completed":
            print("Completed appointment cannot be cancelled.")
            return

        if appointment["status"] == "Cancelled":
            print("Appointment already cancelled.")
            return

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE appointments
            SET status='Cancelled'
            WHERE appointment_id=%s
            """,
            (appointment_id,)
        )

        connection.commit()

        print("Appointment cancelled successfully.")

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def complete_appointment():

    appointment_id = input("Enter Appointment ID: ").strip()

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM appointments WHERE appointment_id=%s",
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            print("Appointment not found.")
            return

        if appointment["status"] == "Cancelled":
            print("Cancelled appointment cannot be completed.")
            return

        if appointment["status"] == "Completed":
            print("Appointment already completed.")
            return

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE appointments
            SET status='Completed'
            WHERE appointment_id=%s
            """,
            (appointment_id,)
        )

        connection.commit()

        print("Appointment marked as completed.")

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)
