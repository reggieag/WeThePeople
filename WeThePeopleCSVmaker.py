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
		#self.petition_loader = json.load(urllib2.urlopen('https://api.whitehouse.gov/v1/petitions/'+self.id+'/signatures.json?'))
		self.petition_signatures = []
		
	def loader(self, petition_id):
		i = 0
		while i < self.sig_total:
			if self.sig_total - i > 1000:
				petition_loader = json.load(urllib2.urlopen('https://api.whitehouse.gov/v1/petitions/'+self.id+'/signatures.json?'+'offset='+str(i)))
				self.petition_signatures += petition_loader['results']
				i += 1000
				print str(i) + ' signatures loaded.'
			else:
				limit = self.sig_total - i
				petition_loader = json.load(urllib2.urlopen('https://api.whitehouse.gov/v1/petitions/'+self.id+'/signatures.json?'+'offset='+str(i)+'&limit='+str(limit)))
				self.petition_signatures += petition_loader['results']
				i += limit
				print str(i) + ' signatures loaded.'
			
			
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
		print '---------------------------------------------------------------------------'


p =  Petition(raw_input('Enter the petition URL: '))
p.petition_info()
print 'loading data...'
p.loader(p.id)
print'cleaning data...'
p.cleaner()
p.writer(raw_input('What do you want to name this file?'))