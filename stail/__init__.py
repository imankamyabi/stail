from pyfiglet import Figlet
from colorama import init
from colorama import Fore, Back, Style
import click

init()

__version__ = '0.1.1'

@click.group()
def main():
  # f = Figlet(font='slant')
  # print(f.renderText('Stail'))
  # print("Version: " + Fore.GREEN + __version__)
  # print(Style.RESET_ALL)
  # hello()
  pass


@main.command()
def version():
  """Print Stail version"""
  f = Figlet(font='slant')
  print(f.renderText('Stail'))
  print("Version: " + Fore.GREEN + __version__)
  print(Style.RESET_ALL)