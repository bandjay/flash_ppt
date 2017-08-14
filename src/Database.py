# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 09:15:07 2017
@author: M179100
"""

import sqlite3 as sql
import time
import os


class Database:
    
    def __init__(self,database): 
        #database = "H:/Gene_DB.db"        
        self.conn = sql.connect(database)        
        
        if self.conn is  None:
            print "DB connection not established" 
        self.db_refresh()            
 
            
    def create_table(self,table_name,table_cols) :
        new_table = str("CREATE TABLE IF NOT EXISTS "+ table_name)
        new_table_cols=" ("
        for tc in range(len(table_cols)):
            if tc!=len(table_cols)-1:
                tc_name,tc_type,tc_constraint=table_cols[tc].split(":")
                new_table_cols=new_table_cols+tc_name+" "+tc_type+" "+tc_constraint+","
            else :
                tc_name,tc_type,tc_constraint=table_cols[tc].split(":")
                new_table_cols=new_table_cols+tc_name+" "+tc_type+" "+tc_constraint+");"
        new_table_sql_command=new_table+new_table_cols
        self.conn.execute(new_table_sql_command)
        #print" Table :",table_name," Created"
                  
    """        
    def create_table(conn, create_table_sql):
        Gene_table = ''' CREATE TABLE IF NOT EXISTS Gene_table (
                                        GENE_SYM text PRIMARY KEY,
                                        Entrez_comments text,
                                        Uniprot_comments text
                                    ); '''    
        try:
            c = conn.cursor()
            c.execute(Gene_table)
        except Error as e:
            print(e)        
    """    
    def insert_records(self,rec):
        #rec=(("ANKRD2","NA","NA"),("FANCD2","NA","NA"),("RUNX1","NA","NA"),("NEFL","NA","NA"))
        #for rec in records:
            try:
                #(GENE_SYM,Entrez_summary,Uniprot_summary)
                self.conn.execute('INSERT INTO Gene_table VALUES(?,?,?,?)',rec)
                #print "Row inserted"
            except sql.IntegrityError:
                pass
                #print ("Gene exists in DB")
                
    def get_records(self,gene):
        gene_summary=[]
        c = self.conn.cursor()
        rec= c.execute(str('SELECT * FROM Gene_table WHERE GENE_SYM=="'+gene+'"'))
        for r in rec:
           gene_summary.append(r[0])
           gene_summary.append(r[1])
           gene_summary.append(r[2])
           gene_summary.append(r[3])
        return gene_summary
    
    def get_gene_list(self):
        c = self.conn.cursor()
        c.row_factory = lambda cursor, row: row[0]
        all_gene=c.execute('SELECT GENE_SYM FROM Gene_table').fetchall()
        return all_gene
    
    def close_db_connection(self):
        self.conn.close()
        #print "DB connection closed"
    
    def db_commit(self):
        self.conn.commit()
        
    def db_refresh(self):
        src_path=os.getcwd()
        config_path=os.path.join(os.path.split(src_path)[0],"config")
        os.chdir(config_path)
        f=open("time_stamp.txt")
        l=f.readlines()
        st=float(l[0]) # time stamp in seconds
        if (time.time()- st >(60*60*24*31*1)): # time stamp for seconds in a month 
            #start_time=time.time()
            #with open("time_stamp.txt","w") as ts:
            #    ts.write(str(start_time))
            print " ===>    !!WARNING : Refresh database by running Database_refresh in ../src \n"
            #c = self.conn.cursor()
            #c.execute(str('DELETE FROM Gene_table'))
        os.chdir(src_path)
    
    def db_update(self,gene,new_record):
        try:
            c = self.conn.cursor()
            #gene="ANKRD26"
            #new_record=('This gene encodes a protein containing N-terminal ankyrin repeats which function in protein-protein interactions. Mutations in this gene are associated with autosomal dominant thrombocytopenia-2. Pseudogenes of this gene are found on chromosome 7, 10, 13 and 16. Multiple transcript variants encoding different isoforms have been found for this gene. [provided by RefSeq, Dec 2011]', 'NA', '195.4\t190\tz=0.24\t453.0\t542\tz=-2.05\t59.7\t33\tpLI=0.00\t20.8\t19\tz=0.12')
            update_query='UPDATE Gene_table SET Entrez_summary=?,Uniprot_summary=?,Exac_table=? WHERE GENE_SYM=="'+gene+'"'
            #print update_query
            #print new_record
            c.execute(update_query,new_record)
            print " ===>    Updated Gene : ",gene," deatails in DB\n"
        except: 
            print "Record update failed"
            



"""        
if __name__== "__main__":  
    database = "H:\Gene_DB.db"  
    rec=(("ANKRD2","NA","NA","180:25:35.4:43:139:116:189:2.4:'z=0.75':'z=0.25':'Nan':'Nan'"),("FANCD2","NA","NA","NA"),("RUNX1","NA","NA","NA"),("NEFL","NA","NA","NA"),("AMNCD1","NA","NA","NA"),("NEFL2","NA","NA","NA"),("NEFL7","NA","NA","NA"))  
    table_name="Gene_table"
    table_cols=["GENE_SYM:text:PRIMARY KEY","Entrez_summary:text:","Uniprot_summary:text:","Exac_table:text:"]
    d=DB(database)
    d.create_table(table_name,table_cols)
    for r in rec:
        d.insert_records(r) 
    d.get_gene_list()
    d.get_records("ANKRD2")
    d.close_db_connection()

"""


    

