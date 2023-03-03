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
    "underline" : "",
    "supported" : False
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
      colors["supported"] = True
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
    colors["supported"] = True


  return colors

def windows():
  if os.name == 'nt':
    return True
  else:
    return False

def converttotype(string):
  try:
    return int(string)
  except:
    return str(string)

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
  return ord(msvcrt.getch())

def getch():
  winkeycodes = {
    "224,72" : "up",
    "224,80" : "down",
    "224,75" : "left",
    "224,77" : "right",
    "224,83" : "delete",
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
      # just to make the delete key work
      if secondkeycode == "27,91,51":
        if _link() == 126:
          return "delete"
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

  matches = re.finditer(r'(ON|TO|WITH)|(EXIT|SPLIT|MERGE|OPEN|CLOSE|DISPLAY|STRIP|APPEND|PREPEND|TABLE):|{(\d*)}|(".*"|<.*>)|(newline|space|\*|charecter)|(\w*)', "".join(text))

  c = getcolors()
  
  for match in matches:
    mgps = match.groups()
    spn = match.span(0)
    if mgps[0] != None:
      for i in range(spn[0], spn[1]):
        text[i] = c["blue"] + text[i]
        text[i+1] = text[i+1] + c["reset"]
      #print(mgps[0] + " OP")
    elif mgps[1] != None:
      for i in range(spn[0], spn[1]):
        text[i] = c["blue"] + text[i]
        text[i+1] = text[i+1] + c["reset"]
      #print(mgps[1] + " FCTN")
    elif mgps[2] != None:
      for i in range(spn[0], spn[1]):
        text[i] = c["green"] + text[i]
        text[i+1] = text[i+1] + c["reset"]
      #print(mgps[2] + " NUMB")
    elif mgps[3] != None:
      for i in range(spn[0], spn[1]):
        text[i] = c["yellow"] + text[i]
        text[i+1] = text[i+1] + c["reset"]
      #print(mgps[3] + " STR")
    elif mgps[4] != None:
      for i in range(spn[0], spn[1]):
        text[i] = c["yellow"] + text[i]
        text[i+1] = text[i+1] + c["reset"]
      #print(mgps[4] + " RPLARG")
    elif mgps[5] in textvar:
      for i in range(spn[0], spn[1]):
        text[i] = c["bold"] + text[i]
        text[i+1] = text[i+1] + c["reset"]
      #print(mgps[5] + " VAR")
    elif not mgps[5] in [" ", "", None]:
      for i in range(spn[0], spn[1]):
        text[i] = c["underline"] + text[i]
        text[i+1] = text[i+1] + c["reset"]
      #print(mgps[5] + " INVLDVAR")

  return text