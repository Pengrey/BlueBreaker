# BlueBreaker
[![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.6-yellow.svg)](https://www.python.org/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Pengrey/BlueBreaker/blob/main/LICENSE)
<img src="https://img.shields.io/badge/Maintained%3F-Yes-96c40f">

## Purpose
BlueBreaker is a simple tool to exfiltrate data by passing commands to an implant through a Mastadon instance and by later retrieving the results by using the Dropbox API.

## Preview
![image](https://user-images.githubusercontent.com/55480558/212151209-d1c7d6d4-ecb4-4b45-9591-b72e834635d0.png)

## Installation

### Server

The server relies on a Mastadon account, this account needs to be able to post to the public timeline or unlisted toots. To set the configuration file please create a config.toml file in the server directory and fill it with the following information:

```toml
server = "Mastadon instance URL"
auth_token = "Mastadon auth token"
dropbox_token = "Dropbox API token"
```

After that you should download the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Implant

The implant relies on the Dropbox API to upload the results of the commands. To set the configuration file please create a config.toml file in the agent directory and fill it with the following information:

```toml
server = "Mastadon instance URL"
user_id = "Mastadon user ID"
dropbox_token = "Dropbox API token"
```

After that you should download the required dependencies by running:

```bash
pip install -r requirements.txt
```

## Usage

### Server

To start the server you should run the following command:

```bash
./Server/run.py
```

### Implant

To start the implant you should run the following command:

```bash
./Implant/run.py
```

## Demo


## Changelog

* 1.0.0
    * Initial release

## Roadmap
- [x] Improve stability
- [x] Improve network fingerprint
- [x] Improve human like interaction
- [X] Improve server side

## Disclaimer

This tool is for educational purposes only. Running this tool against hosts that you do not have explicit permission to test is illegal. You are responsible for any trouble you may cause by using this tool.
