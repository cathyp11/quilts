import requests
from IPython.core.display import HTML
import json
from time import sleep
import re
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import csv

# North American Indian and Native Hawaiian Quilt Collection
url = requests.get("https://quiltindex.org/view/?type=specialcolls&kid=12-91-470")

# # New England Quilt Museum Collection
# url = requests.get("https://quiltindex.org/results/?search=quilts&qproject=New%20England%20Quilt%20Museum%20Collection")

quilt_index = BeautifulSoup(url.text, 'html.parser')
quiltUL = quilt_index.find_all("ul", {"class": "quiltUL"})

# North American Indian and Native Hawaiian Quilt Collection
quilts = quiltUL[1].find_all("li", {"class": "assocQuilt"})

# # New England Quilt Museum Collection
# quilts = quiltUL[0].find_all("li", {"class": "assocQuilt"})


quiltList = []
for q in quilts:
	# creating a default dictionary for each quilt
	quiltDic = {
		'name': None,
		'date': None,
		'location': None,
		'image_url': None,
		'object label': None,
		'time period': None,
		'country': None,
		'state': None,
		'city': None,
		'county': None,
		'tribe': None,
		'desecription': None,
		'history': None,
		'width': None,
		'height': None,
		'edge shape': None,
		'corner shape': None,
		'layout': None,
		'number of quilt blocks': None,
		'size of the quilt blocks': None,
		'arrangement of quilt blocks': None,
		'spacing of quilt blocks': None,
		'motifs': None,
		'techniques': None,


	}
	name = q.find('p', attrs={'class': 'qrName'})
	quiltDic['name'] = name.text

	d = q.find('p', attrs={'class': 'qrDate'}).text
	d_range = re.sub(".*: ", "", d.split(": ",1)[1])

	if "-" in d_range:
		d1 = int(re.findall("(.*)-", d_range)[0])
		d2 = int(re.sub("(.*)(-|\/)","",d_range))
		d_final = (d1+d2) // 2
		quiltDic['date'] = d_final
	elif "/" in d_range:
		d_final = int(re.sub("(.*)(-|\/)","",d_range))
		quiltDic['date'] = d_final
	else:
		quiltDic['date'] = int(re.sub("\D","",d_range))

	lo = q.find('p', attrs={'class': 'qrLocation'}).text
	# check if there's any value for location
	if lo:
		quiltDic['location'] = lo.split(": ",1)[1]

	img = q.find('div', attrs={'class': 'quiltULImage'})['style']
	img_url = img.split("('", 1)[1].split("')")[0]
	quiltDic['image_url'] = img_url
	

	# request to retrieve from the detailed page
	index = re.findall('^(?:[^\/]*\/){4}([^\/]*)',img)[0]

	new_url = "https://quiltindex.org//view/?type=fullrec&kid=" + index

	quiltEach = requests.get(new_url)
	quilt_index = BeautifulSoup(quiltEach.text, 'html.parser')
	newDic = {}
	for p in quilt_index.select('div.info_container p'):
		if p['class'][0] == 'battingWrappersHeader':
			head = re.sub(":","",p.text.lower())
		if p['class'][0] == 'battingWrappersText':
			content = p.text.lower()
			newDic[head] = content
	
	# check each dictionary if they have the value	
	
	# object label
	if 'object label' in newDic:
		quiltDic['object label'] = newDic['object label']
	
	# time period
	if 'time period' in newDic:
		quiltDic['time period'] = newDic['time period']
	
	# country
	if "quiltmaker's country" in newDic:
		quiltDic['country'] = newDic["quiltmaker's country"]
	
	# state
	if "where the quilt was made, state" in newDic:
		quiltDic['state'] = newDic['where the quilt was made, state']
	
	# city
	if "where the quilt was made, city" in newDic:
		quiltDic['city'] = newDic['where the quilt was made, city']
	
	# county
	if "where the quilt was made, county" in newDic:
		quiltDic['county'] = newDic["where the quilt was made, county"]
	
	# Ethnic Background/Tribal Affiliation
	if "quiltmaker's ethnic background/tribal affiliation" in newDic:
		quiltDic['tribe'] = newDic["quiltmaker's ethnic background/tribal affiliation"]
	
	# Essay about this quilt
	if "essay about this quilt." in newDic:
		quiltDic['desecription'] = newDic["essay about this quilt."]
	
	# History of this quilt 
	if "describe anything about the history of the quilt that wasn't already recorded in a previous field." in newDic:
		quiltDic['history'] = newDic["describe anything about the history of the quilt that wasn't already recorded in a previous field."]
	
	# Width
	if "how wide is the quilt?" in newDic:
		quiltDic['width'] = newDic["how wide is the quilt?"]
	
	# Height
	if "how long is the quilt?" in newDic:
		quiltDic['height'] = newDic["how long is the quilt?"]
	
	# Shape of the edge
	if "shape of the edge" in newDic:
		quiltDic['edge shape'] = newDic["shape of the edge"]
	
	# Shape of the corner
	if "shape of the corner" in newDic:
		quiltDic['corner shape'] = newDic["shape of the corner"]
	
	# Quilt's Layout
	if "describe the quilt's layout" in newDic:
		quiltDic['layout'] = newDic["describe the quilt's layout"]
	
	# Number of quilt blocks
	if "number of quilt blocks" in newDic:
		quiltDic['county'] = newDic["number of quilt blocks"]
	
	# Size of the quilt blocks
	if "size of the quilt blocks" in newDic:
		quiltDic['size of the quilt blocks'] = newDic["size of the quilt blocks"]
	
	# Arrangement of quilt blocks
	if "arrangement of quilt blocks" in newDic:
		quiltDic['arrangement of quilt blocks'] = newDic["arrangement of quilt blocks"]
	
	# Spacing of quilt blocks
	if "spacing of quilt blocks" in newDic:
		quiltDic['spacing of quilt blocks'] = newDic["spacing of quilt blocks"]
	
	# Quilting designs used, overall motifs
	if "quilting designs used, overall motifs" in newDic:
		quiltDic['motifs'] = newDic["quilting designs used, overall motifs"]
	
	# Quilting technique used
	if "quilting technique used" in newDic:
		quiltDic['techniques'] = newDic["quilting technique used"]

	sleep(0.5)


	quiltList.append(quiltDic)

# export to csv
keys = quiltList[0].keys()

# file export for American Indian Quilt Index
with open('data/quilt_index_american_indian_updated[1].csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(quiltList)

# # file export for New England Quilt Museum
# with open('data/quilt_index_new.csv', 'w', newline='') as output_file:
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(quiltList)

