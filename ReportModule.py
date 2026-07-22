from LoggerModule import logger


def generate_patient_reports(patients):
    print("\n===== Patient Reports =====")

    if not patients:
        print("No patient data available yet.")
        return

    print(f"Total patients registered : {len(patients)}")

    city_count = {}
    for patient in patients:
        city_name = patient["city"]
        city_count[city_name] = city_count.get(city_name, 0) + 1
    print("\nPatients city-wise:")
    for city_name, count in city_count.items():
        print(f"  {city_name}: {count}")

    disease_count = {}
    for patient in patients:
        disease_name = patient["disease"]
        disease_count[disease_name] = disease_count.get(disease_name, 0) + 1
    print("\nPatients disease-wise:")
    for disease_name, count in disease_count.items():
        print(f"  {disease_name}: {count}")

    blood_group_count = {}
    for patient in patients:
        blood_group = patient["blood_group"]
        blood_group_count[blood_group] = blood_group_count.get(blood_group, 0) + 1
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

    senior_patients = [patient for patient in patients if patient["age"] > 60]
    print(f"\nPatients older than 60 years : {len(senior_patients)}")

    youngest_patient = min(patients, key=lambda patient: patient["age"])
    oldest_patient = max(patients, key=lambda patient: patient["age"])
    print(f"Youngest patient : {youngest_patient['name']} ({youngest_patient['age']} years)")
    print(f"Oldest patient   : {oldest_patient['name']} ({oldest_patient['age']} years)")


def generate_doctor_reports(doctors):
    print("\n===== Doctor Reports =====")

    if not doctors:
        print("No doctor data available yet.")
        return

    print(f"Total doctors : {len(doctors)}")

    department_count = {}
    for doctor in doctors:
        department_name = doctor["department"]
        department_count[department_name] = department_count.get(department_name, 0) + 1
    print("\nDoctors department-wise:")
    for department_name, count in department_count.items():
        print(f"  {department_name}: {count}")

    available_doctors = [doctor for doctor in doctors if doctor["availability_status"] == "Available"]
    unavailable_doctors = [doctor for doctor in doctors if doctor["availability_status"] != "Available"]
    print(f"\nAvailable doctors   : {len(available_doctors)}")
    print(f"Unavailable doctors : {len(unavailable_doctors)}")

    highest_fee_doctor = max(doctors, key=lambda doctor: doctor["consultation_fee"])
    lowest_fee_doctor = min(doctors, key=lambda doctor: doctor["consultation_fee"])
    print(f"\nHighest consultation fee : {highest_fee_doctor['doctor_name']} ({highest_fee_doctor['consultation_fee']})")
    print(f"Lowest consultation fee  : {lowest_fee_doctor['doctor_name']} ({lowest_fee_doctor['consultation_fee']})")


def generate_appointment_reports(appointments, doctors, patients):
    print("\n===== Appointment Reports =====")

    if not appointments:
        print("No appointment data available yet.")
        return

    print(f"Total appointments     : {len(appointments)}")
    print(f"Scheduled appointments : {len([appointment for appointment in appointments if appointment['status'] == 'Scheduled'])}")
    print(f"Completed appointments : {len([appointment for appointment in appointments if appointment['status'] == 'Completed'])}")
    print(f"Cancelled appointments : {len([appointment for appointment in appointments if appointment['status'] == 'Cancelled'])}")

    doctor_count = {}
    department_count = {}
    for appointment in appointments:
        doctor_id = appointment["doctor_id"]
        doctor_count[doctor_id] = doctor_count.get(doctor_id, 0) + 1

        doctor_department = "Unknown"
        for doctor in doctors:
            if doctor["doctor_id"] == appointment["doctor_id"]:
                doctor_department = doctor["department"]
                break
        department_count[doctor_department] = department_count.get(doctor_department, 0) + 1

    print("\nAppointments doctor-wise:")
    for doctor_id, count in doctor_count.items():
        print(f"  {doctor_id}: {count}")

    print("\nAppointments department-wise:")
    for department_name, count in department_count.items():
        print(f"  {department_name}: {count}")

    busiest_doctor_id = max(doctor_count, key=doctor_count.get)
    print(f"\nDoctor with the highest number of appointments : {busiest_doctor_id} ({doctor_count[busiest_doctor_id]} appointments)")

    patient_count = {}
    for appointment in appointments:
        patient_id = appointment["patient_id"]
        patient_count[patient_id] = patient_count.get(patient_id, 0) + 1
    busiest_patient_id = max(patient_count, key=patient_count.get)
    print(f"Patient with the highest number of appointments : {busiest_patient_id} ({patient_count[busiest_patient_id]} appointments)")


def generate_billing_reports(bills, patients):
    print("\n===== Billing Reports =====")

    if not bills:
        print("No billing data available yet.")
        return

    print(f"Total bills : {len(bills)}")

    total_revenue = sum(bill["total_amount"] for bill in bills)
    total_paid = sum(bill["total_amount"] for bill in bills if bill["payment_status"] == "Paid")
    total_pending = sum(bill["total_amount"] for bill in bills if bill["payment_status"] == "Pending")

    print(f"Total revenue        : {total_revenue}")
    print(f"Total paid amount    : {total_paid}")
    print(f"Total pending amount : {total_pending}")

    try:
        average_bill = total_revenue / len(bills)
    except ZeroDivisionError:
        average_bill = 0
    print(f"Average bill amount  : {round(average_bill, 2)}")

    highest_bill = max(bills, key=lambda bill: bill["total_amount"])
    lowest_bill = min(bills, key=lambda bill: bill["total_amount"])
    print(f"Highest bill amount  : {highest_bill['total_amount']} ({highest_bill['bill_id']})")
    print(f"Lowest bill amount   : {lowest_bill['total_amount']} ({lowest_bill['bill_id']})")

    patient_totals = {}
    for bill in bills:
        patient_id = bill["patient_id"]
        patient_totals[patient_id] = patient_totals.get(patient_id, 0) + bill["total_amount"]
    top_patient_id = max(patient_totals, key=patient_totals.get)
    print(f"Patient with the highest total bill : {top_patient_id} ({patient_totals[top_patient_id]})")

    pending_patients = {bill["patient_id"] for bill in bills if bill["payment_status"] == "Pending"}
    print(f"\nPatients with pending payments : {len(pending_patients)}")
    for patient_id in pending_patients:
        print(f"  {patient_id}")


def generate_healthcare_reports(patients, doctors, appointments, bills):
    """One entry point that main.py calls to print all four reports."""
    print("\n########## Healthcare Reports ##########")
    generate_patient_reports(patients)
    generate_doctor_reports(doctors)
    generate_appointment_reports(appointments, doctors, patients)
    generate_billing_reports(bills, patients)
    logger.info("Healthcare reports generated")
