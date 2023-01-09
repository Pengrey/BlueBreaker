# BlueBreaker
[![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.6-yellow.svg)](https://www.python.org/) 
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Pengrey/BlueBreaker/blob/main/LICENSE.md)
<img src="https://img.shields.io/badge/Maintained%3F-Yes-96c40f">

## Purpose
BlueBreaker is a simple tool to exfiltrate data by passing commands through a Mastadon instance and by later retrieving the results by using the Dropbox API.

## Installation

### Server

The server relies on a Mastadon account, this account needs to be able to post to the public timeline or unlisted toots. To set the configuration file please create a config.toml file in the server firectory and fill it with the following information:

```toml
url = "Mastadon instance URL"
auth_token = "Mastadon auth token"
```

After that you should download the required dependencies by running:

```bash
pip install -r requirements.txt
```

### Agent

The agent relies on the Dropbox API to upload the results of the commands. To set the configuration file please create a config.toml file in the agent firectory and fill it with the following information:

```toml
url = "Mastadon instance URL"
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
python3 server.py
```

### Agent

To start the agent you should run the following command:

```bash
python3 agent.py
```

## Demo

https://user-images.githubusercontent.com/55480558/202913781-afd98595-7d50-43d5-a714-6440d2c60045.mp4

## Changelog

* beta
    * Still in development

## Roadmap
- [x] Improve stability
- [x] Improve network fingerprint
- [x] Improve human like interaction
- [ ] Improve server side
- [ ] Add multi agents functionality
- [ ] Add encrypted communication

## Disclaimer

This tool is for educational purposes only. I am not responsible for any damage caused by this tool.

## License

[MIT](https://github.com/Pengrey/BlueBreaker/blob/main/LICENSE)


