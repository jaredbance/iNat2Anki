import requests
import genanki
#import datetime
import urllib
import sys
import os

# Function to fetch observation from iNaturalist API
def fetchObservation(observation_id):
    url = "https://api.inaturalist.org/v1/observations/" + observation_id
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['results'][0] 

def downloadPhotos(observation_data):
    photos = observation_data['observation_photos']
    photo_paths = []
    i = 0
    for photo in enumerate(photos):
        #print(photo[1]['photo']['url'])
        square_img_url = photo[1]['photo']['url']
        img_url = square_img_url.replace('square', 'original')
        img_name = f"observation_{i}_{os.path.basename(img_url)}"
        img_path = os.path.join('media', img_name)
        urllib.request.urlretrieve(img_url, img_path)
        photo_paths.append(img_path)
        i = i + 1
    return photo_paths

def deleteMediaFiles(photo_paths):
    for file in photo_paths:
        os.remove(file)

def createAnkiModel():
  # Define a unique ID for the model
  model_id = 1607392319

  # Define the model for the card
  my_model = genanki.Model(
    model_id,
    'Simple Model with Typing',
    fields=[
      {'name': 'photos'},
      {'name': 'scientificName'},
      {'name': 'commonName'},
    ],
    templates=[
      {
        'name': 'Card 1',
        'qfmt': '{{photos}}<br><br> {{type:scientificName}}',
        'afmt': '{{photos}}<br><br> {{type:scientificName}}<br><br>{{scientificName}}',
      },
    ])
  
  return my_model

def createDeck():
  # Define a unique ID for the deck
  deck_id = 2059400110

  # Create the deck
  my_deck = genanki.Deck(
    deck_id,
    'Sample Deck')
  
  return my_deck

def createNote(taxon_photo_paths, observation_data, my_model, my_deck):
  # Create HTML for taxon photos
  taxon_photos_html = '<br>'.join([f'<img src="{os.path.basename(path)}">' for path in taxon_photo_paths])

  # # Create a note
  # my_note = genanki.Note(
  #   model=my_model,
  #   fields=['What is the capital of France?', 'Paris'])

  my_note = genanki.Note(
    model=my_model,
    fields=[taxon_photos_html, "test", "test"]) #scientificName, commonName])

  # Add the note to the deck
  my_deck.add_note(my_note)
  
def saveDeck(my_deck, taxon_photo_paths):
  # Define the package and add the deck to it
  my_package = genanki.Package(my_deck)

  my_package.media_files = taxon_photo_paths

  # Save the package to a file
  my_package.write_to_file('output.apkg')

if __name__ == "__main__":
    #print(sys.version)
    observation_data = fetchObservation("194502260")
    photo_paths = downloadPhotos(observation_data)
    model = createAnkiModel()
    deck = createDeck()
    createNote(photo_paths, observation_data, model, deck)
    saveDeck(deck, photo_paths)
    deleteMediaFiles(photo_paths)
    print(photo_paths)