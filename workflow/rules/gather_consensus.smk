def get_consensus_snippy(wildcards):
    test = (
        expand(
            "align_samples/{sample}/snippy/{sample}_consensus.fasta",
            sample=list(
                filter(lambda sample: f"{wildcards}" in sample, concatenated_illumina)
            ),
        ),
    )
    return test[0]


def get_consensus_ivar(wildcards):
    test = (
        expand(
            "align_samples/{sample}/iVar/{sample}_consensus.fasta",
            sample=list(
                filter(lambda sample: f"{wildcards}" in sample, concatenated_illumina)
            ),
        ),
    )
    return test[0]


rule gatherConsensusSequences_snippy:
    input:
        snippy=get_consensus_snippy,
    output:
        "{project}/snippy_consensus.fasta",
    shell:
        "python3 ../workflow/scripts/gather_consensus.py '{input.snippy}' {output}"


rule gatherConsensusSequences_iVar:
    input:
        iVar=get_consensus_ivar,
    output:
        "{project}/iVar_consensus.fasta",
    shell:
        "python3 ../workflow/scripts/gather_consensus.py '{input.iVar}' {output}"


rule compare_consensus:
    input:
        consensus_1="{project}/snippy_consensus.fasta",
        consensus_2="{project}/iVar_consensus.fasta",
    conda:
        "../envs/analyse.yaml"
    output:
        "{project}/compare_consensus.csv",
    shell:
        "python3 ../workflow/scripts/analyse_results.py {input.consensus_1} {input.consensus_2} {REFERENCE_FASTA} {output}"


rule compare_consensus_2:
    input:
        "{project}/compare_consensus.csv",
    conda:
        "../envs/analyse.yaml"
    output:
        "{project}/done.csv",
    shell:
        "touch done.csv"

rule get_plots:
    input:
        expand("{project}/compare_consensus.csv", project=project_names),
    output:
        mm =  "snps_MM_stats.png",
        acc = "snps_acc_stats.png",
        ns =  "snps_Ns_stats.png", 
    conda:
          "../envs/analyse.yaml"
    shell:
          "python ./../workflow/scripts/get_snps_plots.py './' "


