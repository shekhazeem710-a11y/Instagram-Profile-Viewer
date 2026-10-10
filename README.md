# Instagram Public Profile Tool

A Python GUI application for viewing publicly available Instagram profile information.

## Features

- Search public profiles by username
- View username and full name
- View public biography and profile URL
- View follower, following, and post counts when available
- View public account, verified, and business status
- View external website link
- Search history during the current session
- Export results to TXT and CSV
- Copy profile information
- Dark-themed graphical interface
- Supports Windows and Kali Linux

## Requirements

- Python 3
- Tkinter
- Instaloader

## Installation — Kali Linux

Install the required packages:

```bash
sudo apt update
sudo apt install python3 python3-tk python3-venv -y
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python3 instagram_tool.py
```

## Installation — Windows

Install Python 3 and enable **Add Python to PATH** during installation.

Open Command Prompt in the project directory and run:

```powershell
python -m pip install -r requirements.txt
python instagram_tool.py
```

## Usage

1. Start the application.
2. Enter a public Instagram username without the `@` symbol.
3. Click **Search**.
4. Review any information that Instagram makes available.
5. Export results to TXT or CSV if required.

## Limitations

- Instagram may restrict automated requests or require authentication.
- Public profile information is not guaranteed to be available.
- Private account content is not accessed.
- The application does not retrieve hidden contact details, passwords, session cookies, or live device location.
- Search history is kept in memory and is cleared when the application closes.

## Privacy and Responsible Use

Use this tool only for lawful purposes and respect people's privacy. Follow Instagram's terms and applicable rules.

## License

MIT License