from pyfiglet import Figlet
from colorama import init
from colorama import Fore, Back, Style

init()

__version__ = '0.1.0'

def main():
  f = Figlet(font='slant')
  print(f.renderText('Stail'))
  print("Version: " + Fore.GREEN + __version__)
  print(Style.RESET_ALL)