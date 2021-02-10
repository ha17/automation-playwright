from playwright import sync_playwright
from xml.dom import minidom
import urllib.request
import json
import time
import datetime
import random

with open('Disc Golf Stats - Golfers.tsv') as golferInfo:
    gInfo = golferInfo.readlines()

stats  = {}
date   = datetime.datetime.now();
dateFileName = (date.strftime('%Y-%m-%d')) + '.data'

def do_instagram(page, handle):
    if not handle:
        return False

    ig_url = "https://www.instagram.com/<handle>/?__a=1".replace('<handle>', handle)

    with urllib.request.urlopen(ig_url) as url:
        data = url.read().decode()
        #data = json.loads(url.read().decode())
        return data



with sync_playwright() as p:
    for browser_type in [p.webkit]:
        browser = browser_type.launch(headless=False)
        page    = browser.newPage()
        i       = -1
        for line in gInfo:
            i += 1

            if (i==0):
                continue

            lineSplitted = line.split("\t")

            pdgaNumber    = lineSplitted[0].strip()
            golfer        = lineSplitted[1].strip()
            currentRating = lineSplitted[2].strip()
            Type          = lineSplitted[3].strip()
            Birthdate     = lineSplitted[4].strip()
            pdgaUrl       = lineSplitted[5].strip()
            ig_handle     = lineSplitted[6].strip()
            tw_handle     = lineSplitted[7].strip()
            yt_channel    = lineSplitted[8].strip()

            if not pdgaNumber:
                continue

            if not ig_handle or ig_handle == '-':
                continue

            igResult = do_instagram(page, ig_handle)
            print(igResult)
            exit()

            try:
                stats[str(pdgaNumber)].append(igResult)
            except KeyError:
                stats[str(pdgaNumber)] = []
                stats[str(pdgaNumber)].append(igResult)

            #print(stats)
            #stats[str(pdgaNumber)].append(do_instagram(ig_handle))
            #print(stats)
            #exit()


            #if ig_handle:
            #if tw_handle:
            #    stats[twitter] = do_twitter(tw_handle)

            #if yt_channel:
            #    stats[youtube] = do_youtube(tw_handle)

            #page.goto(URL)
            #page.waitForTimeout(60000)
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
