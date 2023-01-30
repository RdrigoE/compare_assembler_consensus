from random import random
from Bio import SeqIO
from numpy import identity


def generate_new_reference(old_reference_file, positions_change):
    with open(old_reference_file, "r", encoding="UTF8") as handler:
        old_ref = SeqIO.parse(handler, "fasta")
        old_ref = list(old_ref)[0].seq
        old_ref = str(old_ref)
        old_ref = [*old_ref]
    for position in positions_change:
        print(position)
        if old_ref[position] == "A":
            old_ref[position] = "T"
        elif old_ref[position] == "T":
            old_ref[position] = "A"
        elif old_ref[position] == "C":
            old_ref[position] = "G"
        elif old_ref[position] == "G":
            old_ref[position] = "C"
    new_reference = "".join(old_ref)
    return new_reference


import sys
import re
from random import choices as random_choices


def main():
    output_file = sys.argv[1]
    identity = int(re.findall("(?<=__)(.*?)(?=identity)", output_file)[0])
    size_of_spike_protein = 3821
    number_of_changes = size_of_spike_protein - int(
        size_of_spike_protein * (identity / 100)
    )
    original_reference = (
        "../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.fasta"
    )
    positions_of_spike = list(range(21563, 25384))
    for _ in range(30):
        positions = random_choices(positions_of_spike, k=number_of_changes)
        new_ref = generate_new_reference(original_reference, positions)
        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as new_file:
            new_file.write(
                ">SARS_CoV_2 Severe acute respiratory syndrome coronavirus 2 isolate Wuhan-Hu-1, randomly changed complete genome\n"
            )
            new_file.write(new_ref)


if __name__ == "__main__":
    main()
