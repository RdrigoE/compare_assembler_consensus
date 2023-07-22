"""Analyse SNPs"""
from typing import Literal, Union
from scipy import stats
import re
import csv
from pathlib import Path
from collections import OrderedDict


def find_files_to_analyse(file_path: Path, treatment: str) -> list[str]:
    """
    The find_files_to_analyse function finds all the files in a given directory that are .csv files and contain
    the word 'snps' in their name. It returns a list of these file names.

    :param file_path: Path: Specify the path to the directory containing all of the files
    :return: A list of the names of all files in a given directory
    :doc-author: Trelent
    """
    found_files = []
    for current_file in file_path.iterdir():
        if (
            current_file.is_file()
            and current_file.suffix == ".csv"
            and treatment in current_file.name
        ):
            found_files.append(current_file.name)
    return found_files


def get_lines(file_name: str) -> tuple[list[list[str]], list[list[str]]]:
    """
    The get_lines_snps function takes a list of lists and returns two lists, one with the Snippy data
    and one with the Ivar data. The function assumes that each list in the original list is a
    separate sample (i.e., every other index should be Snippy or Ivar). The function also assumes
    that there are no headers in either file.

    :param data: list[list[str]]: Pass in the data from the csv file
    :return: A tuple of two lists
    :doc-author: Trelent
    """
    with open(file_name, encoding="UTF-8") as handler:
        reader = csv.reader(handler)
        data = list(reader)[1:]

    snippy_data = []
    ivar_data = []

    for idx in range(1, len(data), 2):
        snippy_data.append(data[idx - 1])
        ivar_data.append(data[idx])
    return snippy_data, ivar_data


def get_mean(data: list[list[str]], idx) -> int:
    return sum(list(map(lambda x: int(x[idx]), data))) // len(data)


def get_all(data: list[list[str]], idx) -> list[int]:
    return list(map(lambda x: int(x[idx]), data))


def full_Ns_MM(
    file_list: list[str], treatment: str
) -> list[dict[int, dict[str, list[int]]]]:
    snippy_d: dict[int, dict[str, list[int]]] = OrderedDict()
    ivar_d: dict[int, dict[str, list[int]]] = OrderedDict()
    ids = []
    for file_name in file_list:
        dict_id = int(
            re.findall(f"(?<=SARS_CoV_2_)(.*?)(?={treatment}.csv)", file_name)[
                0
            ]
        )
        snippy, ivar = get_lines(file_name)

        # Ns - 3
        # MM - 4
        # Accuracy - 6
        # snippy info
        snippy_Ns = get_all(snippy, 4)
        snippy_MM = get_all(snippy, 3)
        snippy_acc = get_all(snippy, 6)
        # ivar info
        ivar_Ns = get_all(ivar, 4)
        ivar_MM = get_all(ivar, 3)
        ivar_acc = get_all(ivar, 6)
        snippy_d[dict_id] = {
            "Ns": snippy_Ns,
            "MM": snippy_MM,
            "acc": snippy_acc,
        }

        ivar_d[dict_id] = {"Ns": ivar_Ns, "MM": ivar_MM, "acc": ivar_acc}
        ids.append(dict_id)
    ids.sort(reverse=True)
    snippy_to_return: dict[int, dict[str, list[int]]] = OrderedDict()
    ivar_to_return: dict[int, dict[str, list[int]]] = OrderedDict()
    for item in ids:
        snippy_to_return[item] = snippy_d[item]
        ivar_to_return[item] = ivar_d[item]
    return [snippy_to_return, ivar_to_return]


def get_Ns_MM(
    file_list: list[str], treatment: str
) -> list[dict[int, dict[str, int]]]:
    snippy_d: dict[int, dict[str, int]] = OrderedDict()
    ivar_d: dict[int, dict[str, int]] = OrderedDict()
    ids = []
    for file_name in file_list:
        dict_id = int(
            re.findall(f"(?<=SARS_CoV_2_)(.*?)(?={treatment}.csv)", file_name)[
                0
            ]
        )
        snippy, ivar = get_lines(file_name)
        # snippy info
        snippy_Ns = get_mean(snippy, 4)
        snippy_MM = get_mean(snippy, 3)
        snippy_acc = get_mean(snippy, 6)
        # ivar info
        ivar_Ns = get_mean(ivar, 4)
        ivar_MM = get_mean(ivar, 3)
        ivar_acc = get_mean(ivar, 6)
        snippy_d[dict_id] = {
            "Ns": snippy_Ns,
            "MM": snippy_MM,
            "acc": snippy_acc,
        }

        ivar_d[dict_id] = {"Ns": ivar_Ns, "MM": ivar_MM, "acc": ivar_acc}
        ids.append(dict_id)
    ids.sort(reverse=True)
    snippy_to_return: dict[int, dict[str, int]] = {}
    ivar_to_return: dict[int, dict[str, int]] = {}
    for item in ids:
        snippy_to_return[item] = snippy_d[item]
        ivar_to_return[item] = ivar_d[item]
    return [snippy_to_return, ivar_to_return]


def from_filepath_to_dict(treatment):
    current_directory = Path("./")
    files = find_files_to_analyse(current_directory, treatment)
    # snippy_dict, ivar_dict = get_Ns_MM(files, treatment)
    # [(number of snps, {'Ns': int, 'MM': int}), ]
    snippy_full, ivar_full = full_Ns_MM(files, treatment)
    # [(number of snps, {'Ns': int * 30, 'MM': int * 30}), ]
    return snippy_full, ivar_full


def get_stats(condition: Union[Literal["snps"], Literal["identity"]],
              parameter: Union[Literal["acc"], Literal["Ns"], Literal["MM"]]) -> dict[int, str]:
    snippy, ivar = from_filepath_to_dict(condition)
    # compare snippy 10 snps with ivar 10 snps

    # get them all into 2 arrays
    significative_array = {}
    for key in snippy:
        results = stats.ttest_ind(
            snippy[key][parameter], ivar[key][parameter]
        )
        # print(
        #     f"The value for the {type_of_experience} {key} SNPs is {results[1]}",
        #     end="",
        # )
        if results[1] < 0.001:
            significative_array[key] = "***"
            # print(" and it is significative to 0.001! ***\n")
        elif results[1] < 0.01:
            significative_array[key] = "**"
            # print(" and it is significative to 0.01! **\n")
        elif results[1] < 0.05:
            significative_array[key] = "*"
            # print(" and it is significative to 0.05! *\n")
        else:
            significative_array[key] = ""
            # print("\n")
    return significative_array


# get_stats("identity", "acc")
