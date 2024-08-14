import os

def getNameOrigins(species):
    for file_path in __get_txt_files('resources/mycomatch'):
        with open(file_path, 'r', encoding="latin1") as file:
            lines = file.readlines()
        
        # Flag to track when we've found the "LATIN NAME(S) " line
        latin_name_found = False
        
        for line in lines:
            line = line.strip()
            
            # Check if the line contains "LATIN NAME(S) " followed by another string
            if not latin_name_found and line.startswith("LATIN NAME(S)  " + species):
                latin_name_found = True
                continue
            
            # Once we find the "LATIN NAME(S) ", we search for the "NAME ORIGIN" line
            if latin_name_found and line.startswith("NAME ORIGIN"):
                return line[len("NAME ORIGIN")+2:]
    
    # If no match is found, return None
    return "None"

def __get_txt_files(folder_path):
    # List to store the paths of .txt files
    txt_files = []
    
    # Loop through all files in the specified directory
    for filename in os.listdir(folder_path):
        # Check if the file ends with .txt
        if filename.endswith('.txt'):
            # Append the full path of the file to the list
            txt_files.append(os.path.join(folder_path, filename))
    
    return txt_files
