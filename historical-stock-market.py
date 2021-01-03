from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

CHROME_DRIVER_PATH = ''
URL = 'https://finance.yahoo.com/'
COMPANIES = ["General Motors", "Johnson & Johnson", "Jacobs",
             "Albemarle", "Disney", "AT&T", "American Airline"]

driver = webdriver.Chrome(CHROME_DRIVER_PATH)
driver.get(URL)
time.sleep(2)

driver.find_element_by_id('yfin-usr-qry').send_keys('Disney')
time.sleep(1)
driver.find_element_by_id('header-desktop-search-button').click()
time.sleep(1)

driver.find_element_by_xpath("//span[text() = 'Historical Data']").click()
time.sleep(2)

for i in range(3):
  driver.execute_script('window.scrollBy(0, 5000)')
  time.sleep(1)

HTMLPage = BeautifulSoup(driver.page_source, 'html.parser')

# with open('DIS_stock.html', 'w+', encoding='utf8') as f:
#   f.write(HTMLPage.prettify())

historical_data = HTMLPage.find('table', class_='W(100%) M(0)')

rows = historical_data.find_all('tr', class_='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)')

extracted_data = []

for i in range(0, len(rows)):
  try:
    row_dict = {}
    values = rows[i].find_all('td')
    # print(values)

    if len(values) == 7:
      row_dict['Date'] = values[0].find('span').text.replace(',', '')
      row_dict['Open'] = values[1].find('span').text.replace(',', '')
      row_dict['High'] = values[2].find('span').text.replace(',', '')
      row_dict['Low'] = values[3].find('span').text.replace(',', '')
      row_dict['Close'] = values[4].find('span').text.replace(',', '')
      row_dict['Adj Close'] = values[5].find('span').text.replace(',', '')
      row_dict['Volume'] = values[6].find('span').text.replace(',', '')

      extracted_data.append(row_dict)
  except:
    # To check the exception caused for which company
    print("Row Number: " + str(i))
  finally:
    # Move to next row
    i = i + 1

data_frame = pd.DataFrame(extracted_data)
data_frame.to_csv('Disney.csv', index=False)

