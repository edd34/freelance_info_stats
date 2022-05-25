import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from tinydb import TinyDB
from tqdm import tqdm
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime

# init
load_dotenv()
db = TinyDB("./db.json")
options = Options()
options.headless = True
driver = webdriver.Firefox(
    options=options, service=Service(GeckoDriverManager().install())
)

# login to freelance info
driver.get("https://www.freelance-info.fr/login-page.php")

username_elem = driver.find_element(by=By.ID, value="_username")
password_elem = driver.find_element(by=By.ID, value="_password")

username_elem.clear()
password_elem.clear()

username_elem.send_keys(os.getenv("USERNAME"))  # email freelance-info
password_elem.send_keys(os.getenv("PASSWORD"))  # mot de passe freelance-info
password_elem.send_keys(Keys.RETURN)

list_keywords = os.getenv("KEYWORDS_SEARCH").split(",")
current_date = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

for keyword in tqdm(list_keywords):
    print(keyword)
    driver.get("https://www.freelance-info.fr/missions?keywords=" + keyword)
    driver.find_element(by=By.CSS_SELECTOR, value="button.btn:nth-child(2)").click()
    stats_region = driver.find_elements(
        by=By.CSS_SELECTOR, value="#regiondropdown > optgroup:nth-child(2)"
    )

    tmp_disct_region_nb = {}
    for elem in stats_region[0].text.split("\n"):
        region = elem.split("[")[0]
        nb = elem.split("[")[1].split("]")[0]
        tmp_disct_region_nb[region] = int(nb)
        print(region, nb)
    print(tmp_disct_region_nb, stats_region)
    db.insert(
        {
            "date": current_date,
            "techno": keyword,
            "stats": tmp_disct_region_nb,
            "total": sum(
                [
                    tmp_disct_region_nb[value]
                    for (key, value) in enumerate(tmp_disct_region_nb)
                ]
            ),
        }
    )

driver.close()
