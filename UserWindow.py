import tkinter as tk
from tkinter import END
import shutil
from os import walk, rename
from TXTHandler import TxtHandler
from Popups import AddUserPopup, SendMessagesPopup


class UserWindow():
    def __init__(self, account_index):
        #General setup
        self.users_path = "users"
        self.account_index = account_index

        #Setup window
        self.window = tk.Tk()
        self.window.geometry("300x300")
        self.window.title("Users")

        #Font
        font = "Calibri 16 bold"

        #Display accounts
        self.users_label = tk.Label(self.window, text="User", font=font)
        self.users_label.pack()

        #Buttons for users
        self.user_listbox = tk.Listbox(self.window)
        self.user_listbox.pack()

        self.add_user_button = tk.Button(self.window, text="Add User", command=self.add_user_popup)
        self.add_user_button.place(relx= 0.14, rely=0.72)

        self.remove_user_button = tk.Button(self.window, text="Remove User", command=self.remove_user)
        self.remove_user_button.place(relx= 0.37, rely=0.72)

        self.edit_user_button = tk.Button(self.window, text="Edit User", command=self.edit_user_popup)
        self.edit_user_button.place(relx= 0.67, rely=0.72)

        #Selection button
        self.select_button = tk.Button(self.window, text="Run Bot", command=self.message_popup)
        self.select_button.place(relx=0.40, rely=0.82)

    
    #Show users in display
    def show_in_list(self):
        handler = TxtHandler()
        account_usernames = handler.get_usernames(self.users_path)
        for account in account_usernames:
            self.user_listbox.insert(END, account)

    #Popup for adding an user
    def add_user_popup(self):
        add_user_popup = AddUserPopup(self.user_listbox, self.user_listbox.size(), self.account_index)
        add_user_popup.run()
    
    #Remove user
    def remove_user(self):
        lb_index = self.user_listbox.curselection()
        if lb_index != ():
            #Rearrange folders
            dir_path = f"{self.users_path}/user_{lb_index[0]}"
            shutil.rmtree(dir_path)
            for _, dirs, __ in walk(self.users_path):
                for index, dir in enumerate(dirs[lb_index[0]:]):
                    rename(f"{self.users_path}/{dir}", f"{self.users_path}/user_{index}")

            #Remove in display
            self.user_listbox.delete(lb_index)
    
    def edit_user_popup(self):
        #Remove user
        lb_index = self.user_listbox.curselection()
        if len(lb_index) != 0:
            popup = tk.Tk()
            popup.geometry("200x200")
            popup.title("Edit User")
            
            edit_account_label = tk.Label(popup, text="Edit User")
            edit_account_label.pack()
            edit_account_entry = tk.Entry(popup)
            edit_account_entry.pack()

            error_label = tk.Label(popup, text="This area cannot be empty", fg="red")
            edit_button = tk.Button(popup, text="Edit",
                                    command=lambda:self.edit_user(edit_account_entry.get(), popup, error_label, lb_index))
            edit_button.pack()
    
    def edit_user(self, input, popup, error_label, lb_index):
        #Check whether the input is empty
        if input != "":
            #Overwrite username
            txt_handler = TxtHandler()
            txt_handler.write_item(f"{self.users_path}/user_{lb_index[0]}/username", input)
            #Display new user name on list
            self.user_listbox.delete(lb_index)
            self.user_listbox.insert(lb_index, input)
            popup.destroy()
        elif error_label.winfo_ismapped():
            error_label.place_forget()
        else:
            error_label.pack()
    
    def message_popup(self):
        if len(self.user_listbox.curselection()) != 0:
            send_message_popup = SendMessagesPopup(self.user_listbox.curselection()[0], self.account_index)
            send_message_popup.run()

    def run(self):
        self.show_in_list()
        self.window.mainloop()