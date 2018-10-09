#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import time
try:
    import urllib.request
except:
    import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class RealComp:
    def __init__(self):
        try:
            chromeOptions = Options()
            chromeOptions.add_argument('--headless')
            chromeOptions.add_argument('--hide-scrollbars')
            chromeOptions.add_argument('--disable-gpu')
            chromeOptions.add_argument('--log-level=3')
            chromeOptions.add_argument('--no-sandbox')
            chromeOptions.add_argument('--disable-dev-shm-usage')

            chromeOptions.add_argument('--disable-extensions')
            chromeOptions.add_argument('--profile-directory=Default')
            chromeOptions.add_argument("--disable-infobars")
            chromeOptions.add_argument("--incognito")
            chromeOptions.add_argument("--disable-plugins-discovery")
            chromeOptions.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(chrome_options=chromeOptions)
            self.driver.set_window_size(1119, 870)
            self.driver.set_window_position(420, 1)
            self.driver.implicitly_wait(1)
        except:
            path = 'C://chromedriver.exe'
            chromeOptions = Options()
            chromeOptions.add_argument('--disable-extensions')
            chromeOptions.add_argument('--profile-directory=Default')
            chromeOptions.add_argument("--disable-infobars")
            chromeOptions.add_argument("--incognito")
            chromeOptions.add_argument("--disable-plugins-discovery")
            chromeOptions.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(chrome_options=chromeOptions, executable_path=path)
            self.driver.set_window_size(1119, 870)
            self.driver.set_window_position(420, 1)
            self.driver.implicitly_wait(1)
        print("Chrome Started.")

    def login(self):

        self.driver.implicitly_wait(10)
        self.driver.get("https://www.facebook.com/")
        print("Logging In.")
        self.driver.find_element_by_id('email').send_keys("16umm011@lnmiit.ac.in")
        self.driver.find_element_by_id('pass').send_keys("16umm011")
        self.driver.find_element_by_id("pass").send_keys(u'\ue007')
        # self.driver.find_element_by_xpath ('//*[@id="appMountPoint"]/div/div/div/div[2]/div/div/ul/li[1]/div/a/div/div').click()
        print("Logged In.")
        # sys.exit()

    def srt(self, name, duration, snap, description, timeNdate, link):
        desc = ""
        for d in description:
            desc += d.text
        if not os.path.exists(self.folderName + "/" + str(name) + ".srt"):
            f = open(str(name) + ".vtt", "r")  # , encoding='utf-8')
            fh = open(str(name) + ".srt", "w")  # , encoding='utf-8')
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
            os.rename(str(name) + ".srt", self.folderName + "/" + str(name) + ".srt")
            os.remove(str(name) + ".vtt")
            # downloading image
            try:
                try:
                    urllib.request.urlretrieve(snap, str(name) + ".jpg")
                except:
                    urllib.urlretrieve(snap, str(name) + ".jpg")
                os.rename(str(name) + ".jpg", self.folderName + "/" + str(name) + ".jpg")
            except Exception as e:
                print(e)
                pass
            # saving json data
            j = {'data': []}
            j['data'].append({'duration': duration})
            j['data'].append({'title': self.title})
            j['data'].append({'description': desc})
            j['data'].append({'timestamp': timeNdate})
            j['data'].append({'url': link})
            with open(str(name) + '.json', 'w') as outfile:
                json.dump(j, outfile)
            os.rename(str(name) + '.json', self.folderName + "/" + str(name) + '.json')

            try:
                # , encoding='utf-8'
                with open(self.folderName + "/" + str(name) + ".title", "w") as f:
                    f.write(self.title)
            except:
                pass

        else:
            print("Already Donwnloaded Skipping This.")
            os.remove(str(name) + ".vtt")

    def first_scrap(self):
        # self.login ()
        try:
            with open("urls" + sys.argv[1] + ".txt", 'r') as f:
                linkstovisit = f.read().split("\n")
        except:
            with open("urls.txt", 'r') as f:
                linkstovisit = f.read().split("\n")

        for link in linkstovisit:
            # time.sleep (2)
            try:
                vid = link.split('/')
                if (vid[-1] == ""):
                    # print("Found /")
                    n = str(vid[-4]) + "_" + str(vid[-2])
                    # print(n)
                else:
                    n = str(vid[-3]) + "_" + str(vid[-1])
                    # print (n)
                try:
                    self.folderName = "fb-data-" + sys.argv[1]
                except:
                    self.folderName = "fb-data"

                if not os.path.exists(self.folderName):
                    os.mkdir(self.folderName)

                try:
                    self.mainFilePath = self.folderName + sys.argv[1] + "/" + str(n)
                except:
                    self.mainFilePath = self.folderName + "/" + str(n)

                if os.path.exists(self.mainFilePath + ".nosub"):
                    print("Skipping (nosub) -> " + n)
                else:
                    if os.path.exists(self.mainFilePath + ".srt"):
                        print("Skipping (srt) -> " + n)
                    else:
                        self.driver.implicitly_wait(10)
                        self.driver.get(link)
                        # print (link)
                        time.sleep(10)
                        try:
                            self.driver.find_element_by_id('expanding_cta_close_button').click()
                            # print("Closed")
                        except Exception as e:
                            print(e)
                            pass
                        time.sleep(2)
                        self.driver.find_element_by_id('u_0_j').click()
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
                                timeNdate = soup.find('abbr').attrs['title']
                            except:
                                timeNdate = ""
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
                            fh = open(str(n) + ".nosub", "w")
                            fh.close()
                            os.rename(str(n) + ".nosub", self.mainFilePath + ".nosub")
                            desc = ""
                            for d in description:
                                desc += d.text
                            # downloading image
                            try:
                                try:
                                    urllib.request.urlretrieve(snap, str(n) + ".jpg")
                                except:
                                    urllib.urlretrieve(snap, str(n) + ".jpg")
                                os.rename(str(n) + ".jpg", self.mainFilePath + ".jpg")
                            except Exception as e:
                                print(e)
                                pass
                            # saving json data
                            j = {'data': []}
                            j['data'].append({'duration': duration})
                            j['data'].append({'title': self.title})
                            j['data'].append({'description': desc})
                            j['data'].append({'timestamp': timeNdate})
                            j['data'].append({'url': link})
                            with open(str(n) + '.json', 'w') as outfile:
                                json.dump(j, outfile)
                            os.rename(str(n) + '.json', self.mainFilePath + '.json')
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

                            subsFileHandler = open(n + ".vtt", "w")  # ,encoding='utf-8')
                            subsFileHandler.write(requestObjectv)
                            subsFileHandler.close()
                            print("Subtitle Found For: " + n)
                            self.srt(n, duration, snap, description, timeNdate, link)
            except Exception as e:
                print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
                pass

        print("Closing Chrome.")
        self.driver.close()
        self.driver.quit()


mv = RealComp()
mv.first_scrap()
