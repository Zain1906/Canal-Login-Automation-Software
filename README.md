# Canal+ Login Checker 🛡️

A robust, UI-based login checker for Canal+ accounts built with **Python**, **Selenium (undetected-chromedriver)**, **Tkinter**, and **Pandas**. It reads login credentials from an Excel file, checks their validity by attempting login, and exports valid ones into a separate Excel file. The tool also handles blocked accounts, invalid logins, session restarts, and browser cache clearing—all with minimal user interaction.

---

## ⚙️ Features

- 📂 Load Excel file (`.xlsx`) with `email` and `password` columns
- ✅ Automatically categorizes **Valid**, **Invalid**, and **Blocked** accounts
- 🔐 Uses undetected Chrome driver to bypass bot detection
- 🔁 Auto-restarts Chrome session after 30 attempts
- 🚫 Detects and clears Chrome error modals
- 🧹 Periodic Chrome cache cleanup to prevent memory leaks
- 📊 Progress bar and real-time status updates via GUI
- 💾 Exports valid logins to `valid_logins.xlsx`
- 🧠 Intelligent retry & session management logic
- 🪄 Keeps Chrome open with cached profile for faster performance

---

## 🖼️ GUI Preview

![image](https://github.com/user-attachments/assets/84f444ef-d4d4-47d4-acd8-82f9d5bd77e9)
 <!-- Replace with actual image if needed -->

---

## 📁 Excel Format

Make sure your Excel file has the following columns:

| email              | password    |
|--------------------|-------------|
| user1@example.com  | pass123     |
| user2@example.com  | password456 |

> Rows with empty fields will be ignored automatically.

---
## 📦 Dependencies

This project uses the following libraries:

- `undetected-chromedriver`
- `selenium`
- `pandas`
- `openpyxl`
- `psutil`
- `pyautogui`


## 🧠 How it Works
Uses your existing Chrome profile (Profile 2)

Launches undetectable Chrome browser

Detects login result (valid / invalid / blocked)

Clears sessions & restarts browser intelligently







