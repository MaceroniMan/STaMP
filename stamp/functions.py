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

def merge(text, textstr, texvar):
  text[texvar] = _merge(text[texvar], textstr)
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

def display(text, texvar):
  c = utilities.getcolors()
  pp = _prettyprint(text[texvar], 0, c)[:-1]
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