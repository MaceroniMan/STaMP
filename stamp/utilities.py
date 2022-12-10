import os
import re
import sys
import string

try:
  import msvcrt
except:
  import tty, termios

try:
  import colorama
except:
  pass

def getcolors():
  colors = {
    "red" : "",
    "yellow" : "",
    "green" : "",
    "bold" : "",
    "blue" : "",
    "reset" : "",
    "background" : "",
    "underline" : ""
  }
  
  if os.name == "nt":
    try:
      colors["reset"] = colorama.Style.RESET_ALL
      colors["bold"] = colorama.Style.BRIGHT
      colors["green"] = colorama.Fore.GREEN
      colors["yellow"] = colorama.Fore.YELLOW
      colors["blue"] = colorama.Fore.CYAN
      colors["red"] = colorama.Fore.RED
      colors["background"] = colorama.Back.WHITE
      colors["underline"] = colorama.Style.UNDERLINE
    except:
      pass
  else:
    colors["reset"] = "\033[0m"
    colors["bold"] = "\033[01m"
    colors["green"] = "\033[32m"
    colors["yellow"] = "\033[93m"
    colors["blue"] = "\033[96m"
    colors["red"] = "\033[31m"
    colors["background"] = "\033[0;30;47m"
    colors["underline"] = "\033[4m"

  return colors

def windows():
  if os.name == 'nt':
    return True
  else:
    return False

def varchars():
  return string.ascii_letters + "_"

def _link():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ord(ch)

def _wink():
  ord(msvcrt.getch())

def getch():
  winkeycodes = {
    "224,72" : "up",
    "224,80" : "down",
    "224,75" : "left",
    "224,77" : "right",
    "13" : "enter",
    "9" : "tab",
    "8" : "backspace"
  }
  linkeycodes = {
    "127" : "backspace",
    "13" : "enter",
    "9" : "tab",
    "27,91,65" : "up",
    "27,91,66" : "down",
    "27,91,68" : "left",
    "27,91,67" : "right"
  }
  if os.name == "nt":
    keycode = _wink()
    if keycode == 224:
      secondkeycode = str(keycode) + "," + str(_wink())
      if secondkeycode in winkeycodes:
        return winkeycodes[secondkeycode]
      else:
        return chr(keycode)
    else:
      if str(keycode) in winkeycodes:
        return winkeycodes[str(keycode)]
      else:
        return chr(keycode)
  else:
    keycode = _link()
    if keycode == 27:
      secondkeycode = str(keycode) + "," + str(_link()) + "," + str(_link())
      if secondkeycode in linkeycodes:
        return linkeycodes[secondkeycode]
      else:
        return chr(keycode)
    else:
      if str(keycode) in linkeycodes:
        return linkeycodes[str(keycode)]
      else:
        return chr(keycode)

def error(etype, etext):
  c = getcolors()
  
  print(c["red"] + etype + ": " + etext + c["reset"])

def syntaxhighlight(text, textvar):

  matches = re.finditer(r'(ON|AT)|(EXIT|SPLIT|MERGE|OPEN|CLOSE|DISPLAY)|(:)|(".*")|(newline|space)|(\w*)', "".join(text))

  c = getcolors()
  
  for match in matches:
    mgps = match.groups()
    spn = match.span(0)
    if mgps[0] != None:
      text[spn[0]] = c["green"] + text[spn[0]]
      text[spn[1]-1] = text[spn[1]-1] + c["reset"]
      #print(mgps[0] + " OP")
    elif mgps[1] != None:
      text[spn[0]] = c["blue"] + text[spn[0]]
      text[spn[1]-1] = text[spn[1]-1] + c["reset"]
      #print(mgps[1] + " FCTN")
    elif mgps[2] != None:
      text[spn[0]] = c["blue"] + text[spn[0]]
      text[spn[1]-1] = text[spn[1]-1] + c["reset"]
      #print(mgps[2] + " SYMB")
    elif mgps[3] != None:
      text[spn[0]] = c["yellow"] + text[spn[0]]
      text[spn[1]-1] = text[spn[1]-1] + c["reset"]
      #print(mgps[3] + " STR")
    elif mgps[4] != None:
      text[spn[0]] = c["yellow"] + text[spn[0]]
      text[spn[1]-1] = text[spn[1]-1] + c["reset"]
      #print(mgps[4] + " RPLARG")
    elif mgps[5] in textvar:
      text[spn[0]] = c["bold"] + text[spn[0]]
      text[spn[1]-1] = text[spn[1]-1] + c["reset"]
      #print(mgps[5] + " VAR")
    elif not mgps[5] in [" ", "", None]:
      text[spn[0]] = c["underline"] + text[spn[0]]
      text[spn[1]-1] = text[spn[1]-1] + c["reset"]
      #print(mgps[5] + " INVLDVAR")

  return text