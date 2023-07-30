from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random
from TXTHandler import TxtHandler

class FollowerBot():
    def __init__(self):
        
        #General setup for browser
        self.options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless=new")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument("--allow-running-insecure-content")
        self.options.add_argument("--disable-notifications")
        self.options.add_experimental_option("detach", True)

        self.service = Service(executable_path="chromedriver.exe")
        self.browser = webdriver.Chrome(service=self.service, options=self.options)

        self.wait = WebDriverWait(self.browser, 20)

    #Authentification function to be used for confirming an account
    def auth(self, account_username, account_password):
        try:
            self.browser.get("https://www.instagram.com/accounts/login/")

            time.sleep(random.randrange(2, 4))
            username_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="loginForm"]/div/div[1]/div/label/input""")))
            username_input.send_keys(account_username)

            time.sleep(random.randrange(2, 4))
            password_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="loginForm"]/div/div[2]/div/label/input""")))
            password_input.send_keys(account_password)

            time.sleep(random.randrange(2, 4))
            password_input.send_keys(Keys.ENTER)

            time.sleep(random.randrange(2, 4))
            error_alert = self.browser.find_elements(By.ID, "slfErrorAlert")
            errorPresent = error_alert.__len__() > 0
            time.sleep(random.randrange(2, 4))
            if errorPresent:
                self.browser.close()
                return False

        except:
            self.browser.close()
    
    def find_followers(self, account_username, account_password, username, user_index, max):
        try:
            #Login
            self.browser.get("https://www.instagram.com/accounts/login/")

            time.sleep(random.randrange(2, 4))
            username_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="loginForm"]/div/div[1]/div/label/input""")))
            username_input.send_keys(account_username)

            time.sleep(random.randrange(2, 4))
            password_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="loginForm"]/div/div[2]/div/label/input""")))
            password_input.send_keys(account_password)

            time.sleep(random.randrange(2, 4))
            password_input.send_keys(Keys.ENTER)

            #Find user page
            time.sleep(random.randrange(5,7))
            self.browser.get(f"https://www.instagram.com/{username}")
            time.sleep(2)
            followers_check = self.browser.find_elements(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a")
            time.sleep(1)
            if len(followers_check) == 0:
                #Returns error if followers button is unclickable
                follower_error = "Follower Error"
                self.browser.close()
                return follower_error
            
            else:
                max_followers = int(self.browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a/span").get_attribute("title"))
                if max_followers < max:
                    exceeding_follower_count_error = "Exceeding Error"
                    self.browser.close()
                    return exceeding_follower_count_error
                
                time.sleep(1)
                followers_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a")))
                followers_button.click()
                time.sleep(2)

                #Scrolling down the followers popup constantly
                pop_up_window = WebDriverWait(
                self.browser, 2).until(EC.element_to_be_clickable(
                    (By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")))
                
                followers_xpath = self.wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div")))
                count = 0

                while count < max:
                    self.browser.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight", 
                    pop_up_window)
                    followers = followers_xpath.find_elements(By.CLASS_NAME, "x1dm5mii")
                    count = len(followers)
                    time.sleep(2)
                
                #Getting followers and writing them into os
                time.sleep(5)
                list_of_links = []
                extra_followers = len(followers) - max
                followers = followers[:len(followers) - extra_followers]
                
                for follower in followers:
                    link = follower.find_element(By.TAG_NAME, "a").get_attribute("href")
                    list_of_links.append(link)
                    
                txt_handler = TxtHandler()
                txt_handler.write_all_followers(list_of_links, user_index)
                time.sleep(2)

                all_followers = txt_handler.get_all_followers(user_index)
                #Delete account username from usernames so that it will not try to message itself
                if account_username in all_followers:
                    all_followers.remove(account_username)

                txt_handler.write_current_followers(all_followers, user_index)
                time.sleep(2)
                self.browser.close()
        except Exception as err:
            try:
                print(err)
                unknown_error = "Unknown Error"
                self.browser.close()
                return unknown_error
            except:
                return unknown_error
    
    def send_messages(self, account_username, account_password, user_index, count_to_send, message_to_send):
        #Getting current followers
        txt_handler = TxtHandler()
        all_followers = txt_handler.get_current_followers(user_index)
        if len(all_followers) < int(count_to_send):
            #If current followers is not enough, overwrite current followers
            all_followers = txt_handler.get_all_followers(user_index)
            #Delete account username from usernames so that it wont try to message itself
            if account_username in all_followers:
                all_followers.remove(account_username)

            if len(all_followers) < int(count_to_send):
                not_enough_followers_error = "Not Enough Error"
                self.browser.close()
                return not_enough_followers_error
            
            txt_handler.write_current_followers(all_followers, user_index)

        followers_to_send = []

        #Choose random followers
        for i in range(int(count_to_send)):
            item = random.choice(all_followers)
            followers_to_send.append(item)

            all_followers.remove(item)
        
        #Delete followers whom messages are sent
        txt_handler.write_current_followers(all_followers, user_index)
        
        try:
            #Login
            self.browser.get("https://www.instagram.com/accounts/login/")

            time.sleep(4)
            username_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="loginForm"]/div/div[1]/div/label/input""")))
            username_input.send_keys(account_username)

            time.sleep(4)
            password_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, """//*[@id="loginForm"]/div/div[2]/div/label/input""")))
            password_input.send_keys(account_password)

            time.sleep(4)
            password_input.send_keys(Keys.ENTER)

            not_now_button_element = self.browser.find_elements(By.XPATH, """/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]""")
            if len(not_now_button_element) > 0 and (not_now_button_element[0].is_displayed and not_now_button_element[0].is_enabled):
                not_now_button_element[0] = self.wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]""")))
                not_now_button_element[0].click()
                time.sleep(4)

            direct_message_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[5]/div/div/div/span/div/a/div""")))
            direct_message_button.click()
            time.sleep(4)

            if len(not_now_button_element) > 0 and (not_now_button_element[0].is_displayed and not_now_button_element[0].is_enabled):
                not_now_button_element[0] = self.wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]""")))
                not_now_button_element[0].click()
                self.browser.implicitly_wait(6)
            
            #Sending messages
            for i in range(int(count_to_send)):
                find_users_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div/div""")))
                find_users_button.click()
                time.sleep(4)
                find_users_text_area = self.wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/input""")))
                find_users_text_area.clear()
                find_users_text_area.send_keys(followers_to_send[i])
                time.sleep(4)
                user_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div""")))
                user_button.click()
                time.sleep(4)
                chat_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[4]/div""")))
                chat_button.click()
                time.sleep(4)
                send_message_text_area = self.wait.until(EC.element_to_be_clickable((By.XPATH, """/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[1]/p""")))
                send_message_text_area.send_keys(message_to_send)
                send_message_text_area.send_keys(Keys.ENTER)
                time.sleep(4)
            
            self.browser.close()

        except:
            try:
                unknown_error = "Unknown Error"
                self.browser.close()
                return unknown_error
            except:
                return unknown_error
