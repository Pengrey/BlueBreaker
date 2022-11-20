import toml
import base64
import requests

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


# main function
def main():
    get_url_and_auth_token()

    # Get command from user
    command = input("Enter command: ")

    # Post a toot with the command
    post_toot(command)



if __name__ == "__main__":
    main()