import argparse
import json
from bs4 import BeautifulSoup
import os
import os.path as osp
import hashlib
import requests

def extract_relationships_from_candidate_links(candidates, person_url):
	relationships=[]
	for link in candidates:
		if 'href' not in link.attrs:
			continue
		href=link['href']
		if href.startswith('/dating') and href != '/dating/'+person_url:
			relationships.append(href[8:]) #string slicing to cut off the /dating
	return relationships
		

def get_url_contents(person, cache_dir):
	fname=hashlib.sha1(person.encode('utf-8')).hexdigest()
	full_fname=osp.join(cache_dir, fname)
	contents=None
	
	if osp.exists(full_fname):
		print ('Loading from cache')
		contents = open(full_fname, 'r').read()
	else:
		print('Loading from source')
		r=requests.get("https://www.whosdatedwho.com/dating/"+person)
		contents=r.text
		
		# if dir dne, make one
		dirname = os.path.dirname(full_fname)
		if not os.path.exists(dirname):
    			os.makedirs(dirname)

		with open(full_fname, 'w') as fh:
			fh.write(contents)
	return contents

def extract_rel(person, cache_dir):
	content=get_url_contents(person, cache_dir)
	soup=BeautifulSoup(content, 'html.parser')
	relationships=[]
	
	status_h4=soup.find('h4', 'ff-auto-status')
	try: 
		key_div=status_h4.next_sibling #errors ahoy!
	except:
		#for page not found
		for h in soup.find_all('h1'):
			if h.text.strip()=='Page not found':
				raise Exception('Page not found for '+person)  
				return False
		#for no relationships
		return relationships

	candidate_links=key_div.find_all('a')
	
	relationships.extend(extract_relationships_from_candidate_links(candidate_links, person))
	
	if len(relationships) >1:
		print(relationships)
		raise Exception('Too many relationships- should only be one')
		
	rels_h4=soup.find('h4', 'ff-auto-relationships')
	sib = rels_h4.next_sibling
	
	while sib is not None and sib.name =='p':
		candidate_links=sib.find_all('a')
		sib=sib.next_sibling
		relationships.extend(extract_relationships_from_candidate_links(candidate_links, person))
		
	return relationships
	

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c','--configfile', required=True, help='json file with cache_dir and target_people')
	parser.add_argument('-o', '--outputfile', required=True, help='output json')
	args= parser.parse_args()
	
	with open(args.configfile) as f:
  		inputj = json.load(f)	
	cache_dir=inputj['cache_dir']
	people=inputj['target_people']
	
	d={}
	for person in people:
		relationships=extract_rel(person, cache_dir)
		#print(relationships)
		if relationships==False:
			continue	
		d[person]=relationships
		
	with open(args.outputfile, 'w') as json_file:
		json.dump(d, json_file)

	d1={}
	with open(args.outputfile, 'r') as f:
		d1= json.load(f)
		print(d1)

	
	

if __name__=="__main__":
	main()

