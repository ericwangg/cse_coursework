# CSE 4701
# Eric Wang
# 2020-04-21

import pymysql
import time
import cryptography

# Bank DB Schema
# account_no, name_on_account, balance, account_open_date

def main():
    # Main menu
    print("Main Menu")
    print("1 - Create Account")
    print("2 - Check Balance")
    print("3 - Deposit")
    print("4 - Withdraw")
    print("5 - Transfer")
    print("0 - Exit")
    choice = int(input("Enter your choice: "))

    # connect to mysql DB
    connection = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        db = "cse4701s20_project2",
        # because DEFAULT CHARSET=latin1, instead of 'utf8mb4'
        charset = 'latin1',
        cursorclass = pymysql.cursors.DictCursor)

    if choice == 0:     # Exit option
        print("Have a good day!")
        time.sleep(3)
        return
    elif choice == 1:   # Create Account
        name = input("\nName on account: ")
        bal = int(input("Enter Initial Balance: "))
        create_account(name, bal)
    elif choice == 2:   # Check Balance
        acc_no = int(input("\nEnter Account Number: "))
        check_balance(acc_no)
    elif choice == 3:   # Deposit
        acc_no = int(input("\nEnter the Account Number you would like to Deposit into: "))
        with connection.cursor() as cursor:
            sql = "SELECT * FROM account WHERE account_no = %s"
            cursor.execute(sql, acc_no)
            result = cursor.fetchone()
            if result == None:
                print('Invalid account number. Please try again.')
            else:
                amount = int(input("Enter the amount you would like to Deposit: "))
                if amount < 0:
                    print('\nInvalid amount. Please try again.')
                else:
                    deposit(acc_no, amount)
    elif choice == 4:   # Withdraw
        acc_no = int(input("\nEnter the Account Number you would like to Withdraw from: "))
        with connection.cursor() as cursor:
            sql = "SELECT * FROM account WHERE account_no = %s"
            cursor.execute(sql, acc_no)
            result = cursor.fetchone()
            if result == None:
                print('Invalid account number. Please try again.')
            else:
                amount = int(input("Enter the amount you would like to Withdraw: "))
                if amount < 0:
                    print('\nInvalid amount. Please try again.')
                else:
                    withdraw(acc_no, amount)
    elif choice == 5:   # Transfer
        acc_no1 = int(input("\nEnter the Account Number you would like to Transfer from: "))
        with connection.cursor() as cursor:
            sql = "SELECT * FROM account WHERE account_no = %s"
            cursor.execute(sql, acc_no1)
            result = cursor.fetchone()
            if result == None:
                print('Invalid account number. Please try again.')
        acc_no2 = int(input("Enter the Account Number you would like to Transfer to: "))
        with connection.cursor() as cursor:
            sql = "SELECT * FROM account WHERE account_no = %s"
            cursor.execute(sql, acc_no2)
            result = cursor.fetchone()
            if result == None:
                print('Invalid account number. Please try again.')
        amount = int(input("Enter the amount you would like to Transfer: "))
        if amount < 0:
            print('\nInvalid amount. Please try again.')
        else:
            transfer(acc_no1, acc_no2, amount)
    else:
        print("Not a valid choice. Please try again!")
        time.sleep(3)
        return

