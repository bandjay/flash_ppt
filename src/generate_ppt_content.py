# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 09:51:28 2017

@author: Jay
"""
""" class to generate ppt content """
import re
import os
import warnings
from get_web_content import get_web_content
from Database import Database
#from screen_shots import screen_shots

class generate_ppt_content:
    
    def __init__(self,database_path):
        #self.df_rec=df_rec
        self.database_path=database_path
        #print "ppt content"
    
    """ Heterozygous /Homo function """    
    def het_homo(self,vec):
            dummy=str(vec).split(':')[0]
            arr=dummy.split('/')    
            if arr[0]==arr[1]:
                if arr[0]=='0':
                    return 'NEG'
                else:
                    return 'POS'
            if arr[0]!=arr[1]:
                return 'HET'   
            
    """ method to generate info fields dictionary """        
    def generate_info_dict(self,info):
        gene_dict={}
        #info=variants_dataframe['INFO'][0]
        gene=str(info).split(';')        
        #url=[]
        '''
        i=0
        len(key_dictionary.values())
        for v in key_dictionary.values():
            if v in gene_dict.keys():
                i=i+1
        print i
        '''
        #non_url=[]
        for g in gene:
            if g.__contains__("href") or g.__contains__("www"):
               # url.append(g)
               continue                
            else:
                if g.__contains__("="):
                    #non_url.append(g)
                    k,v=g.split("=")
                    gene_dict[k]=v 
        return gene_dict
    
    ''' method to fecth value in info dictionary by using key '''
    def get_dict_value(self,key):
        try:
            return self.Info_dict[key]
        except:
            return "NA"
        
    
    """ Method to clean phenotypes list """
    def clean_pheno(self,pheno):
        ''' pheonlist parsing '''
        #Opheno="Leukemia,_acute_myeloid,_601626_(3),Platelet_disorder,_familial,_with_associated_myeloid_malignancy,_601399_(3)"
        Opheno="".join(pheno)
        disease_list=Opheno.split("(3)")
        disease_str=[]
        for di in disease_list:
            disease_str.append(re.sub("[_,|]"," ","".join(di)).strip())
        disease_str=[" ".join(di.split()[0:-1])+str( ", MIM: "+di.split()[-1]) for di in disease_str if len(di)!=0]
        return disease_str
    
    """ method to clean exac values """
    def clean_exac_val(self,exac):
         if exac!="NA":
            return "%.4f"%(float(exac)*100)
    
    ''' method to generate dictinary with all keys by parsing the drill_file_fields.txt file in /config '''     
    def generate_key_dictionary(self):     
        ''' getting necessary keys from the drill_file in config direcoty '''        
        #src_path=os.getcwd()
        #import os
        #os.chdir("h:/flash_ppt/config")
        config_path=os.path.join(os.path.split(os.getcwd())[0],"config")
        os.chdir(config_path)     
        key_dictionary={}
        drill_file=open("drill_file_fields.txt")
        drill_lines=drill_file.readlines()
        for catalog in drill_lines:
            name,catalog_file_name,fields,string_format=catalog.split("\t")
            all_fields=fields.split(",")
            required_fields=string_format.split(",")
            for r in required_fields:
                required_field,required_index=r.split("$")
                key=str(name+"_"+required_field)
                if name=="CAVA":
                    value=str(catalog_file_name+"_"+all_fields[int(required_index)])
                else :
                    value=str(catalog_file_name+"."+all_fields[int(required_index)])
                key_dictionary[key]=value 
                              
        #key_dictionary.keys()
        #key_dictionary.values()
        return key_dictionary
        
    ''' method to all of the content required to populate presentation '''
    def generate_content(self,df_rec): 
        self.df_rec=df_rec
        pptcontent={}    # dictionary to store all ppt content for a gene    
        """Info fields of a gene"""        
        Info_rec=self.df_rec[7]  
        #Info_rec=variants_dataframe['INFO'][0]
        ''' generating dictionary of info fields '''
        self.Info_dict= self.generate_info_dict(Info_rec)  
        
        """ 
        ###########################################################
        ##################### Generate PPT content ################
        ###########################################################
        """
        
        """ Presentation Line 1 """
        
        """ calling function het_homo for subject,mom and dad """
        try:
            sub_hh=str(self.het_homo(self.df_rec[9]))
        except:
            sub_hh="NA"
        try:
            mom_hh=str(self.het_homo(self.df_rec[10]))
        except:
            mom_hh="NA"
        try: 
            dad_hh=str(self.het_homo(self.df_rec[11]))
        except:
            dad_hh="NA"

        ''' generating key dictionary by parsing the drill file '''
        key_dictionary=self.generate_key_dictionary()
            
        ''' getting all necessary values from info dictionary by using 
        parsed dictionary keys from drill file fields '''
        try:
            NCBI_GENE=self.get_dict_value(key_dictionary['NCBI_gene'])
            CAVA_GENE=self.get_dict_value(key_dictionary['CAVA_GENE'])
            CAVA_CSN=self.get_dict_value(key_dictionary['CAVA_CSN'])
            CAVA_LOC=self.get_dict_value(key_dictionary['CAVA_LOC'])
            CAVA_IMPACT=self.get_dict_value(key_dictionary['CAVA_IMPACT'])
            Phenotype=self.get_dict_value(key_dictionary['OMIM_Phenotypes'])
            ExAC_AC=self.get_dict_value(key_dictionary['ExAC_AC'])
            ExAC_AN_Adj=self.get_dict_value(key_dictionary['ExAC_AN_Adj'])
            ExAC_AC_Hom=self.get_dict_value(key_dictionary['ExAC_AC_Hom'])
            ExAC_AF_popmax=self.get_dict_value(key_dictionary['ExAC_AF_POPMAX'])
            ExAc_popmax=self.get_dict_value(key_dictionary['ExAC_POPMAX'])
            gnomAD_AC=self.get_dict_value(key_dictionary['gnomAD_AC'])
            gnomAD_Ex_AN_raw=self.get_dict_value(key_dictionary['gnomAD_EX_AN_raw'])
            gnomAD_Ex_Hom=self.get_dict_value(key_dictionary['gnomAD_EX_Hom'])
            gnomAD_AF_popmax=self.get_dict_value(key_dictionary['gnomAD_AF_POPMAX'])
            gnomAD_EX_popmax=self.get_dict_value(key_dictionary['gnomAD_EX_POPMAX'])
            Clinvar_significance=self.get_dict_value(key_dictionary['Clinvar_significance'])
            Clinvar_measureset=self.get_dict_value(key_dictionary['Clinvar_measureset'])
            Clinvar_transcipt=self.get_dict_value(key_dictionary['Clinvar_transcript'])
            Clinvar_protein=self.get_dict_value(key_dictionary['Clinvar_protein'])
            HGMD_pub=self.get_dict_value(key_dictionary['HGMD_Pubmed'])
            HGMD_dna=self.get_dict_value(key_dictionary['HGMD_DNA'])
            #HGMD_gene=self.get_dict_value(key_dictionary['HGMD_GENE'])
            #HGMD_PROT=self.get_dict_value(key_dictionary['HGMD_PROT'])
            Sift=self.get_dict_value(key_dictionary['dbNSFP_Sift'])
            Polyphen=self.get_dict_value(key_dictionary['dbNSFP_Polyphen'])
            #Metalr=self.get_dict_value(key_dictionary['dbNSFP_Metalr'])
            Mutationtaster=self.get_dict_value(key_dictionary['dbNSFP_Mutationtaster'])
            #Vest3=self.get_dict_value(key_dictionary['dbNSFP_Vest3Score'])
            ensemble_id=self.get_dict_value(key_dictionary['HGNC_ensemble_id'])
            entrez_id=self.get_dict_value(key_dictionary['HGNC_entrez_id'])
            omim_id=self.get_dict_value(key_dictionary['HGNC_omim_id'])
            #ucsc_id=self.get_dict_value(key_dictionary['HGNC_ucsc_id'])
            #HGNC_location=self.get_dict_value(key_dictionary['HGNC_location'])
            uniprot_id=self.get_dict_value(key_dictionary['HGNC_uniprot_ids'])
            Phenotype_list=self.get_dict_value(key_dictionary['HPO_term'])
        except:
            raise Exception("In valid keys ,Check drill_file_fields.txt in /config")
        
        if Clinvar_transcipt==Clinvar_protein=="NA":
            #warnings.warn(" WARNING !!!! : using CAVA Protein,transcript not clinvar ")
            tran=CAVA_CSN.split("_")[0]
            try:
                prot=CAVA_CSN.split("_")[1]
            except:
                prot="NA"
        else:
            tran,prot=Clinvar_transcipt,Clinvar_protein
            
        location=CAVA_LOC
        
        if dad_hh==mom_hh=="NEG":
            pptcontent['Gene']=str(NCBI_GENE +" , " +sub_hh + " , " + tran+" , " + prot+ " , [DENOVO] "+" Dad is : " + dad_hh +" , "+"Mom is : " + mom_hh)
        else:
            pptcontent['Gene']=str(NCBI_GENE +" , " +sub_hh + " , " + tran+" , " + prot+ " , "+" Dad is : " + dad_hh +" , "+"Mom is : " + mom_hh)
        """ Presentation Line 2 """
        pptcontent['Disease']=str(" & ".join(self.clean_pheno(Phenotype)))
        
        """ Presentation Line 3 """
        if ExAC_AC==ExAC_AN_Adj==ExAC_AC_Hom==ExAC_AF_popmax==ExAc_popmax=="NA":
            Exac_string="ExAC => Not reported"
        else:
            Exac_string=str("ExAC =>  "+ExAC_AC+"/"+ExAC_AN_Adj+" ("+ExAC_AC_Hom+" hom ;"+self.clean_exac_val(ExAC_AF_popmax)+"% "+ExAc_popmax + ")")
        if gnomAD_AC==gnomAD_Ex_AN_raw==gnomAD_Ex_Hom==gnomAD_AF_popmax==gnomAD_EX_popmax=="NA":
            gnomAD_string="gnomAD => Not reported"   
        else:
            gnomAD_string=str("gnomAD => " + gnomAD_AC + "/"+ gnomAD_Ex_AN_raw +" ("+ gnomAD_Ex_Hom +" hom;"+self.clean_exac_val(gnomAD_AF_popmax)+"% "+gnomAD_EX_popmax+")")
        pptcontent['Exac']= Exac_string+" , "+gnomAD_string 
        """ Presentation Line 4 """            
        if Clinvar_significance==Clinvar_measureset==HGMD_pub==HGMD_dna=="NA":
            pptcontent['Clinvar']=str("ClinVar => Not reported , HGMD => Not reported")
        elif Clinvar_significance==Clinvar_measureset=="NA" :
            pptcontent['Clinvar']=str("ClinVar => Not reported"+"  , HGMD => PMID: "+ HGMD_pub + ", DNA: "+HGMD_dna)
        elif HGMD_pub==HGMD_dna=="NA":
            pptcontent['Clinvar']=str("ClinVar => "+Clinvar_significance+" , ID: "+Clinvar_measureset +"  , HGMD => Not reported")
        else: 
            pptcontent['Clinvar']=str("ClinVar => "+Clinvar_significance+" , ID: "+Clinvar_measureset +"  , HGMD => PMID: "+ HGMD_pub + ", DNA: "+HGMD_dna)
        
        """ Presentation Line 5 """
        pptcontent['In_silico']=str("In silico  =>  SIFT : "+Sift+"  ,  Polyphen : "+Polyphen+" , Mutation Taster Pred : "+"".join(Mutationtaster)+"  ,  CAVA_IMPACT : "+CAVA_IMPACT)
        
        """ Presentation Line 6 """
        pptcontent['Loc']=str("Location =>  "+location)#+" ,  Region => NA")
        
        
        """ URLS """
        #Cid="ENSG00000144554"
        #Entrez_id="2177"
        #Uniport_id="Q9BXW9"
        
        exac_url=str("http://exac.broadinstitute.org/gene/"+ensemble_id)
        ncbi_url=str("https://www.ncbi.nlm.nih.gov/gene/"+entrez_id)
        uniprot_url=str("http://www.uniprot.org/uniprot/"+uniprot_id)
        marrvel_url=str("http://marrvel.org/search/gene/"+CAVA_GENE)
        genecards_url=str("http://www.genecards.org/cgi-bin/carddisp.pl?gene="+CAVA_GENE) 
        if Clinvar_measureset!="NA":
            clinvar_url=str("https://www.ncbi.nlm.nih.gov/clinvar/variation/"+Clinvar_measureset)
            pptcontent['clinvar_url']=clinvar_url
        else :
            pptcontent['clinvar_url']="NA"
        if HGMD_pub!="NA":
            hgmd_pub_url=str("http://www.ncbi.nlm.nih.gov/pubmed/?term="+HGMD_pub)
            pptcontent['hgmd_pub_url']=hgmd_pub_url
        else:
            pptcontent['hgmd_pub_url']="NA"
        if omim_id!="NA":
            omim_url=str("https://www.omim.org/entry/"+omim_id+"?search="+omim_id+"&highlight="+omim_id)
            pptcontent['omim_url']=omim_url
        else:
            pptcontent['omim_url']="NA"
            
        '''
        ##########################################################
        ############# Searching DB for gene ######################
        ##########################################################
        '''
        #dirs=os.getcwd().split("\\")
        #home=str(dirs[0]+"\\"+dirs[1])
        db_path=os.path.join(self.database_path,"GENE_DB.db")               
        db=Database(db_path)
        #rec=(("ANKRD2","NA","NA"),("FANCD2","NA","NA"),("RUNX1","NA","NA"),("NEFL","NA","NA"),("AMNCD1","NA","NA"),("NEFL2","NA","NA"),("NEFL7","NA","NA"))  
        table_name="Gene_table"
        table_cols=["GENE_SYM:text:PRIMARY KEY","Entrez_summary:text:","Uniprot_summary:text:","Exac_table:text:"]
        db.create_table(table_name,table_cols)
        #db.insert_records(rec) 
        gene_list=[str(i) for i in db.get_gene_list()]
        Cgene=NCBI_GENE
        if Cgene in gene_list:
            print " ===>    Gene found in Database \n"
            summaries=db.get_records(Cgene)
            entrez_summary=str(summaries[1])
            uniprot_summary=str(summaries[2])
            pptcontent['exac_table']=str(summaries[3])
            #pptcontent['exac_table']="NA"
            db.close_db_connection()
        else :  
            """web search for summary exac and entrez summary """   
            print " ===>    Fetching gene details from web \n"
            wp=get_web_content(exac_url,ncbi_url,uniprot_url)
            pptcontent['exac_table']= wp.exac_tab_vals()
            entrez_summary=wp.entrez_gene_summary()
            uniprot_summary=wp.uniprot_gene_summary()
            rec=(Cgene,entrez_summary,uniprot_summary,pptcontent['exac_table'])
            db.insert_records(rec)
            db.db_commit()
            db.close_db_connection()
            print " ===>    Gene details added to DB \n"

        
        """ Presentation Line 7 """    
        
        pptcontent['entrez_summary']=str("Entrez Gene Summary / (CAVA_GENE_ID : "+ensemble_id+")  => "+entrez_summary )
        
        """ Presentation Line 8 """    
        
        pptcontent['uniprot_summary']=str("Uniprot Gene Summary =>  "+uniprot_summary)       
        
        """ ADD neceassary URLs of sources """
        pptcontent['exac_url']=exac_url
        pptcontent['ncbi_url']=ncbi_url
        pptcontent['uniprot_url']=uniprot_url
        pptcontent['marrvel_url']=marrvel_url
        pptcontent['genecards_url']=genecards_url 
                  
        """ adding phenotypes list to ppt content """
        #pheno_list="Bruising_susceptibility,Autosomal_dominant_inheritance,Thrombocytopenia"
        def clean_phenotypes(pheno_list):
            #pheno_list="Motor_delay,Hyporeflexia,Autosomal_dominant_inheritance,Decreased_motor_nerve_conduction_velocity,Areflexia,Myelin_outfoldings,Autosomal_recessive_inheritance,Pes_cavus,Onion_bulb_formation,Juvenile_onset,Segmental_peripheral_demyelination/remyelination,Distal_sensory_impairment,Clusters_of_axonal_regeneration,Heterogeneous,Variable_expressivity,Decreased_number_of_peripheral_myelinated_nerve_fibers,Distal_amyotrophy,Distal_muscle_weakness,Hammertoe,Steppage_gait,Ptosis,Scoliosis,Increased_connective_tissue,Hypotrophy_of_the_small_hand_muscles,Nemaline_bodies,Foot_dorsiflexor_weakness,High_palate,Facial_palsy,Split_hand,Ulnar_claw,Flexion_contracture"
            pheno_items=pheno_list.split(",") 
            pheno_items=[re.sub("_"," ",p) for p in pheno_items]
            try:
                dom_recess=[p for p in pheno_items if p.__contains__("dominant")or p.__contains__("recessive")]
                inheritance=[dm for dm in dom_recess if dm.__contains__("Autosomal")]
            except:
                inheritance="NA"
            try:    
                pheno_types=[p for p in pheno_items if p not in inheritance]
            except:
                pheno_types="NA"
                
            ''' Inheritance Label '''    
            inheritance="".join(inheritance)
            recessive=inheritance.__contains__("recessive")
            dominant=inheritance.__contains__("dominant")        
            if recessive and dominant:
                pptcontent['Inheritance']= "AD/AR"
            elif dominant:
                pptcontent['Inheritance'] = "AD"  
            elif recessive:
                pptcontent['Inheritance'] = "AR"
            else:
                pptcontent['Inheritance']= "NA"

            pptcontent['phenotype_list']=pheno_types
            #else:
             #   pptcontent['phenotype_list']=pheno_types[0:14]
            
            
        clean_phenotypes(Phenotype_list)
                  
        """
        Capturing Screenshots (disabled) / un-comment below code chunk to enable screen shot capturing
        """
        #img_dir_comm=str("mkdir img")
        #os.popen(img_dir_comm)
        #Cgene="FANCD2"
        #home="h:/rp"
        #screen_shots(Cgene,home) ## triggering screenshot generation by calling screen_shots.py
                  
        return pptcontent
    
    """ method to generate content for subject in the presentation 
    it takes full variant_dataframe to generate table content """
    def subject_slide_content(self,variants_dataframe):
        slide_content=[]  
        Info_records=variants_dataframe.values.tolist()
        key_dict=self.generate_key_dictionary()
        for I in Info_records:            
            info_rec=I[7]
            inf_dic={}
            gene=str(info_rec).split(';')        
            #url=[]
            #non_url=[]
            for g in gene:
                if g.__contains__("href") or g.__contains__("www"):
                    # url.append(g)
                    continue                
                else:
                    if g.__contains__("="):
                        #non_url.append(g)
                        k,v=g.split("=")
                        inf_dic[k]=v 
            #print inf_dic['CAVA_CSN']
            
            if key_dict['NCBI_gene'] in inf_dic.keys():
                gene=inf_dic[key_dict['NCBI_gene']]
            else:
                gene="NA"
            if key_dict['Clinvar_transcript'] in inf_dic.keys():    
                Clinvar_transcipt=inf_dic[key_dict['Clinvar_transcript']]
            else:
                Clinvar_transcipt="NA"
            if key_dict['Clinvar_protein'] in inf_dic.keys():
                Clinvar_protein=inf_dic[key_dict['Clinvar_protein']]
            else:
                Clinvar_protein="NA"
            if key_dict['CAVA_CSN'] in inf_dic.keys():
                CAVA_CSN=inf_dic[key_dict['CAVA_CSN']]
            else :
                CAVA_CSN="NA"
            if Clinvar_transcipt==Clinvar_protein=="NA":
                tran=CAVA_CSN.split("_")[0]
                try:
                    prot=CAVA_CSN.split("_")[1]
                except:
                    prot="NA"
            else:
                tran,prot=Clinvar_transcipt,Clinvar_protein
        
        
            slide_content.append([gene,tran,prot])
        return slide_content   

""" DEBUGGING       
pc=generate_ppt_content(params[0],database_path)
pc.generate_info_dict(params[0][7])
pc.generate_key_dictionary()
"""