import os

species: list[str] = ["SARS_CoV_2"]
snps = [10, 20, 40, 60, 80, 100, 150, 200, 300, 400, 500]

holder: str = "SARS_CoV_2_500"

for s in species:
    for snp in snps:
        print(f"Replacing string: {s}_{snp}snps")
        os.system(f"sed -i 's/{holder}/{s}_{snp}/' workflow/Snakefile")
        os.system("snakemake -c 12 --use-conda")
        holder = f"{s}_{snp}"
