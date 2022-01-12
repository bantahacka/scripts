# AES128 ECB Strongarm Token Cracker (Used for a CTF)
import requests
import time
from sys import exit

global complete_chars
complete_chars = []
global failed_chars
failed_chars = []
global complete_secret
complete_secret = []
global char_found
char_found = False
global username
username = ''
global target_cipher
target_cipher = ''
global new_len
new_len = 15

url = '**** Enter url here ****'
password = '1'

def get_target(size):

    global char_found
    global target_cipher
    global new_len
    if len(complete_chars) == 0:
        username = "!" * (size - 1)
    else:
        username = "!" * (new_len - len(complete_chars))
    print("Reference Username Length: " + str(len(username)))
    print("Reference Username: " + username)
    obj = {'username':username, 'password':password}
    x = requests.post(url, obj)
    target_cipher = x.cookies['*enter token field here*']
    print("Target cipher generated: " + target_cipher)

def generate_username():
    global char_found
    global complete_chars
    global failed_chars
    global username
    global new_len
    if char_found == True:
        failed_chars = []
        get_target(16)
        if len(complete_chars) == 0:
            username = "!" * 16
        else:
            username = "!" * (new_len - len(complete_chars))
        username = list(username)
        for i in range(len(complete_chars)):
            username.append(complete_chars[i])
        username.append("!")
        username = ''.join(username)
        print("New username: "+username)
        char_found = False
    else:
        if len(complete_chars) > 0:
            username = "!" * (new_len - len(complete_chars))
        else:
            username = "!" * (new_len - len(complete_chars))
            if len(failed_chars) == 0 and len(complete_chars) == 0:
                username+= "!"
        if len(failed_chars) > 0:
            username = list(username)
            lastchar = failed_chars.pop()
            lastchar2 = lastchar
            lastchar = ord(lastchar)
            lastchar = lastchar+1
            if lastchar > 126:
                print("Unable to find any matches. Exiting...")
                return False
            lastchar = chr(lastchar)
            failed_chars.append(lastchar2)
            add_comp = ''.join(complete_chars)
            for c in add_comp:
                username.append(c)
            username.append(lastchar)
            username = ''.join(username)
    return username

def send_requests():
    global char_found
    global complete_chars
    global complete_secret
    global failed_chars
    global target_cipher
    while True:
        username = generate_username()
        print("Trying: " + username)
        url = '**** enter url here ****'
        password = '1'
        obj = {'username':username, 'password':password}
        x = requests.post(url, obj)
        cookie = x.cookies['*enter token field here*']
        if not cookie:
            print("No cookie returned. Reason: " + x.text)
        print(cookie[0:32])
        print(target_cipher[0:32])
        complen = len(complete_chars)
        if cookie[0:32] == target_cipher[0:32]:
            print("Match found: " + username)
            if complen == 0:
                complete_chars.append(username[-1])
                complete_secret.append(username[-1])
            else:
                complete_chars.append(username[-1])
                complete_secret.append(username[-1])
            if len(complete_chars) == 16 and len(complete_secret) == 16:
                print("Secret found: " + (''.join(complete_secret)))
                break
            char_found = True
            continue
        else:
            print("Match not found.")
            failed_chars.append(username[-1])
            char_found = False
            continue
def main():
    get_target(16)
    send_requests()


if __name__ == "__main__":
    main()

