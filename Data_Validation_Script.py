#pip install cerberus (add !pip for notebook issues)
#pip install python-magic-win64
from winmagic import magic
import glob
#import cerberus

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("/Users/jagth/Documents/ML/Datasets"))

# Any results you write to the current directory are saved as output.
#check filetypes and loop through directory
def data_validation(missingdata, rel_filepath):
    """
    This function takes as an arg the word you are searching for in a file or directory.
    It outputs the type of file and whether the search word is present.

    >>>data_validation("cheese")
    >>>/filepath/file.txt is UTF-8 Unicode text, with long lines, with no line terminators (json)
    cheese data missing in file.txt
    """
    for file in glob.glob(rel_filepath):
        print(f"Validation info for {file}:")
    #check filetype
        file_type = magic.from_file(file)
        print(f"File type is: \t {file_type}")
        
    #check for missing data
    if missingdata.lower() in open(file).read():
        print(f"{missingdata} data: \t Present")
    else:
        print(f"{missingdata} data: \t Missing")
        
    #get the city    
    with open(file,"r") as f:
        city = 'Seattle'
        for line in f.readlines():
            #if line.startswith(city):
            if city in line:
                print(f"File info: \t {line}")
            else:
                print(f"{file} does not have: \t {city}")
data_validation('Position', "/Users/jagth/Documents/ML/Datasets/*")