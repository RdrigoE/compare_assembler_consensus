from random import choices as random_choices
import re
import sys
from random import random
from typing import NamedTuple, TypedDict
from Bio import SeqIO
from pandas.io.parsers.readers import csv


class AltTimes(TypedDict, total=False):
    a: int
    t: int
    g: int
    c: int


class AltValues(NamedTuple):
    times: int
    nucleotides: AltTimes


def get_dictionary(filename: str) -> dict[int, AltValues]:
    with open(filename, "r", encoding="utf8") as handle:
        reader = csv.reader(handle)
        dic: dict[int, AltValues] = {}
        for row in reader:
            row_key, row_value, *nucleotides = row[0].split("\t")
            temp_dict = {}
            for i in nucleotides:
                key, value = i.split("-")
                temp_dict[key] = int(value)

            dic[int(row_key)] = AltValues(
                int(row_value), temp_dict)
    return dic


def choose_alternative(alt_nucleotides: AltTimes) -> str:
    total = sum(alt_nucleotides.values())
    percentage = {}
    sum_count = 0
    for key in alt_nucleotides:
        sum_count += alt_nucleotides[key]/total
        percentage[key] = sum_count
    choice = random()
    for key in percentage:
        if percentage[key] >= choice:
            return key
    raise ValueError("This is not supose to happen")


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
