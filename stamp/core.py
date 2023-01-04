import re
import functions
import utilities

def __short(item):
  shorts = {
    "newline" : "\n",
    "space" : " ",
    "charecter" : "$CHAR$",
    "*" : "$CHAR$"
  }
  if item in shorts:
    return shorts[item]
  else:
    return None

def __parsequotes(text, strict=False):
  if text.startswith('"') and text.endswith('"'):
    return [text[1:-1], "str"]
  else:
    theshort = __short(text)
    if theshort == None:
      return None
    elif strict:
      if theshort.startswith("$") and theshort.endswith("$"):
        return [theshort, "bad"]
      else:
        return [theshort, "short"]
    else:
      return [theshort, "short"]

def __isvarname(text):
  for char in text:
    if not char in utilities.varchars():
      return False
  if __short(text) == None:
    return True
  else:
    return False

def run(line, history, text, flags, config):
  #((?P<on_cmd>\w+): (?P<on_var>\w+) ON (?P<on_arg>[\w]+|(".+")))
  #((?P<to_cmd>\w+): (?P<to_arg>[\w]+|(".+")) TO (?P<to_var>\w+))
  #((?P<ch_var>\w+)\s*(\{(?P<ch_cond>[-:]*\d*)\}))
  #((?P<sg_cmd>\w+): (?P<sg_arg>\w+))

  m = re.match(r'((?P<on_cmd>\w+): (?P<on_var>\w+) ON (?P<on_arg>[\w]+|(".+")))|((?P<to_cmd>\w+): (?P<to_arg>[\w]+|(".+")) TO (?P<to_var>\w+))|((?P<ch_var>\w+)\s*(\{(?P<ch_cond>[-:]*\d*)\}))|((?P<sg_cmd>\w+): (?P<sg_arg>\w+))', line)

  if m == None:
    currentmatch = {}
  else:
    currentmatch = m.groupdict()

  # logic just for reading starting text
  if flags["fileopen"]:
    if m == None:
      if flags["fileopen.text"] == "":
        flags["fileopen.text"] += line
      else:
        flags["fileopen.text"] += "\n" + line
    else:
      if currentmatch["sg_cmd"] == "CLOSE":
        if flags["fileopen.name"] == currentmatch["sg_arg"]:
          text[flags["fileopen.name"]] = flags["fileopen.text"]
          flags["fileopen"] = False
        else:
          utilities.error("value error", "ending name is not same as starting name")
      else:
        if flags["fileopen.text"] == "":
          flags["fileopen.text"] += line
        else:
          flags["fileopen.text"] += "\n" + line

  elif m != None:
    if currentmatch["on_cmd"] != None:
      if currentmatch["on_cmd"] == "SPLIT":
        if currentmatch["on_var"] in text:
          textstr = __parsequotes(currentmatch["on_arg"])
          if textstr != None:
            text = functions.split(text, textstr, currentmatch["on_var"])
          else:
            utilities.error("syntax error", "invalid string")
        else:
          utilities.error("value error", "variable does not exist")

      elif currentmatch["on_cmd"] == "MERGE":
        if currentmatch["on_var"] in text:
          textstr = __parsequotes(currentmatch["on_arg"], strict=True)
          mergechar = ""
          if textstr[0] == None:
            utilities.error("syntax error", "invalid string")
          elif textstr[0] != "bad":
            mergechar = textstr[0]
            text = functions.merge(text, mergechar, currentmatch["on_var"])
          else: # if it is a special short
            utilities.error("syntax error", "invalid string rep for this function")
        else:
          utilities.error("value error", "variable does not exist")

      else:
        utilities.error("function error", "the function '" + currentmatch["on_cmd"] + "' (ON) does not exist")
          
    elif currentmatch["to_cmd"] != None:
      if currentmatch["to_cmd"] == "APPEND":
        if currentmatch["to_var"] in text:
          textstr = __parsequotes(currentmatch["to_arg"], strict=True)
          mergechar = ""
          if textstr[0] == None:
            utilities.error("syntax error", "invalid string")
          elif textstr[0] != "bad":
            mergechar = textstr[0]
            text = functions.append(text, mergechar, currentmatch["to_var"], prepend=False)
          else: # if it is a special short
            utilities.error("syntax error", "invalid string rep for this function")
        else:
          utilities.error("value error", "variable does not exist")

      else:
        utilities.error("function error", "the function '" + currentmatch["to_cmd"] + "' (TO) does not exist")

      if currentmatch["to_cmd"] == "PREPEND":
        if currentmatch["to_var"] in text:
          textstr = __parsequotes(currentmatch["to_arg"], strict=True)
          mergechar = ""
          if textstr[0] == None:
            utilities.error("syntax error", "invalid string")
          elif textstr[0] != "bad":
            mergechar = textstr[0]
            text = functions.append(text, mergechar, currentmatch["to_var"], prepend=True)
          else: # if it is a special short
            utilities.error("syntax error", "invalid string rep for this function")
        else:
          utilities.error("value error", "variable does not exist")

      else:
        utilities.error("function error", "the function '" + currentmatch["to_cmd"] + "' (TO) does not exist")
      
    elif currentmatch["ch_var"] != None:
      pass
      
    elif currentmatch["sg_cmd"] != None:
      if currentmatch["sg_cmd"] == "OPEN":
        if __isvarname(currentmatch["sg_arg"]):
          flags["fileopen"] = True
          flags["fileopen.name"] = currentmatch["sg_arg"]
          flags["fileopen.text"] = ""
        else:
          utilities.error("syntax error", "invalid string")
          
      elif currentmatch["sg_cmd"] == "CLOSE":
        utilities.error("scope error", "'CLOSE' function never opened")
        
      elif currentmatch["sg_cmd"] == "DISPLAY":
        if __isvarname(currentmatch["sg_arg"]):
          if currentmatch["sg_arg"] in text:
            functions.display(text, currentmatch["sg_arg"])
          else:
            utilities.error("syntax error", "variable does not exist")
        else:
          utilities.error("syntax error", "argument must be variable")

      elif currentmatch["sg_cmd"] == "STRIP":
        if __isvarname(currentmatch["sg_arg"]):
          if currentmatch["sg_arg"] in text:
            functions.strip(text, currentmatch["sg_arg"])
          else:
            utilities.error("syntax error", "variable does not exist") # make this look better!!!
        else:
          utilities.error("syntax error", "argument must be variable")
          
      elif currentmatch["sg_cmd"] == "MERGE":
        if __isvarname(currentmatch["sg_arg"]):
          if currentmatch["sg_arg"] in text:
            text = functions.merge(text, config["merge.char"], currentmatch["sg_arg"])
          else:
            utilities.error("syntax error", "variable does not exist")
        else:
          utilities.error("syntax error", "argument must be variable")

      else:
        utilities.error("function error", "the function '" + currentmatch["sg_cmd"] + "' does not exist")
          
    else:
      utilities.error("syntax error", "no such function exists")

  elif line == "EXIT:":
    flags["exit"] = True
  else:
    utilities.error("syntax error", "invalid command")

  return text, history, flags