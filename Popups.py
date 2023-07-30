import tkinter as tk
from tkinter import END
import time
import shutil
import threading
from os import makedirs
from TXTHandler import TxtHandler
from FollowerBot import FollowerBot


class AddUserPopup():
    def __init__(self, list_box, lb_index, account_index):
        #Window setup
        self.window = tk.Tk()
        self.window.geometry("200x200")
        self.window.title("Add User")

        #General setup
        self.user_listbox = list_box
        self.lb_index = lb_index
        self.account_index = account_index
        self.users_path = "users"

        #Widgets
        self.add_user_label = tk.Label(self.window, text="Add User")
        self.add_user_label.pack()

        self.add_user_entry = tk.Entry(self.window)
        self.add_user_entry.pack()

        self.min_followers_label = tk.Label(self.window, text="Enter the Amount of Followers")
        self.min_followers_label.pack()

        self.min_followers_entry = tk.Spinbox(self.window)
        self.min_followers_entry.pack()

        self.error_label = tk.Label(self.window, text="This area cannot be empty!", fg="red")
        self.digit_error_label = tk.Label(self.window, text="This must be a number!", fg="red")
        self.add_button = tk.Button(self.window, text="Add", command=self.add_user)
        self.add_button.pack()
    

    def add_user(self):
        #Check whether the input is empty
        if self.add_user_entry.get() != "" and (self.min_followers_entry.get() != "" and self.min_followers_entry.get().isnumeric()):
            self.add_button.configure(state="disabled")
            #create folder
            txt_handler = TxtHandler()
            dir_path = f"{self.users_path}/user_{self.lb_index}"
            makedirs(dir_path, exist_ok=True)
            txt_handler.write_item(f"{dir_path}/username", self.add_user_entry.get())

            t = threading.Thread(target=self.bot_find, daemon=True)
            t.start()
        
        elif self.add_user_entry.get() == "" or self.min_followers_entry.get() == "":
            if self.error_label.winfo_ismapped():
                self.error_label.pack_forget()
            self.error_label.pack()
        
        elif not self.min_followers_entry.get().isnumeric():
            if self.digit_error_label.winfo_ismapped():
                self.digit_error_label.pack_forget()
            self.digit_error_label.pack()
    

    def bot_find(self):
        time.sleep(3)
        #Get followers of user
        info_label = tk.Label(self.window, text="Getting Followers", fg = "blue")
        feedback_label = tk.Label(self.window, text=f"Got {str(int(self.min_followers_entry.get()))} Followers", fg="green")
        error_label = tk.Label(self.window, text="Unable to View This User's Followers", fg="red")
        follower_error_label = tk.Label(self.window, text="An Unknown Error Occured!", fg="red")
        exceeding_error_label = tk.Label(self.window, text="Follower Amount Too High!", fg="red")

        info_label.pack()
        time.sleep(1)
        follower_bot = FollowerBot()
        txt_handler = TxtHandler()
        account_username = txt_handler.get_item(f"accounts/account_{self.account_index}/username")
        account_password = txt_handler.get_item(f"accounts/account_{self.account_index}/password")

        start_bot = follower_bot.find_followers(account_username,
                                       account_password,
                                       self.add_user_entry.get(),
                                       self.lb_index,
                                       int(self.min_followers_entry.get()))
        
        if  start_bot == "Follower Error":
            
            info_label.pack_forget()
            feedback_label.pack_forget()
            follower_error_label.pack_forget()
            exceeding_error_label.pack_forget()
            error_label.pack()
            dir_path = f"{self.users_path}/user_{self.lb_index}"
            shutil.rmtree(dir_path, False)
        
        elif start_bot == "Exceeding Error":

            info_label.pack_forget()
            feedback_label.pack_forget()
            follower_error_label.pack_forget()
            error_label.pack_forget()
            exceeding_error_label.pack()
            dir_path = f"{self.users_path}/user_{self.lb_index}"
            shutil.rmtree(dir_path, False)

        elif start_bot == "Unknown Error":
            
            info_label.pack_forget()
            feedback_label.pack_forget()
            error_label.pack_forget()
            exceeding_error_label.pack_forget()
            follower_error_label.pack()
            dir_path = f"{self.users_path}/user_{self.lb_index}"
            shutil.rmtree(dir_path, False)

        else:
            self.user_listbox.insert(END, self.add_user_entry.get())
            info_label.pack_forget()
            error_label.pack_forget()
            feedback_label.pack()
        
        self.add_button.configure(state="active")

    
    #Run mainloop
    def run(self):
        self.window.mainloop()

class SendMessagesPopup():
    def __init__(self, user_index, account_index):
        #Window setup
        self.window = tk.Tk()
        self.window.geometry("200x200")
        self.window.title("Send Messages")

        #General setup
        self.user_index = user_index
        self.account_index = account_index

        #Widgets
        self.message_label = tk.Label(self.window, text="Enter Your Message")
        self.message_label.pack()

        self.message_entry = tk.Entry(self.window)
        self.message_entry.pack()

        self.message_count_label = tk.Label(self.window, text="Select Number of Followers to Send")
        self.message_count_label.pack()

        self.message_count_entry = tk.Spinbox(self.window, increment=500)
        self.message_count_entry.pack()

        self.send_button = tk.Button(self.window, text="Send", command=self.send_messages)
        self.send_button.pack()

        self.error_label = tk.Label(self.window, text="This area cannot be empty!", fg="red")
    
    def send_messages(self):
        #Sending message
        if (self.message_entry.get() != "" and
            self.message_count_entry.get().isdigit() and
            self.message_count_entry.get() != "0"):

            self.send_button.configure(state="disabled")
            threading.Thread(target=self.bot_send).start()

        elif self.error_label.winfo_ismapped():
                self.error_label.pack_forget()
                self.error_label.pack()
        else:
            self.error_label.pack()

    def bot_send(self):
        #Sending message logic
        info_label = tk.Label(self.window, text="Sending Messages", fg="blue")
        info_label.pack()
        feedback_label = tk.Label(self.window, text="Messages Sent to Followers", fg="green")
        error_label = tk.Label(self.window, text="An Unknown Error Occured", fg="red")
        not_enough_followers_label = tk.Label(self.window, text="Message Count Too High!", fg="red")

        follower_bot = FollowerBot()
        txt_handler = TxtHandler()
        account_username = txt_handler.get_item(f"accounts/account_{self.account_index}/username")
        account_password = txt_handler.get_item(f"accounts/account_{self.account_index}/password")

        bot_start = follower_bot.send_messages(account_username,
                                      account_password,
                                      self.user_index,
                                      self.message_count_entry.get(),
                                      self.message_entry.get())
        
        if  bot_start == "Not Enough Error":
            info_label.pack_forget()
            feedback_label.pack_forget()
            error_label.pack_forget()
            not_enough_followers_label.pack()
        
        elif bot_start == "Unknown Error":    
            info_label.pack_forget()
            feedback_label.pack_forget()
            not_enough_followers_label.pack_forget()
            error_label.pack()

        else:
            info_label.pack_forget()
            error_label.pack_forget()
            not_enough_followers_label.pack_forget()
            feedback_label.pack()
    
    #Run mainloop
    def run(self):
        self.window.mainloop()