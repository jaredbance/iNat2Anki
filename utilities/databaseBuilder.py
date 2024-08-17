#
# THIS CODE IS MESSY. IT'S ONLY PURPOSE IS TO CREATE AND SAVE A DATABASE FROM THE MYCOMATCH TEXT FILES.
#

import os
import pickle 

UNKNOWN = "Unknown"

class mycoMatchFields:
    nameOrigin = UNKNOWN
    spores = UNKNOWN
    edibility = UNKNOWN
    taste = UNKNOWN
    odour = UNKNOWN
    habitat = UNKNOWN
    def __str__(self):
        return self.nameOrigin + " " + self.spores + " " + self.edibility + " " + self.taste + " " + self.taste + " " + self.odour + " " + self.habitat

def buildMap():
    map = {}
    # Flag to track when we've found the "LATIN NAME(S) " line
    for file_path in __get_txt_files('resources/mycomatch'):
        latin_name_found = False
        key = ""
        value = mycoMatchFields()
        with open(file_path, 'r', encoding="latin1") as file:
            lines = file.readlines()
        
        for line in lines:
            line = line.strip()
            
            # Check if the line contains "LATIN NAME(S) " followed by species name
            if not latin_name_found and line.startswith("LATIN NAME(S)"):
                latin_name_found = True
                key = __getLatinName(line)
                continue
            
            # Once we find the "LATIN NAME(S) ", we search for the other line
            if latin_name_found:
                if line.strip().isnumeric() or line.strip() == "":
                    latin_name_found = False
                    # if key in map:
                    #     print("ERROR for " + key)
                    map[key] = value
                    value = mycoMatchFields()
                    continue

                fieldType = __getFieldType(line)
                match fieldType:
                    case "ODOR":
                        value.odour = __getFieldValue(line).replace("^","")
                    case "TASTE":
                        value.taste = __getFieldValue(line).replace("^","")
                    case "EDIBILITY":
                        value.edibility = __getFieldValue(line).replace("^","")
                    case "HABITAT":
                        value.habitat = __getFieldValue(line).replace("^","")
                    case "SPORE DEPOSIT":
                        value.habitat = __getFieldValue(line).replace("^","")
                    case "NAME ORIGIN":
                        value.nameOrigin = __getFieldValue(line).replace("^","")
        map[key] = value
    return map

def __get_txt_files(folder_path):
    #return ["resources/mycomatch/gil_Origin.txt"]
    # List to store the paths of .txt files
    txt_files = []
    
    # Loop through all files in the specified directory
    for filename in os.listdir(folder_path):
        # Check if the file ends with .txt
        if filename.endswith('.txt'):
            # Append the full path of the file to the list
            txt_files.append(os.path.join(folder_path, filename))

    return txt_files

def __getLatinName(line):
    latinName = ""
    start = len("LATIN NAME(S)  ")
    count = 0
    spaceCounter = 0
    for char in line:
        count = count + 1
        if count <= start:
            continue
        if char == " ":
            spaceCounter = spaceCounter + 1
        if spaceCounter == 2:
            break
        latinName = latinName + char
    return latinName

def __getFieldValue(line):
    value = ""
    spaceCounter = 0
    start = False
    for char in line:
        if (start == False):
            if char == " ":
                spaceCounter = spaceCounter + 1
            if spaceCounter == 2:
                start = True
        else:
            value = value + char
    return value

def __getFieldType(line):
    spaceCounter = 0
    field = ""
    for char in line:
        field = field + char
        if char != " ":
            spaceCounter = 0
        else:
            spaceCounter = spaceCounter + 1

        if spaceCounter == 2:
            return field[:len(field)-2]
        
def __verify(map):
    for file_path in __get_txt_files('resources/mycomatch'):
        with open(file_path, 'r', encoding="latin1") as file:
            lines = file.readlines()
        
        for line in lines:
            line = line.strip()
            
            # Check if the line contains "LATIN NAME(S) " followed by species name
            if line.startswith("LATIN NAME(S)"):
                key = __getLatinName(line)
                if map[key] == None:
                    return "Missing " + key
    print("no missing keys")

def __verify2():
    for file_path in __get_txt_files('resources/mycomatch'):
        list = []
        with open(file_path, 'r', encoding="latin1") as file:
            lines = file.readlines()
        
        for line in lines:
            line = line.strip()
            
            # Check if the line contains "LATIN NAME(S) " followed by species name
            if line.isnumeric():
                print(line)
    #return list

def __verify3():
    lastNum = 0
    with open("numbers.txt", 'r', encoding="latin1") as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        if (int(line) - lastNum) != 1:
            print("Skipped here: " + line)
            return
        lastNum = int(line)

def saveMap(map):
    with open('myocmatch.pkl', 'wb') as f:
        pickle.dump(map, f)
        
    #with open('mycomatch.pkl', 'rb') as f:
    #    loaded_dict = pickle.load(f)

if __name__ == "__main__":
    map = buildMap()
    print(len(map))
    saveMap(map)
    #__verify(map)

