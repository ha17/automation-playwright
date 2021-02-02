from playwright import sync_playwright

#
# Demonstrates: 
#  - using browser context to alter geolocation
#    - geolocation spoofing allows you to check how your web site looks, if it changes based on a user's location.
#  - using broswer context to change the browser to iPhone dimensions, and provide an iPhone user-agent
#  - waiting for an element to appear on the page, before proceeding
#  - taking a full-page screenshot
#

with sync_playwright() as p:
    iphone_11 = p.devices['iPhone 11 Pro']
    browser = p.webkit.launch(headless=False)
    context = browser.newContext(
        **iphone_11,
        locale='en-US',
        geolocation={ 'longitude': 12.492507, 'latitude': 41.889938 },
        permissions=['geolocation']
    )
    page = context.newPage()
    page.goto('https://maps.google.com')
    page.click('text="Your location"')
    page.waitForSelector('.ml-promotion-no-thanks')
    page.screenshot(path='iphone-google-maps-popup.png')
    browser.close()
