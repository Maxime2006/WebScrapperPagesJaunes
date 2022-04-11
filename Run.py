from random import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time 
import random
import os
import csv
import sys

def write_url_csv(urls):
    fieldnames = ["URL PagesJaunes"]
    del urls[-1]
    for url in urls :
        rows = [
            {
            "URL PagesJaunes" : url
        }]
        with open('URL_'+sys.argv[1]+'.csv', 'a', encoding='UTF8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if os.stat('URL_'+sys.argv[1]+'.csv').st_size == 0:
                writer.writeheader()
            writer.writerows(rows)

def get_valeurs(driver, liens):
    for lien in liens:
        driver.get(lien[0])
        time.sleep(1)
        accepte_cookie(driver)
        try: 
            nom = driver.find_element(By.XPATH, "//html/body/main/div[2]/section/div[2]/div[1]/div[1]/div/div[1]/h1")
            nom = nom.text
        except NoSuchElementException:
            nom = ""
        try: 
            cat = driver.find_element(By.XPATH, "//html/body/main/div[2]/section/div[2]/div[1]/div[1]/div/div[2]/div")
            cat = cat.text
        except NoSuchElementException:
            cat = ""
        try: 
            note = driver.find_element(By.XPATH,("//html/body/main/div[2]/section/div[2]/div[1]/div[1]/div/div[3]/a/span[1]/span/strong"))
            note = note.text
        except NoSuchElementException:
            note = ""
        try: 
            clicknum = driver.find_element(By.XPATH,"//a[@title='Afficher les N°']")
            clicknum.click
            time.sleep(1)
        except NoSuchElementException:
            pass
        try: 
            num = driver.find_element(By.XPATH,"//html/body/main/div[2]/section/div[6]/div[1]/div[1]/div/div/div[1]/div/span/span[2]")
            num = num.text
        except NoSuchElementException:
            num = ""
        try: 
            adresse = driver.find_element(By.XPATH, "//html/body/main/div[2]/section/div[6]/div[1]/div[9]/div[2]/div/div/div[1]/a/span[1]")
            CP = driver.find_element(By.XPATH, "//html/body/main/div[2]/section/div[6]/div[1]/div[9]/div[2]/div/div/div[1]/a/span[2]")
            D = driver.find_element(By.XPATH, "//html/body/main/div[2]/section/div[6]/div[1]/div[9]/div[2]/div/div/div[1]/a/span[3]")
            address = adresse.text +CP.text+" "+D.text
        except NoSuchElementException:
            address = ""
        try: 
            site = driver.find_element(By.XPATH,"//html/body/main/div[2]/section/div[6]/div[1]/div[1]/div/div/div[3]/a/span[2]")
            site = site.text
        except NoSuchElementException:
            site = ""
        write_conf_csv(nom, cat, note, num, address, site, lien)
        time.sleep(random.randint(4, 9))

def read_URL(driver):
    with open('URL_'+sys.argv[1]+'_final.csv', newline='') as f:
        reader = csv.reader(f)
        liens = list(reader)
    del liens[0]
    get_valeurs(driver, liens)

def delete_duplicate():
    with open('URL_'+sys.argv[1]+'.csv','r') as in_file, open('URL_'+sys.argv[1]+'_final.csv','w') as out_file:
  
        seen = set()
        
        for line in in_file:
            if line in seen: 
                continue

            seen.add(line)
            out_file.write(line)

def write_conf_csv(nom, cat, note, num, address, site, url):
    fieldnames = ["Nom de l'entreprise", "Catégories", "note /5", "Numéro de téléphone", "Adresse", "Site internet", "URL PagesJaunes"]

    rows = [
        {"Nom de l'entreprise": nom,
         "Catégories" : cat,
         "note /5" : note,
         "Numéro de téléphone" : num,
         "Adresse" : address,
         "Site internet" : site,
         "URL PagesJaunes" : url
       }]

    with open('Base_De_Donnee_'+sys.argv[1]+'.csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if os.stat('Base_De_Donnee_'+sys.argv[1]+'.csv').st_size == 0:
            writer.writeheader()
        writer.writerows(rows)

def page_suivante(driver, liens):
    try:
        accepte = driver.find_element(By.ID,"pagination-next")
        time.sleep(random.randint(4,10))
        accepte.click()
        get_url(driver, liens)
    except NoSuchElementException:
        pass
    

def get_url(driver, liens):
    lnks=driver.find_elements(By.TAG_NAME, "a")
    for lnk in lnks:
        if "/pros/" in lnk.get_attribute('href'):
            liens.append(lnk.get_attribute('href'))
    try:
        page_suivante(driver, liens)
    except NoSuchElementException:
        return liens

def accepte_cookie(driver):
    try:
        accepte = driver.find_element(By.ID,"didomi-notice-agree-button")
        accepte.click()
        return True
    except NoSuchElementException:
        return False

def recherche(driver, departement):
    liens =[]
    recherche = driver.find_element(By.ID,"quoiqui")
    ville = driver.find_element(By.ID,"ou")
    chercher = driver.find_element(By.XPATH,"//button[@title='Trouver']")
    recherche.send_keys(sys.argv[1])
    ville.send_keys(departement)
    chercher.click()
    time.sleep(1)
    liens.append(get_url(driver, liens))
    write_url_csv(liens)

def main():
    try:
        if sys.argv[1] == 0:
            pass
    except IndexError:
        print("Run.py --help")
        return
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        print("Run.py [Recherche] [Département(s)]\nRun.py boulangerie\nRun.py boulangerie 1\nRun.py boulangerie 1-10")
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        driver = webdriver.Chrome("chromedriver.exe", chrome_options=options)
        time.sleep(1)
        try:
            if "-" in sys.argv[2]:
                for i in range(int(sys.argv[2].split("-")[0]),int(sys.argv[2].split("-")[1])):
                    time.sleep(1)
                    driver.get("https://www.pagesjaunes.fr/")
                    time.sleep(1)
                    accepte_cookie(driver)
                    time.sleep(1)
                    if i < 10:
                        recherche(driver, "0"+str(i))
                    else: 
                        recherche(driver, i)
            else:
                driver.get("https://www.pagesjaunes.fr/")
                time.sleep(1)
                accepte_cookie(driver)
                time.sleep(1)
                if int(sys.argv[2]) < 10:
                    if "0" in str(sys.argv[2]):
                        recherche(driver, sys.argv[2])
                    else:
                        recherche(driver, "0"+str(sys.argv[2]))
                else: 
                    recherche(driver, sys.argv[2])
        except IndexError:
            for i in range(1,96):
                time.sleep(1)
                driver.get("https://www.pagesjaunes.fr/")
                time.sleep(1)
                accepte_cookie(driver)
                time.sleep(1)
                if i < 10:
                    recherche(driver, "0"+str(i))
                else: 
                    recherche(driver, i)
        delete_duplicate()
        read_URL(driver) 
        driver.close()

if __name__ == "__main__":
   main()