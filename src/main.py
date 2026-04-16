#!/usr/bin/env python3

"""
   Title: /pfsense-backup/src/main.py
   Description: Start of the program, runs the backup process with out a GUI
   Author: Joseph Harry
   Copyright (C): Joseph Harry 2026
   Date: 2026-04-16 10:39:39

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


import time
import os
import json

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import WebDriverException
except ImportError as e:
    os.error(f'❌  Selenium not installed: {e}')

def get_settings():
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, 'settings.json')) as f:
            settings = json.load(f)
            # print(f'✅  Loaded settings: {settings}')
        return settings
    except Exception:
        return None
    except Exception:
        return '', ''

def get_credentials():

    try:
        path = os.path.dirname(__file__)
        with open(os.path.join(path, 'credentials.json')) as f:
            creds = json.load(f)

    except:
        return "", ""

    return creds


def set_chrome_options(chrome_options,settings):

    # Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) 96.0.4664.113 Safari/537.36

    chrome_options.add_argument("user-agent=Mozilla/5.0 (X11; Fedora; Linux x86_64)"
                                + "AppleWebKit/537.36 (KHTML, like Gecko)"
                                + "96.0.4664.113 Safari/537.36")

    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")

    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    if settings['incognito']:
        chrome_options.add_argument("--incognito")

    if settings['mute_audio']:
        chrome_options.add_argument("--mute-audio")

    if settings['maximize_window']:
        chrome_options.add_argument("start-maximized")

    if settings['headless']:
        chrome_options.add_argument("--headless")

def login(settings):
    global DRIVER

    chrome_options = Options()
    
    path = os.path.dirname(os.path.abspath(__file__))
    print(f'🔧  Setting download directory to: {path}/{settings["download_directory"]}')

    chrome_options.add_argument("download.default_directory="+path+"/"+settings['download_directory'])
    set_chrome_options(chrome_options, settings)

    try:
        service = ChromeService(executable_path=settings['chromedriver_path'])
        DRIVER = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f'❌  Could not start Chrome: {e}')
        return

    DRIVER.get(settings['url'])

    DRIVER.implicitly_wait(15)

    try:
        have_account = WebDriverWait(DRIVER, 10).until(
            EC.presence_of_element_located(
                (By.ID, 'usernamefld'))
        )
        login_to_pfsense()

    except WebDriverException as e:
        exit(e)

def login_to_pfsense():
    global DRIVER

    creds = get_credentials()
    if creds['username'] == "" or creds['password'] == "":
        os.error('❌  Could not load credentials.json')

    print('🔐  Logging into pfSense...')
    username_input = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.ID, 'usernamefld'))
    )
    username_input.send_keys(creds['username'])
    
    password_input = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.ID, 'passwordfld'))
    )
    password_input.send_keys(creds['password'])

    submit_button = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'btn-success'))
    )
    print('✅  Login form filled, submitting...')

    submit_button.click()


def backup_config():
    print('💾  Starting backup process...')

    global DRIVER
    extra_data = WebDriverWait(DRIVER, 10).until(
        EC.presence_of_element_located((By.ID, 'backupdata'))
    )
    extra_data.click()
    
    # sleep for a bit to let the page load, otherwise the submit button may not be clickable yet
    time.sleep(.5)

    submit_button = WebDriverWait(DRIVER, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    submit_button.click()




def main():

    global DRIVER
    
    # --- settings ---
    settings = get_settings()
    if settings is None:
        os.error('❌  Could not load settings.json')

    login(settings)
    backup_config()

    DRIVER.close()
    DRIVER.quit()

if __name__ == '__main__':
    main()