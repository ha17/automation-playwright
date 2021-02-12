#from playwright import sync_playwright
from playwright.sync_api import sync_playwright
import time
import re
import sys
import argparse
parser = argparse.ArgumentParser()

#
# Demonstrates:
#  - using browser context to viewport size and emulate phone/tablet/laptop/desktop widths
#  - iterating through each supported browser
#  - iterating through each supported breakpoint
#  - waiting to proceed
#  - taking a screenshot
#

try:
    url = sys.argv[1].strip()
except Exception as e:
    #print(e)
    print("[[EXITING]] - Please pass in a url")
    exit()

# parser.add_argument("-full", "--fullpage", help="Screencap a full page or just above-the-fold?")
# parser.add_argument("-url", "--urls", help="Single URL, or list of them")
# args = parser.parse_args()

###

urlPathed = re.sub('[^a-zA-Z-0-9]', '', url)

with sync_playwright() as p:

    browser_types = {
        "chrome": p.chromium,
        # "firefox": p.firefox,
        # "safari": p.webkit
    }

    emulations    = {
        '1-iphone-emulation': p.devices['iPhone 11 Pro'],
        '2-ipad-emulation'  : p.devices['iPad Pro 11'],
        '3-laptop': '1280x1024',
        '4-desktop': '1440x1024',
        '5-hd-desktop': '1920x1080'
    }

    for browser_type in browser_types:
        for emulation in emulations:
            browser = browser_types[browser_type].launch(headless=False)

            try:
                if isinstance(emulations[emulation], str):
                    splittedEmulation = emulations[emulation].split('x')
                    context = browser.new_context(viewport={'width': int(splittedEmulation[0]), 'height': int(splittedEmulation[1])})
                else:
                    context = browser.new_context(**emulations[emulation])
            except Exception as e:
                print(e)
                continue

            page = context.new_page()
            page.goto(url)
            time.sleep(7)
            ssPath = browser_type + '-' + emulation + '-' + urlPathed + '.png'
            # if args.fullpage:
            #     page.screenshot(path=f'./{browser_type}-{emulation}-{urlPathed}.png', full_page=True)
            # else:
            page.screenshot(path=f'./{browser_type}-{emulation}-{urlPathed}.png')

            try:
                page.screenshot(path=ssPath)
            except Exception as e:
                print(e)

            browser.close()
