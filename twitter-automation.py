#importing dependencies
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import wait
from selenium.webdriver.support.ui import WebDriverWait
import itertools
from bs4 import BeautifulSoup
import requests
import googleapiclient
from googleapiclient import discovery
from googleapiclient import errors