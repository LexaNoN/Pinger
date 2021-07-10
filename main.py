from pythonping import ping
from time import sleep

import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.warning("----- Start new loop! -----")

points = 0.0  # Counter of "point's"
errorcheck = False  # Switch for logger
errorcheckisp = False
errorcheckrouter = False


def pingmine(ip):  # Try to check
    try:  # Sometimes windows create exception. Ok boomer
        response_list = ping(ip, count=2)
    except OSError:
        logger.error("OS can't connect, check console")
        return "Error"
    if not response_list.rtt_max_ms == 2000:  # 2000 - Packet loss. We can check not max, but
        return True
    elif response_list.rtt_max_ms == 2000:  # I think it be more "useful"
        return False


def checkip(ip):  # Sum point
    global points, errorcheckisp, errorcheckrouter
    check = pingmine(ip)
    if ip == "92.68.1.1":  # Default gateway of my ISP. NewApex (UA). Thanks for stability!
        if check is True and errorcheckisp is True:
            logger.warning("ISP reconnected!")
            errorcheckisp = False
            return True
        elif check is False and errorcheckisp is False:
            logger.warning("ISP lost!")
            errorcheckisp = True
            return False

    elif ip == "192.168.0.1":  # Router check
        if check is True and errorcheckrouter is True:
            logger.warning("Router reconnected!")
            errorcheckrouter = False
            return True
        elif check is False and errorcheckrouter is False:
            logger.warning("Router lost!")
            errorcheckrouter = True
            return False

    else:
        if check is True and points >= 0.5:  # Border from 0
            points = points - 0.5
        elif check is False and points <= 4:  # To 5
            points = points + 1


print("Programm has been started!")

while True:
    sleep(0.5)  # Here we can add some ping addresses.
    checkip("8.8.8.8")  # Google
    checkip("1.1.1.1")  # CloudFare
    # print("Error point: " + str(points))

    if points >= 3 and errorcheck is False:
        print("Internet lost!")
        logger.warning("Internet lost!")
        if errorcheckisp is True or checkip("92.68.1.1") is False:
            checkip("192.168.0.1")
        else:
            checkip("92.68.1.1")
        errorcheck = True
    elif points <= 3 and errorcheck is True:
        print("Internet resume!")
        logger.warning("Internet resume!")
        errorcheck = False
