import json
import time
import urllib2
import csv

class Petition:
	def __init__(self, URL):
		decoder = json.load(urllib2.urlopen('https://api.whitehouse.gov/v1/petitions.json?url='+URL))
		self.id = decoder['results'][0]['id']
		self.name = decoder['results'][0]['title']
		self.sig_total = decoder['results'][0]['signatureCount']
		self.petition_loader = json.load(urllib2.urlopen('https://api.whitehouse.gov/v1/petitions/'+self.id+'/signatures.json?'))
		self.petition_signatures = self.petition_loader['results']

	def cleaner(self):
		'''
		drops unwanted fields
		'''
		delete_keys=['id','type']
		for dicts in self.petition_signatures:
			for keys in delete_keys:
				dicts.pop(keys)
		for dicts in self.petition_signatures:
			dicts['created'] = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(dicts['created']))

	def writer(self, output):
		'''
		Writes the name, zip code, and timestamp
		to a csv.
		'''
		petitionheader = ['name', 'zip code','timestamp']
		petition_fieldnames = ['name', 'zip', 'created']
		with open(str(output)+'.csv','wb') as f:
			petitionwriter = csv.DictWriter(f,petition_fieldnames)
			petitionwriter.writer.writerow(petitionheader)
			petitionwriter.writerows(self.petition_signatures)

	def petition_info(self):
		'''
		Print's the petition ID, name, and total
		number of signatures.
		'''
		print '---------------------------------------------------------------------------'
		print ('The petition ID is '+self.id+'')
		print('The petition name is '+self.name)
		print('The total number of signatures so far is '+str(self.sig_total))



p =  Petition(raw_input('Enter the petition URL: '))
p.petition_info()
p.cleaner()
p.writer(raw_input('What do you want to name this file?'))

