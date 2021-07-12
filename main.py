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
error_check = False  # Switch for logger
error_check_isp = False  # Switch for ISP
error_check_router = False  # Switch for Router
os_error_check = False  # Switch for OSError

ISP_GATEWAY = "92.68.1.1"
LOCAL_IP = "192.168.0.1"
GOOGLE_DNS = "8.8.8.8"
CLOUDFLARE_DNS = "1.1.1.1"
SLEEP_TIME = 0.5
PACKET_LOSS = 2000
PING_COUNT = 2
POINTS_BORDER = 5


def ping_test(ip):  # Try to check
    global os_error_check
    try:  # Sometimes windows create exception. Ok boomer
        response_list = ping(ip, count=PING_COUNT)
    except OSError:
        if os_error_check is False:
            logger.error("OS can't connect")
            os_error_check = True
        return False
    os_error_check = False

    return not response_list.rtt_max_ms == PACKET_LOSS


def check_ip(ip):  # Sum point
    global points, error_check_isp, error_check_router
    check = ping_test(ip)
    if ip == ISP_GATEWAY:  # Default gateway of my ISP. NewApex (UA). Thanks for stability!
        if check and error_check_isp:
            logger.warning("ISP reconnected!")
            error_check_isp = False
            return True
        elif not check and not error_check_isp:
            logger.warning("ISP lost!")
            error_check_isp = True
            return False

    elif ip == LOCAL_IP:  # Router check
        if check and error_check_router:
            logger.warning("Router reconnected!")
            error_check_router = False
            return True
        elif not check and not error_check_router:
            logger.warning("Router lost!")
            error_check_router = True
            return False

    else:
        if check and points >= 1:  # Border from 0
            points -= 1
        elif not check and points <= POINTS_BORDER:  # To 6
            points += 1


print("Program has been started!")

while True:
    sleep(SLEEP_TIME)  # Here we can add some ping addresses.
    check_ip(GOOGLE_DNS)  # Google
    check_ip(CLOUDFLARE_DNS)  # CloudFare
    print("Error point: " + str(points))

    if points >= 3 and not error_check:
        print("Internet lost!")
        logger.warning("Internet lost!")
        if error_check_isp or not check_ip(ISP_GATEWAY):
            check_ip(LOCAL_IP)
        else:
            check_ip(ISP_GATEWAY)
        error_check = True
    elif points <= 3 and error_check:
        print("Internet resume!")
        logger.warning("Internet resume!")
        error_check = False
