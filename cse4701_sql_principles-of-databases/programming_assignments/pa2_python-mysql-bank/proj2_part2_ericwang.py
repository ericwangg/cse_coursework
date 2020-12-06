# CSE 4701
# Eric Wang
# 2020-04-21

import pymysql
import time
# import cryptography

# Bank DB Schema
# account_no, name_on_account, balance, account_open_date

def main():
    # Main menu
    online = True
    while online == True:
        menu()
        choice_text = input("Enter your choice: ")
        choice = int(choice_text)
        connection = mysql_DB()
        if choice_text == 'm':
            return
        elif choice == 0:
            print("Have a good day!")
            time.sleep(2)
            online = False
        elif choice == 1:   # Create Account
            create_account(connection)
        elif choice == 2:   # Check Balance
            check_balance(connection)
        elif choice == 3:   # Deposit
            deposit(connection)
        elif choice == 4:   # Withdraw
            withdraw(connection)
        elif choice == 5:   # Transfer
            transfer(connection)
        else:
            print("\n   Not a valid choice. Please try again!\n")


def mysql_DB():
    connection = pymysql.connect(
        host = "localhost",
        user = "root",
        passwd = "",
        db = "cse4701s20_project2",
        # because DEFAULT CHARSET=latin1, instead of 'utf8mb4'
        charset = 'latin1',
        cursorclass = pymysql.cursors.DictCursor)
    return connection

def menu():
    print("\n----------- Main Menu -----------")
    print("      +---+----------------+     ")
    print("      | 1 | Create Account |     ")
    print("      | 2 | Check Balance  |     ")
    print("      | 3 | Deposit        |     ")
    print("      | 4 | Withdraw       |     ")
    print("      | 5 | Transfer       |     ")
    print("      | 0 | Exit           |     ")
    print("      +---+----------------+     ")
    print("---------------------------------")
    print("--- Press any key at any time ---")
    print("--- to return to Main Menu    ---")
    print("---------------------------------\n")

def create_account(connection):
    name = input("\nName on account: ")
    while True:
        balance_text = input("\nEnter Initial Balance: ")
        if "-" in balance_text and balance_text.replace("-","").isnumeric() == True:
            print("\n   Invalid amount. Please try again.")
        elif "." in balance_text and balance_text.replace(".","").isnumeric() == True:
            print("\n   Sorry, cannot deposit an increment less than $1.")
        # elif balance_text.isnumeric() == False:
        #     break
        else:
            balance = int(balance_text)
            with connection.cursor() as cursor:
                sql = "INSERT INTO account (name_on_account, balance) VALUES('%s', %d);" % (name, balance)
                cursor.execute(sql)
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
                # WHERE name_on_account = “12”
                # AND balance = 12
                # ) AS max_date_table
                # WHERE account_open_date = max_date;

                values = (name, balance)
                cursor.execute(sql, values)
                result = cursor.fetchone()
                # acc_no = result.get('MAX(account_no)')
                # acc_opendate = result.get('MAX(account_open_date)')
                acc_no = result.get('account_no')
                acc_opendate = result.get('max_date')
                print("\n+---   Account Created Successfully   ---")
                print(f"|Account Number: {acc_no}")
                print(f"|Name on account: {name}")
                print(f"|Balance: {balance}")
                print(f"|Account opened on: {acc_opendate}")
                print("+----------------------------------------\n")
            connection.commit()
            break

def check_balance(connection):
    while True:
        acc_no_text = input("\nEnter Account Number: ")
        if acc_no_text.isnumeric() == False:
            break
        else:
            acc_no = int(acc_no_text)
            with connection.cursor() as cursor:
                sql = "SELECT * FROM account WHERE account_no = %s;"
                cursor.execute(sql, acc_no)
                result = cursor.fetchone()
                if result == None:
                    print("Invalid account number. Please try again.")
                else:
                    acc_name = result.get('name_on_account')
                    acc_bal = result.get('balance')
                    acc_opendate = result.get('account_open_date')
                    print("\n+---   Checking Account Balance   ---")
                    print(f"|Account Number: {acc_no}")
                    print(f"|Name on account: {acc_name}")
                    print(f"|Balance: {acc_bal}")
                    print(f"|Account opened on: {acc_opendate}")
                    print("+------------------------------------\n")
            connection.commit()
            break

