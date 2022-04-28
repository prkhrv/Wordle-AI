from abc import abstractmethod
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
from numpy import random
from time import sleep

class Bot:

  """
  \\TODO: Write class docstring
  
  
  """

  def __init__(self):
    """
    Creates instance of Chrome Web Driver and initializes state with official guess list

    """
    
    self.driver = webdriver.Chrome(ChromeDriverManager().install())
    self.state = np.loadtxt('wordle-answers.txt', dtype = str)
    self.pattern = "a"*5

  def open_wordle(self):
      """
      Navigates to official NYT Wordle site

      """

      # Navigate to NYT Wordle site
      self.driver.get('https://www.nytimes.com/games/wordle/index.html')
      # Minimize tab
      self.actions = ActionChains(self.driver)
      self.actions.click().perform()
      sleep(2.5)

  @abstractmethod
  def play_wordle():
    pass
