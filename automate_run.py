import os

species = ["Flu"]  # ["MPOX", "SARS_CoV_2", "Flu"]
coverage = ["010", "030", "100"]

holder = "Flu_c100"

for s in species:
    for c in coverage:
        print(f"Replacing string: {s}_c{c}")
        os.system(f"sed -i 's/{holder}/{s}_c{c}/' workflow/Snakefile")
        os.system("snakemake -c 12 --use-conda --ri")
        holder = f"{s}_c{c}"
