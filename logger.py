from termcolor import colored
from colorama import init
import datetime
init()

class log:
    def info(event):
    	d = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    	print(colored('[{}] {}',"cyan").format(d,event))

    def error(event):
    	d = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    	print(colored('[{}] {}','red').format(d,event))

    def warning(event):
    	d = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    	print(colored('[{}] {}',"yellow").format(d,event))

    def success(event):
    	d = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    	print(colored('[{}] {}',"green").format(d,event))


if __name__ == '__main__':
    log.info('------------------------------------------------')
    log.info('                   Python3 Logger')
    log.info('                 Written by @ymmxl')
    log.info('------------------------------------------------')
