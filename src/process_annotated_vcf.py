# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 14:49:35 2017
@author: Jay
"""
""" class to process vcf file and return a pandas dataframe"""

import pandas as pd             
import gzip
class process_annotated_vcf:

    def __init__(self,filename):
        self.filename=filename
        
    def process(self):  
        try:
            if self.filename.__contains__("gz"):
                input_file=gzip.open(self.filename,"rb")
            else :
                """ Perl python part for file word wrap removal """
                #perl_command=str("Perl word_wrap_remove.pl ")+str(self.filename)+str("  >  ")+str(self.filename)+str(".out")
                #os.popen(perl_command)  
                input_file=open(self.filename)
        except:
            raise Exception( "Input annotated vcf file does not exists ,please check the path")
                                                                                                                                       
        #os.chdir("h:/rp/vcfs")
        #input_file=gzip.open("h:/flash_ppt/sample_vcfs/SL2-377.vcf.gz", 'rb')

        lines=input_file.readlines()
        #comments=[l for l in lines if l.startswith('##')]
        records=[l for l in lines if not l.startswith('##')]                                                          
        rec=[r for r in records if r!='\n']       
        field_names=rec[0].split('\t')
        var_names=[f.strip('\n#') for f in field_names]        
    
        """ creating pandas df from vcf file """
        dataf=pd.DataFrame(data=None,columns=var_names)
        
        for r in range(2,len(rec)):
            values=rec[r].split("\t")                                                                  
            row=pd.Series(values,var_names)
            dataf=dataf.append([row],ignore_index=True)
        
        if dataf.shape[0]>30:
            raise Exception("There are more than 30 variants in input file")                                                                                                                                                                                                                                                               
        return dataf 
            

