import json

# Global list to store transactions
transactions = []

# File handling functions
def load_transactions():#Load transactions from the JSON file.
    global transactions
    try:
        with open("transactions.json", "r") as file:
            transactions = json.load(file)
    except FileNotFoundError:
        print("File not found")
        transactions = []
   
def save_transactions():#Save transactions to the JSON file
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)

# Feature implementations
def add_transaction():#Add a new transaction
    try:#Getting inputs 
        amount = float(input("Enter the Transaction amount: "))#Adding Transaction amount
        category = input("Enter the Transaction category: ") #Adding Transaction category
        tran_type = input("Enter the Transaction type - income or expense: ")#Adding Transaction type
        date = input("Enter the Transaction date (YYYY-MM-DD): ")#Adding Transaction date
        new_transaction = {"Amount": amount, "Category": category, "Type": tran_type, "Date": date}
        transactions.append(new_transaction)#Adding new transaction
        save_transactions()#Saving the Transaction
        print("Transaction added successfully.")
    except ValueError:#To stop the code crashing, with error
        print("Invalid input. Please enter the correct input.")

def view_transactions():#View  transactions.
    if transactions:
        i = 1
        for transaction in transactions:
            print(f"{i} Amount={transaction['Amount']} Category={transaction['Category']} Type={transaction['Type']} Date={transaction['Date']}")
            i += 1
    else:
        print("No Transactions")

def update_transaction():#Update  transactions
    view_transactions()
    try:
        while True:#Getting inputs to update the transaction
            update = int(input("Enter the number of the transaction that you want to update: ")) - 1 #Getting Transaction number user wants to update
            if 0 <= update < len(transactions):
                amount = float(input("Enter the new transaction amount: "))#Adding New Transaction amount
                category = input("Enter the new category: ")#Adding New Transaction category
                tran_type = input("Enter the new transaction type: ")#Adding New Transaction type
                date = input("Enter the transaction date (YYYY-MM-DD): ")#Adding New Transaction date
                transactions[update] = {"Amount": amount, "Category": category, "Type": tran_type, "Date": date}#Updated Transaction
                save_transactions()#Saving New transaction
                print("Transaction updated successfully.")
                break
            else:
                print("Given input is incorrect.")
    except ValueError:#To stop the code crashing, with error
        print("Invalid input. Please enter numeric values where required.")

def delete_transaction():#Delete a transaction
    view_transactions()
    try:
        trans_del = int(input("Enter the transaction number that you want to delete: ")) - 1 #Getting Transaction number user wants to delete
        if 0 <= trans_del < len(transactions):
            del transactions[trans_del]
            save_transactions()
        else:
            print("Invalid transaction number.")
    except ValueError:#To stop the code crashing, with error
        print("Incorrect number. Please recheck it.")

def display_summary():#Display the summary of transactions
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        if transaction['Type'] == "income":
            total_income += transaction['Amount']
        elif transaction['Type'] == "expense":
            total_expense += transaction['Amount']

    net_income = total_income - total_expense#Calculating net income

    print(f"Summary of Transactions - Total Income: {total_income} Total Expense: {total_expense} Net Income: {net_income}")

def main_menu():
    load_transactions()  # Load transactions at the start
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Display Summary")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            update_transaction()
        elif choice == '4':
            delete_transaction()
        elif choice == '5':
            display_summary()
        elif choice == '6':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
