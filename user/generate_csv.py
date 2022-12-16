import csv


def make_file(coverage, species):
    output = f"{species}_c{coverage}.csv"
    header = ["sample_name", "fastq1", "fastq2", "tech"]
    for sample in range(1, 31):
        sample_name = f"sample_{sample}_c{coverage}_{species}"
        sample_1 = f"{sample_name}_1.fastq.gz"
        sample_2 = f"{sample_name}_2.fastq.gz"
        with open(output, "a") as csv_handler:
            writer = csv.writer(csv_handler)
            if sample == 1:
                writer.writerow(header)
            writer.writerow([sample_name, sample_1, sample_2, "illumina"])


if __name__ == "__main__":
    coverage = [10, 30, 100]
    species = ["SARS_CoV_2", "Flu", "MPOX"]
    for cov in coverage:
        for spec in species:
            make_file(cov, spec)
