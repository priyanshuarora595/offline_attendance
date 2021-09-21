import os
import glob
from settings import MEDIA_ROOT

folder = str(MEDIA_ROOT)
files = glob.glob(folder)

def my_scheduled_job():
  print(files)