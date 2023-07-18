

from typing import Literal, TypedDict, Union 


class Sample_Dict(TypedDict):
    fastq1: str
    fastq2: str
    tech: Union[Literal["illumina"], Literal["ont"]]


def create_sample_dict(number_of_samples: int, list_of_snps: list[int], locus: str) -> dict[str, Sample_Dict]:
    sample_dict: dict[str, Sample_Dict] = {}
    for snp in list_of_snps:
        for sample_number in range(1, number_of_samples + 1):
            key = f"sample_{sample_number}__{snp}snps_{locus}"
            sample_dict[key] = {
                "fastq1": f"sample_{sample_number}__{snp}snps_{locus}_1.fastq.gz",
                "fastq2": f"sample_{sample_number}__{snp}snps_{locus}_2.fastq.gz",
                "tech": "illumina"
            }
    return sample_dict
