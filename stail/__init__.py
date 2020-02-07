from pyfiglet import Figlet

__version__ = '0.1.0'

def main():
  f = Figlet(font='slant')
  print(f.renderText('Stail'))