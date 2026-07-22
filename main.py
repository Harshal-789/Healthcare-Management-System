from PatientModule import (
    register_patient,
    view_all_patients,
    search_patient,
    update_patient,
    delete_patient,
)

from DoctorModule import (
    add_doctor,
    view_all_doctors,
    search_doctor,
)

from AppointmentModule import (
    book_appointment,
    view_all_appointments,
    cancel_appointment,
    complete_appointment,
)

from BillingModule import (
    generate_bill,
    view_all_bills,
    search_patient_bills,
    update_payment_status,
)

from ReportModule import (
    generate_healthcare_reports,
)


def patient_menu():
    while True:
        print("\n========== PATIENT MANAGEMENT ==========")
        print("1. Register Patient")
        print("2. View All Patients")
        print("3. Search Patient")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_patient()

        elif choice == "2":
            view_all_patients()

        elif choice == "3":
            search_patient()

        elif choice == "4":
            update_patient()

        elif choice == "5":
            delete_patient()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def doctor_menu():
    while True:
        print("\n========== DOCTOR MANAGEMENT ==========")
        print("1. Add Doctor")
        print("2. View All Doctors")
        print("3. Search Doctor")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_doctor()

        elif choice == "2":
            view_all_doctors()

        elif choice == "3":
            search_doctor()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def appointment_menu():
    while True:
        print("\n========== APPOINTMENT MANAGEMENT ==========")
        print("1. Book Appointment")
        print("2. View All Appointments")
        print("3. Cancel Appointment")
        print("4. Complete Appointment")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            book_appointment()

        elif choice == "2":
            view_all_appointments()

        elif choice == "3":
            cancel_appointment()

        elif choice == "4":
            complete_appointment()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def billing_menu():
    while True:
        print("\n========== BILLING MANAGEMENT ==========")
        print("1. Generate Bill")
        print("2. View All Bills")
        print("3. Search Patient Bills")
        print("4. Update Payment Status")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            generate_bill()

        elif choice == "2":
            view_all_bills()

        elif choice == "3":
            search_patient_bills()

        elif choice == "4":
            update_payment_status()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def report_menu():
    while True:
        print("\n========== REPORTS ==========")
        print("1. Generate Healthcare Reports")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            generate_healthcare_reports()

        elif choice == "0":
            break

        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n")
        print("=" * 60)
        print("      HOSPITAL PATIENT MANAGEMENT SYSTEM")
        print("=" * 60)
        print("1. Patient Management")
        print("2. Doctor Management")
        print("3. Appointment Management")
        print("4. Billing Management")
        print("5. Reports")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            patient_menu()

        elif choice == "2":
            doctor_menu()

        elif choice == "3":
            appointment_menu()

        elif choice == "4":
            billing_menu()

        elif choice == "5":
            report_menu()

        elif choice == "0":
            print("\nThank you for using Hospital Patient Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()