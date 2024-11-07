<h1 align="center">
  <br>
  Cloudflare DDNS Application
  <br>
</h1>

<h4 align="center">A Dynamic DNS updater service for Cloudflare domains built on Python, CustomTKinter, and PyStray.</h4>

<p align="center">
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/blob/main/README.md"><img alt="GitHub lang" src="https://img.shields.io/badge/lang-en-red.svg"></a>
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/blob/main/README.pt-br.md"><img alt="GitHub lang" src="https://img.shields.io/badge/lang-pt--br-green.svg"></a>
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/commits/main/"><img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/Matozo0/cloudflare-ddns-app"></a>
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/Matozo0/cloudflare-ddns-app?style=for-the-badg"></a>
  <a href="https://github.com/Matozo0/cloudflare-ddns-app/releases"><img alt="GitHub downloads" src="https://img.shields.io/github/downloads/Matozo0/cloudflare-ddns-app/latest/total"></a>
</p>

<p align="center">
  <a href="#features">Features</a> -
  <a href="#how-to-use">How To Use</a> -
  <a href="#download">Download</a> -
  <a href="#setup">Setup</a> -
  <a href="#license">License</a>
</p>

## Features

- **Automated IP Detection**: Automatically detects and updates your public IP address at configurable intervals.
- **Seamless Cloudflare API Integration**: Updates DNS records securely using your Cloudflare account's API.
- **Minimal Configuration**: Simple setup with local configuration for enhanced security and flexibility.
- **Local Security**: Your API keys and domain configurations stay private on your local machine.
- **Cross-Platform Support**: Available as a Windows executable or Python script.
- **Error Handling and Notifications**: Provides logs and optional alerts for successful or failed updates.
- **Manual Update Option**: Instantly trigger updates through the system tray menu.

## How To Use

### Running the Application

1. **Download the Executable**: Navigate to the [Releases](https://github.com/Matozo0/cloudflare-ddns-app/releases) page and download the latest version for Windows.
2. **Run the Executable**: Simply double-click the downloaded executable file to start the application.
3. **Interact with the Tray Icon**:
   - Left-click on the system tray icon to access `Settings`.
   - Right-click on the system tray icon to access options such as `Settings`, `Update now`, and `Exit`.

> **Note**: Linux and MacOS versions will be available soon.

## Manual Python Setup

#### Prerequisites

- **Python 3.11+**
- **Cloudflare Account** with Global API Key access.
- **Dependencies**: Listed in `requirements.txt`

#### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Matozo0/cloudflare-ddns-app.git
   cd cloudflare-ddns-app
   ```

2. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

## Download

For ease of use, you can download the pre-compiled executable from the [Releases](https://github.com/Matozo0/cloudflare-ddns-app/releases/) page.

## License

This project is licensed under the [Apache License 2.0](https://github.com/Matozo0/cloudflare-ddns-app/blob/main/LICENSE) .

---

> GitHub [@Matozo0](https://github.com/Matozo0)
