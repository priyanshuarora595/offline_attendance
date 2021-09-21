from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import  IntervalTrigger
from crontab import CronTab
import time 
import os
import glob
from offline_attendance.settings import MEDIA_ROOT



def update_media_func():
    
    folder = str(MEDIA_ROOT)
    folder = folder.replace('\\','/')
    folder+='/'
    files = os.listdir(folder)
    for file in files:
        print(file)
        os.remove(folder+str(file))
    

def update():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_media_func,'interval',days=1)
    scheduler.start()