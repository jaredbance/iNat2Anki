import requests
import genanki
#import datetime
import urllib
import sys
import os
from random import randint

# Function to fetch observation from iNaturalist API
def fetchObservation(observation_id):
    url = "https://api.inaturalist.org/v1/observations/" + observation_id
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['results'][0] 

def downloadPhotos(observation_data):
    photos = observation_data['observation_photos']
    photo_paths = []
    id = observation_data['id']
    i = 0
    for photo in enumerate(photos):
        #print(photo[1]['photo']['url'])
        square_img_url = photo[1]['photo']['url']
        img_url = square_img_url.replace('square', 'original')
        img_name = f"observation_{id}_{i}_{os.path.basename(img_url)}"
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
      {'name': 'addtionalQuestions'},
      {'name': 'addtionalAnswers'},
    ],
    templates=[
      {
        'name': 'Taxon Card',
        'qfmt': '{{photos}}<br><br><p>Addtional Questions:</p>{{addtionalQuestions}}<br><br>{{type:scientificName}}',
        'afmt': '{{photos}}<br><br> {{type:scientificName}}<br><br><div style="font-size: 30px;"><i>{{scientificName}}</i></div><br><br><p style="display:inline">Common Name: </p>{{commonName}}<br><br><p>Addtional Answers:</p>{{addtionalAnswers}}',
      },
    ])
  
  return my_model

def createDeck():
  # Define a unique ID for the deck
  deck_id = randomNumber(10)

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

  commonName = ""
  if 'preferred_common_name' in observation_data['taxon']:
    commonName = observation_data['taxon']['preferred_common_name']

  my_note = genanki.Note(
    model=my_model,
    fields=[taxon_photos_html, observation_data['taxon']['name'], commonName, "- None", " - None"])

  # Add the note to the deck
  my_deck.add_note(my_note)
  
def saveDeck(my_deck, taxon_photo_paths):
  # Define the package and add the deck to it
  my_package = genanki.Package(my_deck)

  my_package.media_files = taxon_photo_paths

  # Save the package to a file
  my_package.write_to_file('output.apkg')

def randomNumber(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

if __name__ == "__main__":
    file = open('input.txt', 'r')
    line = ""
    model = createAnkiModel()
    deck = createDeck()
    media = []
    line = file.readline()
    while line != "":
      observation_data = fetchObservation(line.strip())
      photo_paths = downloadPhotos(observation_data)
      createNote(photo_paths, observation_data, model, deck)
      print(photo_paths)
      media.extend(photo_paths)
      line = file.readline()
    saveDeck(deck, media)
    deleteMediaFiles(media)
    