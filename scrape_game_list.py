from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import json

def main():
    driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    driver.get("https://thefinalfantasy.net/games/complete-list.html")
    elements = driver.find_element(By.ID, "gameList").find_elements(By.XPATH, "./tbody/*")

    data = []
    for element in elements:
        columns = element.find_elements(By.TAG_NAME, "td")
        data.append({
            "name": columns[0].text,
            "system": columns[1].text,
            "release": columns[2].text,
            "region": columns[3].text
        })
    with open("in/gamelist.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    print("File saved to ./gamelist.json")


if __name__ == '__main__':
    main()

