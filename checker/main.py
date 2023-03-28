from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium_recaptcha_solver import RecaptchaSolver, StandardDelayConfig
from colorama import Fore,Back,Style
import undetected_chromedriver as uc
from pypasser import reCaptchaV2
import time 
from random import randint
import colorama
from fake_useragent import UserAgent
import argparse
colorama.init(autoreset=True)

class Main:
    def __init__(self,urx):
        self.ur = urx
        self.options = Options()
        # self.options.add_argument('--headless')
        # self.options.add_argument('--disable-gpu')
        ua = UserAgent()
        usera = ua.random
        print(usera)
        # self.options.add_argument(f'user-agent={usera}')
        # self.options.add_argument("user-data-dir=C:\chromeprofile2")
        self.driver = uc.Chrome(options=self.options)
        # self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.options) 
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 30)
        self.solver = RecaptchaSolver(driver=self.driver)
    def Save(self,file,data):
        with open(file,"a") as f:
            f.write(data + "\n")

    def GetDetail(self,url,numbers):
        self.driver.get(url)
        number = WebDriverWait(self.driver, 90).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section[2]/div/div[2]/form/div/div/div[1]/div/textarea")))
        number.send_keys(numbers)
        try:
            recaptcha_iframe = self.driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
            slvr = self.solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            if slvr is not None:
                recaptcha_iframe = self.driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
                slvr = self.solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        except Exception as e:
            print(e)
        
        WebDriverWait(self.driver, 90).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/section[2]/div/div[2]/form/div/div/div[6]/div/button"))).click()
        if "0 valid" in self.driver.page_source:
            print(Fore.LIGHTBLUE_EX+"zero!")
        else:
            try:
                valid = WebDriverWait(self.driver, 90).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/section[2]/div/div[3]/div[1]/div/div[2]/div/textarea")))
                print(Fore.LIGHTGREEN_EX+"[+]INFO",Fore.LIGHTGREEN_EX+valid.text+" VALID")
                self.Save("valid.txt",valid.text)
            except Exception as e:
                print(e)
        if "0 invalid" in self.driver.page_source:
            print(Fore.LIGHTBLUE_EX+"zero!")
        else:
            try:
                invalid = WebDriverWait(self.driver, 90).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div/section[2]/div/div[3]/div[2]/div/div[2]/div/textarea")))
                print(Fore.LIGHTGREEN_EX+"[+]INFO",Fore.RED+invalid.text+" INVALID")
                self.Save("ivalid.txt",invalid.text)
            except Exception as e:
                print(e)
                   
        time.sleep(20)


parser = argparse.ArgumentParser(description='number checker')
parser.add_argument('-f', '--file', type=str, help='Nama file yang ingin dibaca.', required=True)
args = parser.parse_args()
mn = Main("B08TVDWM9W")
time.sleep(2)
with open(args.file, "r") as f:
    data = f.read()
mn.GetDetail("https://sms.cx/bulk-phone-validator/",data)
