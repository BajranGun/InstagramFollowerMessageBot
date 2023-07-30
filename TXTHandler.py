from os import walk

class TxtHandler():
    def __init__(self):
        self.accounts_path = "accounts"
        self.users_path = "users"

    # Get usernames from directory
    def get_usernames(self, usernames):
        userlist = []
        for _, dirs, __ in walk(usernames):
            for dir in dirs:
                with open(usernames + "/" + dir + "/username.txt", "r") as f:
                    user = f.read()
                    userlist.append(user)
                f.close()
        return userlist

    #Get username or password of an account from directory
    def get_item(self, path):
        with open(path + ".txt", "r") as f:
            item = f.read()
        return item

    #Overwrite the username or password of an account
    def write_item(self, path, item):
        with open(path + ".txt", "w") as f:
            f.write(item)
        f.close()
    
    #Overwrite to all existing followers of a user
    def write_all_followers(self, list_of_links, user_index):
        path = f"{self.users_path}/user_{str(user_index)}/followers"
        with open(path + '.txt', 'w') as f:
            for follower in list_of_links:
                follower = follower.split("https://www.instagram.com/")[1]
                follower = follower.split("/")[0]
                f.write(follower + "\n")
            f.close()
    
    #Overwrite to current followers of a user
    def write_current_followers(self, list_of_users, user_index):
        path = f"{self.users_path}/user_{str(user_index)}/current_followers"
        with open(path + '.txt', 'w') as f:
            for follower in list_of_users:
                f.write(follower + "\n")
            f.close()

    #Get all followers of a user
    def get_all_followers(self, user_index):
        path = f"{self.users_path}/user_{str(user_index)}/followers.txt"
        with open(path, "r") as f:
            followers = f.read().split("\n")
        f.close()
        return followers
    
    #Get current followers of a user
    def get_current_followers(self, user_index):
        path = path = f"{self.users_path}/user_{str(user_index)}/current_followers.txt"
        with open(path, "r") as f:
            followers = f.read().split("\n")
        f.close()
        return followers