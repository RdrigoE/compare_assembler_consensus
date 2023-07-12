import re
import sys
from Bio import SeqIO, SeqFeature, SeqRecord
import csv
from random import random
import numpy as np

# Percentage rollete


def get_dictionary(filename: str) -> dict[int, int]:
    with open(filename, "r", encoding="utf8") as handle:
        reader = csv.reader(handle)
        dic = {}
        for row in reader:
            key, value = row[0].split("\t")
            dic[int(key)] = int(value)
    return dic


def rollete_choice(percentage_list: list[float]) -> int:
    random_number = random()
    for idx, percentage in enumerate(percentage_list):
        if random_number <= percentage:
            return idx
    return len(percentage_list) - 1


def rollete(data: dict[int, int], roll_times: int):
    """
    The rollete function takes a dictionary of values and their counts,
    and returns a list of the chosen values. The function uses the rollete method to
    choose which value to pick next based on its percentage chance of being picked.
    The function will continue until it has rolled all the desired values.

    :param data: dict[int: Represent the position of the value in the rollete, and int is used to represent how many times that value has been chosen
    :param int]: Specify the type of data that is going to be returned
    :param roll_times: int: Determine how many times the function will roll
    :return: A list of values that were chosen
    :doc-author: Trelent
    """
    chosen_values: list[int] = []
    percentage_list: list[float] = []
    positions_list: list[int] = []
    current_percentage: float = 0
    total_count = sum(data.values())
    for _ in range(roll_times):
        # print(_)
        for key, value in data.items():
            current_percentage += value / total_count
            percentage_list.append(current_percentage)
            positions_list.append(key)
        chosen_index = rollete_choice(percentage_list)
        chosen_key = positions_list[chosen_index]
        chosen_values.append(chosen_key)
        total_count -= data[chosen_key]
        del data[chosen_key]
        percentage_list = []
        positions_list = []
        current_percentage = 0
    return chosen_values


def generate_rollete(positions_file, roll_times: int):
    """
    The generate_rollete function takes a file of positions and rolls the rollete that many times.
    The function returns a list of strings, each string is one roll.

    :param positions_file: Get the dictionary of words from the file
    :param roll_times: int: Specify how many times the rollete will be rolled
    :return: A list of strings
    :doc-author: Trelent
    """
    dictionary = get_dictionary(positions_file)
    return rollete(dictionary, roll_times)


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
    number_of_snps = int(re.findall("(?<=__)(.*?)(?=snps)", output_file)[0])

    positions_file = "../workflow/scripts/positions_2022_11_2022_12.csv"
    original_reference = (
        "../user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.fasta"
    )
    for _ in range(30):
        positions = generate_rollete(positions_file, number_of_snps)
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
