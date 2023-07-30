from os import makedirs, walk, rename
import shutil
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import END
from TXTHandler import *
from UserWindow import UserWindow
from FollowerBot import FollowerBot


class MainWindow():
    def __init__(self):
        #General setup
        self.accounts_path = "accounts"
        
        #Setup window
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window.title("InstaBot")

        #Font
        font = "Calibri 16 bold"

        #Display accounts
        self.accounts_label = tk.Label(self.window, text="Accounts", font=font)
        self.accounts_label.pack()

        #Buttons for accounts
        self.account_listbox = tk.Listbox(self.window)
        self.account_listbox.pack()

        self.add_account_button = tk.Button(self.window, text="Add Account", command=self.add_account_popup)
        self.add_account_button.place(relx= 0.03, rely=0.75)

        self.remove_account_button = tk.Button(self.window, text="Remove Account", command=self.remove_account)
        self.remove_account_button.place(relx= 0.33, rely=0.75)

        self.edit_account_button = tk.Button(self.window, text="Edit Account", command=self.edit_account_popup)
        self.edit_account_button.place(relx= 0.7, rely=0.75)

        #Feedback labels
        self.confirmed_label = tk.Label(self.window, text="Acc Confirmed", fg="green")
        self.error_label = tk.Label(self.window, text="Incorrect Acc", fg="red")

        #Confirm account button
        self.confirm_account_button = tk.Button(self.window, text="Confirm Acc", command=self.create_thread)
        self.confirm_account_button.place(relx=0.710, rely=0.2)

        #Selection button
        self.select_button = tk.Button(self.window, text="Select Account", command=self.select_account)
        self.select_button.place(relx=0.35, rely=0.9)

        #Show items on list at the start
        self.show_in_list()


    #Show items on list at the start
    def show_in_list(self):
        handler = TxtHandler()
        account_usernames = handler.get_usernames(self.accounts_path)
        for account in account_usernames:
            self.account_listbox.insert(END, account)

    #Account confirmation on demand
    def create_thread(self):
        threading.Thread(target=self.confirm_account).start()

    def confirm_account(self):
        self.confirm_account_button.configure(state="disabled")
        #Showing progress
        progress_bar = ttk.Progressbar(self.window, orient="horizontal", length=100, mode="indeterminate")
        confirming_label = tk.Label(self.window, text="Confirming", fg="blue")

        if len(self.account_listbox.curselection()) != 0:
            progress_bar.place(relx=0.710, rely=0.45)
            confirming_label.place(relx=0.75, rely=0.36)
            self.confirmed_label.place_forget()
            self.error_label.place_forget()
            progress_bar.start()

            #Setup
            follower_bot = FollowerBot()
            txt_handler = TxtHandler()
            lb_index = self.account_listbox.curselection()[0]
            username = txt_handler.get_item(f"{self.accounts_path}/account_{lb_index}/username")
            password = txt_handler.get_item(f"{self.accounts_path}/account_{lb_index}/password")
            
            #Login bot
            if follower_bot.auth(username, password) == False:
                progress_bar.place_forget()
                confirming_label.place_forget()
                self.confirmed_label.place_forget()
                self.error_label.place_forget()
                self.error_label.place(relx=0.73, rely=0.36)
            else:
                progress_bar.place_forget()
                confirming_label.place_forget()
                self.error_label.place_forget()
                self.confirmed_label.place_forget()
                self.confirmed_label.place(relx=0.71, rely=0.36)
        self.confirm_account_button.configure(state="active")

    
    #Popup for adding an account
    def add_account_popup(self):
        #Setup popup window
        popup = tk.Tk()
        popup.geometry("200x200")
        popup.title("Add Account")

        add_username_label = tk.Label(popup, text="Enter Username")
        add_username_label.pack()
        add_username_entry = tk.Entry(popup)
        add_username_entry.pack()

        add_password_label = tk.Label(popup, text="Enter Password")
        add_password_label.pack()
        add_password_entry = tk.Entry(popup)
        add_password_entry.pack()

        error_label = tk.Label(popup, text="This area cannot be empty!", fg="red")
        pass_error_label = tk.Label(popup, text="Password Must Be \n At Least 6 Characters", fg="red")
        add_button = tk.Button(popup, text="Add", command=lambda:self.add_account(add_username_entry.get(),
                                                                                  add_password_entry.get(),
                                                                                  popup,
                                                                                  error_label,
                                                                                  pass_error_label))
        
        add_button.pack()

    
    def add_account(self, un_input, pass_input, popup, error_label, pass_error_label):

        #Check whether the inputs are empty
        if un_input and pass_input != "":
            if len(pass_input) >= 6:
                #Overwrite the username and password
                dir_path = f"{self.accounts_path}/account_{self.account_listbox.size()}"
                makedirs(dir_path, exist_ok=True)

                write_account = TxtHandler()
                write_account.write_item(dir_path + "/username", un_input)

                write_account.write_item(dir_path + "/password", pass_input)

                #Display account username on list
                self.account_listbox.insert(END, un_input)

                #Close the popup window
                popup.destroy()

            elif pass_error_label.winfo_ismapped():
                pass_error_label.pack_forget()
                pass_error_label.pack()
            else:
                pass_error_label.pack()

        elif error_label.winfo_ismapped():
            error_label.pack_forget()
            error_label.pack()
        else:
            error_label.pack()
        
        #Login to account to check whether inputs are correct? Ask Dogukan.
    
    #Remove account
    def remove_account(self):
        lb_index = self.account_listbox.curselection()
        if len(lb_index) != 0:
            dir_path = f"{self.accounts_path}/account_{lb_index[0]}"
            shutil.rmtree(dir_path, False)

            if lb_index != ():
                for _, dirs, __ in walk(self.accounts_path):
                    for index, dir in enumerate(dirs[lb_index[0]:]):
                        rename(f"{self.accounts_path}/{dir}", f"{self.accounts_path}/account_{index}")

                self.account_listbox.delete(lb_index)
    
    def edit_account_popup(self):
        #Edit account
        lb_index = self.account_listbox.curselection()
        if len(lb_index) != 0:
            popup = tk.Tk()
            popup.geometry("200x200")
            popup.title("Edit Account")
            
            edit_username_label = tk.Label(popup, text="Enter Username")
            edit_username_label.pack()
            edit_username_entry = tk.Entry(popup)
            edit_username_entry.pack()

            edit_password_label = tk.Label(popup, text="Enter Password")
            edit_password_label.pack()
            edit_password_entry = tk.Entry(popup)
            edit_password_entry.pack()

            error_label = tk.Label(popup, text="This area cannot be empty", fg="red")
            edit_button = tk.Button(popup, text="Edit",
                                    command=lambda:self.edit_account(use_input=edit_username_entry.get(),
                                                                     pass_input=edit_password_entry.get(),
                                                                     popup=popup,
                                                                     error_label=error_label,
                                                                     lb_index=lb_index))
            edit_button.pack()
    
    def edit_account(self, use_input, pass_input, popup, error_label, lb_index):
        #Display new acount name on list
        if not (use_input == "" and pass_input == ""):
            #Overwrite username and password
            txtHandler = TxtHandler()
            txtHandler.write_item(f"{self.accounts_path}/account_{lb_index[0]}/username", use_input)
            self.account_listbox.delete(lb_index)
            self.account_listbox.insert(lb_index, use_input)

            txtHandler.write_item(f"{self.accounts_path}/account_{lb_index[0]}/password", pass_input)
            popup.destroy()

        elif error_label.winfo_ismapped():
            error_label.place_forget()
        else:
            error_label.pack()
    
    #Selecting an account
    def select_account(self):
        lb_index = self.account_listbox.curselection()
        if len(lb_index) != 0:
            user_window = UserWindow(lb_index[0])
            user_window.run()


    def run(self):
        self.window.mainloop()