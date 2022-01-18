from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

def isi_siak(username, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome('chromedriver.exe', options=options)

    # use line below if you want more refresh in shorter time, might impact login time
    # maybe useful when your faculty goes to war on the same time as other faculty
    # driver.set_page_load_timeout(5)

    login(driver, username, password)


    matkul=[]
    with open('matkul.txt') as file_inp:
        for line in file_inp:
            matkul.append(line.strip())
    
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit")
            time.sleep(0.5)

            # Keep this up to date
            if ("Pesan untuk pembimbing akademis" in driver.page_source):
                break
            raise NoSuchElementException

        except NoSuchElementException:
            logout(driver)
            login(driver, username, password)

    while True:
        try:
            for kelas in matkul:
                try:
                    element=driver.find_element_by_xpath("//a[text()='{}']".format(kelas))
                    label=element.find_element_by_xpath('..')
                    ans=label.get_attribute('for')
                    clicked=driver.find_element_by_xpath('//input[@id="{}"]'.format(ans))
                    clicked.click()

                except NoSuchElementException:
                    continue

            driver.find_element_by_name('submit').click()

            if ("IRS berhasil tersimpan!" in driver.page_source):
                break

            raise NoSuchElementException

        except NoSuchElementException:
            driver.get("https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit")

    print("Otsu")
    input()
    driver.close()

def login(driver, username, password):
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Authentication/")
            element = driver.find_element_by_id("u")
            element.send_keys(username)
            element = driver.find_element_by_name("p")
            element.send_keys(password)
            element.send_keys(Keys.RETURN)

        except:
            if ("Logout Counter" in driver.page_source):
                break

            continue

        try:
            driver.get("https://academic.ui.ac.id/main/Welcome/Index")
            if ("Logout Counter" in driver.page_source):
                break

            raise Exception

        except:
            continue
        
def logout(driver):
    while True:
        try:
            driver.get("https://academic.ui.ac.id/main/Welcome/Index")
            driver.find_element_by_partial_link_text('Logout').click()

        except:
            try:
                driver.find_element_by_id("u")
                break

            except:
                continue
        try:
            driver.get("https://academic.ui.ac.id/main/Authentication/")
            driver.find_element_by_id("u")
            break

        except:
            continue
            

if __name__ == "__main__":
    uspass=[]
    with open('user_pass.txt') as file_inp:
        for line in file_inp:
            uspass.append(line.strip())

    isi_siak(uspass[0],uspass[1])