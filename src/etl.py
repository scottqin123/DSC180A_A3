import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np
import subprocess as sp
import shlex
import seaborn
import os
import json
import argparse

with open('config.json') as json_file:
    config = json.load(json_file)
fp = config['filepath'][0]
file = config['file'][0]
op = config['output'][0]
maf = config['maf'][0]
geno = config['geno'][0]
mind = config['mind'][0]

if not os.path.exists(fp):
    cmd = shlex.split('mkdir -p ' + fp)
    sp.call(cmd, shell = True)
def filter_SNP():    
    sp.call('plink2   --vcf ' + file + '   --make-bed   --snps-only   --maf ' + str(maf) + '   --geno ' + str(geno) + '   --mind ' + str(mind) + '   --recode   --out ' + op, shell = True)

def pca_first_round():
    sp.call('plink2 --bfile ' + op + ' --pca', shell = True)

def filter_allSNP():
    for i in range(1, 21):
        name = 'plink2   --vcf /datasets/dsc180a-wi20-public/Genome/vcf/sample/chr22_test.vcf.gz   --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode   --out data/interim/chr22'
        'ALL.chr' + int(i) + '.shapeit2_integrated_v1a.GRCh38.20181129.phased.vcf.gz'
        '   --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode  vcf   --out data/interim/chr22'
    
def merge_All():
    vcf = ''
    for i in range(1,23):
        vcf = vcf + 'vcf' + str(i) + '.vcf' + ' '
    vcf
    name = 'bcftools concat --output result.vcf' +  ' ' + vcf 
    sp.call(name, shell = True)
    
    
def remove_outlier(file = 'plink.eigenvec'):
    # read the vcf file as a dataframe
    tb = pd.read_table(file, header = None, sep = ' ')

    # calculate the standard deviation and multiply it by 2
    twostdv = np.std(tb[2])*2

    #reindex
    temp = tb.set_index(tb[0])
    temp = temp.drop([0,1], axis = 1)

    # choose the first 10 components
    temp = temp.iloc[:, 0:10]
    #select the outliers, which are two standard deviation away from the mean
    ol = (temp.abs()<twostdv).all(axis = 1)
    ollist = list(ol[ol == False].index)
    #write the outlier list into a text file
    with open('ollist.txt', 'w') as filehandle:
        for listitem in o:
            filehandle.write('%s\n' % listitem)

def first_plot(file = 'plink.eigenvec'):
    tb = pd.read_table(file, header = None, sep = ' ')
    tb.plot(2,3, kind = 'scatter')

def pca_second_round():
    sp.call('plink2 --bfile ' + op + ' --remove-fam listfile.txt --pca', shell = True)

def second_plot(file = 'plink.eigenvec'):
    tb = pd.read_table(file, header = None, sep = ' ')
    tb.plot(2,3, kind = 'scatter')


import urllib

# this function takes in a number and a file name and download it
def dlgenome(number, file):
    tempfile = urllib.request.urlopen("ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/" + number + '/sequence_read/' + file)
    with open(str(number) + '.fastq','wb') as output:
        output.write(tempfile.read())

#this function takes in a json and download all the needed file
def dlall(js):
    for i in js['file']:
        dlgenome(js['name'], i)