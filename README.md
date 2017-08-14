# flash_ppt 

## Author: Jay Bandlamudi

### Genetic report automation tool at MAYO CLINIC 


### Flash ppt is a software/tool written in python ,to automate the pptx genetic report generation process in data pipelines.

### Back ground:
#### Genetic report contains information about  gene variants from a subject/patient and it is used by Genetic counselors to analyse disease and provide counseling to patients. Genetic information comes from several sources such as multiple catalog files(from clinical labs across the world) and websites such as OMIM,NCBI,HGMD etc., 
#### At Mayo Genetic counselors prepares these reports manually typically it takes 3 hours to put together a single report .As report preparation  is cumbersome so the whole process is automated in order to reduce the human effort.With automation a single report can be generated in less than a minute.

#### Annotations of a variant can be obtained from bior annotation , as the sample vcf is already annotated you dont have to run annotation step in Instructions.

### Dependencies

* python 2.7
* pptx,pandas,selenium,bs4,biopython,sqlite3

```
$ sudo pip install pptx,pandas,selenium,bs4,biopython,sqlite3
```

### Instructions to run tool by using sample vcfs [[Instrcutions](https://github.com/bandjay/flash_ppt/blob/master/Instructions.txt)]

### class-diagram for different modules of tool ![class_diagram](https://github.com/bandjay/flash_ppt/blob/master/class_diagram.PNG)

### sample pptx report generated using the tool [[sample_report](https://github.com/bandjay/flash_ppt/blob/master/sample_report.pptx)]

### More details can be found in the presentation [[Tool Presentation](https://github.com/bandjay/flash_ppt/blob/master/Tool_Presentation.pptx)]

