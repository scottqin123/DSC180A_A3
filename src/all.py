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

pop = pd.read_excel('sample_info.xlsx')
tb = pd.read_table('plink.eigenvec', header = None, sep = ' ')
tb['pop'] = pop['Population']
tb['conti'] = tb['pop'].apply(to_conti)
def to_conti(x):
    if x == 'ACB' and 'ASW' and 'ESN' and 'GWD' and 'LWK' and 'MSL' and 'YRI':
        return 'African'
    elif x == 'BEB' and 'GIH' and 'ITU' and 'PJL' and 'STU':
        return 'Indo'
    elif x == 'GBR' and 'FIN' and 'IBS' and 'TSI':
        return 'Euro'
    elif x == 'CDX' and 'CHB' and 'JPT' and 'KHV' and 'CHS':
        return 'Asia'
    elif x == 'CLM' and 'MXL' and 'PEL' and 'PUR':
        return 'Latin'

def filterSNP():
    for i in range(1,23):
        n1 = 'plink2   --vcf /datasets/dsc180a-wi20-public/Genome/vcf/'
        n2 = 'ALL.chr' + str(i) + '.shapeit2_integrated_v1a.GRCh38.20181129.phased.vcf.gz'
        n3 = '   --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode  vcf   --out  '
        n4 = 'vcf' + str(i)
        sp.call(n1 + n2 + n3 + n4, shell = True)
def merge():
    vcf = ''
    for i in range(1,23):
        vcf = vcf + 'vcf' + str(i) + '.vcf' + ' '
    name = 'bcftools concat --output result.vcf' +  ' ' + vcf
    sp.call(name, shell = True)
def vcf():
    sp.call('plink2 --vcf result.vcf    --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode  --out  data/interim/chr22', shell = True)
    
def plot1():
    pop = pd.read_excel('sample_info.xlsx')
    tb = pd.read_table('plink.eigenvec', header = None, sep = ' ')
    tb['pop'] = pop['Population']
    tb['conti'] = tb['pop'].apply(to_conti)
    seaborn.scatterplot(x = tb[2], y = tb[3], hue = tb['conti'])
def plot2():
    seaborn.scatterplot(x = tb[2], y = tb[4], hue = tb['conti'])
def plot3():
    seaborn.scatterplot(x = tb[3], y = tb[4], hue = tb['conti'])