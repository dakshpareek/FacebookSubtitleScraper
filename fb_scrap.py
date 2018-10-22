#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import os
import re
import sys
import time
import urllib.request

# import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class RealComp:
    firsttime = 'true'

    def __init__(self):
        options = Options()
        options.add_argument ('--headless')
        options.add_argument('--hide-scrollbars')
        options.add_argument('--disable-gpu')
        options.add_argument('--log-level=3')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Chnage Path
        # path = '/usr/bin/chromedriver'
        path = 'C://chromedriver.exe'
        #
        # print ("Starting Chrome Headless.")
        #
        try:
            self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        except:
            self.driver = webdriver.Chrome(chrome_options=options)
        #
        print("Chrome Started.")
        #
        #
        #
        # self.driver = webdriver.Chrome (path)
        # # #self.driver.maximize_window ()

    def login(self):

        self.driver.implicitly_wait(1)
        self.driver.get("https://www.facebook.com/")
        print("Logging In.")
        self.driver.find_element_by_id('email').send_keys("16umm011@lnmiit.ac.in")
        self.driver.find_element_by_id('pass').send_keys("16umm011")
        self.driver.find_element_by_id("pass").send_keys(u'\ue007')
        # self.driver.find_element_by_xpath ('//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/ul/li[1]/div/a/div/div').click()
        print("Logged In.")
        # sys.exit()

    def srt(self, name, duration, snap, description, timeNdate, link, olink):
        desc = ""
        for d in description:
            desc += d.text
        if not os.path.exists("fb-data-" + sys.argv[1] + "/" + str(name) + ".srt"):
            f = open("fb-data-" + sys.argv[1] + "/" + str(name) + ".vtt", "r")  # , encoding='utf-8')
            fh = open("fb-data-" + sys.argv[1] + "/" + str(name) + ".srt", "w")  # , encoding='utf-8')
            count = 1
            # Removing WEBVTT Header line.
            for line in f.readlines():
                if line[:6] == 'WEBVTT':
                    continue
                line = re.sub(r'(:\d+)\.(\d+)', r'\1,\2', line)
                if line == '\n':
                    fh.write("\n" + str(count) + "\n")
                    count += 1
                else:
                    fh.write(line.strip() + "\n")
            f.close()
            fh.close()
            os.rename(str(name) + ".srt", "fb-data-" + sys.argv[1] + "/" + str(name) + ".srt")
            os.remove(str(name) + ".vtt")
            # downloading image
            try:
                urllib.request.urlretrieve(snap, str(name) + ".jpg")
                os.rename(str(name) + ".jpg", "fb-data-" + sys.argv[1] + "/" + str(name) + ".jpg")
            except Exception as e:
                print(e)
                pass
            # saving json data
            j = {'data': []}
            j['data'].append({'duration': duration})
            j['data'].append({'title': self.title})
            j['data'].append({'description': desc})
            j['data'].append({'timestamp': timeNdate})
            j['data'].append({'url': olink})
            with open("fb-data-" + sys.argv[1] + "/" + str(name) + '.json', 'w') as outfile:
                json.dump(j, outfile)
            os.rename(str(name) + '.json', "fb-data-" + sys.argv[1] + "/" + str(name) + '.json')

            try:
                # , encoding='utf-8'
                with open("fb-data-" + sys.argv[1] + "/" + str(name) + ".title", "w") as f:
                    f.write(self.title)
            except:
                pass

        else:
            print("Already Donwnloaded Skipping This.")
            os.remove(str(name) + ".vtt")

    def first_scrap(self):
        # self.login ()

        with open("urls" + sys.argv[1] + ".txt", 'r') as f:
            linkstovisit = f.read().split("\n")

        for link in linkstovisit:
            # time.sleep (2)

            try:
                olink = link
                vid = link.split('/')
                if (vid[-1] == ""):
                    # print("Found /")
                    n = str(vid[-4]) + "_" + str(vid[-2])
                    # print(n)
                else:
                    n = str(vid[-3]) + "_" + str(vid[-1])
                    # print (n)
                if os.path.exists("fb-data-" + sys.argv[1] + "/" + str(n) + ".nosub"):
                    print("Skipping (nosub) -> " + n)
                else:
                    if os.path.exists("fb-data-" + sys.argv[1] + "/" + str(n) + ".srt"):
                        print("Skipping (srt) -> " + n)
                    else:
                        self.driver.implicitly_wait(1)
                        self.driver.get(link)
                        # print (link)

                        try:
                            try:
                                try:
                                    self.driver.execute_script("arguments[0].scrollIntoView();",
                                                               self.driver.find_element_by_id('u_0_m'))
                                    self.driver.find_element_by_id('u_0_m').click()
                                except:
                                    self.driver.execute_script("arguments[0].scrollIntoView();",
                                                               self.driver.find_element_by_id('u_0_j'))
                                    self.driver.find_element_by_id('u_0_j').click()
                            except:
                                self.driver.execute_script("arguments[0].scrollIntoView();",
                                                           self.driver.find_element_by_id('u_0_m'))
                                self.driver.find_element_by_id('u_0_m').click()
                        except:
                            try:
                                self.driver.implicitly_wait(.31)
                                self.driver.find_element_by_id('expanding_cta_close_button').click()
                                try:
                                    try:
                                        self.driver.execute_script("arguments[0].scrollIntoView();",
                                                                   self.driver.find_element_by_id('u_0_m'))
                                        self.driver.find_element_by_id('u_0_m').click()
                                    except:
                                        self.driver.execute_script("arguments[0].scrollIntoView();",
                                                                   self.driver.find_element_by_id('u_0_j'))
                                        self.driver.find_element_by_id('u_0_j').click()
                                except:
                                    self.driver.execute_script("arguments[0].scrollIntoView();",
                                                               self.driver.find_element_by_id('u_0_m'))
                                    self.driver.find_element_by_id('u_0_m').click()
                                # print("Closed")
                            except Exception as e:
                                self.driver.implicitly_wait(1)
                                pass
                        time.sleep(2)
                        # tm=self.driver.find_element_by_id('_2yu7')
                        # print(tm)
                        # time.sleep(1000)
                        try:
                            data = self.driver.page_source
                            soup = BeautifulSoup(data, "lxml")
                            soup1 = soup.find("track")
                            try:
                                title = soup.find("span", {'class': '_50f7'})
                            except:
                                title = ""
                            try:
                                timeNdate = soup.find('abbr').attrs['data-utime']
                                a = datetime.datetime.fromtimestamp(int(timeNdate))
                                timeNdate = a.strftime("%Y-%m-%d, %H:%M:%S")
                            except:
                                timeNdate = ""
                            print(timeNdate)
                            try:
                                duration = soup.find('div', {'class': '_2yu7'}).attrs['aria-valuemax']
                            except:
                                duration = ""
                            try:
                                snap = soup.find('img', {'class': '_4lpf'}).attrs['src'].replace('amp;', '')
                            except:
                                snap = ""
                            try:
                                description = soup.find('div', {'class': '_5pbx userContent _3576'}).findAll(
                                    'p')  # .text
                            except:
                                description = []
                            # print(description)
                        except:
                            pass
                        try:
                            self.title = title.text
                        except:
                            self.title = ""
                            # print("Error")
                            pass
                        # sys.exit()
                        print(self.title)
                        # print(soup1)

                        if soup1 == None:
                            print("No Subtitle Found")
                            fh = open("fb-data-" + sys.argv[1] + "/" + str(n) + ".nosub", "w")
                            fh.close()
                            # os.rename (str (n) + ".nosub", "fb-data-"+sys.argv[1]+"/" + str (n) + ".nosub")
                            desc = ""
                            for d in description:
                                desc += d.text
                            # downloading image
                            try:
                                urllib.request.urlretrieve(snap, str(n) + ".jpg")
                                os.rename(str(n) + ".jpg", "fb-data-" + sys.argv[1] + "/" + str(n) + ".jpg")
                            except Exception as e:
                                print(e)
                                pass
                            # saving json data
                            j = {'data': []}
                            j['data'].append({'duration': duration})
                            j['data'].append({'title': self.title})
                            j['data'].append({'description': desc})
                            j['data'].append({'timestamp': timeNdate})
                            j['data'].append({'url': olink})
                            with open("fb-data-" + sys.argv[1] + "/" + str(n) + '.json', 'w') as outfile:
                                json.dump(j, outfile)
                            # os.rename(str(n) + '.json', "fb-data-" + sys.argv[1] + "/" + str(n) + '.json')
                            '''
                            try:
                                with open ("fb-data-"+sys.argv[1]+"/" + str (n) + ".title", "w") as f:
                                    f.write(self.title)
                            except Exception as e:
                                print(e)
                                pass
                            '''
                        else:
                            link = soup1.attrs['src']
                            # print(link)
                            self.driver.get(link)
                            # time.sleep(100)
                            requestObjectv = self.driver.page_source
                            requestObjectv = requestObjectv.encode('cp1252', "ignore").decode("utf-8", "ignore")
                            # print(requestObjectv)

                            subsFileHandler = open("fb-data-" + sys.argv[1] + "/" + n + ".vtt",
                                                   "w")  # ,encoding='utf-8')
                            subsFileHandler.write(requestObjectv)
                            subsFileHandler.close()
                            print("Subtitle Found For: " + n)
                            self.srt(n, duration, snap, description, timeNdate, link, olink)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                pass

        print("Closing Chrome.")
        self.driver.close()
        self.driver.quit()


mv = RealComp()
mv.first_scrap()
