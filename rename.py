"""
Get the correct syntax to rename the function name. Otherwise we're all good :)
"""

import idaapi
import idautils
import time

def read_input():
  """
  This function reads the results of the output generated by the function_compare.py script and creates a dictionary of the function to be renamed and what it should be
  renamed to.
  """
  input_file_name= 'input_to_rename_function.txt'
  with open(input_file_name, 'r') as f:
    functions= f.readlines()

  renamed_functions= {}
  for i in functions:
    t1= i.split("\t")
    src= t1[0].split('<')
    address= src[1]
    address= address.rstrip()
    dest= t1[1].split(',')

    """
    Use the destination filename as the value. This is what you need to rename your function to.
    """
    #renamed_functions[address]= str(dest[0])
    renamed_functions[address]= dest
  return renamed_functions

def rename_functions_ida(renamed_functions):
  single_count= 0
  multiple_count= 0
  for key, val in renamed_functions.items():
    funcname= GetFunctionName(int(key))
    if len(val) == 1 and funcname.startswith('sub_'):
      single_count+= 1
      val= 'single_'+str(single_count)
    elif len(val) > 1 and funcname.startswith('sub_'):
      multiple_count+= 1
      val= 'multiple_'+str(multiple_count)
    else:
      continue

    r1= MakeNameEx(int(key), val, SN_NOWARN)
    if r1 == 0:
      print "Renaming of %s failed" %int(key)
    else:
      print "Renaming of %s succeeded" %int(key)
  print single_count+multiple_count," functions were renamed in IDA"
  time.sleep(3)
    
#Wait for analysis to complete
idaapi.autoWait()

#Read results of function_compare.py which compares functions inside a binary with functions in all the existing libraries
renamed_functions= {}
renamed_functions= read_input()

#Rename functions in IDA for the source binary
rename_functions_ida(renamed_functions)

#Exit IDA
idc.Exit(0)
