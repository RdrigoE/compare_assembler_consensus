def get_consensus(wildcards):
    return f"align_samples/{wildcards.sample}/snippy/snps.depth.gz"


rule getCoverage:
    input:
        consensus=get_consensus,
    output:
        coverage="align_samples/{sample}/{sample}_coverage.csv",
    conda:
        "../envs/coverage.yaml"
    shell:
        "python ../workflow/software/getCoverage/getCoverage.py -i {input.consensus} -r {REFERENCE_FASTA} -o {output.coverage}"


rule mergeCoverage:
    input:
        expand(
            "align_samples/{sample}/{sample}_coverage.csv",
            sample=config_user["samples"],
        ),
    output:
        coverage_regular=expand(
            "{project}/coverage.csv",
            project=config_user["project"],
        ),
        coverage_translate=expand(
            "{project}/coverage_translate.csv",
            project=config_user["project"],
        ),
    shell:
        "python ../workflow/scripts/mergeCoverage.py '{input}' {output.coverage_regular} {output.coverage_translate} {REFERENCE_GB}"
