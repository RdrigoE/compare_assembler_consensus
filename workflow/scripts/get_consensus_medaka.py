"""tbd"""
import sys
import re
from tabnanny import check
from Bio import SeqIO, SeqRecord
from collections import Counter
from Bio.Seq import Seq


def check_elements(dict_elements):
    """tbd"""
    for key in dict_elements:
        if key not in "ATGCN-":
            return True
    return False


def restructure_consensus(consensus):
    """tbd"""
    consensus = [*consensus]
    vcf_file = (
        f"{re.findall('(?<=)(.*?)(?=/consensus)', consensus_file)[0]}/snps.vcf"
    )
    vcf_info = {}
    with open(vcf_file, "r", encoding="UTF-8") as handle_vcf:
        for line in handle_vcf:
            if line.startswith("#"):
                continue
            line = line.strip().split("\t")
            vcf_info[line[1]] = line[4]
    for n_idx, nucleotide in enumerate(consensus):
        if nucleotide not in "ATGCN-":
            consensus[n_idx] = vcf_info.get(str(n_idx + 1), "N")
    return Seq("".join(consensus))


consensus_files = sys.argv[1].split(" ")
output_file = sys.argv[2]

final_consensus_file = []
for consensus_file in consensus_files:
    aligned_sequence = list(SeqIO.parse(consensus_file, "fasta"))[1]
    aligned_sequence.id = f"{re.findall('(?<=align_samples/)(.*?)(?=/)',consensus_file)[0]}__{aligned_sequence.id}"
    dict_elements = Counter(aligned_sequence.seq)
    restruture_consensus = check_elements(dict_elements)
    if restruture_consensus:
        aligned_sequence.seq = restructure_consensus(aligned_sequence.seq)
    final_consensus_file.append(aligned_sequence)
with open(output_file, "w", encoding="utf-8") as handle_fasta_out_align:
    SeqIO.write(final_consensus_file, handle_fasta_out_align, "fasta")
