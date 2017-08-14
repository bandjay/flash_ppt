# -*- coding: utf-8 -*-
"""
Created on Wed Jul 05 10:39:18 2017
@author: M179100
"""

import time
import os
import argparse
from multiprocessing.dummy import Pool as ThreadPool

""" importing user defined modules """
from Database import Database
from get_web_content import get_web_content


class Database_refresh:
### adding all HGNC gene to DB 
    def __init__(self,dbpath):
        self.dbpath=dbpath
        
        #dbpath="H:/Gene_DB.db" 
        ''' Accessing database '''
        
        db=Database(os.path.join(self.dbpath,"GENE_DB.db"))
        
        ''' Getting list of existing gene list from database '''
        list_of_genes=db.get_gene_list()
        print " ===>    There are : ",len(list_of_genes) ," existing genes in DB \n"
        
        src_path=os.getcwd()
        config_path=os.path.join(os.path.split(src_path)[0],"config")
        os.chdir(config_path)
            
        ''' Creating a dictionary for all ids required to do web search such as entrez,ensemble,uniprot ids
            Parsing HGNC_GENE_LIST.txt file in ../config directorty '''
        hgnc_file=open("HGNC_GENE_LIST.txt")
        hgnc_lines=hgnc_file.readlines()
        hgnc_lines=hgnc_lines[1:]
        gene_ids_dict={}
        for hl in hgnc_lines:
                        gene_sym,ent_id,en_id,uni_id=hl.split("\t")[1],hl.split("\t")[18],hl.split("\t")[19],hl.split("\t")[25]            
                        gene_ids_dict[gene_sym]=(ent_id,en_id,uni_id)  
        
        def search_web(gs):       
            try:
                Entrez_id,Cid,Uniprot_id=gene_ids_dict[gs][0],gene_ids_dict[gs][1],gene_ids_dict[gs][2]
                exac_url=str("http://exac.broadinstitute.org/gene/"+Cid)
                ncbi_url=str("https://www.ncbi.nlm.nih.gov/gene/"+Entrez_id)
                uniprot_url=str("http://www.uniprot.org/uniprot/"+Uniprot_id)                
                wp=get_web_content(exac_url,ncbi_url,uniprot_url)
                exac_table= wp.exac_tab_vals()
                entrez_summary=wp.entrez_gene_summary()
                uniprot_summary=wp.uniprot_gene_summary()                    
                new_rec=[entrez_summary,uniprot_summary,exac_table]
                return [gs,new_rec]
            except:
                pass  
            
        ''' multi processing for gene web search '''
        print " ===>    Fetching Gene Details from web \n"
        pool = ThreadPool(8) 
        updated_records= pool.map(search_web,list_of_genes) 
        #ur=updated_records[0]
        i=1
        try:
            for ur in updated_records:
                en,uni,ex=[str(u) for u in ur[1]]
                db.db_update(str(ur[0]),(en,uni,ex))           
                #print " ===> Updated ",i, " Gene deatils in Database \n"
                i=i+1
        except:
            pass
        db.db_commit()
        db.close_db_connection()
        print " ===>    Gene details updated in Database \n"        
        with open("time_stamp.txt","w") as ts:
                ts.write(str(time.time()))
        print " ===>    Updated time stamp , refresh needed in a month from now \n"
        
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Tool to generate automated report for variants')
    parser.add_argument('-d','--database_path', help='path for database ex: /home/m17****/auto_report_tool/GENE_DB.db', required=True)
    args = vars(parser.parse_args())
    dbpath=args['database_path']
    Database_refresh(dbpath)
    
        
    
        
