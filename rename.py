"""
Get the correct syntax to rename the function name. Otherwise we're all good :)
"""

import idaapi
import idautils

def read_input():
  """
  This function reads the results of the output generated by the function_compare.py script and creates a dictionary of the function to be renamed and what it should be
  renamed to.
  """
  input_file_name= 'input_to_rename_function.txt'
  with open(input_file_name, 'rU') as f:
    functions= f.readlines()

  renamed_functions= {}
  for i in functions:
    t1= i.split("\t")
    src= t1[0].split('<')
    address= src[1]
    
    dest= t1[1].split('>')

    #Use the destination filename as the value. This is what you need to rename your function to.
    renamed_functions[address]= dest[0]

  return renamed_functions

def rename_functions_ida(renamed_functions):
  for key, val in renamed_functions.items():
    val= 'library_'+val
    #MakeNameEx(funcaddress,"glibc_"+name,SN_NOWARN)

#Wait for analysis to complete
idaapi.autoWait()

#Read results of function_compare.py which compares functions inside a binary with functions in all the existing libraries
renamed_functions= {}
renamed_functions= read_input()

#Rename functions in IDA for the source binary
rename_functions_ida(renamed_functions)

#Exit IDA
idc.Exit(0)