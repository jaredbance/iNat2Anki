# iNatFungi2Anki

This script converts any iNaturalist observation of fungi into an Anki flashcard. 

Additional details scraped from [MycoMatch](https://www.mycomatch.com/) are included to enhance the study of taxonomy.

# Requirments
1) Python 3.x
3) Git installed on your computer

# Pre-Setup (you only have to do these steps once)
1) Open up Terminal (MAC) or Command Prompt (WINDOWS)
1) Clone the repo `git clone https://github.com/jaredbance/iNatFungi2Anki.git`
2) Install dependancies from "requirements.txt":

   Mac:
   ```
   python -m venv myenv
   source myenv/bin/activate
   python -m pip install -r requirements.txt
   ```
   Windows:
   ```
   python -m venv myenv
   myenv\Scripts\activate
   python -m pip install -r requirements.txt
   ```

# Usage
1) Open up Terminal (MAC) or Command Prompt (WINDOWS) and navigate to the folder you cloned the repo to
2) Pull latest version of the script `git pull`
4) Load your virtual environment:

   Mac:
   ```
   source myenv/bin/activate
   ```
   Windows:
   ```
   myenv\Scripts\activate
   ```
6) Add iNat observation IDs to the `input.txt` file. One ID per line.
   - For example, the iNat ID for observation `https://www.inaturalist.org/observations/230398888` is `230398888`
8) Run the script in the terminal
   ```bash
   python main.py
   ```
9) Outputted Anki deck is saved to "output.apkg"

# Sample Flashcard
Front of card | Back of card
--- | --- 
![alt text](https://raw.githubusercontent.com/jaredbance/iNatFungi2Anki/master/demoPics/1.png) | ![alt text](https://raw.githubusercontent.com/jaredbance/iNatFungi2Anki/master/demoPics/2.png)
