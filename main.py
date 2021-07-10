from pythonping import ping
from time import sleep

import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info("----- Start new loop! -----")

points = 0.0  # Counter of ping error's
errorcheck = False  # Switch for logger
errorcheckisp = False  # Switch for ISP
errorcheckrouter = False  # Switch for Router
oserrorcheck = False  # Switch for OSError


def pingmine(ip):  # Try to check
    global oserrorcheck
    try:  # Sometimes windows create exception. Ok boomer
        response_list = ping(ip, count=2)
    except OSError:
        if oserrorcheck is False:
            logger.error("OS can't connect")
            oserrorcheck = True
        return False
    oserrorcheck = False

    return not response_list.rtt_max_ms == 2000


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
        if check is True and points >= 1:  # Border from 0
            points = points - 1
        elif check is False and points <= 5:  # To 6
            points = points + 1


print("Programm has been started!")

while True:
    sleep(0.5)  # Here we can add some ping addresses.
    checkip("8.8.8.8")  # Google
    checkip("1.1.1.1")  # CloudFare
    print("Error point: " + str(points))

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
