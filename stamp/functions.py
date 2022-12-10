def _split(currentelement, splitby):
  if type(currentelement) == str:
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

def display(text, texvar):
  print(text[texvar])