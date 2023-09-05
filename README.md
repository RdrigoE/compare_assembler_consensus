# Create Conda Environment to run Snakemake 
`mamba env create --name assembler --file config/assembler.yaml` 

# Configure run at 'user/sars_cov_2.yaml' 

```
coverage: 1000
fasta_reference: ../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.fasta
gb_reference: ../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.gbk
project_name: SARS_CoV_2
identity: 100,95,90,85,80,75,70,50
number_of_samples: 2
primers_fasta: sars_cov_2_artic_4_1.fasta
```

# Runnig
```
snakemake -c 8 --use-conda
``` 

# Results

The plots are located in the folder results:
- "Mean_identity_acc_stats.png",
- "Mean_identity_MM_stats.png",
- "Mean_identity_Ns_stats.png",
- "Median_identity_acc_stats.png",
- "Median_identity_MM_stats.png",
- "Median_identity_Ns_stats.png",
- "scatter_identity_acc.png",
- "scatter_identity_MM.png",
- "scatter_identity_Ns.png",

