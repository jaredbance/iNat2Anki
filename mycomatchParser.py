import os

class mycoMatchFields:
    def __init__(self, nameOrigin, spores, edibility, taste, odour, habitat):
        self.nameOrigin = nameOrigin
        self.spores = spores
        self.edibility = edibility
        self.taste = taste
        self.odour = odour
        self.habitat = habitat

def __getNameOrigins(species):
    return __getField(species, "NAME ORIGIN")

def __getSpores(species):
    return __getField(species, "SPORE DEPOSIT")

def __getEdibility(species):
    return __getField(species, "EDIBILITY")

def __getTaste(species):
    return __getField(species, "TASTE")

def __getOdour(species):
    return __getField(species, "ODOR")

def __getHabitat(species):
    return __getField(species, "HABITAT")

def getFields(species, rank):
    if rank != "species":
        return None
    nameOrigins = __getNameOrigins(species)
    if nameOrigins == None:
        return None # species doesn't exist in myco match
    spores = __getSpores(species)
    edibility = __getEdibility(species)
    taste = __getTaste(species)
    odour = __getOdour(species)
    habitat = __getHabitat(species)
    return mycoMatchFields(nameOrigins, spores, edibility, taste, odour, habitat)

def __getField(species, field):
    for file_path in __get_txt_files('resources/mycomatch'):
        with open(file_path, 'r', encoding="latin1") as file:
            lines = file.readlines()
        
        # Flag to track when we've found the "LATIN NAME(S) " line
        latin_name_found = False
        
        for line in lines:
            line = line.strip()
            
            # Check if the line contains "LATIN NAME(S) " followed by species name
            if not latin_name_found and line.startswith("LATIN NAME(S)  " + species):
                latin_name_found = True
                continue
            
            # Once we find the "LATIN NAME(S) ", we search for the other line
            if latin_name_found and line.startswith(field):
                return line[len(field)+2:].replace('^', '')
    
    # If no match is found, return None
    return None

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
