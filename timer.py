from  datetime import datetime
import time

"""
启动时间
"""


class Timer(object):
    def __init__(self,appointment_time,interval=5) -> None:
        
        #'15:11:11'
        self.appointment_time = datetime.strptime(appointment_time,"%H:%M:%S")
        self.interval = interval

    def start(self):
        now_time = datetime.now
        while True:
            if datetime.strptime(now_time().strftime("%H:%M:%S"),"%H:%M:%S") >= self.appointment_time:
                break
            else:
                time.sleep(self.interval)
