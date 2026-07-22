from LoggerModule import logger

from database_connection import (
    get_database_connection,
    close_database_connection
)

def generate_patient_reports():

    print("\n===== Patient Reports =====")

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM patients")

        patients = cursor.fetchall()

        if not patients:
            print("No patient data available yet.")
            return

        print(f"Total patients registered : {len(patients)}")

        city_count = {}

        for patient in patients:

            city = patient["city"]

            city_count[city] = city_count.get(city, 0) + 1

        print("\nPatients city-wise:")

        for city, count in city_count.items():

            print(f"  {city}: {count}")

        disease_count = {}

        for patient in patients:

            disease = patient["disease"]

            disease_count[disease] = disease_count.get(disease, 0) + 1

        print("\nPatients disease-wise:")

        for disease, count in disease_count.items():

            print(f"  {disease}: {count}")

        blood_group_count = {}

        for patient in patients:

            blood_group = patient["blood_group"]

            blood_group_count[blood_group] = (
                blood_group_count.get(blood_group, 0) + 1
            )

        print("\nPatients blood-group-wise:")

        for blood_group, count in blood_group_count.items():

            print(f"  {blood_group}: {count}")

        gender_count = {}

        for patient in patients:

            gender = patient["gender"]

            gender_count[gender] = gender_count.get(gender, 0) + 1

        print("\nPatients gender-wise:")

        for gender, count in gender_count.items():

            print(f"  {gender}: {count}")

        senior_patients = [
            patient for patient in patients
            if patient["age"] > 60
        ]

        print(
            f"\nPatients older than 60 years : {len(senior_patients)}"
        )

        youngest_patient = min(
            patients,
            key=lambda patient: patient["age"]
        )

        oldest_patient = max(
            patients,
            key=lambda patient: patient["age"]
        )

        print(
            f"Youngest patient : {youngest_patient['name']} "
            f"({youngest_patient['age']} years)"
        )

        print(
            f"Oldest patient   : {oldest_patient['name']} "
            f"({oldest_patient['age']} years)"
        )

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def generate_doctor_reports():

    print("\n===== Doctor Reports =====")

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM doctors")

        doctors = cursor.fetchall()

        if not doctors:
            print("No doctor data available yet.")
            return

        print(f"Total doctors : {len(doctors)}")

        department_count = {}

        for doctor in doctors:

            department = doctor["department"]

            department_count[department] = (
                department_count.get(department, 0) + 1
            )

        print("\nDoctors department-wise:")

        for department, count in department_count.items():

            print(f"  {department}: {count}")

        available_doctors = [
            doctor
            for doctor in doctors
            if doctor["availability_status"] == "Available"
        ]

        unavailable_doctors = [
            doctor
            for doctor in doctors
            if doctor["availability_status"] != "Available"
        ]

        print(f"\nAvailable doctors   : {len(available_doctors)}")
        print(f"Unavailable doctors : {len(unavailable_doctors)}")

        highest_fee_doctor = max(
            doctors,
            key=lambda doctor: doctor["consultation_fee"]
        )

        lowest_fee_doctor = min(
            doctors,
            key=lambda doctor: doctor["consultation_fee"]
        )

        print(
            f"\nHighest consultation fee : "
            f"{highest_fee_doctor['doctor_name']} "
            f"({highest_fee_doctor['consultation_fee']})"
        )

        print(
            f"Lowest consultation fee  : "
            f"{lowest_fee_doctor['doctor_name']} "
            f"({lowest_fee_doctor['consultation_fee']})"
        )

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def generate_appointment_reports():

    print("\n===== Appointment Reports =====")

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM appointments")

        appointments = cursor.fetchall()

        if not appointments:
            print("No appointment data available yet.")
            return

        cursor.execute("SELECT * FROM doctors")

        doctors = cursor.fetchall()

        print(f"Total appointments     : {len(appointments)}")

        scheduled = len([
            appointment
            for appointment in appointments
            if appointment["status"] == "Scheduled"
        ])

        completed = len([
            appointment
            for appointment in appointments
            if appointment["status"] == "Completed"
        ])

        cancelled = len([
            appointment
            for appointment in appointments
            if appointment["status"] == "Cancelled"
        ])

        print(f"Scheduled appointments : {scheduled}")
        print(f"Completed appointments : {completed}")
        print(f"Cancelled appointments : {cancelled}")

        doctor_count = {}
        department_count = {}

        for appointment in appointments:

            doctor_id = appointment["doctor_id"]

            doctor_count[doctor_id] = (
                doctor_count.get(doctor_id, 0) + 1
            )

            department = "Unknown"

            for doctor in doctors:

                if doctor["doctor_id"] == doctor_id:

                    department = doctor["department"]

                    break

            department_count[department] = (
                department_count.get(department, 0) + 1
            )

        print("\nAppointments doctor-wise:")

        for doctor_id, count in doctor_count.items():

            print(f"  {doctor_id}: {count}")

        print("\nAppointments department-wise:")

        for department, count in department_count.items():

            print(f"  {department}: {count}")

        busiest_doctor = max(
            doctor_count,
            key=doctor_count.get
        )

        print(
            f"\nDoctor with the highest number of appointments : "
            f"{busiest_doctor} ({doctor_count[busiest_doctor]} appointments)"
        )

        patient_count = {}

        for appointment in appointments:

            patient_id = appointment["patient_id"]

            patient_count[patient_id] = (
                patient_count.get(patient_id, 0) + 1
            )

        busiest_patient = max(
            patient_count,
            key=patient_count.get
        )

        print(
            f"Patient with the highest number of appointments : "
            f"{busiest_patient} ({patient_count[busiest_patient]} appointments)"
        )

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def generate_billing_reports():

    print("\n===== Billing Reports =====")

    connection = None
    cursor = None

    try:

        connection = get_database_connection()

        if connection is None:
            print("Database connection failed.")
            return

        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM bills")

        bills = cursor.fetchall()

        if not bills:
            print("No billing data available yet.")
            return

        print(f"Total bills : {len(bills)}")

        total_revenue = sum(
            bill["total_amount"]
            for bill in bills
        )

        total_paid = sum(
            bill["total_amount"]
            for bill in bills
            if bill["payment_status"] == "Paid"
        )

        total_pending = sum(
            bill["total_amount"]
            for bill in bills
            if bill["payment_status"] == "Pending"
        )

        print(f"Total revenue        : {total_revenue}")
        print(f"Total paid amount    : {total_paid}")
        print(f"Total pending amount : {total_pending}")

        average_bill = total_revenue / len(bills)

        print(f"Average bill amount  : {round(average_bill, 2)}")

        highest_bill = max(
            bills,
            key=lambda bill: bill["total_amount"]
        )

        lowest_bill = min(
            bills,
            key=lambda bill: bill["total_amount"]
        )

        print(
            f"Highest bill amount  : "
            f"{highest_bill['total_amount']} "
            f"({highest_bill['bill_id']})"
        )

        print(
            f"Lowest bill amount   : "
            f"{lowest_bill['total_amount']} "
            f"({lowest_bill['bill_id']})"
        )

        patient_totals = {}

        for bill in bills:

            patient_id = bill["patient_id"]

            patient_totals[patient_id] = (
                patient_totals.get(patient_id, 0)
                + bill["total_amount"]
            )

        top_patient = max(
            patient_totals,
            key=patient_totals.get
        )

        print(
            f"Patient with the highest total bill : "
            f"{top_patient} ({patient_totals[top_patient]})"
        )

        pending_patients = {
            bill["patient_id"]
            for bill in bills
            if bill["payment_status"] == "Pending"
        }

        print(
            f"\nPatients with pending payments : "
            f"{len(pending_patients)}"
        )

        for patient_id in pending_patients:

            print(f"  {patient_id}")

    except Exception as error:

        logger.exception(error)

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_database_connection(connection)

def generate_healthcare_reports():

    print("\n########## Healthcare Reports ##########")

    try:

        generate_patient_reports()

        generate_doctor_reports()

        generate_appointment_reports()

        generate_billing_reports()

        logger.info("Healthcare reports generated")

    except Exception as error:

        logger.exception(error)
