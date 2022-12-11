import core
import utilities
import os

VERSION = "0.1"

def runinterpreter():
  colors = utilities.getcolors()

  if colors["supported"]:
    print("STaMP - " + VERSION + " - " + colors["green"] + "Extended Colors" + colors["reset"])
  else:
    print("STaMP - " + VERSION)
  
  print("\x1b[?25l", end="")
  
  # setup
  history = {}
  text = {}
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

    text, history, flags = core.run("".join(endstrarr), history, text, flags)

    if flags["exit"]:
      done = True

  print("\x1b[?25h", end="")

if __name__ == "__main__":
  runinterpreter()