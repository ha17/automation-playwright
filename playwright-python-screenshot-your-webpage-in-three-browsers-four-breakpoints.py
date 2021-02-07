from playwright import sync_playwright
import time
import re

#
# Demonstrates: 
#  - using browser context to viewport size and emulate phone/tablet/laptop/desktop widths
#  - iterating through each supported browser
#  - iterating through each supported breakpoint 
#  - waiting to proceed
#  - taking a screenshot
#

## Set this
url = 'https://maps.google.com'


###

urlPathed = re.sub('[^a-zA-Z-0-9]', '', url)

with sync_playwright() as p:
    
    browser_types = {
        "chrome": p.chromium,
        "firefox": p.firefox,
        "safari": p.webkit
    }

    emulations    = {
        'iphone': p.devices['iPhone 11 Pro'],
        'ipad'  : p.devices['iPad Pro 11'],
        'laptop': '1280x1024',
        'desktop': '1440x1024' 
    }

    for browser_type in browser_types:
        for emulation in emulations:
            browser = browser_types[browser_type].launch(headless=False)

            try:
                if emulation == 'laptop' or emulation == 'desktop':
                    splittedEmulation = emulations[emulation].split('x')
                    context = browser.newContext(viewport={'width': int(splittedEmulation[0]), 'height': int(splittedEmulation[1])})
                else:
                    context = browser.newContext(**emulations[emulation])
            except Exception as e:
                print(e)
                continue

            page = context.newPage()
            page.goto(url)
            time.sleep(3)
            ssPath = browser_type + '-' + emulation + '-' + urlPathed + '.png'
            page.screenshot(path=f'./{browser_type}-{emulation}-{urlPathed}.png')
            try:
                page.screenshot(path=ssPath)
            except Exception as e:
                print(e)

            browser.close()
