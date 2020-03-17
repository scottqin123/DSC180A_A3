import etl

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

with open('config.json') as json_file:
    config = json.load(json_file)
fp = config['filepath'][0]
file = config['file'][0]
op = config['output'][0]
maf = config['maf'][0]
geno = config['geno'][0]
mind = config['mind'][0]

with open('dl.json') as json_file:
    config = json.load(json_file)
name = config['name'][0]
file = config['file'][0]

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('data', help='input file to be edited in config file')
parser.add_argument('process', help='data manipulation')

args = parser.parse_args()


if args.process == 'filter':
    etl.filter_SNP()
elif args.process == 'firstPCA':
    etl.pca_first_round()
elif args.process == 'first_plot':
    etl.first_plot()
elif args.process == 'secondPCA':
    etl.pca_second_round()
elif args.process == 'second_plot':
    etl.second_plot()
elif args.process == 'outlier':
    etl.remove_outlier()
elif args.process == 'dl':
    etl.dlgenome(name, file)
elif args.process == 'dlall':
    etl.dlall(name, file)
else:
    print("Please insert valid argument")
    #pca_first_round('data/interim/chr22', "chr22_test.vcf.gz")




#mkdir -p data/interim
#plink2   --vcf /datasets/dsc180a-wi20-public/Genome/vcf/sample/chr22_test.vcf.gz   --make-bed   --snps-only   --maf 0.05   --geno 0.1   --mind 0.05   --recode   --out data/interim/chr22
#plink2 --bfile data/interim/chr22 --pca
#plink2 --bfile data/interim/chr22 --remove-fam listfile.txt --pca

