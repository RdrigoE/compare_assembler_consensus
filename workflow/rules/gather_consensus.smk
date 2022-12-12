
rule gatherConsensusSequences_snippy:
    input:
        snippy=expand(
            "align_samples/{sample}/snippy/{sample}_consensus.fasta",
            sample=concatenated_illumina,
        ),
    output:
        "{project}/snippy_consensus.fasta",
    shell:
        "python3 ../workflow/scripts/gather_consensus.py '{input.snippy}' {output}"


rule gatherConsensusSequences_iVar:
    input:
        iVar=expand(
            "align_samples/{sample}/iVar/{sample}_consensus.fasta",
            sample=concatenated_illumina,
        ),
    output:
        "{project}/iVar_consensus.fasta",
    shell:
        "python3 ../workflow/scripts/gather_consensus.py '{input.iVar}' {output}"
