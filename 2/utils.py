#! /usr/bin/python

def collapse(llist):
  collapsedList = []
  for item in llist:
    if item not in collapsedList:
      collapsedList.append(item)
  return collapsedList
  
def wordWrap(length, line):
  if len(line) < length:
    return line
  else:
    head = line[:length] + '\n'
    tail = line[length:]
    if len(tail) > length:
      q = wordWrap(length, tail)
      return head + q
  return head + tail
    
