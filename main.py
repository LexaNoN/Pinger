from pythonping import ping
from time import sleep

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


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
    if check is True and points >= 1:  # Border from 0
        points = points - 1
    elif check is False and points <= 5:  # To 6
        points = points + 1


logger.info("----- Start new loop! -----")
while True:
    sleep(0.5)  # Here we can add some ping addresses.
    checkip("8.8.8.8")  # Google
    checkip("1.1.1.1")  # CloudFare
    # print("Error point: " + str(points))

    if points >= 3 and errorcheck is False:
        # Lost internet
        logger.warning("Internet lost!")
        # Check ISP
        if pingmine("92.68.1.1") is False:
            if errorcheckisp is True:
                logger.warning("ISP reconnected!")
                errorcheckisp = False
            elif errorcheckisp is False:
                logger.warning("ISP lost!")
                errorcheckisp = True
                # If ISP is lost, check router
                if pingmine("192.168.0.1") is False:
                    if errorcheckrouter is True:
                        logger.warning("Router reconnected!")
                        errorcheckrouter = False
                    elif errorcheckrouter is False:
                        logger.warning("Router lost!")
                        errorcheckrouter = True
        errorcheck = True
    elif points <= 3 and errorcheck is True:
        logger.warning("Internet resume!")
        errorcheck = False
