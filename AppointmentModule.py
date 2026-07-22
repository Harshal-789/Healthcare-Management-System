import ValidationModule as valid
from LoggerModule import logger


def find_patient_by_id(patients, patient_id):
    """Return the matching patient record if the ID exists."""
    for patient in patients:
        if patient["patient_id"].lower() == patient_id.lower():
            return patient
    return None
 

def find_doctor_by_id(doctors, doctor_id):
    """Return the matching doctor record if the ID exists."""
    for doctor in doctors:
        if doctor["doctor_id"].lower() == doctor_id.lower():
            return doctor
    return None


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


def book_appointment(appointments, patients, doctors):
    """Book a new appointment after checking patient, doctor and slot."""
    print("\n--- Book Appointment ---")

    try:
        appointment_id = input("Enter Appointment ID: ").strip()
        if not appointment_id:
            print("Appointment ID cannot be empty.")
            return

        existing_appointment = None
        for appointment in appointments:
            if appointment["appointment_id"].lower() == appointment_id.lower():
                existing_appointment = appointment
                break

        if existing_appointment is not None:
            print(f"Appointment ID {appointment_id} already exists.")
            return

        patient_id = input("Enter Patient ID: ").strip()
        patient = find_patient_by_id(patients, patient_id)
        if patient is None:
            print("Patient ID does not exist.")
            logger.warning(f"Booking failed, Patient ID {patient_id} not found")
            return

        doctor_id = input("Enter Doctor ID: ").strip()
        doctor = find_doctor_by_id(doctors, doctor_id)
        if doctor is None:
            print("Doctor ID does not exist.")
            logger.warning(f"Booking failed, Doctor ID {doctor_id} not found")
            return

        if doctor["availability_status"] != "Available":
            print("Doctor is currently unavailable.")
            logger.warning(f"Doctor {doctor_id} is unavailable")
            return

        appointment_date = input("Enter appointment date (DD-MM-YYYY): ").strip()
        if not valid.validate_date(appointment_date):
            print("Invalid date format. Please use DD-MM-YYYY.")
            return

        appointment_time = input("Enter appointment time (e.g. 10:30 AM): ").strip()
        if not valid.validate_time(appointment_time):
            print("Invalid time format. Please use HH:MM AM/PM.")
            return

        slot_is_taken = any(
            appointment["doctor_id"].lower() == doctor_id.lower()
            and appointment["appointment_date"] == appointment_date
            and appointment["appointment_time"].lower() == appointment_time.lower()
            and appointment["status"] == "Scheduled"
            for appointment in appointments
        )
        if slot_is_taken:
            print("Appointment slot is already booked.")
            logger.warning(f"Doctor {doctor_id} already booked at that slot")
            return

        new_appointment = {
            "appointment_id": appointment_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_date": appointment_date,
            "appointment_time": appointment_time,
            "status": "Scheduled",
        }

        appointments.append(new_appointment)
        print(f"Appointment {appointment_id} booked successfully.")
        logger.info(f"Appointment {appointment_id} booked successfully")

    except Exception:
        print("Something went wrong while booking the appointment.")
        logger.exception("Unexpected error while booking appointment")


def view_all_appointments(appointments, patients, doctors):
    """Show all appointments along with patient and doctor names."""
    print("\n--- All Appointments ---")

    if not appointments:
        print("No appointments available.")
        return

    for appointment in appointments:
        patient = find_patient_by_id(patients, appointment["patient_id"])
        doctor = find_doctor_by_id(doctors, appointment["doctor_id"])

        patient_name = patient["name"] if patient else "Unknown"
        doctor_name = doctor["doctor_name"] if doctor else "Unknown"
        department = doctor["department"] if doctor else "Unknown"

        show_appointment_details(appointment, patient_name, doctor_name, department)


def cancel_appointment(appointments):
    """Cancel a scheduled appointment."""
    print("\n--- Cancel Appointment ---")
    appointment_id = input("Enter Appointment ID: ").strip()

    for appointment in appointments:
        if appointment["appointment_id"].lower() == appointment_id.lower():
            if appointment["status"] == "Completed":
                print("This appointment is already completed and cannot be cancelled.")
                return
            if appointment["status"] == "Cancelled":
                print("This appointment is already cancelled.")
                return

            appointment["status"] = "Cancelled"
            print(f"Appointment {appointment_id} cancelled.")
            logger.info(f"Appointment {appointment_id} cancelled")
            return

    print("Appointment ID does not exist.")


def complete_appointment(appointments):
    """Mark a scheduled appointment as completed."""
    print("\n--- Complete Appointment ---")
    appointment_id = input("Enter Appointment ID: ").strip()

    for appointment in appointments:
        if appointment["appointment_id"].lower() == appointment_id.lower():
            if appointment["status"] == "Cancelled":
                print("A cancelled appointment cannot be marked as completed.")
                return
            if appointment["status"] == "Completed":
                print("This appointment is already completed.")
                return

            appointment["status"] = "Completed"
            print(f"Appointment {appointment_id} marked as completed.")
            logger.info(f"Appointment {appointment_id} completed")
            return

    print("Appointment ID does not exist.")
