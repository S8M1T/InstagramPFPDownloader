import instaloader
import requests
import os
import getpass
from cryptography.fernet import Fernet

def getCredentials():
    if os.path.exists("credentials.key") and os.path.exists("credentials.txt"):
        with open("credentials.key", "rb") as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        with open("credentials.txt", "rb") as encrypted_file:
            encrypted_credentials = encrypted_file.read()
        decrypted_credentials = fernet.decrypt(encrypted_credentials)
        decrypted_credentials = decrypted_credentials.decode("utf-8")
        return decrypted_credentials.splitlines()
    else:
        key = Fernet.generate_key()
        with open("credentials.key", "wb") as key_file:
            key_file.write(key)
        fernet = Fernet(key)
        username_input = input("Enter your username: ")
        password_input = getpass.getpass("Enter your password: ")
        credentials = username_input + "\n" + password_input
        encrypted_credentials = fernet.encrypt(credentials.encode("utf-8"))
        with open("credentials.txt", "wb") as encrypted_file:
            encrypted_file.write(encrypted_credentials)
        return username_input, password_input

def downloadProfilePicture(username, username_input, password_input):
    L = instaloader.Instaloader()
    L.login(username_input, password_input)
    profile = instaloader.Profile.from_username(L.context, username)
    profile_picture_url = profile.profile_pic_url

    response = requests.get(profile_picture_url)
    if response.status_code == 200:
        suffix = 1
        filename = f"{username}.jpg"
        while os.path.exists(filename):
            filename = f"{username}({suffix}).jpg"
            suffix += 1
        with open(filename, "wb") as f:
            f.write(response.content)
            print(f"Profile picture of {username} successfully saved as {filename}!")
    else:
        print(f"Could not download profile picture of {username}. Response status code: {response.status_code}")

username_input, password_input = getCredentials()
username = input("Enter the username of an account whose pfp you want to download: ")
downloadProfilePicture(username, username_input, password_input)