def create_account(name, balance):
    connection = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        db = "cse4701s20_project2",
        # because DEFAULT CHARSET=latin1, instead of 'utf8mb4'
        charset = 'latin1',
        cursorclass = pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "INSERT INTO account (name_on_account, balance) VALUES('%s', %d);" % (name, balance)
        cursor.execute(sql)
    connection.commit()
    with connection.cursor() as cursor:
        # sql = "SELECT * FROM account WHERE name_on_account = %s AND balance = %d;" % (name, bal)
        # sql = "SELECT MAX(account_no), MAX(account_open_date) FROM account WHERE name_on_account = %s AND balance = %s;"
        sql = "SELECT * FROM account INNER JOIN( SELECT MAX(account_open_date) AS max_date FROM account WHERE name_on_account=%s AND balance=%s) AS max_date_table WHERE account_open_date = max_date;"

        # -----THE ABOVE SQL STATEMENT---
        # -----Checks MAX(account_open_date) for the given name and Balance
        # -----Then finds the account_no that has this account_open_date
        #
        # SELECT *
        # FROM account
        # INNER JOIN(
        # SELECT MAX(account_open_date) AS max_date
        # FROM account
        # WHERE name_on_account = “name”
        # AND balance = balance
        # ) AS max_date_table
        # WHERE account_open_date = max_date;

        values = (name, balance)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        # acc_no = result.get('MAX(account_no)')
        # acc_opendate = result.get('MAX(account_open_date)')
        acc_no = result.get('account_no')
        acc_opendate = result.get('max_date')
        print("\n---Account Created Successfully---")
        print(f"Account Number: {acc_no}")
        print(f"Name on account: {name}")
        print(f"Balance: {balance}")
        print(f"Account opened on: {acc_opendate}")
        print("----------------------------------\n")
    connection.commit()

def check_balance(acc_no):
    connection = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        db = "cse4701s20_project2",
        # because DEFAULT CHARSET=latin1, instead of 'utf8mb4'
        charset = 'latin1',
        cursorclass = pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "SELECT * FROM account WHERE account_no = %s;"
        values = acc_no
        cursor.execute(sql, values)

        result = cursor.fetchone()
        if result == None:
            print("Invalid account number. Please try again.")
            time.sleep(3)
        else:
            acc_name = result.get('name_on_account')
            acc_bal = result.get('balance')
            acc_opendate = result.get('account_open_date')
            print("\n---Checking Account Balance---")
            print(f"Account Number: {acc_no}")
            print(f"Name on account: {acc_name}")
            print(f"Balance: {acc_bal}")
            print(f"Account opened on: {acc_opendate}")
            print("------------------------------\n")
            time.sleep(5)   # keeps info up for 5 seconds
    connection.commit()

def deposit(acc_no, amount):
    connection = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        db = "cse4701s20_project2",
        # because DEFAULT CHARSET=latin1, instead of 'utf8mb4'
        charset = 'latin1',
        cursorclass = pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        sql = "UPDATE account SET balance = balance + %s WHERE account_no = %s;"
        values = (amount, acc_no)
        cursor.execute(sql, values)
    connection.commit()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM account WHERE account_no = %s"
        cursor.execute(sql, acc_no)
        result = cursor.fetchone()
        acc_name = result.get('name_on_account')
        acc_bal = result.get('balance')
        acc_opendate = result.get('account_open_date')
        print("\n---Deposit Successful---")
        print(f"Account Number: {acc_no}")
        print(f"Name on account: {acc_name}")
        print(f"Balance: {acc_bal}")
        print(f"Account opened on: {acc_opendate}")
        print('------------------------')
        print("\n")
    connection.commit()

def withdraw(acc_no, amount):
    connection = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        db = "cse4701s20_project2",
        # because DEFAULT CHARSET=latin1, instead of 'utf8mb4'
        charset = 'latin1',
        cursorclass = pymysql.cursors.DictCursor)
    with connection.cursor() as cursor:
        sql = "UPDATE account SET balance = balance - %s WHERE account_no = %s;"
        values = (amount, acc_no)
        cursor.execute(sql, values)
    connection.commit()
    with connection.cursor() as cursor:
        sql = "SELECT * FROM account WHERE account_no = %s"
        cursor.execute(sql, acc_no)
        result = cursor.fetchone()
        acc_name = result.get('name_on_account')
        acc_bal = result.get('balance')
        acc_opendate = result.get('account_open_date')
        print("\n---Withdrawal Successful---")
        print(f"Account Number: {acc_no}")
        print(f"Name on account: {acc_name}")
        print(f"Balance: {acc_bal}")
        print(f"Account opened on: {acc_opendate}")
        print('---------------------------')
        print("\n")
    connection.commit()

def transfer(acc_no1, acc_no2, amount):
    print('\n---Transfer Complete---')
    withdraw(acc_no1, amount)
    deposit(acc_no2, amount)

if __name__ == "__main__":
    main()
    time.sleep(5)
