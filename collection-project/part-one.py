import requests
import csv
import json

base_url = 'https://www.loc.gov/free-to-use'

#print(base_url)

parameters = {
    'fo' : 'json'
}

#print(parameters)

collection = 'libraries'

collection_response = requests.get(base_url + '/' + collection, params=parameters)

print('Free to Use Libraries:',collection_response.url)

collection_json = collection_response.json()

#print (collection_json)

print(collection_json.keys())

for object in collection_json['content']['set']['items']:
    print(object)

print('Number of Free to Use Library Objects:',len(collection_json['content']['set']['items']))

#print(collection_json['content']['set']['items'][0].keys())

library_collection_list_filepath = '../si676-assignment-1.1/library_collection_list.csv'
headers = ['image','link','title']

with open(library_collection_list_filepath, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    for item in collection_json['content']['set']['items']:
        item['title'] = item['title'].rstrip()
        writer.writerow(item)
    print('Exported CSV data to:',library_collection_list_filepath)