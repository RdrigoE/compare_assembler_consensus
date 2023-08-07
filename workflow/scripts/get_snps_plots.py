"""Analyse SNPs"""
import sys
from plots import plot_line, scatter_plot
import csv
from pathlib import Path
import matplotlib.pyplot as plt
from collections import OrderedDict

font_name = 'FreeSerif'
plt.rcParams['font.family'] = font_name


def find_files_to_analyse(file_path: Path) -> list[str]:
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
            current_file.is_dir() and not str(current_file).startswith(
                "__") and "identity" in str(current_file)
        ):
            found_files.append(current_file.name + "/compare_consensus.csv")
    return found_files


def get_lines_snps(file_name: str) -> tuple[list[list[str]], list[list[str]]]:
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

    for line in data:
        if line[1] == "snippy":
            snippy_data.append(line)
        elif line[1] == "ivar":
            ivar_data.append(line)
    return (snippy_data, ivar_data)


def get_mean(data: list[list[str]], idx) -> int:
    return sum(list(map(lambda x: int(x[idx]), data))) // len(data)


def get_median(data: list[list[str]], idx) -> int:
    new_data = sorted(list(map(lambda x: int(x[idx]), data)))
    return new_data[len(data)//2]


def get_all(data: list[list[str]], idx) -> list[int]:
    return list(map(lambda x: int(x[idx]), data))


def full_Ns_MM(
    file_list: list[str],
) -> list[dict[int, dict[str, list[int]]]]:
    snippy_d: dict[int, dict[str, list[int]]] = OrderedDict()
    ivar_d: dict[int, dict[str, list[int]]] = OrderedDict()
    ids = []
    for file_name in file_list:

        for idx, char in enumerate(file_name):
            if char.isalpha():
                stop_at = idx
                break

        dict_id = int(file_name[:stop_at])
        snippy, ivar = get_lines_snps(file_name)

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


def get_Ns_MM(file_list: list[str]) -> list[dict[int, dict[str, int]]]:
    snippy_d: dict[int, dict[str, int]] = OrderedDict()
    ivar_d: dict[int, dict[str, int]] = OrderedDict()
    ids = []
    for file_name in file_list:

        for idx, char in enumerate(file_name):
            if char.isalpha():
                stop_at = idx
                break

        dict_id = int(file_name[:stop_at])
        snippy, ivar = get_lines_snps(file_name)
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


def get_Ns_MM_median(file_list: list[str]) -> list[dict[int, dict[str, int]]]:
    snippy_d: dict[int, dict[str, int]] = OrderedDict()
    ivar_d: dict[int, dict[str, int]] = OrderedDict()
    ids = []
    for file_name in file_list:

        for idx, char in enumerate(file_name):
            if char.isalpha():
                stop_at = idx
                break

        dict_id = int(file_name[:stop_at])
        snippy, ivar = get_lines_snps(file_name)
        # snippy info
        snippy_Ns = get_median(snippy, 4)
        snippy_MM = get_median(snippy, 3)
        snippy_acc = get_median(snippy, 6)
        # ivar info
        ivar_Ns = get_median(ivar, 4)
        ivar_MM = get_median(ivar, 3)
        ivar_acc = get_median(ivar, 6)
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


if __name__ == "__main__":
    current_directory = Path(sys.argv[1])
    files = find_files_to_analyse(current_directory)
    snippy_dict_mean, ivar_dict_mean = get_Ns_MM(files)
    snippy_dict_median, ivar_dict_median = get_Ns_MM_median(files)
    snippy_full, ivar_full = full_Ns_MM(files)

    print(snippy_dict_median, ivar_dict_median)
    print(snippy_dict_mean, ivar_dict_mean)

    for parameter in ("Ns", "acc", "MM"):
        plot_line(
            labels=list(ivar_dict_mean.keys()),
            snippy=list(
                map(lambda x: x.get(parameter, 0), snippy_dict_mean.values())),
            ivar=list(map(lambda x: x.get(parameter, 0),
                      ivar_dict_mean.values())),
            title="Mean",
            parameter=parameter,
            condition='identity',
            dashed=True,
            stats=True,
        )
        plot_line(
            labels=list(ivar_dict_median.keys()),
            snippy=list(
                map(lambda x: x.get(parameter, 0), snippy_dict_median.values())),
            ivar=list(map(lambda x: x.get(parameter, 0),
                      ivar_dict_median.values())),
            title="Median",
            parameter=parameter,
            condition='identity',
            dashed=True,
            stats=True,
        )
        scatter_plot(input_snippy=snippy_full,
                     input_ivar=ivar_full,
                     parameter=parameter,
                     condition='identity',
                     )
