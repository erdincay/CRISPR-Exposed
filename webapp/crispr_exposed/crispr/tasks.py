from celery import task
import tempfile

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@task()
def blastn(FASTA):
    ## generatign random file names
    fasta_temp = tempfile.NamedTemporaryFile()
    blast_temp = tempfile.NamedTemporaryFile()
    
    fasta_file = open(os.path.join(BASE_DIR, "crispr/blast", fasta_temp.name) ,'w')
    fasta_file.writelines(">input\n"+FASTA)
    fasta_file.close()
    
    ## blastn command
    exit_code = os.system("blastn -query " +
                str(os.path.join(BASE_DIR, 'crispr/blast', fasta_temp.name)) + " -db " +
                str(os.path.join(BASE_DIR, 'crispr/blast/db/spacers.fasta')) + " -out " +
                str(os.path.join(BASE_DIR, 'crispr/blast', blast_temp.name)))

    ## loop until file is generated
    blast_result_txt = ''
    if(exit_code == 0):
        try:
            blast_result_file = open(os.path.join(BASE_DIR, "crispr/blast", blast_temp.name), 'r')
            if(blast_result_file):
                ## reading blast result file into memory
                blast_result_txt = blast_result_file.read()
                blast_result_file.close()
                #break
        except File.DoesNotExist:
            pass        ## raise?
    else:
        blast_result_txt = "Oops...!\tSorry, something went wrong while running blast!\nPlease try again."
    return blast_result_txt
