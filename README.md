# universal-price-tracker

Other programs exist to track the price of items that you're interested in, but they're often restricted to support **specific websites**. This program is a **universal price tracker**, allowing you to track the price of **any** item you find online on **any** website. If it detects a drop in price, it will alert you.

By default, it will alert you by posting an entry to a Notion page. You can modify the code to be alerted however you prefer.

![image](https://github.com/kellenvu/price-tracker/assets/56773806/9721fac2-356d-4193-a4bb-880e512b4325)

![image](https://github.com/kellenvu/price-tracker/assets/56773806/1321ef0a-8693-4771-a5cf-f5a4a996a0f8)

# Installation and Usage

## Setup

1. Download the repository.

1. Run `pip install -r requirements.txt`.

1. In the `Config` section of the code, set `SCRIPT_DIRECTORY_ABS_PATH` to be the absolute path to the repository, e.g. `D:\Users\User\Path\To\universal-price-tracker`.

1. Modify the rest of the configuration as desired.

## Adding an Item to the List of Tracked Items

1. When you find an item online whose price you want to track, make an entry for it in the Excel file.

    1. Under `Item`, put the name of the item.

    1. Under `URL`, put the URL of the page that contains the price.

    1. Under `CSS Selector`, put a comma-delimited list of CSS selectors for the price HTML element. The script will return the first price found using these CSS selectors.

        1. A CSS selector is a pattern that is used to find HTML elements in CSS. To get the CSS selector, right-click the price and click `Inspect` to examine the classes and IDs of the HTML elements associated with the price. Use [combinators](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_selectors/Selectors_and_combinators) to come up with a CSS selector for the price.

   1. You can leave `Last Tracked Price` empty.

## Running the Program

1. You can run the program once to update the price of each item in the Excel file. Just run `python track_price.py`.

1. If you want the program to run periodically, you can set up a scheduler. On Windows, I followed [these instructions](https://stackoverflow.com/a/43988165) to create a .bat file that runs the program within my desired virtual environment, and then I followed [these instructions](https://helpdeskgeek.com/windows-11/how-to-schedule-a-batch-file-to-run-in-windows-11-10-using-task-scheduler/) to create a scheduler that runs this .bat file once per day.

## Setting Up Alerts

1. You can modify the `alert()` function to determine how you want to be notified about price drops. By default, it tries to notify you by posting to a Notion database. To set up the Notion integration, follow steps 1 and 2 in [this guide](https://kellenvu.github.io/blog/integrate-siri-with-notion-for-free), then add the Notion internal integration secret and database ID to the `Config` section of the code.
