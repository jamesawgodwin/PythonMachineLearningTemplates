#pip install cerberus (add !pip for notebook issues)
#pip install python-magic-win64
from winmagic import magic
import glob
#import cerberus //json specific
import os
import re
import dateutil.parser as dparser

def check_file_type(file):
    """check for file types in directory"""
    file_type = magic.from_file(file)
    print(f"File type: {file_type}")
    
def check_missing_data(file):
    """check for missing relevant data"""
    if bool(re.search('cheese|ham|blah', open(file).read().lower())):
        print(f"Relevant data: \t Present")
    else: 
        print(f"Relevant data: \t Missing")
        
def get_upload_date(file):
    """Find and parse the date uploaded"""
    with open(file, "r") as f:
        for line in f.readlines():
            if line.startswith("Cheese is good"):
                date = dparser.parse(line,fuzzy=True).date()
                print(f"Date uploaded: \t {date}")
                
def check_relevant_data(directory):
    """function to check the file type and presence of search term"""
    
    for file in glob.glob(f"{directory}*.txt"):
        print(f"Validation info for {file}:")

        check_file_type(file)
        check_relevant_data(file)
        get_upload_date(file)
        
        print("\n")
