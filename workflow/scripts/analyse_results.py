"""Compare Multiple Consensus Sequences and Return the differences between them."""
import csv
import sys
import subprocess
from Bio import SeqIO


def read_multiple_fastas(file_name):
    with open(file_name) as handler:
        return list(SeqIO.parse(handler, "fasta"))


def read_unique_fasta(file_name):
    with open(file_name) as handler:
        return list(SeqIO.parse(handler, "fasta"))[0]


def get_alt_positions(g1, g2):
    positions = {}
    for p, (n1, n2) in enumerate(zip(g1.seq, g2.seq)):
        if n1 != n2:
            positions[p] = n1
    return positions


def compare_sequences(tool, ref, pos_interest):
    matches, missmatch, ns, gaps = 0, 0, 0, 0
    dict_acc = {}
    for p, (n1, n2) in enumerate(zip(tool, ref)):
        if p in pos_interest:
            dict_acc[p] = n1
        if n1 == "N":
            ns += 1
        elif n1 == "-":
            gaps += 1
        elif n1 == n2:
            matches += 1
        else:
            missmatch += 1

    return matches, missmatch, ns, gaps, dict_acc


def main():
    snippy_consensus_file = sys.argv[1]
    ivar_consensus_file = sys.argv[2]
    reference_fasta = sys.argv[3]
    output = sys.argv[4]
    reference_fasta = read_unique_fasta(reference_fasta)
    snippy_consensus = read_multiple_fastas(snippy_consensus_file)
    ivar_consensus = read_multiple_fastas(ivar_consensus_file)

    snippy_results = []
    for record in snippy_consensus:
        id = record.id
        parts = id.split("__")
        alt_reference_name = "__".join(parts[:2])
        alt_reference_fasta = read_unique_fasta(
            f"../user/alt_ref/{alt_reference_name}.fasta")
        snp_positions = get_alt_positions(alt_reference_fasta, reference_fasta)
        matches, missmatch, ns, gaps, pos_interest = compare_sequences(
            record.seq, alt_reference_fasta.seq, snp_positions.keys())

        count_acc = 0
        for key in pos_interest:
            if pos_interest[key] == snp_positions[key]:
                count_acc += 1
        if len(snp_positions.keys()) > 0:
            accuracy = int(count_acc / len(snp_positions.keys()) * 100)
        else:
            accuracy = 100
        snippy_results.append(
            (id, "snippy", matches, missmatch, ns, gaps, accuracy))

    ivar_results = []
    for record in ivar_consensus:
        id = record.id
        parts = id.split("__")
        alt_reference_name = "__".join(parts[:2])
        alt_reference_fasta = read_unique_fasta(
            f"../user/alt_ref/{alt_reference_name}.fasta")
        snp_positions = get_alt_positions(alt_reference_fasta, reference_fasta)
        matches, missmatch, ns, gaps, pos_interest = compare_sequences(
            record.seq, alt_reference_fasta.seq, snp_positions.keys())

        count_acc = 0
        for key in pos_interest:
            if pos_interest[key] == snp_positions[key]:
                count_acc += 1
        if len(snp_positions.keys()) > 0:
            accuracy = int(count_acc / len(snp_positions.keys()) * 100)
        else:
            accuracy = 100
        ivar_results.append(
            (id, "ivar", matches, missmatch, ns, gaps, accuracy))

    with open(output, "w") as handler:
        csv_writer = csv.writer(handler)
        csv_writer.writerow(("Sample", "Tool", "Matches",
                            "Missmatch", "N", "Gaps(-)", "Accuracy"))
        csv_writer.writerows(snippy_results)
        csv_writer.writerows(ivar_results)


if __name__ == "__main__":
    main()
