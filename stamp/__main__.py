import core
import utilities
import sys
import argparse

VERSION = "0.3"

def versionstamp():
  colors = utilities.getcolors()

  if colors["supported"]:
    print("STaMP Interpreter - " + VERSION + " - " + colors["green"] + "Extended " + colors["blue"] + "Colors" + colors["reset"])
  else:
    print("STaMP Interpreter - " + VERSION)

  return colors

def runinterpreter(config, text):
  colors = versionstamp()
  
  print("\x1b[?25l", end="")
  
  # setup
  history = {}
  flags = {
    "fileopen" : False,
    "fileopen.text" : "",
    "fileopen.name" : "",
    "exit" : False
  }
  done = False


  while not done:
    endstrarr = []
    position = 0
    maxstrlength = 0

    while True:
      narr = endstrarr.copy()

      narr.append(" ")

      if len(narr) > maxstrlength:
        maxstrlength = len(narr)

      if flags["fileopen"]:
        print("\r. " + "".join(narr[:position]) + colors["background"] + narr[position] + colors["reset"] + "".join(narr[position+1:]) + " "*(maxstrlength-len(narr)), end="")
      else:
        narr = utilities.syntaxhighlight(narr, text)
      
        print("\r#> " + "".join(narr[:position]) + colors["background"] + narr[position] + colors["reset"] + "".join(narr[position+1:]) + " "*(maxstrlength-len(narr)), end="")

      
      char = utilities.getch()

      if char == "enter":
        if flags["fileopen"]:
          print("\r. " + "".join(narr) + " "*(maxstrlength-len(narr)))
        else:
          print("\r#> " + "".join(narr) + " "*(maxstrlength-len(narr)))
        break
      elif char == "left":
        if position > 0:
          position -= 1
      elif char == "right":
        if position < len(endstrarr):
          position += 1
      elif char == "backspace":
        if position > 0:
          endstrarr.pop(position-1)
          position -= 1
      elif char == "delete":
        if position < len(endstrarr):
          endstrarr.pop(position)
      elif char in ["up", "down"]:
        pass
      else:
        position += 1
        endstrarr.insert(position-1, char)

    text, history, flags = core.run("".join(endstrarr), history, text, flags, config)

    if flags["exit"]:
      done = True

  print("\x1b[?25h", end="")

def loadconfig(filename, defaultconfig):
  ftext = None
  try:
    with open(filename, "r") as file:
      ftext = file.read()
  except:
    utilities.error("file error", "file '" + filename + "' does not exist")
    return defaultconfig

  lines = ftext.split("\n")
  for line in range(len(lines)):
    cline = lines[line].split(":")
    if len(cline) < 2:
      utilities.error("value error", "line '" + str(line+1) + "' is not formatted correctly")
      return defaultconfig
    configitem = cline[0]
    setto = utilities.converttotype(":".join(cline[1:]))
    if configitem in defaultconfig:
      defaultconfig[configitem] = setto
    else:
      utilities.error("value error", "the set value on line '" + str(line+1) + "' does not exist")
      return defaultconfig

  # if everything goes as planned
  return defaultconfig

if __name__ == "__main__":
  config = {
    "merge.char" : "",
  }
  text = {}
  runinterpretertf = True
  
  parser = argparse.ArgumentParser(prog = 'stamp')
  
  parser.add_argument('--config', '-c', help='loads a config file', dest="configfile")

  parser.add_argument('--loadstr', '-l', help='loads a string value from a file', nargs=2, metavar=("STRNAME", "FILENAME"), dest="loadstr")

  parser.add_argument('--version', '-v', help='displays the version', action="store_true")

  args = parser.parse_args()

  if args.configfile:
    config = loadconfig(args.configfile, config)

  if args.loadstr:
    try:
      with open(args.loadstr[1], "r") as file:
        toloadtext = file.read()
      text[args.loadstr[0]] = toloadtext
    except:
      utilities.error("file error", "file '" + args.loadstr[1] + "' does not exist")
      sys.exit()

  if args.version:
    runinterpretertf = False
    versionstamp()

  if runinterpretertf:
    try:
      runinterpreter(config, text)
    except Exception as e:
      print("\x1b[?25h", end="")
      raise e