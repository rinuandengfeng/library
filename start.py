from appoinment_seat import LibrarySeat

from log import logger

import time

import schedule


appointment_seat = LibrarySeat()

def start() -> None:
    try:
        #每天18:59进行登录
        # schedule.every(10).day.at("18:59").do(appointment_seat.logins)   
        # #每天19:00进行预约     
        # schedule.every(10).day.at("19:00").do(appointment_seat.seat_start)
        schedule.every().day.at("18:59").do(appointment_seat.logins)
        schedule.every().day.at("19:00").do(appointment_seat.seat_start)
        while True:
            schedule.run_pending()
            time.sleep(5)
            print("111")
    except Exception as e:
        logger.error(e)
    

if __name__ == "__main__":
    start()