def deposit(connection):
    loop_1 = True
    while loop_1 == True:
        acc_no_text = input("\nEnter the Account Number you would like to Deposit to: ")
        if acc_no_text.isnumeric() == False:        # anything other than a number considered as "any key" return to menu
            break
        else:
            acc_no = int(acc_no_text)
            with connection.cursor() as cursor:
                sql = "SELECT * FROM account WHERE account_no = %s FOR UPDATE;"
                cursor.execute(sql, acc_no)
                result = cursor.fetchone()
                if result == None:
                    print("\n   Invalid account number. Please try again.")
                    connection.commit()
                else:
                    # if valid account number, display current balance
                    acc_bal = result.get('balance')
                    print("\n+---   Existing Account Balance   ---")
                    print(f"|Account Number: {acc_no}")
                    print(f"|Name on account: {result.get('name_on_account')}")
                    print(f"|Balance: {acc_bal}")
                    print(f"|Account opened on: {result.get('account_open_date')}")
                    print("+------------------------------------\n")
                    connection.commit()
                    # then ask for deposit amount
                    while True:
                        amount_text = input("Enter the amount you would like to Withdraw: ")
                        # if it is a negative number
                        if "-" in amount_text and amount_text.replace("-","").isnumeric() == True:
                            print("\n   Invalid amount. Please try again. \n")
                        # if it is a flaot, less than $1 increment amount or less than $1
                        elif "." in amount_text and amount_text.replace(".","").isnumeric() == True:
                            print("\n   Sorry, you cannot deposit increments less than $1. \n")
                        elif amount_text.isnumeric() == False:
                            loop_1 = False
                            break
                        else:
                            amount = int(amount_text)
                            with connection.cursor() as cursor:
                                sql = "UPDATE account SET balance = balance + %s WHERE account_no = %s;"
                                values = (amount, acc_no)
                                cursor.execute(sql, values)
                            with connection.cursor() as cursor:
                                sql = "SELECT * FROM account WHERE account_no = %s;"
                                cursor.execute(sql, acc_no)
                                result = cursor.fetchone()
                                acc_name = result.get('name_on_account')
                                acc_bal = result.get('balance')
                                acc_opendate = result.get('account_open_date')
                                print("\n+---   Deposit Successful   ---")
                                print(f"|Account Number: {acc_no}")
                                print(f"|Name on account: {acc_name}")
                                print(f"|Balance: {acc_bal}")
                                print(f"|Account opened on: {acc_opendate}")
                                print('+------------------------------')
                            connection.commit()
                            loop_1 = False
                            break

def withdraw(connection):
    # First checking the account number, whether it's valid or not, then locking it
    loop_1 = True
    while loop_1 == True:
        acc_no_text = input("\nEnter the Account Number you would like to Withdraw from: ")
        if acc_no_text.isnumeric() == False:
            break
        else:
            acc_no = int(acc_no_text)
            with connection.cursor() as cursor:
                sql = "SELECT * FROM account WHERE account_no = %s FOR UPDATE;"
                cursor.execute(sql, acc_no)
                result = cursor.fetchone()
                if result == None:
                    print("\n   Invalid account number. Please try again.")
                    connection.commit()
                else:
                    # if valid account number, display current balance
                    acc_bal = result.get('balance')
                    print("\n+---   Existing Account Balance   ---")
                    print(f"|Account Number: {acc_no}")
                    print(f"|Name on account: {result.get('name_on_account')}")
                    print(f"|Balance: {acc_bal}")
                    print(f"|Account opened on: {result.get('account_open_date')}")
                    print("+------------------------------------\n")
                    connection.commit()
                    # then ask for withdrawal amount
                    while True:
                        amount_text = input("Enter the amount you would like to Withdraw: ")
                        if "-" in amount_text and amount_text.replace("-","").isnumeric() == True:
                            print("\n   Invalid amount. Please try again. \n")
                        elif "." in amount_text and amount_text.replace(".","").isnumeric() == True:
                            print("\n   Sorry, you cannot withdraw increments less than $1. \n")
                        elif amount_text.isnumeric() == False:
                            loop_1 = False
                            break
                        else:
                            amount = int(amount_text)
                            if amount > acc_bal:
                                print("\n   Insufficient funds. Please try again. \n")
                            elif amount <= acc_bal:
                                with connection.cursor() as cursor:
                                    sql = "UPDATE account SET balance = balance - %s WHERE account_no = %s;"
                                    values = (amount, acc_no)
                                    cursor.execute(sql, values)
                                with connection.cursor() as cursor:
                                    sql = "SELECT * FROM account WHERE account_no = %s;"
                                    cursor.execute(sql, acc_no)
                                    result = cursor.fetchone()
                                    acc_name = result.get('name_on_account')
                                    acc_bal = result.get('balance')
                                    acc_opendate = result.get('account_open_date')
                                    print("\n+---   Withdrawal Successful   ---")
                                    print(f"|Account Number: {acc_no}")
                                    print(f"|Name on account: {acc_name}")
                                    print(f"|Balance: {acc_bal}")
                                    print(f"|Account opened on: {acc_opendate}")
                                    print('+---------------------------------')
                                connection.commit()
                                loop_1 = False
                                break

