import csv
import re
import json
import glob
import os
from os.path import join

current_file_path = os.getcwd()

print(current_file_path)

metadata_file_path = os.path.join('collection-project','item-metadata')

print(metadata_file_path)

file_count = 0

for file in glob.glob('../si676-assignment-1.1/collection-project/item-metadata/item_metadata-*.json'):
    file_count += 1
    print(file)

print('Located',file_count,'Metadata Files')

list_of_item_metadata_files = list()
for file in glob.glob('../si676-assignment-1.1/collection-project/item-metadata/item_metadata-*.json'):
    list_of_item_metadata_files.append(file)

#print(list_of_item_metadata_files)

print(len(list_of_item_metadata_files))

#list_of_item_metadata_files.sort()

#for file in list_of_item_metadata_files:
    #print(file)

with open(list_of_item_metadata_files[1], 'r', encoding='utf-8') as item:
    print('The File in Question:',list_of_item_metadata_files[0],'\n')

    item_data = json.load(item)

    for element in item_data.keys():
        print(element,':',item_data[element])

print(item_data.keys())

#(['source_created', 'restriction', 'other_number', 'resource_links', 'title', 'related_items', 'medium_brief', 'service_medium', 'collections', 'part_of_group', 'stmt_of_responsibility', 'other_titles', 'link', 'other_control_numbers', 'notes', 'modified', 'summary', 'formats', 'marc', 'mediums', 'group_has_items', 'thumb_gallery', 'rights_information', 'display_offsite', 'related_names', 'created_published', 'title_translation', 'id', 'contents', 'raw_collections', 'call_number', 'sort_date', 'subjects', 'source_modified', 'part_of', 'terms', 'reproduction_number', 'repository', 'service_low', 'date', 'created', 'control_number', 'place', 'creators', 'created_published_date'])

print('\ndate:',item_data['date'], type(item_data['date']))

print('\nformat:',item_data['format'], type(item_data['format']))

#Example for a Single Sample Item

collection_info_csv = 'collection_items_data.csv'

headers = ['source_file', 'item_id', 'title', 'date', 'source_url', 'phys_format', 'dig_format', 'rights']

with open(list_of_item_metadata_files[1], 'r', encoding='utf-8') as data:
    item_data = json.load(data)
    source_file = str(file)
    try:
        item_id = item_data['library_of_congress_control_number']
    except:
        item_id = item_data['link'].split('/')[-2]
    title = item_data['title']
    date = item_data['date']
    source_url = item_data['link']
    try:
        phys_format = item_data['format'][0]
    except:
        phys_format = 'Not found'
    try:
        dig_format = item_data['online_format'][0]
    except:
        dig_format = 'Not found'
    #mime_type = item_data['mime_type']
    try:
        rights = item_data['rights_information']
    except:
        rights = 'Undetermined'

    row_dict = dict()
    row_dict['source_file'] = source_file
    row_dict['item_id'] = item_id
    row_dict['title'] = title
    row_dict['date'] = date
    row_dict['source_url'] = source_url
    row_dict['phys_format'] = phys_format
    row_dict['dig_format'] = dig_format
    row_dict['rights'] = rights
    print('created row dictionary:',row_dict)

    # write to the csv
    with open(collection_info_csv, 'w', encoding='utf-8') as fout:
        writer = csv.DictWriter(fout, fieldnames=headers)
        writer.writeheader()
        writer.writerow(row_dict)
        print('Created:',collection_info_csv)

collection_info_csv = 'collection_items_data.csv'


headers = ['source_file', 'item_id', 'title', 'date', 'source_url', 'phys_format', 'dig_format', 'rights']

with open(list_of_item_metadata_files[1], 'r', encoding='utf-8') as data:

    item_data = json.load(data)

print(item_data['image_url'][3])

#Now Trying the Rest of the Items

items_data_file = os.path.join('collection_items_data.csv')

if os.path.isfile(items_data_file):
    os.unlink(items_data_file)
    print('removed',items_data_file)

row_dict = ()

from datetime import date

date_string_for_today = date.today().strftime('%Y-%m-%d') # see https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

print(date_string_for_today)

collection_info_csv = os.path.join('..','si676-assignment-1.1','collection-project','collection_items_data.csv')
file_count = 0
items_written = 0
error_count = 0

# add in a couple of extras for Omeka, including item type and date uploaded

headers = ['item_type', 'date_uploaded', 'source_file', 'creator', 'title', 'creation_date', 'source_url', 'format', 'description', 'digital_id', 'rights_advisory', 'language', 'location', 'notes', 'subject', 'image_url']

for file in list_of_item_metadata_files:
    file_count += 1
    print('opening',file)
    with open(file, 'r', encoding='utf-8') as item:
        try:
            item_data = json.load(item)
        except:
            print('error loading',file)
            error_count += 1
            continue

        item_type = 'Item'
        date_uploaded = date_string_for_today
        #source of data
        source_file = str(file)
        try:
            digital_id = item_data['digital_id'][0].split()[-1]
        except:
            digital_id = 'Digital ID Unavailable'
        title = item_data['title']
        try:
            description = item_data['summary']
        except:
            description = 'Description Unavailable'
        try:
            language = item_data['language']
        except:
            language = 'Language Information Unavailable'
        try:
            location = item_data['location']
        except:
            location = 'Location Information Unavailable'
        try:
            notes = item_data['notes']
        except:
            notes = 'Notes Unavailable'
        try:
            subject = item_data['subject']
        except:
            subject = 'Subject Information Unavailable'
        try:
            source_url = item_data['link']
        except:
            source_url = 'Source URL Unavailable'
        try:
            format = item_data['format'][0]
        except:
            format = 'Format Information Unavailable'
        try:
            creator = item_data['contributor_names']
        except:
            creator = 'Creator Information Unavailable'
        try:
            rights_advisory = item_data['rights_advisory']
        except:
            rights_advisory = 'Undetermined'
        try:
            image_url = item_data['image_url'][2]
        except:
            image_url = 'Did not identify a URL.'
        try:
            creation_date = item_data['date']
            date_pattern = r'\b(\d{4}-\d{2}-\d{2})\b'
            date_match = re.search(date_pattern, item_data['date'])
            if date_match:
                date = date_match.group(1)
            else:
                creation_date = 'Creation Date Unavailable'
        except:
            creation_date = 'Creation Date Unavailable'

        row_dict = dict()

        # look for the item metadata, assign it to the dictionary;
        # start with some basic elements likely (already enumerated in the headers list) :
        row_dict['item_type'] = item_type
        row_dict['date_uploaded'] = date_uploaded
        row_dict['source_file'] = source_file
        row_dict['digital_id'] = digital_id
        row_dict['title'] = title
        row_dict['description'] = description
        row_dict['language'] = language
        row_dict['location'] = location
        row_dict['title'] = title
        row_dict['notes'] = notes
        row_dict['subject'] = subject
        row_dict['source_url'] = source_url
        row_dict['format'] = format
        row_dict['creator'] = creator
        row_dict['rights_advisory'] = rights_advisory
        row_dict['image_url'] = image_url
        row_dict['creation_date'] = creation_date

        # write to the csv
        with open(collection_info_csv, 'a', encoding='utf-8', newline='') as file_out:
            writer = csv.DictWriter(file_out, fieldnames=headers)
            if items_written == 0:
                writer.writeheader()
            writer.writerow(row_dict)
            items_written += 1
            print('Appending',item_id)

print('\n\n--- LOG ---')
print('Created',collection_info_csv)
print('with',items_written,'items')
print(error_count,'Errors (info not written)')