from playwright import sync_playwright
import time

#
# Demonstrates: 
#  - using browser context to alter device size
#  - taking a full-page screenshot
#

url = 'http://whatsmyuseragent.org/'

with sync_playwright() as p:
    browser_types = [p.chromium, p.webkit]
    iphone_11 = p.devices['iPhone 11 Pro']
    
    # Open up the three browser types, same page, we will
    # take a screenshot of the page to show our User-Agent for each
    for browser_type in browser_types:
        browser = browser_type.launch(headless=False)

        context = browser.newContext(
            **iphone_11
        )

        # Note, we are using "context" not "browser"
        page = context.newPage() 

        page.goto(url)
        page.screenshot(path=f'example-phone-{browser_type.name}.png')

        browser.close()
        time.sleep(2)



    # Now, let's open up the same three browsers with the same page, but
    # as a desktop browser, instead of mobile.
    for browser_type in browser_types:
        browser = browser_type.launch()

        page = browser.newPage()
        page.goto(url)
        page.screenshot(path=f'example-{browser_type.name}.png')

        time.sleep(2)
        browser.close()
