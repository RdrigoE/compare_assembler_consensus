from typing import Literal, NamedTuple, Union
import get_stats
import matplotlib.pyplot as plt


font_name = 'FreeSerif'
plt.rcParams['font.family'] = font_name
fontlabel = {"size": 11}
fonttitle = {"size": 15}


class Xlim(NamedTuple):
    left: int
    right: int


def plot_line(labels: list[int],
              snippy: list[int],
              ivar: list[int],
              parameter: Union[Literal["acc"], Literal["Ns"], Literal["MM"]],
              condition: Union[Literal["snps"], Literal["identity"]],
              dashed: bool = False,
              xlim: Union[Xlim, None] = None,
              stats: bool = False
              ):
    keys = {
        "Ns": "Ns",
        "acc": "Accuracy",
        "MM": "Mismatches"
    }
    line_thikness = 2
    colors = ["#304D63", "#ED8975"]

    plt.title(f"Mean {keys[parameter]}", pad=15, fontdict=fonttitle)
    if xlim:
        plt.xlim(xlim.left, xlim.right)
    plt.plot(
        labels,
        snippy,
        label="snippy",
        linewidth=line_thikness,
        color=colors[0]
    )
    if dashed:
        plt.plot(
            labels,
            ivar,
            label="iVar",
            linewidth=line_thikness,
            linestyle="dashed",
            color=colors[1]
        )
    else:
        plt.plot(
            labels,
            ivar,
            label="iVar",
            linewidth=line_thikness,
            color=colors[1]
        )

    if condition == "snps":
        plt.xlabel("Number of SNPs", labelpad=10, fontdict=fontlabel)
    elif condition == "identity":
        plt.xlabel("Identity frequency (%)", labelpad=10, fontdict=fontlabel)

    plt.ylabel(f"Mean {keys[parameter]} across 30 samples",
               labelpad=10, fontdict=fontlabel)
    plt.xscale("linear")
    plt.legend()

    if stats:
        significance_dict = get_stats.get_stats(condition, parameter)
        for idx, item in enumerate(significance_dict):
            plt.text(
                x=item, y=max(snippy[idx], ivar[idx]), s=significance_dict[item]
            )
        plt.savefig(f"{condition}_{parameter}_stats.png", dpi=300)
    else:
        plt.savefig(f"{condition}_{parameter}.png", dpi=300)
    plt.clf()


def scatter_plot(
    input_snippy: dict[int, dict[str, list[int]]],
    input_ivar: dict[int, dict[str, list[int]]],
    parameter: Union[Literal["acc"], Literal["Ns"], Literal["MM"]],
    condition: Union[Literal["snps"], Literal["identity"]],
):

    snippy_y = []
    ivar_y = []
    global_x = []
    keys = {
        "Ns": "Ns",
        "acc": "Accuracy",
        "MM": "Mismatches"
    }
    for key in input_snippy:
        for idx, value in enumerate(input_snippy[key][parameter]):
            global_x.append(key)
            snippy_y.append(value)
            ivar_y.append(input_ivar[key][parameter][idx])
    plt.scatter(x=global_x, y=snippy_y, label="snippy", marker="o")
    plt.scatter(x=global_x, y=ivar_y, label="iVar", marker="v")
    plt.xticks(rotation=90)
    plt.legend()

    if condition == "snps":
        plt.xlabel("Number of SNPs", labelpad=10, fontdict=fontlabel)
    elif condition == "identity":
        plt.xlabel("Identity frequency (%)", labelpad=10, fontdict=fontlabel)
    plt.ylabel(f"{keys[parameter]} per sample",
               labelpad=10, fontdict=fontlabel)
    plt.title(f"Number of {keys[parameter]}", fontdict=fonttitle)
    plt.savefig(f"scatter_{condition}_{parameter}.png", dpi=300)
    plt.clf()
