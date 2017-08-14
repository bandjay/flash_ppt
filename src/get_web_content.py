# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 13:42:33 2017

@author: Jay
"""
""" Class to get web page contents for genes """
""" This class takes respective URLS for web search"""
from bs4 import BeautifulSoup
import requests
import re
import os
from Bio import Entrez

class get_web_content:  
    
    def __init__(self,exac_url,ncbi_url,uniprot_url):
        self.exac_url=exac_url
        self.ncbi_url=ncbi_url
        self.uniprot_url=uniprot_url  
        
    def exac_tab_vals(self):    
        page = requests.get(self.exac_url)
        #exac_url='http://exac.broadinstitute.org/gene/ENSG00000140443'
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find("table", attrs={"class":"table"})
        exac_tab_vals = []
        try:
            for row in table.find_all("tr")[1:]:
                dataset = [td.get_text() for td in row.find_all("td")] [1:]           
                exac_tab_vals.append(re.sub("[ \n]","","\t".join(dataset)))  
            return "\t".join(exac_tab_vals)
        except:
            return "NA"
            
    '''
    -----------------------------------------------------------------
    Upgraded web contetnt search using python APIS
    Earlier version of webscraping is commented at the end of program
    -----------------------------------------------------------------
    '''
    def entrez_gene_summary(self):        
        #ncbi_url="https://www.ncbi.nlm.nih.gov/gene/3480"
        #ncbi_id=os.path.split(ncbi_url)[1]
        ncbi_id=os.path.split(self.ncbi_url)[1] 
        #print ncbi_id
        #print ("CATCHING UP APIs")
        try:
            Entrez.email = "jaycb@live.com"
            #print "before handle"
            handle = Entrez.esummary(db="gene", id=ncbi_id)
            #print "after handle"
            record = Entrez.read(handle)
            summary=record['DocumentSummarySet']['DocumentSummary'][0]['Summary']
            #print summary
        except:
            summary="NA"
        return summary
    
    def uniprot_gene_summary(self):
        #uniprot_url="http://www.uniprot.org/uniprot/P08069"
        page = requests.get(self.uniprot_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            summary=soup.find("span",attrs={"property":"schema:text"}).get_text().split("<p>")[0].strip()
        except:
            summary="NA"
        return summary

        

'''
-----------------  debugging --------------------------------------

exac_url='http://exac.broadinstitute.org/gene/ENSG00000140443'
ncbi_url="https://www.ncbi.nlm.nih.gov/gene/3480"
uniprot_url="http://www.uniprot.org/uniprot/P08069"
we=get_web_content(exac_url,ncbi_url,uniprot_url)
we.uniprot_gene_summary()
we.exac_tab_vals()
we.entrez_gene_summary()


---------------- WEB SCRAPING OLD version -------------------------
def entrez_gene_summary(self):        
        #ncbi_url="https://www.ncbi.nlm.nih.gov/gene/3480"
        page = requests.get(self.ncbi_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        try:
            summary=soup.find("div",attrs={"class":"section"}).find('dt', text='Summary').find_next_sibling('dd').text
        
        except:
            summary="NA"
        return summary
'''




