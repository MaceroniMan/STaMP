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
  text[textvar] = _merge(text[textvar], textstr)
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
  pp = _prettyprint(text[textvar], 0, c)[:-1]
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
      rlist.append(_append(item, addchar, prepend))
    return rlist

def append(text, textstr, textvar, prepend=False):
  text[textvar] = _append(text[textvar], textstr, prepend)
  return text

def _change(currentelement, editstr):
  if type(currentelement) == str:
    return None
  else:
    rlist = []
    for item in currentelement:
      rv = _change(item, editstr)
      if rv == None:
        return eval("currentelement[" + editstr + "]")
      else:
        rlist.append(rv)
    return rlist

def change(text, textvar, editnum):
  text[textvar] = _change(text[textvar], editnum)
  return text

def _table(currentelement):
  if type(currentelement) == str:
    return None
  else:
    rstr = ""
    for item in currentelement:
      rs = _table(item)
      if rs == None:
        for i in currentelement:
          rstr += i + "  "
      else:
        rstr += rs
    return rstr + "\n"

def table(text, textvar):
  printvalue = _table(text[textvar])
  if printvalue == None:
    print(text[textvar])
  else:
    print(printvalue)

def _replace(currentelement, findstr, replacewith):
  if type(currentelement) == str:
    return currentelement.replace(findstr, replacewith)
  else:
    rlist = []
    for item in currentelement:
      rlist.append(_replace(item, findstr, replacewith))
    return rlist

def replace(text, textvar, findstr, replacewith):
  text[textvar] = _replace(text[textvar], findstr, replacewith)
  return text