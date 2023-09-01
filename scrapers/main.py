import os
import re
import time
import csv
import pickle
import random
import argparse
import pandas as pd
from tqdm import tqdm

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


url = "https://www.youtube.com/results?search_query="

label_dict = {'Technology': ['smartphone', 'pc hardware', 'computer gpu', 'laptop review'],
              'Educational-programming': ['python tutorials', 'c++ tutorials', 'c tutorials'],
              'Educational': ['math', 'statistics'],
              'Gaming': ['pc games review'],
               }




        
        


