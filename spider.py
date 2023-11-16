from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

servico = Service(GeckoDriverManager().install())
navegador = webdriver.Firefox(service=servico)

def wait(seconds: float) -> WebDriverWait:
    print(f"Esperando com timeout de {seconds} segundos...")
    time = WebDriverWait(navegador, seconds)
    return time

def findID(id: str):
    try:
        return navegador.find_element(By.ID, id)
    except Exception as e:
        print('Element not found: ', e)
    return None

def waitUntilInvisible(seconds: float, xpath: str) -> None:
    wait(seconds).until(EC.invisibility_of_element_located(('xpath', xpath)))

def sendDownloadedFileToFolder(iteration: int) -> bool:
    try:
        file: str = "DadosBO_202" + str(year) + "_" + str(iteration) + "(FURTO DE VEÍCULOS).xls"           #DadosBO_2020_1(FURTO DE VEÍCULOS).xls
        downloadFolderString: str = os.path.expanduser("~\\Downloads")
        downloadFolderPath = os.path.join(downloadFolderString, file)
        destinationFolder: str = os.path.join(os.path.expanduser("~\\Documents\\Python Scraper\\Files"), file)
        with open(downloadFolderString, 'r') as origFile:
            os.rename(origFile, destinationFolder)
        return True
    except Exception as e:
        print("Impossible to move file to location: ", e)
    return False

navegador.get("https://www.ssp.sp.gov.br/transparenciassp/Consulta2022.aspx")

findID('cphBody_btnFurtoVeiculo').click()

year = 0

for i in range(20, 23):
    findID('cphBody_lkAno' + str(i)).click()
    waitUntilInvisible(300, '/html/body/div[2]')
    wait(3)

    for i in range(1,13):
        findID('cphBody_lkMes' + str(i)).click()
        waitUntilInvisible(300, '/html/body/div[2]')
        findID('cphBody_ExportarBOLink').click()
        waitUntilInvisible(300, '/html/body/div[2]')
        wait(3)

        sendDownloadedFileToFolder(i)
        wait(3)

    year +=1

