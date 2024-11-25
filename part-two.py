import requests
import csv
import json
import os
import glob
from os.path import join

def regenerate_library_collection(libraries_csv):
    collection_items = list()
    with open(libraries_csv, 'r', newline='', encoding='utf-8') as f:
        data = csv.DictReader(f)
        for row in data:
            row_dictionary = dict()
            for field in data.fieldnames:
                row_dictionary[field] = row[field]
            collection_items.append(row_dictionary)
        return collection_items

libraries_csv = os.path.join('..', 'si676-assignment-1.1', 'library_collection_list.csv')


#print('Filepath:',libraries_csv)

libraries_set_list = regenerate_library_collection(libraries_csv)

#print(libraries_set_list)

libraries_set_list[0]

loc_url = 'https://www.loc.gov/pictures'

#print(loc_url)

parameters = {
    'fo' : 'json'
}

#print(parameters)

item_metadata_directory = os.path.join('..', 'si676-assignment-1.1', 'item-metadata')

collection_project_directory = os.path.join('..', 'si676-assignment-1.1', 'collection-project')

if os.path.isdir(item_metadata_directory):
    print('I have located', item_metadata_directory)
else:
    os.mkdir(item_metadata_directory)
    print('I have created', item_metadata_directory)

item_count = 0
error_count = 0
file_count = 0

data_directory = 'collection-project'
object_metadata_directory = 'item-metadata'
object_metadata_file_prefix = 'item_metadata'
json_suffix = '.json'

for object in libraries_set_list:
    if object['link'] == 'link':
        continue
    if '?' in object['link']:
        object_id = object['link']
        short_id = object['link'].split('/')[2]
        object_metadata = requests.get(loc_url + object_id, params={'fo':'json'})
        print('requested', object_metadata.url, object_metadata.status_code)
        if object_metadata.status_code != 200:
            print('requested', object_metadata.url, object_metadata.status_code)
            error_count += 1
            continue
        try:
            object_metadata.json()
        except:
            error_count += 1
            print('No available JSON data')
            continue
        file_out = os.path.join('..', data_directory, item_metadata_directory, str(object_metadata_file_prefix + '-' + short_id + json_suffix))
        with open(file_out, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(object_metadata.json()['item']))
            file_count += 1
            print('Created file to:', file_out)
        item_count += 1
    else:
        object_id = object['link']
        short_id = object['link'].split('/')[2]
        object_metadata = requests.get(loc_url + object_id, params={'fo':'json'})
        print('requested', object_metadata.url, object_metadata.status_code)
        if object_metadata.status_code != 200:
            print('requested', object_metadata.url, object_metadata.status_code)
            error_count += 1
            continue
        try:
            object_metadata.json()
        except:
            error_count += 1
            print('No available JSON data')
            continue
        file_out = os.path.join('..', data_directory, item_metadata_directory, str(object_metadata_file_prefix + '-' + short_id + json_suffix))
        with open(file_out, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps(object_metadata.json()['item']))
            file_count += 1
            print('Created file to', file_out)
        item_count += 1

print('Status Log')
print('Items Pulled from LOC:', item_count)
print('Error Count', error_count)
print('Files Created', file_count)

main_directory = os.path.join('/', 'Users', 'gcpbr', 'Documents', 'umich', 'courses', 'si676', 'si676-assignment-1.1')
project_directory = 'collection-project'
files_directory = 'item-files'
metadata_directory = 'item-metadata'

loc_files = os.path.join(main_directory, project_directory, files_directory)
print('Searching for', loc_files)

if os.path.isdir(loc_files):
    print('I have located', loc_files)
else:
    os.mkdir(loc_files)
    print('I have created', loc_files)

search_for_metadata_here = os.path.join(metadata_directory)

print(search_for_metadata_here)

metadata_file_list = glob.glob(search_for_metadata_here + '/*.json')

print(metadata_file_list)

object_image_urls = list()
count = 0

for object in metadata_file_list:
    with open(object, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
#print(metadata.keys())
        #image_url_number = len(metadata['link'])
        image_url = metadata['link'][-1]
        object_image_urls.append(image_url)
        count += 1

print(f'Identified {str(count)} object URLs')