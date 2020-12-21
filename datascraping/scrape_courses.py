import argparse
from bs4 import BeautifulSoup
import os
import os.path as osp
import hashlib
import requests
import sys
import csv

def get_url_contents(cache_dir, page):
	fname=hashlib.sha1(page.encode('utf-8')).hexdigest()
	full_fname=osp.join(cache_dir, fname)
	contents=None
	
	if osp.exists(full_fname):	
		contents = open(full_fname, 'r').read()
	else:
		r=requests.get("https://www.mcgill.ca/study/2020-2021/courses/search?page="+page)
		contents=r.text
		
		# if dir dne, make one
		dirname = os.path.dirname(full_fname)
		if not os.path.exists(dirname):
    			os.makedirs(dirname)

		with open(full_fname, 'w') as fh:
			fh.write(contents)
	return contents

def process_link(link):
        validstr=True #validity checker
        split=link.split() #split into words
        name=split[0]+' '+split[1]
        title=''
        credits=[]
        for idx, z in enumerate(split[2:]):
                if '(' in z: #reached credits
                        credits=split[2+idx:]
                        break
                else: #append to title
                        if len(title)==0:
                                title=z
                        else: title=title+' '+(z)
        #validate form
        if len(title)==0:
                validstr=False
        if len(credits)!=2 or 'credit' not in credits[1]:
                validstr=False
        #if valid, return
        if validstr:
                str=name,title, credits[0][1:]
                return (str)
        else:
                return False

def getcourses(cache_dir, page):
	content=get_url_contents(cache_dir, page)
	soup=BeautifulSoup(content, 'html.parser')
	
	vrow=soup.find_all('div', 'views-row') #data is located in children of views-row
 		
	writer= csv.writer(sys.stdout) #want csv file, but to write to stdout
	header = 'CourseID','Course Name','# of credits'
	writer.writerow(header)
	for v in vrow:
		z=v.find('a') #find the link
		data=process_link(z.text.strip()) #process the link for the csv
		if data !=False: #if valid, write it
			writer.writerow(data)
		

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-c','--caching_dir', required=True, help='json file with cache_dir and target_people')
	parser.add_argument('page', help='page number')
	args= parser.parse_args()
	
	content=getcourses(args.caching_dir, args.page)
	

if __name__=="__main__":
	main()

