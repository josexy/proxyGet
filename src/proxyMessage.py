
import random
import proxy_config
from termcolor import colored
from colorama import init
class Color(object):
    Red='red'
    Green='green'
    Blue='blue'
    Yellow='yellow'
    Magenta='magenta'
    White='white'
    Cyan='cyan'

    On_Red='on_'+Red
    On_Green='on_'+Green
    On_Blue='on_'+Blue
    On_Yellow='on_'+Yellow
    On_Magenta='on_'+Magenta
    On_White='on_'+White
    On_Cyan='on_'+Cyan

    Bold='bold'
    Dark='dark'
    Underline='underline'
    Blink='blink'
    Reverse='reverse'
    Concealed='concealed'

    @staticmethod
    def random_fgcolor():
        return random.choice([Color.Red,Color.Blue,Color.Green,Color.Cyan,Color.Magenta,Color.White,Color.Yellow])

init(autoreset=True)
class CliMessage(object):
    @staticmethod
    def print(text,fgcolor=None,attr=None,bgcolor=None):
        if not proxy_config.OUTPUT_DEBUG_INFO:
            return
        if attr:
            attr=[attr]
        print(colored(text,fgcolor,bgcolor,attr))
    @staticmethod
    def put_status(status='successed'):
        """
        print a status text with color
        :param status: successed,failed,warning
        :return:
        """
        if not proxy_config.OUTPUT_DEBUG_INFO:
            return
        status_code=''
        status_color=()
        if status.strip()=='successed':
            status_code='*'
            status_color=(Color.Green,None,[Color.Bold])
        elif status.strip()=='warning':
            status_code='-'
            status_color=(Color.Yellow,None,[Color.Bold])
        else:
            status_code='!'
            status_color=(Color.Red,None,[Color.Bold])
        print(colored(f'[{status_code}]',*status_color),end=' ')
    @staticmethod
    def print_with_status(text,fgcolor=None, attr=None, bgcolor=None,status='successed'):
        CliMessage.put_status(status)
        CliMessage.print(text,fgcolor,attr,bgcolor)
