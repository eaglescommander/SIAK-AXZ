from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

auth_page = "https://academic.ui.ac.id/main/Authentication/"
home_page = "https://academic.ui.ac.id/main/Welcome/Index"
siak_page = "file:///C:/Users/Eagles/Desktop/Side%20Projects/SIAK-AXZ/examples/page-example.html"

def war():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome('chromedriver.exe', options=options)

    # use line below if you want more refresh in shorter time, might impact login time
    # maybe useful when your faculty goes to war on the same time as other faculty
    # driver.set_page_load_timeout(5)

    username = ""
    password = ""
    display_name = ""
    common_matkul = ""
    chosen_matkul = ""

    with open("credentials.txt", "r") as file:
        creds = []
        for line in file:
            creds.append(line.strip())

        username = creds[0]
        password = creds[1]
        display_name = creds[2]
        common_matkul = creds[3]
        chosen_matkul = creds[4]
    
    print("Credentials loaded!")
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Display name: {display_name}")
    print(f"Common matkul: {common_matkul}")
    print(f"Chosen matkul: {chosen_matkul}")

    matkul={}
    with open("matkul.txt", "r") as file:
        for line in file:
            (code, name) = line.split()
            matkul[name] = code

    print("Matkul loaded!")
    print("Chosen matkul:")
    for name, code in matkul.items():
        print(f"{name} {code}")

    login(driver, username, password, display_name)
    
    while True:
        try:
            driver.get(siak_page)
            time.sleep(0.5)

            if ("Anda tidak dapat mengisi IRS" in driver.page_source):
                raise NoSuchElementException

            # Keep this up to date
            if (
                "Pesan untuk pembimbing akademis" in driver.page_source
                or common_matkul in driver.page_source
                or chosen_matkul in driver.page_source
            ):
                break

            raise NoSuchElementException

        except NoSuchElementException:
            logout(driver)
            login(driver, username, password, display_name)

    while True:
        try:
            for name, code in matkul.items():
                try:
                    radio_button = driver.find_element(By.XPATH, '//input[@value="{}"]'.format(code))
                    
                    if(not radio_button.is_selected()):
                        radio_button.click()
                        print(f"{name} chosen! (code: {code})")
                    else:
                        print(f"{name} already chosen! (code: {code})")

                except NoSuchElementException:
                    print(f"Cannot find {name}! (code: {code})")
                    continue

            driver.find_element(By.NAME, 'submit').click()

            if ("IRS berhasil tersimpan!" in driver.page_source or "Daftar IRS" in driver.page_source):
                for name, code in matkul.items():
                    if (name not in driver.page_source):
                        print(f"Did not find {name}! (code: {code})")
                        print("Retrying...")
                        raise NoSuchElementException
                break

            raise NoSuchElementException

        except NoSuchElementException:
            driver.get(siak_page)

    print("Process finished! Press enter to exit...")
    input()
    driver.close()

def login(driver, username, password, display_name):
    print("Logging in...")

    while True:
        try:
            driver.get(auth_page)
            element = driver.find_element(By.ID, "u")
            element.send_keys(username)
            element = driver.find_element(By.NAME, "p")
            element.send_keys(password)
            element.send_keys(Keys.RETURN)

        except Exception as e:
            if ("Logout Counter" in driver.page_source or display_name in driver.page_source):
                print("Logged in!")
                break

            continue

        try:
            driver.get(home_page)
            if ("Logout Counter" in driver.page_source or display_name in driver.page_source):
                print("Logged in!")
                break
            raise Exception
        except:
            continue
        
def logout(driver):
    print("Logging out...")

    while True:
        try:
            driver.get(home_page)
            driver.find_element(By.PARTIAL_LINK_TEXT, 'Logout').click()
        except:
            try:
                driver.find_element(By.ID, "u")
                print("Logged out!")
                break
            except:
                continue

        try:
            driver.get(auth_page)
            driver.find_element(By.ID, "u")
            print("Logged out!")
            break
        except:
            continue

if __name__ == "__main__":
    print("SIAK AXZ - Blitzkrieg")
    print("Starting...")
    war()
