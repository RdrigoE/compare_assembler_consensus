import csv


def make_file(coverage, species):
    output = f"{species}_{coverage}snps.csv"
    header = ["sample_name", "fastq1", "fastq2", "tech"]
    for sample in range(1, 31):
        sample_name = f"sample_{sample}__{coverage}snps_{species}"
        sample_1 = f"{sample_name}_1.fastq.gz"
        sample_2 = f"{sample_name}_2.fastq.gz"
        with open(output, "a") as csv_handler:
            writer = csv.writer(csv_handler)
            if sample == 1:
                writer.writerow(header)
            writer.writerow([sample_name, sample_1, sample_2, "illumina"])


import yaml


def write_yaml(yaml_file_path: str, dump_dict: dict) -> None:
    """
    The write_yaml function writes a dictionary to a yaml file.

    :param yaml_file_path:str: Specify the path to the yaml file that will be written
    :param dump_dict:dict: Specify the dictionary that is to be written to a yaml file
    :return: None
    :doc-author: Trelent
    """
    with open(yaml_file_path, "w", encoding="utf-8") as file:
        yaml.dump(dump_dict, file)


def make_yaml(snps, species):
    dict = {}
    dict["project_name"] = f"{species}_{snps}snps"
    dict[
        "fasta_reference"
    ] = "../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.fasta"
    dict[
        "gb_reference"
    ] = "../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.gbk"
    dict["primers"] = "../user/primers/sars_cov_2.bed"
    dict["folder"] = f"{species}_{snps}snps"
    dict["coverage"] = 100
    dict["create_fastq_ref"] = f"../user/alt_ref/{species}_{snps}snps.fasta"
    write_yaml(f"{species}_{snps}snps.yaml", dict)


if __name__ == "__main__":
    snps = [10, 20, 40, 60, 80, 100, 150, 200, 300, 400, 500]
    species = ["SARS_CoV_2"]
    for snp in snps:
        for spec in species:
            make_file(snp, spec)
            make_yaml(snp, spec)
