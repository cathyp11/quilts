import requests
from bs4 import BeautifulSoup
import json
import csv
import re


query = {'q': 'native american quilts', 'rows': 200, 'api_key': 'MDPQchPlMHyfSuLeiosNu5zfPpZwMqXi0OgFxiIP'}
url  = requests.get('https://api.si.edu/openaccess/api/v1.0/search', params = query)

smith = url.json()

nmaiList = []

for row in smith['response']['rows']:
	# create dictionary for each row
	rowDic = {
		'title': None, 
		'culture/people': None, 
		'media/materials': None, 
		'techniques': None, 
		'dimensions': None, 
		'date created': None, 
		'place': None, 
		'continent': None,
		'country': None,
		'state': None,
		'county': None,
		'city': None,
		'image_url': None
		}

	# Title
	rowDic['title'] = row['title']

	# Culture/People
	for name in row['content']['freetext']['name']:
		if name['label'] == 'Culture/People':
			rowDic['culture/people'] = name['content'] 
	
	# Media/Materials
	if 'physicalDescription' in row['content']['freetext'].keys():
		for des in row['content']['freetext']['physicalDescription']:
			if des['label'] == 'Media/Materials':
				rowDic['media/materials'] = des['content'] 

		# Techniques 
			if des['label'] == 'Techniques':
				rowDic['techniques'] = des['content'] 

		# Dimensions
			if des['label'] == 'Dimensions':
				rowDic['dimensions'] = des['content'] 

	# Date Created
	if 'date' in row['content']['freetext'].keys():
		rowDic['date created'] = row['content']['freetext']['date'][0]['content']
	# else:
	# 	rowDic['date created'] = None

	# Place
	if 'place' in row['content']['freetext'].keys():
		rowDic['place'] = row['content']['freetext']['place'][0]['content']


	# geolocations
	if 'geoLocation' in row['content']['indexedStructured'].keys():
		for geo in row['content']['indexedStructured']['geoLocation']:
			# Continent
			if 'L1' in geo.keys():
				rowDic['continent'] = geo['L1']['content']

			# Country
			if 'L2' in geo.keys():
				rowDic['country'] = geo['L2']['content']

			# State
			if 'L3' in geo.keys():
				rowDic['state'] = geo['L3']['content']

			# County
			if 'L4' in geo.keys():
				rowDic['county'] = geo['L4']['content']

			# City
			if 'L5' in geo.keys():
				rowDic['city'] = geo['L5']['content']

	# access link to each quilt
	if 'guid' in row['content']['descriptiveNonRepeating'].keys():
		page_link = row['content']['descriptiveNonRepeating']['guid']
		page_detail = requests.get(page_link)
		soup = BeautifulSoup(page_detail.text, 'html.parser')
		if soup.find('div',{"class":"mediaplayer-wrapper"}):
			div = soup.find('div',{"class":"mediaplayer-wrapper"})			

			# Image Link
			if 'id=' in div.find('img')['src']:
				img_link = re.findall(r'id=(.*)', div.find('img')['src'])[0]
			else:
				img_link = div.find('img')['src']

			rowDic['image_url'] = img_link

		elif soup.find('a',{"class":"fullImageLink"}):
			a = soup.find_all("a", class_="fullImageLink")[0]		
			# print(a)
			# Image Link
			img_link = a.find('img')['src']
			# print(img_link)

			rowDic['image_url'] = img_link
	# print(img_link)
		
	nmaiList.append(rowDic)

	keys = nmaiList[0].keys()

	with open('data/smithsonian_links.csv', 'w', newline='') as output_file:
	    dict_writer = csv.DictWriter(output_file, keys)
	    dict_writer.writeheader()
	    dict_writer.writerows(nmaiList)

