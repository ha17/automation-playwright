from playwright import sync_playwright
from xml.dom import minidom
import time
import datetime
import random

with open('YT-channels.urls') as channelUrls:
    URLs = channelUrls.readlines()

#Pull their "videos" page
#Pull in the existing video URLs we have
#Parse the list of videos somehow
#Save them to a NEW file with date
#Copy that file to clipboard
#Paste into Media Appearance, split into columns.
#Pull down enough of the players, etc, to cover those new rows
#Copy and paste new ones to

i      = 0
date   = datetime.datetime.now();
dateFileName = (date.strftime('%Y-%m-%d')) + '.data'

with sync_playwright() as p:
    for browser_type in [p.webkit]:
        browser = browser_type.launch(headless=False)
        page    = browser.newPage()
        for nameUrl in URLs:
            videos = {}
            nameUrlSplitted = nameUrl.split(',')
            Name            = nameUrlSplitted[0].strip()
            URL             = nameUrlSplitted[1].strip()
            page.goto(URL)
            page.waitForTimeout(60000)
            #break

            rows = page.querySelectorAll('div#items ytd-grid-video-renderer.ytd-grid-renderer');
            for row in rows:
                videoUrl   = row.querySelector('#meta a').getAttribute('href').strip()
                videoTitle = row.querySelector('#meta a').getAttribute('title').strip()
                #videoDate  = row.querySelector('#meta a').getAttribute('title').strip()
                #print(videoUrl)
                #print(videoTitle)
                videos[videoUrl] = ('"%s","%s","%s"' % (Name, 'https://youtube.com' + videoUrl, videoTitle))

            #print(videos)
            #break # debug

            with open('./data/'+dateFileName+Name, mode='wt', encoding='utf-8') as fileVideos:
                fileVideos.write('\n'.join(videos.values()))
    browser.close()
