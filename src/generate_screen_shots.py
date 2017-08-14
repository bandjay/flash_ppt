# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 08:59:47 2017

@author: M179100
"""

""" class to take screenshots using selenium """
#from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os


class screen_shots:
    
    def __init__(self,gene,homepath):        
        self.imgpath=os.path.join(homepath,"img")
        self.gene=gene
        os.chdir(self.imgpath)
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")
        self.chrome = webdriver.Chrome(chrome_options=chrome_options)
        self.gene_summary_gen()
        self.gene_exac_gen()
        self.chrome.quit()
       
    
    def gene_summary_gen(self):                
        """ 
        ######################################################
        ########## summary from Gene cards web page  #########
        ######################################################
        """
        Gene_sum_url=str("http://www.genecards.org/cgi-bin/carddisp.pl?gene="+self.gene+"#summaries")
        self.chrome.get(Gene_sum_url)
        self.chrome.save_screenshot(str("Gene_")+self.gene+str("_summary.png")) # saves screenshot of entire page
        #chrome.quit()
        #im=Image.open(str("Gene_")+self.gene+str("_summary.png"))                 
        #crop_rectangle1 = (100,50, im.size[0]-100, im.size[1]-30)
        #cropped_im1 = im.crop(crop_rectangle1)
        #cropped_im1=cropped_im1.resize((700, 450), Image.ANTIALIAS)
        #cropped_im1.save(str("Gene_")+self.gene+str("_summary.png")) 
        
        print("Gene summary captured")
        
        
    def gene_exac_gen(self):                
        """ 
        #############################################################
        ########## Exac,phenotype snapshots from marrvel web page ###
        #############################################################
        """           
        """ Genearting the Exac cropped picture"""
            
        Gene_exac_url=str("http://marrvel.org/search/gene/"+self.gene+"#ExACPanel")
        self.chrome.get(Gene_exac_url)
        time.sleep(5.0)
        self.chrome.save_screenshot(str("Gene_")+self.gene+str("_Exac.png")) # saves screenshot of entire page
        #chrome.quit()
            
        #im=Image.open(str("Gene_")+self.gene+str("_Exac.png"))        
        #crop_rectangle1 = (250,75,750, 325)
        #cropped_im1 = im.crop(crop_rectangle1)
        #cropped_im1=cropped_im1.resize((400, 300), Image.ANTIALIAS)
        #cropped_im1.save(str("Gene_")+self.gene+str("_Exac.png")) 
            
        """ Genearting the Phenotype cropped picture"""
        Gene_phe_url=str("http://marrvel.org/search/gene/"+self.gene)
        self.chrome.get(Gene_phe_url)
        time.sleep(2.0)
        self.chrome.save_screenshot(str("Gene_")+self.gene+str("_PhenoType.png"))
            
        #im1=Image.open(str("Gene_")+self.gene+str("_PhenoType.png"))        
        #crop_rectangle = (760,75,1320, 350)
        #cropped_im2 = im1.crop(crop_rectangle)
        #cropped_im2=cropped_im2.resize((400, 300), Image.ANTIALIAS)
        #cropped_im2.save(str("Gene_")+self.gene+str("_PhenoType.png"))             
            
        print("Gene Exac,Phenotype tables captured") 
        
    


    