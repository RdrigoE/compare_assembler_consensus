from random import choices as random_choices
import re
import sys
from typing import NamedTuple, TypedDict
from Bio import SeqIO
import csv
from random import random

# Percentage rollete


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


def rollete_choice(percentage_list: list[float]) -> int:
    random_number = random()
    for idx, percentage in enumerate(percentage_list):
        if random_number <= percentage:
            return idx
    return len(percentage_list) - 1


def rollete(data: dict[int, AltValues], roll_times: int):
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
    total_count = sum(map(lambda x: x.times, data.values()))
    for _ in range(roll_times):
        # print(_)
        for key, value in data.items():
            current_percentage += value.times / total_count
            percentage_list.append(current_percentage)
            positions_list.append(key)
        chosen_index = rollete_choice(percentage_list)
        chosen_key = positions_list[chosen_index]
        chosen_values.append(chosen_key)
        total_count -= data[chosen_key].times
        del data[chosen_key]
        percentage_list = []
        positions_list = []
        current_percentage = 0
    return chosen_values


def generate_rollete(dictionary: dict[int, AltValues], roll_times: int):
    """
    The generate_rollete function takes a file of positions and rolls the rollete that many times.
    The function returns a list of strings, each string is one roll.

    :param positions_file: Get the dictionary of words from the file
    :param roll_times: int: Specify how many times the rollete will be rolled
    :return: A list of strings
    :doc-author: Trelent
    """
    return rollete(dictionary, roll_times)


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


def get_ref_id(ref: str):
    with open(ref) as handler:
        return list(SeqIO.parse(handler, "fasta"))[0].id


def main():
    original_reference = sys.argv[1]
    output_file = sys.argv[2]
    identity = int(re.findall("(?<=__)(.*?)(?=identity)", output_file)[0])
    size_of_spike_protein = 3821
    positions_of_spike = list(range(21563, 25384))
    number_of_changes = size_of_spike_protein - int(
        size_of_spike_protein * (identity / 100)
    )
    positions = random_choices(positions_of_spike, k=number_of_changes)
    new_ref = generate_new_reference(original_reference, positions)
    reference_id = ">" + \
        get_ref_id(original_reference) + " randomly changed complete genome\n"
    with open(output_file, "w", encoding="utf-8") as new_file:
        new_file.write(
            reference_id
        )
        new_file.write(new_ref)


if __name__ == "__main__":
    main()
