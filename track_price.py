
import json
import sys
import openpyxl
import os
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

##########
# CONFIG
##########
EXCEL_FILEPATH = 'items.xlsx'
SCRIPT_DIRECTORY_ABS_PATH = r''
NOTION_SECRET = ''
NOTION_DATABASE_ID = ''


def alert(items_with_price_drop):
    """
    Alerts the user about items with price drops.

    This function posts a message to a Notion page using the Notion API.
    """
    message = "Price dropped for the following items:\n"
    for item in items_with_price_drop:
        message += f"{item['name']} is now ${item['current_price']:.2f} (was ${item['last_price']:.2f}). Link: {item['url']}\n"

    endpoint = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_SECRET}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    body = {
        "parent": {
            "database_id": NOTION_DATABASE_ID
        },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": "Price tracker"
                        }
                    }
                ]
            },
            "Status": {
                "select": {
                    "name": "High priority"
                }
            }
        },
        "children": [
            {
                "object": "block",
                "paragraph": {
                    "rich_text": [
                        {
                            "text": {
                                "content": message
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(body))

    if response.status_code == 200:
        print("Message successfully posted to Notion!")
    else:
        print(
            f"Failed to post message to Notion. Status code: {response.status_code}, Response: {response.text}")


def get_price(driver, item):
    driver.get(item['url'])

    # Explicitly wait until the element is present
    price_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, item['css_selector']))
    )

    # Use a regex pattern to match any numeric value including decimal points
    match = re.search(r'(\d+\.\d+|\d+)', price_element.text)
    if match and match.group(0):
        return float(match.group(0))
    else:
        raise ValueError(f"No price found for {item['name']} at {item['url']}")


def get_driver():
    # Options to suppress logging
    chrome_options = Options()
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging'])
    # chrome_options.add_argument("--headless")  # Hide UI
    return webdriver.Chrome(options=chrome_options)


def main():
    os.chdir(SCRIPT_DIRECTORY_ABS_PATH)
    
    with open('output.txt', 'w') as f:
        sys.stdout = f

        driver = get_driver()

        workbook = openpyxl.load_workbook(EXCEL_FILEPATH)
        sheet = workbook.active

        items_with_price_drop = []

        # Assuming the data starts on row 2 (row 1 being the header)
        for row in range(2, sheet.max_row + 1):
            item = {
                'name': sheet.cell(row=row, column=1).value,
                'url': sheet.cell(row=row, column=2).value,
                'css_selector': sheet.cell(row=row, column=3).value,
                'last_price': sheet.cell(row=row, column=4).value
            }

            try:
                current_price = get_price(driver, item)
                sheet.cell(row=row, column=4).value = current_price

                print(f"{item['name']} costs ${current_price:.2f}")

                if item['last_price'] is None:
                    continue

                if current_price < float(item['last_price']):
                    item['current_price'] = current_price
                    items_with_price_drop.append(item)

            except Exception as e:
                print(f"Error retrieving price for {item['name']}: {e}")
                continue

        workbook.save(EXCEL_FILEPATH)
        driver.quit()

        if items_with_price_drop:
            alert(items_with_price_drop)


if __name__ == "__main__":
    main()
