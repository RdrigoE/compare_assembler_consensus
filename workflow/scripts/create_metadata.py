import csv
from pathlib import Path
from dataclasses import dataclass
import sys

@dataclass
class SampleClean:
    species: str
    coverage: int
    sample: int

def main() -> None:
    """tbd"""
    current_dir = Path(path_files).glob('*')
    fastq_list = list(map(str, list(current_dir)))
    fastq_list.sort()
    fastq_list.pop(0)
    clean_names = []
    for sample in fastq_list:
        species_coverage, sample_position = sample.split('_coverage_')
        species, coverage = species_coverage.split('_c')
        sample = sample_position.split('_')[0]
        new_sample = SampleClean(species, coverage, sample)
        if new_sample not in clean_names:
            clean_names.append(new_sample)
    with open(output, 'w', encoding='utf-8') as csv_handler:
        writer = csv.writer(csv_handler)
        writer.writerow(['sample_name', 'fastq1', 'fastq2', 'tech'])
        for sample in clean_names:
            sample_name = f"sample_{sample.sample}_c{sample.coverage}_{sample.species}"
            sample_1 = f"{sample.species}_c{sample.coverage}_coverage_{sample.sample}_1.fastq.gz"
            sample_2 = f"{sample.species}_c{sample.coverage}_coverage_{sample.sample}_2.fastq.gz"
            writer.writerow([sample_name,sample_1,sample_2,'illumina'])




if __name__ == '__main__':
    path_files = sys.argv[1]
    output = sys.argv[2]
    main()