# price-tracker

This program allows you to track the price of **any** item you find online, on **any** website. If it detects a drop in price, it will alert you. By default, it will alert you by posting an entry to a Notion page. You can modify the code to be alerted however you prefer.

# Installation and Usage

## Setup

1. Download the repository.

2. [Create a Python virtual environment](https://code.visualstudio.com/docs/python/environments#_creating-environments) and [activate it](https://docs.python.org/3/library/venv.html#how-venvs-work).

3. Run `pip install -r requirements.txt`.

4. In the `Config` section of the code, set `SCRIPT_DIRECTORY_ABS_PATH` to be the absolute path to the repository, e.g. `D:\Users\User\Path\To\price-tracker`.

## Tracking an Item's Price

1. When you find an item online whose price you want to track, make an entry for it in the Excel file.

    1. Under
