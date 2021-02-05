from playwright import sync_playwright
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

#    print(emulations['laptop'].split('x')[0])
#    exit()
# Todo: fix viewport emulation in the try block
# Firefox mobile emulation?

    for browser_type in browser_types:
        for emulation in emulations:
            browser = browser_types[browser_type].launch(headless=False)

            try:
                if emulation == 'laptop' or emulation == 'desktop':
                    splittedEmulation = emulations[emulation].split('x')
                    context = browser.newContext(viewport={'width': splittedEmulation[0], 'height': splittedEmulation[1]})
                else:
                    context = browser.newContext(**emulations[emulation])
            except:
                continue

            page = context.newPage()
            page.goto(url)
            page.waitForSelector('.ml-promotion-no-thanks')
            page.screenshot(path=browser_type + '-' + emulation + '-' + urlPathed + '.png')
    browser.close()
