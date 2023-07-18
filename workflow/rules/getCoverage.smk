def get_consensus(wildcards):
    return f"align_samples/{wildcards.sample}/snippy/snps.depth.gz"


rule getCoverage:
    input:
        consensus=get_consensus,
    output:
        coverage="align_samples/{sample}/{sample}_coverage.csv",
    shell:
        "python ../workflow/scripts/getCoverage.py -i {input.consensus} -r {REFERENCE_FASTA} -o {output.coverage} -g {REFERENCE_GB} -t 30"


def get_coverage(wildcards):
    test = expand(
        "align_samples/{sample}/{sample}_coverage.csv",
        sample=list(filter(lambda x: f"{wildcards}" in x, config_user["samples"])),
    )
    return test


rule mergeCoverage:
    input:
        coverage=get_coverage,
    output:
        coverage_regular="{project}/coverage.csv",
        coverage_translate="{project}/coverage_translate.csv",
    shell:
        "python ../workflow/scripts/mergeCoverage.py '{input.coverage}' {output.coverage_regular} {output.coverage_translate} {REFERENCE_GB}"
