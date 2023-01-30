import csv
import yaml


def make_file(identity, species):
    output = f"{species}_{identity}identity.csv"
    header = ["sample_name", "fastq1", "fastq2", "tech"]
    for sample in range(1, 31):
        sample_name = f"sample_{sample}__{identity}identity_{species}"
        sample_1 = f"{sample_name}_1.fastq.gz"
        sample_2 = f"{sample_name}_2.fastq.gz"
        with open(output, "a") as csv_handler:
            writer = csv.writer(csv_handler)
            if sample == 1:
                writer.writerow(header)
            writer.writerow([sample_name, sample_1, sample_2, "illumina"])


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


def make_yaml(identity, species):
    dict = {}
    dict["project_name"] = f"{species}_{identity}identity"
    dict[
        "fasta_reference"
    ] = "../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.fasta"
    dict[
        "gb_reference"
    ] = "../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.gbk"
    dict["primers"] = "../user/primers/sars_cov_2.bed"
    dict["folder"] = f"{species}_{identity}identity"
    dict["coverage"] = 100
    dict[
        "create_fastq_ref"
    ] = f"../user/alt_ref/{species}_{identity}identity.fasta"
    write_yaml(f"{species}_{identity}identity.yaml", dict)


if __name__ == "__main__":
    # snps = [99, 98, 97, 96, 95, 93, 91, 89, 85, 80, 70]
    snps = [84, 79, 70]

    species = ["SARS_CoV_2"]
    for snp in snps:
        for spec in species:
            make_file(snp, spec)
            make_yaml(snp, spec)
