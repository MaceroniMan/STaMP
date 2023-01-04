import utilities

def _split(currentelement, splitby):
  if type(currentelement) == str:
    if splitby == "$CHAR$":
      return [*currentelement]
    else:
      return currentelement.split(splitby)
  else:
    rlist = []
    for item in currentelement:
      rlist.append(_split(item, splitby))
    return rlist

def split(text, textstr, texvar):
  text[texvar] = _split(text[texvar], textstr)
  return text

def _merge(currentelement, charby):
  if type(currentelement) == str:
    return None
  else:
    endr = []
    for item in currentelement:
      mergeresult = _merge(item, charby)
      if mergeresult == None:
        return charby.join(currentelement)
      else:
        endr.append(mergeresult)
    return endr

def merge(text, textstr, textvar):
  text[texvar] = _merge(text[textvar], textstr)
  return text  

def _prettyprint(item, indentlvl, c):
  rstr = ""
  if type(item) == str:
    item = item.replace("\n", c["blue"] + "\\n\n" + c["yellow"])
    return " "*indentlvl + c["yellow"] + "'" + item + "'" + c["reset"] + ","
  else:
    rstr += " "*indentlvl + "[" + "\n"
    for i in item:
      ritem = _prettyprint(i, indentlvl+1, c)
      rstr += ritem + "\n"
    rstr += " "*indentlvl + "],"

  return rstr

def display(text, textvar):
  c = utilities.getcolors()
  pp = _prettyprint(text[texxtvar], 0, c)[:-1]
  print(pp)

def _strip(currentelement):
  if type(currentelement) == str:
    return currentelement.strip()
  else:
    rlist = []
    for item in currentelement:
      rlist.append(_strip(item))
    return rlist

def strip(text, textvar):
  text[textvar] = _strip(text[textvar])
  return text

def _append(currentelement, addchar, prepend):
  if type(currentelement) == str:
    if prepend:
      return addchar + currentelement
    else:
      return currentelement + addchar
  else:
    rlist = []
    for item in currentelement:
      rlist.append(_append(item))
    return rlist

def append(text, textstr, textvar, prepend=False):
  text[textvar] = _append(text[textvar], textstr, prepend)
  return text