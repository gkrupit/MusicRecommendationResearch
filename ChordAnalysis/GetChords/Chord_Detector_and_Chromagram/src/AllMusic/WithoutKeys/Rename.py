import os

path = os.getcwd()
filenames = os.listdir(path)

for filename in filenames:
  new_filename = filename[0].upper() + filename[1:]
  os.rename(filename, new_filename) 
