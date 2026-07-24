from sqlalchemy import func

from database import SessionLocal

from models.customer_model import Customer
from models.account_model import Account
from models.transaction_model import Transaction
from models.loan_model import Loan
from models.branch_model import Branch

from utilities.logger_config import (
    application_logger,
    exception_logger
)


def daily_transaction_report():

    session = None

    try:

        session = SessionLocal()

        report = session.query(
            Transaction.transaction_id,
            Transaction.transaction_reference,
            Transaction.transaction_type,
            Transaction.amount,
            Transaction.transaction_date
        ).all()

        if not report:
            print("No Transactions Found.")
            return

        for transaction in report:

            print({
                "Transaction ID": transaction.transaction_id,
                "Reference": transaction.transaction_reference,
                "Type": transaction.transaction_type,
                "Amount": transaction.amount,
                "Date": str(transaction.transaction_date)
            })

        application_logger.info("Viewed Daily Transaction Report.")

    except Exception as e:

        exception_logger.exception(str(e))
        print("Error:", e)

    finally:

        if session:
            session.close()


def account_balance_report():

    session = None

    try:

        session = SessionLocal()

        accounts = session.query(Account).all()

        if not accounts:
            print("No Accounts Found.")
            return

        for account in accounts:

            print({
                "Account Number": account.account_number,
                "Customer ID": account.customer_id,
                "Account Type": account.account_type,
                "Balance": account.balance,
                "Status": account.account_status
            })

        application_logger.info("Viewed Account Balance Report.")

    except Exception as e:

        exception_logger.exception(str(e))
        print("Error:", e)

    finally:

        if session:
            session.close()


def active_loan_report():

    session = None

    try:

        session = SessionLocal()

        loans = session.query(Loan).filter(
            Loan.loan_status == "Active"
        ).all()

        if not loans:
            print("No Active Loans Found.")
            return

        for loan in loans:

            print({
                "Loan ID": loan.loan_id,
                "Customer ID": loan.customer_id,
                "Loan Type": loan.loan_type,
                "Sanctioned Amount": loan.sanctioned_amount,
                "Remaining Amount": loan.remaining_amount,
                "EMI": loan.emi_amount
            })

        application_logger.info("Viewed Active Loan Report.")

    except Exception as e:

        exception_logger.exception(str(e))
        print("Error:", e)

    finally:

        if session:
            session.close()


def defaulter_report():

    session = None

    try:

        session = SessionLocal()

        loans = session.query(Loan).filter(
            Loan.loan_status == "Active"
        ).all()

        if not loans:
            print("No Loan Records Found.")
            return

        for loan in loans:

            if loan.remaining_amount > 0:

                print({
                    "Loan ID": loan.loan_id,
                    "Customer ID": loan.customer_id,
                    "Remaining Amount": loan.remaining_amount,
                    "Loan Status": loan.loan_status
                })

        application_logger.info("Viewed Defaulter Report.")

    except Exception as e:

        exception_logger.exception(str(e))
        print("Error:", e)

    finally:

        if session:
            session.close()


def branch_wise_deposit_report():

    session = None

    try:

        session = SessionLocal()

        report = session.query(
            Branch.branch_name,
            func.sum(Account.balance)
        ).join(
            Account,
            Branch.branch_id == Account.branch_id
        ).group_by(
            Branch.branch_name
        ).all()

        if not report:
            print("No Records Found.")
            return

        for record in report:

            print({
                "Branch": record[0],
                "Total Deposit": record[1]
            })

        application_logger.info("Viewed Branch Wise Deposit Report.")

    except Exception as e:

        exception_logger.exception(str(e))
        print("Error:", e)

    finally:

        if session:
            session.close()


def customer_summary_report():

    session = None

    try:

        session = SessionLocal()

        customers = session.query(Customer).all()

        if not customers:
            print("No Customers Found.")
            return

        for customer in customers:

            account_count = session.query(Account).filter(
                Account.customer_id == customer.customer_id
            ).count()

            loan_count = session.query(Loan).filter(
                Loan.customer_id == customer.customer_id
            ).count()

            print({
                "Customer ID": customer.customer_id,
                "Customer Name": customer.first_name + " " + customer.last_name,
                "Accounts": account_count,
                "Loans": loan_count,
                "Status": customer.customer_status
            })

        application_logger.info("Viewed Customer Summary Report.")

    except Exception as e:

        exception_logger.exception(str(e))
        print("Error:", e)

    finally:

        if session:
            session.close()