rule freebayes_snippy:
    input:
        samples="align_samples/{sample}/snippy/snps.bam",
        ref=REFERENCE_FASTA,
    output:
        "align_samples/{sample}/snippy/sample__{sample}_freebayes.vcf",
    conda:
        "../envs/freebayes.yaml"
    params:
        "--min-mapping-quality 20 --min-base-quality 20 --min-coverage 100 --min-alternate-count 10  --min-alternate-fraction 0.01 --ploidy 2 -V ",
    shell:
        "freebayes {params} -f {input.ref} {input.samples} > {output}"


rule freebayes_iVar:
    input:
        samples="align_samples/{sample}/iVar/snps.bam",
        ref=REFERENCE_FASTA,
    output:
        "align_samples/{sample}/iVar/sample__{sample}_freebayes.vcf",
    conda:
        "../envs/freebayes.yaml"
    params:
        "--min-mapping-quality 20 --min-base-quality 20 --min-coverage 100 --min-alternate-count 10  --min-alternate-fraction 0.01 --ploidy 2 -V ",
    shell:
        "freebayes {params} -f {input.ref} {input.samples} > {output}"
