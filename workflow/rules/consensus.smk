rule compare_consensus:
    input:
        consensus_1="{project}/snippy_consensus.fasta",
        consensus_2="{project}/iVar_consensus.fasta",
    conda:
        "../envs/analyse.yaml"
    output:
        "{project}/compare_consensus.csv",
    shell:
        "python3 ../workflow/scripts/analyse_results.py {input.consensus_1} {input.consensus_2} {REFERENCE_GB} {output}"
