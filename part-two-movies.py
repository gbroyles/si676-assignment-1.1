import requests
import csv
import json
import os
import glob
from os.path import join

def regenerate_movies_collection(movies_csv):
    collection_items = list()
    with open(movies_csv, 'r', newline='', encoding='utf-8') as f:
        data = csv.DictReader(f)
        for row in data:
            row_dictionary = dict()
            for field in data.fieldnames:
                row_dictionary[field] = row[field]
            collection_items.append(row_dictionary)
        return collection_items

movies_csv = os.path.join('..', 'si676-assignment-1.1', 'movie_collection_list.csv')


#print('Filepath:',movies_csv)

movies_set_list = regenerate_movies_collection(movies_csv)

#print(movies_set_list)

movies_set_list[0]

loc_url = 'https://www.loc.gov'

#print(loc_url)

parameters = {
    'fo' : 'json'
}

#print(parameters)

item_metadata_directory = os.path.join('..', 'si676-assignment-1.1', 'movie-item-metadata')

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
object_metadata_directory = 'movie-item-metadata'
object_metadata_file_prefix = 'movie-item_metadata'
json_suffix = '.json'

for object in movies_set_list:
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
files_directory = 'movie-item-files'
metadata_directory = 'movie-item-metadata'

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
        image_url_number = len(metadata['image_url'])
        image_url = metadata['image_url'][-1]
        object_image_urls.append(image_url)
        count += 1

print(f'Identified {str(count)} object URLs')

object_image_urls

movies_set_list_with_images = list()

for object in metadata_file_list:
    with open(object, 'r', encoding='utf-8') as object_info:
        object_metadata = json.load(object_info)
        object_metadata_dictionary = dict()
        object_metadata_dictionary['item_URI'] = object_metadata['id']
        try:
            object_metadata_dictionary['lccn'] = object_metadata['library_of_congress_control_number']
        except:
            object_metadata_dictionary['lccn'] = None
        object_metadata_dictionary['title'] = object_metadata['title']
        object_metadata_dictionary['image_URL_large'] = object_metadata['image_url'][-1]

        movies_set_list_with_images.append(object_metadata_dictionary)

print(movies_set_list_with_images[0])
print(object_metadata_dictionary.keys())

item_count = 0
error_count = 0
file_count = 0

image_file_prefix = 'img_'

for object in movies_set_list_with_images:
        image_url = object['image_URL_large']
        short_id = object['item_URI'].split('/')[-2]
        print('Searching for', image_url)
        item_count += 1

        r = requests.get(image_url)
        if r.status_code == 200:
            image_out = os.path.join('/', 'Users', 'gcpbr', 'Documents', 'umich', 'courses', 'si676', 'si676-assignment-1.1', 'collection-project', 'movie-item-files', str(image_file_prefix + short_id + '.jpg'))
            with open(image_out, 'wb') as file:
                file.write(r.content)
                print('File Created',image_out)
                file_count += 1

print('Status Log')
print('Files Pulled from LOC:',item_count)
print('Error Count:',error_count)
print('Files Completed:',file_count)