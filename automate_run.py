import os

species: list[str] = ["SARS_CoV_2"]
# snps = [99, 98, 97, 96, 95, 93, 91, 89, 85, 80, 70]
snps = [85, 80, 70]

holder: str = "SARS_CoV_2_70"

for s in species:
    for snp in snps:
        print(f"Replacing string: {s}_{snp}identity")
        os.system(f"sed -i 's/{holder}/{s}_{snp}/' workflow/Snakefile")
        os.system("snakemake -c 12 --use-conda -k")
        holder = f"{s}_{snp}"
