from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd
import os

def main():
    attempt = 0
    max_attempt = 5
    data = []

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    while attempt < max_attempt:
        try:
            service = Service(ChromeDriverManager().install())
            option = webdriver.ChromeOptions()
            option.add_argument("--max-size")
            driver = Chrome(service=service, options=option)

            driver.get("https://www.booking.com/index.es.html?aid=2311236;label=es-pe-booking-desktop-a03KozpSYV0ovtPDxxDT6gS652829001784:pl:ta:p1:p2:ac:ap:neg:fi:tikwd-65526620:lp9186207:li:dec:dm;ws=&gclid=EAIaIQobChMI_9Li_8aJiQMVBV5IAB03_AmLEAAYAiAAEgLEG_D_BwE")
            
            time.sleep(5)
            
            ### En la página de Booking se muestra un modal al inicio, se dará un click fuera de este para quitarlo
            ActionChains(driver).move_by_offset(0, 0).click().perform() 

            ### Campo ubicación
            search_location = WebDriverWait(driver,15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/form/div/div[1]/div/div/div[1]/div/div/input"))
            )
            search_location.send_keys('Barcelona') #Colocar barcelona

            ### Campo de fecha
            date_field = WebDriverWait(driver,15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/form/div/div[2]/div/div/button[1]"))
            )
            date_field.click()

            fechas_flexibles_menu = WebDriverWait(driver,15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div/nav/div[1]/ul/li[2]/button"))
            )
            fechas_flexibles_menu.click()
            
            radio_otro = WebDriverWait(driver,15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div/nav/div[3]/div/div[1]/div[1]/div/fieldset/div/div[4]/label/span[3]/div"))
            )
            radio_otro.click()

            months = driver.find_elements(By.CSS_SELECTOR, '.b0932df2e7.e375bc2404')
            for month in months[:3]:
                month.click()

            btn_search = WebDriverWait(driver,15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div[2]/div/form/div/div[4]/button"))
            )
            btn_search.click()
            
            time.sleep(5)
            cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')
            
            for carta in cards[:50]:
                # Aquí puedes extraer información específica de cada carta.
                title = carta.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text 
                address = carta.find_element(By.CSS_SELECTOR, 'span[data-testid="address"]').text 
                price = carta.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text 
                div_score = carta.find_element(By.XPATH, '//div[@data-testid="review-score"]//div[@class="ac4a7896c7"]').text 
                rooms = 1 ## Por defecto la pagina nos da 1

                ## Arreglando Puntuacion
                score_value = div_score.split(":")[1].strip().replace(",", ".")  # Obtén el número y reemplaza la coma con un punto
                score_value = float(score_value)  
                data.append({'Nombre': title, 'Dirección': address, 'Precio': price, 'Puntuación': score_value, 'Habitaciones': rooms})    
            
            btn_rooms = WebDriverWait(driver,15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[2]/div/div[1]/div/form/div/div[3]/div/button"))
            )
            btn_rooms.click()
            
            add_room = WebDriverWait(driver,15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[2]/div/div[1]/div/form/div/div[3]/div/div/div/div/div[3]/div[2]/button[2]"))
            )
            add_room.click()

            ### La ubicación del botón BUSCAR cambia despues de la primera busqueda por lo que lo actualizamo
            btn_search = WebDriverWait(driver,15).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[2]/div/div[1]/div/form/div/div[4]/button"))
            )
            btn_search.click()

            time.sleep(5)
            cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

            for carta in cards[:50]:
                # Aquí puedes extraer información específica de cada carta.
                title = carta.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').text 
                address = carta.find_element(By.CSS_SELECTOR, 'span[data-testid="address"]').text 
                price = carta.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').text 
                div_score = carta.find_element(By.XPATH, '//div[@data-testid="review-score"]//div[@class="ac4a7896c7"]').text 
                rooms = 2 ## Para este ejemplo solo se añadira una habitación más

                ## Arreglando el texto de Puntuacion
                score_value = div_score.split(":")[1].strip().replace(",", ".")  # Obtén el número y reemplaza la coma con un punto
                score_value = float(score_value)  
                data.append({'Nombre': title, 'Dirección': address, 'Precio': price, 'Puntuación': score_value, 'Habitaciones': rooms})  

            break

        except Exception as e:
            attempt += 1
            print("Intento: ", attempt)
            print(e)
            if attempt < max_attempt:
                time.sleep(5)

        finally:
            if driver:
                driver.quit()
    df = pd.DataFrame(data)
    print(df)
    print(output_path)
    df.to_csv(output_path + "\\dataset-output\\final_scraping-ejercicio_1.csv", index=False)

if __name__ == '__main__':
    main()
