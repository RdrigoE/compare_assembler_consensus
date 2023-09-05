# Create Conda Environment to run Snakemake 
`mamba env create --name assembler --file config/assembler.yaml` 

# Configure run at 'user/sars_cov_2.yaml' 

```
coverage: 1000 # Coverage on the artificial samples
fasta_reference: ../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.fasta
gb_reference: ../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.gbk
project_name: SARS_CoV_2
snps: 0,10,20,30,40,50,100,200,300,400,500,1000 #condition of SNPs 
number_of_samples: 2 # Number of samples per condition
primers_fasta: sars_cov_2_artic_4_1.fasta # Primers for iVar
alt_positions: ../user/input_new_references/positions_sars_cov_2.tsv #file with optional nucleotides in each position
```

# Alternative positions example

```
Position    Occurences  A-occurences T-occurences C-occurences G-occurences
21617	1326	A-0	T-1326	C-0	G-0
21986	1325	A-1325	T-0	C-0	G-0
22577	1326	A-1326	T-0	C-0	G-0
22199	1326	A-32	T-0	C-0	G-1294
```
If there is a mutation in the first 3 positions the alternative nucleotide will be T in the first and A in the second and third.
In the last position most of the time it will be G, but sometimes it will be A

# Runnnig
```
snakemake -c 8 --use-conda
``` 

# Results

The plots are located in the folder results:
- "Mean_snps_acc_stats.png",
- "Mean_snps_MM_stats.png",
- "Mean_snps_Ns_stats.png",
- "Median_snps_acc_stats.png",
- "Median_snps_MM_stats.png",
- "Median_snps_Ns_stats.png",
- "scatter_snps_acc.png",
- "scatter_snps_MM.png",
- "scatter_snps_Ns.png",

