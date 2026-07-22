import ValidationModule as valid
from LoggerModule import logger


def find_patient_by_id(patients, patient_id):
    """Return the matching patient record if the ID exists."""
    for patient in patients:
        if patient["patient_id"].lower() == patient_id.lower():
            return patient
    return None


def find_appointment_by_id(appointments, appointment_id):
    """Return the matching appointment record if the ID exists."""
    for appointment in appointments:
        if appointment["appointment_id"].lower() == appointment_id.lower():
            return appointment
    return None


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


def generate_bill(bills, patients, appointments):
    """Create a bill for a completed appointment."""
    print("\n--- Generate Patient Bill ---")

    try:
        bill_id = input("Enter Bill ID: ").strip()
        if not bill_id:
            print("Bill ID cannot be empty.")
            return

        existing_bill = None
        for bill in bills:
            if bill["bill_id"].lower() == bill_id.lower():
                existing_bill = bill
                break

        if existing_bill is not None:
            print(f"Bill ID {bill_id} already exists.")
            return

        patient_id = input("Enter Patient ID: ").strip()
        if find_patient_by_id(patients, patient_id) is None:
            print("Patient ID does not exist.")
            return

        appointment_id = input("Enter Appointment ID: ").strip()
        appointment = find_appointment_by_id(appointments, appointment_id)
        if appointment is None:
            print("Appointment ID does not exist.")
            return

        if appointment["status"] != "Completed":
            print("Bill can only be generated for a completed appointment.")
            return

        existing_appointment_bill = None
        for bill in bills:
            if bill["appointment_id"].lower() == appointment_id.lower():
                existing_appointment_bill = bill
                break

        if existing_appointment_bill is not None:
            print("A bill has already been generated for this appointment.")
            return

        consultation_fee_text = input("Enter consultation fee: ").strip()
        medicine_charges_text = input("Enter medicine charges: ").strip()
        laboratory_charges_text = input("Enter laboratory charges: ").strip()
        room_charges_text = input("Enter room charges: ").strip()
        discount_text = input("Enter discount: ").strip()

        amount_inputs = [consultation_fee_text, medicine_charges_text, laboratory_charges_text, room_charges_text, discount_text]
        if not all(valid.validate_amount(amount) for amount in amount_inputs):
            print("Charges and discount cannot be negative or non-numeric.")
            logger.error("Invalid amount entered while generating bill")
            return

        consultation_fee = float(consultation_fee_text)
        medicine_charges = float(medicine_charges_text)
        laboratory_charges = float(laboratory_charges_text)
        room_charges = float(room_charges_text)
        discount = float(discount_text)

        gross_amount = consultation_fee + medicine_charges + laboratory_charges + room_charges

        if discount > gross_amount:
            print("Discount cannot be greater than the gross amount.")
            return

        total_amount = gross_amount - discount

        payment_status = input("Payment status (Paid/Pending): ").strip()
        if not valid.validate_status(payment_status, valid.VALID_PAYMENT_STATUS):
            print("Invalid payment status. Must be Paid or Pending.")
            return

        new_bill = {
            "bill_id": bill_id,
            "patient_id": patient_id,
            "appointment_id": appointment_id,
            "consultation_fee": consultation_fee,
            "medicine_charges": medicine_charges,
            "laboratory_charges": laboratory_charges,
            "room_charges": room_charges,
            "discount": discount,
            "gross_amount": gross_amount,
            "total_amount": total_amount,
            "payment_status": payment_status.strip().title(),
        }

        bills.append(new_bill)
        print(f"Bill {bill_id} generated successfully. Total amount: {total_amount}")
        logger.info(f"Bill {bill_id} generated for patient {patient_id}")

    except Exception:
        print("Something went wrong while generating the bill.")
        logger.exception("Unexpected error while generating bill")


def view_all_bills(bills, patients):
    """Show all bills, along with the patient's name."""
    print("\n--- All Bills ---")

    if not bills:
        print("No bills found.")
        return

    for bill in bills:
        patient = find_patient_by_id(patients, bill["patient_id"])
        patient_name = patient["name"] if patient else "Unknown"
        show_bill_details(bill, patient_name)


def search_patient_bills(bills, patients):
    """Show every bill for one patient plus a quick total summary."""
    print("\n--- Search Patient Bills ---")
    patient_id = input("Enter Patient ID: ").strip()

    patient_bills = [bill for bill in bills if bill["patient_id"].lower() == patient_id.lower()]

    if not patient_bills:
        print("No bills found for this patient.")
        return

    total_billed = sum(bill["total_amount"] for bill in patient_bills)
    total_paid = sum(bill["total_amount"] for bill in patient_bills if bill["payment_status"] == "Paid")
    total_pending = sum(bill["total_amount"] for bill in patient_bills if bill["payment_status"] == "Pending")

    for bill in patient_bills:
        patient = find_patient_by_id(patients, bill["patient_id"])
        patient_name = patient["name"] if patient else "Unknown"
        show_bill_details(bill, patient_name)

    print("-" * 30)
    print(f"Total Billed  : {total_billed}")
    print(f"Total Paid    : {total_paid}")
    print(f"Total Pending : {total_pending}")


def update_payment_status(bills):
    """Move a bill from Pending to Paid."""
    print("\n--- Update Payment Status ---")
    bill_id = input("Enter Bill ID: ").strip()

    for bill in bills:
        if bill["bill_id"].lower() == bill_id.lower():
            if bill["payment_status"] == "Paid":
                print("This bill is already marked as Paid.")
                return

            bill["payment_status"] = "Paid"
            print(f"Bill {bill_id} marked as Paid.")
            logger.info(f"Payment status updated for bill {bill_id}")
            return

    print("Bill ID does not exist.")
