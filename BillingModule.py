import ValidationModule as valid

from LoggerModule import logger

from PatientModule import find_patient_by_id

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


# def find_appointment_by_id(appointments, appointment_id):
#     """Return the matching appointment record if the ID exists."""
#     for appointment in appointments:
#         if appointment["appointment_id"].lower() == appointment_id.lower():
#             return appointment
#     return None


def show_bill_details(bill, patient_name):
    """Print one bill in a simple format."""
    print("-" * 30)
    print(f"Bill ID       : {bill['bill_id']}")
    print(f"Patient       : {patient_name} ({bill['patient_id']})")
    print(f"Appointment   : {bill['appointment_id']}")
    print(f"Gross Amount  : {bill['gross_amount']}")
    print(f"Discount      : {bill['discount']}")
    print(f"Total Amount  : {bill['total_amount']}")
    print(f"Payment       : {bill['payment_status']}")


def generate_bill():

    print("\n--- Generate Patient Bill ---")

    connection = None
    cursor = None

    try:

        patient_id = input("Enter Patient ID: ").strip()

        patient = find_patient_by_id(patient_id)

        if patient is None:
            print("Patient not found.")
            return

        appointment_id = input("Enter Appointment ID: ").strip()

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM appointments
            WHERE appointment_id=%s
            """,
            (appointment_id,)
        )

        appointment = cursor.fetchone()

        if appointment is None:
            print("Appointment not found.")
            return

        if str(appointment["patient_id"]) != str(patient_id):
            print("This appointment does not belong to the entered patient.")
            return

        if appointment["status"] != "Completed":
            print("Bill can only be generated for a completed appointment.")
            return

        cursor.execute(
            """
            SELECT *
            FROM bills
            WHERE appointment_id=%s
            """,
            (appointment_id,)
        )

        if cursor.fetchone():
            print("Bill has already been generated for this appointment.")
            return

        consultation_fee_text = input("Enter Consultation Fee: ").strip()
        medicine_charges_text = input("Enter Medicine Charges: ").strip()
        laboratory_charges_text = input("Enter Laboratory Charges: ").strip()
        room_charges_text = input("Enter Room Charges: ").strip()
        discount_text = input("Enter Discount: ").strip()

        amount_inputs = [
            consultation_fee_text,
            medicine_charges_text,
            laboratory_charges_text,
            room_charges_text,
            discount_text
        ]

        if not all(valid.validate_amount(amount) for amount in amount_inputs):
            print("Invalid amount entered.")
            return

        consultation_fee = float(consultation_fee_text)
        medicine_charges = float(medicine_charges_text)
        laboratory_charges = float(laboratory_charges_text)
        room_charges = float(room_charges_text)
        discount = float(discount_text)

        gross_amount = (
            consultation_fee +
            medicine_charges +
            laboratory_charges +
            room_charges
        )

        if discount > gross_amount:
            print("Discount cannot be greater than Gross Amount.")
            return

        total_amount = gross_amount - discount

        payment_status = input("Payment Status (Paid/Pending): ").strip().title()

        if not valid.validate_status(
            payment_status,
            valid.VALID_PAYMENT_STATUS
        ):
            print("Invalid payment status.")
            return

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO bills
            (
                patient_id,
                appointment_id,
                consultation_fee,
                medicine_charges,
                laboratory_charges,
                room_charges,
                discount,
                gross_amount,
                total_amount,
                payment_status
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                patient_id,
                appointment_id,
                consultation_fee,
                medicine_charges,
                laboratory_charges,
                room_charges,
                discount,
                gross_amount,
                total_amount,
                payment_status
            )
        )

        connection.commit()

        print(
            f"Bill generated successfully. Bill ID : {cursor.lastrowid}"
        )

        logger.info(
            f"Bill {cursor.lastrowid} generated successfully."
        )

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)


def view_all_bills():

    print("\n--- All Bills ---")

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
        FROM bills
        ORDER BY bill_id
        """

        cursor.execute(query)

        bills = cursor.fetchall()

        if not bills:
            print("No bills found.")
            return

        for bill in bills:

            patient = find_patient_by_id(bill["patient_id"])

            patient_name = patient["name"] if patient else "Unknown"

            show_bill_details(
                bill,
                patient_name
            )

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)


def search_patient_bills():

    print("\n--- Search Patient Bills ---")

    patient_id = input("Enter Patient ID: ").strip()

    patient = find_patient_by_id(patient_id)

    if patient is None:
        print("Patient not found.")
        return

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM bills
            WHERE patient_id=%s
            ORDER BY bill_id
            """,
            (patient_id,)
        )

        bills = cursor.fetchall()

        if not bills:
            print("No bills found for this patient.")
            return

        total_billed = 0
        total_paid = 0
        total_pending = 0

        for bill in bills:

            show_bill_details(
                bill,
                patient["name"]
            )

            total_billed += bill["total_amount"]

            if bill["payment_status"] == "Paid":
                total_paid += bill["total_amount"]
            else:
                total_pending += bill["total_amount"]

        print("-" * 30)
        print(f"Total Billed  : {total_billed}")
        print(f"Total Paid    : {total_paid}")
        print(f"Total Pending : {total_pending}")

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)


def update_payment_status():

    print("\n--- Update Payment Status ---")

    bill_id = input("Enter Bill ID: ").strip()

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT *
            FROM bills
            WHERE bill_id=%s
            """,
            (bill_id,)
        )

        bill = cursor.fetchone()

        if bill is None:
            print("Bill not found.")
            return

        if bill["payment_status"] == "Paid":
            print("This bill is already marked as Paid.")
            return

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE bills
            SET payment_status='Paid'
            WHERE bill_id=%s
            """,
            (bill_id,)
        )

        connection.commit()

        print(f"Bill {bill_id} marked as Paid.")

        logger.info(
            f"Payment status updated for bill {bill_id}"
        )

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)
