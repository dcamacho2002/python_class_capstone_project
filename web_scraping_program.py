from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install())) 

driver.get("https://www.baseball-almanac.com/yearmenu.shtml")

year = driver.find_elements(By.CSS_SELECTOR, "a[href*='yearly']")

data = []
for e in year:
    years = e.text.strip()
    link = e.get_attribute('href')
    if years and link:
        data.append([years, link])

every = []
for year, url in data[:5]:
    driver.get(url)
    rows = driver.find_elements(By.CSS_SELECTOR, "table tr")
    for row in rows:
        tds = row.find_elements(By.CSS_SELECTOR, 'td')
        if len(tds) >= 2:
            event = tds[0].text.strip()
            stat = tds[1].text.strip()
            if event in ['Statistic', 'Name(s)', 'Team', 'Team | Roster']:
                continue
            every.append([year, event, stat])

with open('mlb_years.csv', 'w', newline = '') as f:
    writer = csv.writer(f)
    writer.writerow(['Year', 'Event', 'Statistic'])
    writer.writerows(every) 

print(f'Saved {len(every)} events and stats to mlb_years.csv')

driver.quit()