import requests
from datetime import datetime
import pytz
from lxml import html
import re
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

########################Credenciais###########################################################
API_KEY = ""
city = "nova friburgo"
link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=pt_br"
##############################################################################################


def login():
  
    
  # Inicializar o navegador
  chrome_options = Options()
  chrome_options.add_argument("--headless")  # Adiciona a opção headless
  driver = webdriver.Chrome(options=chrome_options)
  global wait 
  wait = WebDriverWait(driver,10)


  # Abrir o Twitter
  driver.get("https://twitter.com/login")
  
  #Login
  username_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-1dz5y72.r-fdjqy7.r-13qz1uu')))
  username_login.send_keys('UsernameTwitter')

  
  first_button_login = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]/div')
  first_button_login.click()

  password_login = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'r-30o5oe.r-1niwhzg.r-17gur6a.r-1yadl64.r-deolkf.r-homxoj.r-poiln3.r-7cikom.r-1ny4l3l.r-t60dpp.r-1dz5y72.r-fdjqy7.r-13qz1uu')))
  password_login.send_keys('SenhaTwitter')
  
  second_button_login = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div')
  second_button_login.click()
  
  

  
def get_rain_probability_information():
    page = requests.get('https://weather.com/weather/hourbyhour/l/5432dd4d88fd97b5ad64e0034495a0f4cc8cebe6f05d5764f7c6481214ffed97')
    tree = html.fromstring(page.content)
    buyers = tree.xpath('//*[@id="detailIndex0"]/summary/div/div/div[3]/span/text()')
    temp1 = str(buyers)
    temp2 = (re.sub(r"%|'|[|]|", "", temp1))
    return temp2




def get_climate_conditions():
    requisicao = requests.get(link)
    requisicao_dic = requisicao.json()
    humidity = requisicao_dic['main']['humidity']
    city = requisicao_dic['name']
    description = requisicao_dic['weather'][0]['description']
    temperature = requisicao_dic['main']['temp'] - 273.15
    tz_NY = pytz.timezone('America/Sao_paulo')
    datetime_NY = datetime.now(tz_NY)
    
    return city, description, round(temperature), humidity

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Adiciona a opção headless
    driver = webdriver.Chrome(options=chrome_options)
    while True:
        city, description, temperature, humidity = get_climate_conditions()

        if "chuva" in description:
            print(city)
            print(f"Temperatura: {temperature}°C")
            print(f"Clima: {description}")
            print(f"Umidade: {humidity}")
            print("Probabilidade de Chuva: 100%")
            print("Horário da previsão:", datetime.now().strftime("%H:%M:%S"))
            tweet = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')))
            tweet.send_keys('{}\nTemperatura: {}°C\nClima: {}\nUmidade: {}\nProbabilidade de chuva: 100%\nHorário: {}'.format(city,temperature,description,humidity,datetime.now().strftime("%H:%M:%S")))
            time.sleep(2)
            post_tweet = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/span/span")))
            post_tweet.click()

            time.sleep(3600)  # Esperar 1 minuto antes de atualizar novamente

        else:
            rain_probability = get_rain_probability_information()
            print(city)
            print(f"Temperatura: {temperature}°C")
            print(f"Clima: {description}")
            print(f"Umidade: {humidity}")
            print(f"Probabilidade de Chuva {rain_probability[1:-1]}%")
            print("Horário da previsão:", datetime.now().strftime("%H:%M:%S"))
            tweet = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')))
            tweet.send_keys('{}\nTemperatura: {}°C\nClima: {}\nUmidade: {}\nProbabilidade de chuva: {}%\nHorário: {}'.format(city,temperature,description,humidity,rain_probability[1:-1],datetime.now().strftime("%H:%M:%S")))
            time.sleep(2)
            post_tweet = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/span/span")))
            post_tweet.click()

            time.sleep(3600) 

if __name__ == "__main__":
    login()
    main()
    
