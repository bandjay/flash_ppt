# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 09:47:18 2017

@author: M179100
"""

""" python wrapper to obtain annotated vcf from variants.txt file """
import os
import argparse

class annotate_variants:
        def __init__(self,input_variant_file,output_vcf_name,output_path):
          print " Running annotation "
          bior_path="/home/m179100/bior_annotate/trunk/bior_annotate.sh"
          input_variant_file=input_variant_file
          drill_file_path="/home/m179100/flash_ppt/config/auto_drill_file_fields"
          catalog_file_path="/home/m179100/flash_ppt/config/auto_catalog_file"
          output_vcf_name,output_path=output_vcf_name,output_path
          annotate_command=str(bior_path+" -v "+input_variant_file+" -d "+drill_file_path+" -c "+catalog_file_path+
                              " -o "+output_vcf_name+" -O "+output_path+" -Q NA -l")
          try:
              os.popen(annotate_command)
              print "Annotation is complete"
          except:
              print "Annotation is getting error" 
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Python program to annotate the variants file')
    parser.add_argument('-i','--input', help='input variant file path', required=True)
    parser.add_argument('-n','--name', help='output annotated vcf file name', required=True)
    parser.add_argument('-o','--output', help='output path to save the annotated vcf', required=True)
    args = vars(parser.parse_args())
    input_variant_file=args['input']
    output_vcf_name=args['name']
    output_path=args['output']
    annotate_variants(input_variant_file,output_vcf_name,output_path)
