import tkinter as tk
from tkinter import ttk
import json


class FinanceTrackerGUI:
    def __init__(self, root):
        self.root = root#root window making
        self.root.title("Personal Finance Tracker")
        self.create_widgets()
        self.transactions = self.load_transactions("transactions.json")#Loading transactions from JSON
        self.error_label = ttk.Label(self.root)#Creating label
        self.error_label.pack()#packing

    def display_error_message(self, message):
        self.error_label.config(text=message)  #updating error label  

    def create_widgets(self):
        # Frame for table and scrollbar
        self.tab_frame = ttk.Frame(self.root)  
        self.tab_frame.pack(fill=tk.BOTH, expand=True)#packing frame into window

        # Treeview for displaying transactions
        self.transaction_tree = ttk.Treeview(self.tab_frame, columns=("Type", "Category", "Amount", "Date"), show="headings")
        self.transaction_tree.heading("Type", text="Type", command=lambda: self.sort_by_column(self.transaction_tree, "Type", False))
        self.transaction_tree.heading("Category", text="Category", command=lambda: self.sort_by_column(self.transaction_tree, "Category", False))  
        self.transaction_tree.heading("Amount", text="Amount", command=lambda: self.sort_by_column_extra(self.transaction_tree, "Amount", False))  
        self.transaction_tree.heading("Date", text="Date", command=lambda: self.sort_by_column(self.transaction_tree, "Date", False))  
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)#packing Treeview into frame

        # Scrollbar for the Treeview
        tree_scrollbar = ttk.Scrollbar(self.tab_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)#packing scrollbar into frame
        self.transaction_tree.config(yscrollcommand=tree_scrollbar.set)

        # Search bar and button for type
        self.type_label = ttk.Label(self.root, text="Type:")#creating a label for type search Bar
        self.type_label.pack()#packing type label into root window
        self.type_entry = ttk.Entry(self.root)#create entry widget for type search
        self.type_entry.pack()#packing type entry widget into root window
        self.type_button = ttk.Button(self.root, text="Search", command=self.search_by_type)#creating a search button for type
        self.type_button.pack()#packing type search button into root window

        # Search bar and button for category
        self.category_label = ttk.Label(self.root, text="Category:")#creating a label for category search Bar
        self.category_label.pack()#packing category label into root window
        self.category_entry = ttk.Entry(self.root) #create entry widget for category search 
        self.category_entry.pack()#packing category entry widget into root window
        self.category_button = ttk.Button(self.root, text="Search", command=self.search_by_category)#creating a search button for category
        self.category_button.pack()#packing category search button into root window

        # Search bar and button for amount
        self.amount_label = ttk.Label(self.root, text="Amount:")#creating a label for amount search Bar  
        self.amount_label.pack()#packing amount label into root window
        self.amount_entry = ttk.Entry(self.root) #create entry widget for amount search  
        self.amount_entry.pack()#packing amount entry widget into root window
        self.amount_button = ttk.Button(self.root, text="Search", command=self.search_by_amount)#creating a search button for category
        self.amount_button.pack()#packing amount search button into root window

        # Search bar and button for date
        self.date_label = ttk.Label(self.root, text="Date:")#creating a label for date search Bar  
        self.date_label.pack()#packing date label into root window
        self.date_entry = ttk.Entry(self.root)#create entry widget for date search   
        self.date_entry.pack()#packing date entry widget into root window
        self.date_button = ttk.Button(self.root, text="Search", command=self.search_by_date)#creating a search button for date
        self.date_button.pack()#packing date search button into root window

    def load_transactions(self, file_name):#Loading Transactions from JSON file
        try:
            with open(file_name, "r") as file: 
                return json.load(file)
        except FileNotFoundError:
            self.display_error_message(f"{file_name} - File not found")
            return {}

    def display_transactions(self, transactions):
          for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)#Deleting existing items in the treeview
    
          for transaction in transactions:
            self.transaction_tree.insert("", "end", values=( transaction["Type"], transaction["Category"], transaction["Amount"], transaction["Date"]  ))#Inserting transactions
          

    def sort_by_column(self, tree, col, reverse):
         data = [(tree.set(child, col), child) for child in tree.get_children('')] #Getting data from treeview
         data.sort(reverse=reverse)#Sorting
         for index, (val, child) in enumerate(data):
             tree.move(child, '', index)#Moving
         tree.heading(col, command=lambda: self.sort_by_column(tree, col, not reverse))#Setting command

    def sort_by_column_extra(self, tree, col, reverse):#To fix amount sorting error (Convert value to float before sorting)
      data = [(float(tree.set(child, col)), child) for child in tree.get_children('')]
      data.sort(reverse=reverse)
      for index, (val, child) in enumerate(data):
          tree.move(child, '', index)
      tree.heading(col, command=lambda: self.sort_by_column_extra(tree, col, not reverse))


    def search_by_type(self):
        type_query = self.type_entry.get().lower()#Getting type search query
        if not type_query:
            self.display_transactions(self.transactions)#Displaying all transactions if no query
            return

        filtered_transactions = [transaction for transaction in self.transactions if type_query in transaction["Type"].lower()]#Filtering transactions by type
        self.display_transactions(filtered_transactions)#Displaying filtered transactions

    
    def search_by_category(self):
       category_query = self.category_entry.get().lower()#Getting category search query
       if not category_query:
           self.display_transactions(self.transactions)#Displaying all transactions if no query
           return

       filtered_transactions = [transaction for transaction in self.transactions if category_query in transaction["Category"].lower()]#Filtering transactions by category
       self.display_transactions(filtered_transactions)#Displaying filtered transactions

    def search_by_amount(self):
        amount_query = self.amount_entry.get()#Getting amount search query
        if not amount_query:
            self.display_transactions(self.transactions)#Displaying all transactions if no query
            return
        try:
             amount_query = float(amount_query)
        except ValueError:
            self.display_error_message("Entered Amount is Invalid")
            return

        filtered_transactions = [transaction for transaction in self.transactions if float(transaction["Amount"]) == amount_query]#Filtering transactions by amount
        self.display_transactions(filtered_transactions)#Displaying filtered transactions
     
    def search_by_date(self):
        date_query = self.date_entry.get()#Getting date search query
        if not date_query:
            self.display_transactions(self.transactions)#Displaying alltransactions if no query
            return

        filtered_transactions = [transaction for transaction in self.transactions if transaction["Date"] == date_query]#Filtering transactions by date
        self.display_transactions(filtered_transactions)#Displaying filtered transactions
        

def main():
    root = tk.Tk()#Creating root window
    app = FinanceTrackerGUI(root)#Creating instance of FinanceTrackerGUIA class
    app.display_transactions(app.transactions)#Displaying transactions in GUI
    root.mainloop()#Running mainloop

if __name__ == "__main__":
    main()