def transfer(connection):
    # Require 3+ while loops here to control when inputs break out and return to menu
    loop_1 = True
    loop_2 = True
    while loop_1 == True:
        acc_no1_text = input("\nEnter the Account Number you would like to Withdraw from: ")
        if acc_no1_text.isnumeric() == False:
            break
        else:
            acc_no1 = int(acc_no1_text)
            with connection.cursor() as cursor:
                sql = "SELECT * FROM account WHERE account_no = %s FOR UPDATE;"
                cursor.execute(sql, acc_no1)
                result1 = cursor.fetchone()
                if result1 == None:
                    print("\n   Invalid account number. Please try again.")
                    connection.commit()
                else:
                    # if valid account number, display current balance
                    acc_bal1 = result1.get('balance')
                    acc_name1 = result1.get('name_on_account')
                    acc_date1 = result1.get('account_open_date')
                    print("\n---Existing Account Balance for Withdrawal---")
                    print(f"Account Number: {acc_no1}")
                    print(f"Name on Account: {acc_name1}")
                    print(f"Balance: {acc_bal1}")
                    print(f"Account opened on: {acc_date1}")
                    print("---------------------------------------------\n")
                    connection.commit()
                    # then ask for withdrawal amount
                    while loop_2 == True:
                        acc_no2_text = input("\nEnter the Account Number you would like to Deposit to: ")
                        if acc_no2_text.isnumeric() == False:        # anything other than a number considered as "any key" return to menu
                            loop_1 = False
                            break
                        else:
                            acc_no2 = int(acc_no2_text)
                            with connection.cursor() as cursor:
                                sql = "SELECT * FROM account WHERE account_no = %s FOR UPDATE;"
                                cursor.execute(sql, acc_no2)
                                result2 = cursor.fetchone()
                                if result2 == None:
                                    print("\n   Invalid account number. Please try again.")
                                    connection.commit()
                                else:
                                    # if valid account number, display current balance
                                    acc_bal2 = result2.get('balance')
                                    acc_name2 = result2.get('name_on_account')
                                    acc_date2 = result2.get('account_open_date')
                                    print("\n---Existing Account Balance for Deposit---")
                                    print(f"Account Number: {acc_no2}")
                                    print(f"Name on Account: {acc_name2}")
                                    print(f"Balance: {acc_bal2}")
                                    print(f"Account opened on: {acc_date2}")
                                    print("------------------------------------------\n")
                                    connection.commit()
                                    # Now ask for transfer amount
                                    while True:
                                        amount_text = input("Enter the amount you would like to Transfer: ")
                                        if "-" in amount_text and amount_text.replace("-","").isnumeric() == True:
                                            print("\n   Invalid amount. Please try again. \n")
                                        elif "." in amount_text and amount_text.replace(".","").isnumeric() == True:
                                            print("\n   Sorry, you cannot withdraw increments less than $1. \n")
                                        elif amount_text.isnumeric() == False:
                                            loop_1 = False
                                            loop_2 = False
                                            break
                                        else:
                                            amount = int(amount_text)
                                            if amount > acc_bal1:
                                                print("\n   Insufficient funds. Please try again. \n")
                                            elif amount <= acc_bal1:
                                                with connection.cursor() as cursor:     # Withdrawing
                                                    sql = "UPDATE account SET balance = balance - %s WHERE account_no = %s;"
                                                    values = (amount, acc_no1)
                                                    cursor.execute(sql, values)
                                                    print("\n   Please wait. Network experiencing high traffic...")
                                                    time.sleep(10)      # simulating network congestion
                                                with connection.cursor() as cursor:     # Depositing
                                                    sql = "UPDATE account SET balance = balance + %s WHERE account_no = %s;"
                                                    values = (amount, acc_no2)
                                                    cursor.execute(sql, values)
                                                    print("\n   Please wait again. Network experiencing high traffic...")
                                                    time.sleep(10)      # simulating more network congestion
                                                with connection.cursor() as cursor:
                                                    sql = "SELECT * FROM account WHERE account_no = %s;"
                                                    cursor.execute(sql, acc_no1)
                                                    result1_new = cursor.fetchone()
                                                    acc_bal1_new = result1_new.get('balance')
                                                with connection.cursor() as cursor:
                                                    sql = "SELECT * FROM account WHERE account_no = %s;"
                                                    cursor.execute(sql, acc_no2)
                                                    result2_new = cursor.fetchone()
                                                    acc_bal2_new = result2_new.get('balance')
                                                    print("\n+------   Transfer Successful   ------+")
                                                    print('|--------------------------------------')
                                                    print("+-----   Withdrawal Account Info   ----")
                                                    print('|--------------------------------------')
                                                    print(f"|Account Number: {acc_no1}")
                                                    print(f"|Name on Account: {acc_name1}")
                                                    print(f"|Account Balance: {acc_bal1_new}")
                                                    print(f"|Account opened on: {acc_date1}")
                                                    print('|--------------------------------------')
                                                    print('+-----   Deposit Account Info   -------')
                                                    print('|--------------------------------------')
                                                    print(f"|Account Number: {acc_no2}")
                                                    print(f"|Name on Account: {acc_name2}")
                                                    print(f"|Account Balance: {acc_bal2_new}")
                                                    print(f"|Account opened on: {acc_date2}")
                                                    print('+--------------------------------------')
                                                connection.commit()
                                                loop_1 = False
                                                loop_2 = False
                                                break

if __name__ == "__main__":
    main()
