from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Caminhos corretos
chromedriver_path = r"C:\SeleniumDrivers\chromedriver_win64\chromedriver.exe"

options = Options()
service = Service(chromedriver_path)

def abrir_site(url):
    """Abre site no Chrome via Selenium e retorna o driver"""
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    return driver

def fechar_site(driver):
    """Fecha site aberto pelo Selenium"""
    driver.quit()