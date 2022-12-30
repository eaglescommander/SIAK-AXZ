from selenium import webdriver
from selenium.webdriver.common.by import By
import time

"""
features:
1. Automatic login/logout
2. Automatic detection when can fill IRS
3. Automatic filling of IRS
4. Excellent error handling. Can skip matkul if its not available or invalid
"""

# ======= windows
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')
# driver = webdriver.Chrome('./chromedriver', options=options)

# ======= linux. put chromedriver on folder
driver = webdriver.Chrome("./chromedriver")

login_url = "https://academic.ui.ac.id/main/Authentication/"
homepage_url = "https://academic.ui.ac.id/main/Welcome/"
logout_url = "https://academic.ui.ac.id/main/Authentication/Logout"
siak_url = "https://academic.ui.ac.id/main/CoursePlan/CoursePlanEdit"

down_string = "Universitas Indonesia"
matkul_code = {}

with open("matkul.txt", "r") as file:
    for line in file:
        (kelas, nama) = line.split()
        matkul_code[nama] = kelas

# fill your login credentials here
user = ""
passw = ""
display_name = "" # yang ditampilin di pojok kanan atas siak. ex: Galangkangin Gotera
common_matkul = "" # matkul yang dijamin ada pada pengisian IRS. Misalnya DDP atau Tennis (Substring sseperti Tenn tidak apa-apa)
chosen_matkul = ""

with open("credentials.txt", "r") as file:
    creds = []
    for line in  file:
        creds.append(line.strip())

    user = creds[0]
    passw = creds[1]
    display_name = creds[2]
    common_matkul = creds[3]
    chosen_matkul = creds[4]

def logout_page():
    driver.get(logout_url)
    time.sleep(0.5)

def login_page():
    #driver.get(login_url)

    username = driver.find_element(By.NAME, "u")
    username.clear()
    username.send_keys(user)
    time.sleep(0.1)

    password = driver.find_element(By.NAME, "p")
    password.clear()
    password.send_keys(passw)
    time.sleep(0.1)
    driver.find_element(By.XPATH, "//input[@value='Login']").click()

def war_page():
    #driver.get(siak_url)
    #time.sleep(2)
    for name, kode in matkul_code.items():

        # antisipasi salah masukkin kode
        try:
            radio_input = driver.find_element(By.XPATH, f"//input[@value='{kode}']")
            if(not radio_input.is_selected()): 
                radio_input.click()
                print(f"{name} dipilih! (kode: {kode})")
                time.sleep(0.1)
            else :
                print(f"{name} sudah dipilih! (kode: {kode})")
        except:
            print(f"{name} tidak ada! (kode: {kode})")
            #time.sleep(5)

    button = driver.find_element(By.XPATH, "//input[@value='Simpan IRS']")
    button.click()

if __name__ == "__main__":
    #new_term = "Tahun Ajaran 2019/2020 Term 1"
    driver.get(login_url)
    time.sleep(0.5)

    while(True):

        # refresh manual bre
        while(display_name not in driver.page_source and 
              "Magister Kriminologi" not in driver.page_source):
            driver.refresh()
            

        # login
        if "Magister Kriminologi" in driver.page_source:
            login_page()
            continue

        # case di homepage
        if driver.current_url == homepage_url:
            driver.get(siak_url)
            time.sleep(0.5)
            continue

        # case di tempat irs
        if "CoursePlanEdit" in driver.current_url:

            if "Anda tidak dapat mengisi IRS" in driver.page_source:
                print("BELUM BISA NGISI")
                logout_page()
                continue

            print("In WAR PAGE")
            
            time.sleep(1.5)

            # logout, belom bisa ngisi
            if common_matkul not in driver.page_source:
                print("BELUM BISA NGISI")
                logout_page()
                continue

            print("WARRRRRRRRRRRRRRRRRRRR!!!!!!!!!!!")
            war_page()
            time.sleep(1.5)

            # kalau gagal, ulang lagi ngisinya
            if (chosen_matkul not in driver.page_source):
                print("ngulang isi bre")
                driver.get(siak_url)
                continue

            
            print("SUKSESS")
            break # SUKSES!!!

    while True:
    	pass
