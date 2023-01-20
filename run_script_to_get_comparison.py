import os

species = ["flu", "mpx", "sars_dataset"]
coverage = [10, 30, 100]
alt = ["", "_alt"]

path = "results/"

snippy = "/snippy_consensus.fasta"
iVar = "/iVar_consensus.fasta"


ref_dic = {
    "flu": "user/references/A_H3N2_A_Victoria_361_2011.fasta",
    "mpx": "user/references/monkeypox_MT903344_MPXV_UK_P2_wo_NN.fasta",
    "sars_dataset": "user/references/SARS_CoV_2_COVID_19_Wuhan_Hu_1_MN908947.fasta",
}

for spec in species:
    for cov in coverage:
        for a in alt:
            folder_game = spec + "_" + str(cov) + a
            file_path = path + folder_game
            snippy_file = file_path + snippy
            iVar_file = file_path + iVar
            output = file_path + "/" + folder_game + ".csv"
            os.system(
                f"python3 get_stats_aligment.py {snippy_file} {iVar_file} {ref_dic[spec]} {output}"
            )
