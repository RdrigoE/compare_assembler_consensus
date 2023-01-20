from Bio import SeqIO
from Bio.Seq import Seq
import csv
import sys


def get_fasta_sequences(file_name: str) -> list:
    with open(file_name, "r") as handler:
        sequences = list(SeqIO.parse(handler, "fasta"))
        return sequences


def compare_reference(sequence: str, reference: str):
    gaps = 0
    n_s = 0
    miss_match = 0
    matches = 0
    for idx, nt in enumerate(sequence):
        if idx < len(reference):
            if nt == reference[idx]:
                matches += 1
            elif nt == "N":
                n_s += 1
            elif nt == "-":
                gaps += 1
            else:
                miss_match += 1
    return [matches, miss_match, n_s, gaps]


def main():
    snippy_file = sys.argv[1]
    iVar_file = sys.argv[2]
    reference_file = sys.argv[3]
    output_file = sys.argv[4]
    snippy = get_fasta_sequences(snippy_file)
    iVar = get_fasta_sequences(iVar_file)
    reference = get_fasta_sequences(reference_file)

    dictionary = {}
    # Get the keys in dictionary
    for identifier in snippy:
        dictionary[identifier.id] = {"snippy": [], "iVar": []}

    # Analyse Snippy Consensus
    if len(reference) == 1:
        for entry in snippy:
            dictionary[entry.id]["snippy"] = compare_reference(
                entry.seq, reference[0].seq
            )
    else:
        n_locus = len(reference) - 1
        current_locus = 0
        for entry in snippy:
            dictionary[entry.id]["snippy"] = compare_reference(
                entry.seq, reference[current_locus].seq
            )
            if current_locus < n_locus:
                current_locus += 1
            else:
                current_locus = 0

    if len(reference) == 1:
        for entry in iVar:
            dictionary[entry.id]["iVar"] = compare_reference(
                entry.seq, reference[0].seq
            )
    else:
        n_locus = len(reference) - 1
        current_locus = 0
        for entry in iVar:
            dictionary[entry.id]["iVar"] = compare_reference(
                entry.seq, reference[current_locus].seq
            )
            if current_locus < n_locus:
                current_locus += 1
            else:
                current_locus = 0

    header = ["Sample", "Tool", "Matches", "Missmatch", "N", "Gaps(-)"]
    with open(output_file, "w") as handler:
        writer = csv.writer(handler)
        writer.writerow(header)
        for key, value in dictionary.items():
            writer.writerow(
                [
                    key,
                    "snippy",
                    value["snippy"][0],
                    value["snippy"][1],
                    value["snippy"][2],
                    value["snippy"][3],
                ]
            )
            writer.writerow(
                [
                    key,
                    "iVar",
                    value["iVar"][0],
                    value["iVar"][1],
                    value["iVar"][2],
                    value["iVar"][3],
                ]
            )


if __name__ == "__main__":
    main()
