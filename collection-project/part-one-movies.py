import requests
import csv
import json

base_url = 'https://www.loc.gov/free-to-use'

#print(base_url)

parameters = {
    'fo' : 'json'
}

#print(parameters)

collection = 'motion-picture-theaters'

collection_response = requests.get(base_url + '/' + collection, params=parameters)

print('Free to Use Movie Theaters:',collection_response.url)

movie_collection_json = collection_response.json()

with open("collection.json", "w") as f:
    json.dump(movie_collection_json, f)

#print (movie_collection_json)

print(movie_collection_json.keys())

for object in movie_collection_json['content']['set']['items']:
    print(object)

print('Number of Free to Use Movie Theater Objects:',len(movie_collection_json['content']['set']['items']))

#print(movie_collection_json['content']['set']['items'][0].keys())

movie_collection_list_filepath = '../si676-assignment-1.1/movie_collection_list.csv'
headers = ['image','link','title']

with open(movie_collection_list_filepath, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for item in movie_collection_json['content']['set']['items']:
        item['title'] = item['title'].rstrip()
        writer.writerow(item)
    print('Exported CSV data to:',movie_collection_list_filepath)