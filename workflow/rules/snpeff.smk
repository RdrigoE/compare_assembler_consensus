replace = f"sed -i 's/SARS_CoV_2/MN908947.3/g' " if len(SEGMENTS) == 1 else "true "


rule prepare_snpeff:
    input:
        ref_gb=REFERENCE_GB,
        ref_fa=REFERENCE_FASTA,
    output:
        "align_samples/{sample}/snp_ready.txt",
    conda:
        "../envs/snpeff.yaml"
    shell:
        "python ../workflow/scripts/create_snpeff_text.py $CONDA_PREFIX {input.ref_gb} {input.ref_fa} {REFERENCE_NAME} {output} "


rule snpeff_sample_ivar:
    input:
        i1="align_samples/{sample}/iVar/snps.vcf",
        i2="align_samples/{sample}/snp_ready.txt",
    output:
        "align_samples/{sample}/iVar/sample__{sample}_snpeff.vcf",
    conda:
        "../envs/snpeff.yaml"
    threads: 12
    params:
        "-no-downstream -no-upstream -no-intergenic -no-utr -noStats -c ../workflow/db/snpeff.config",
    shell:
        "{replace} {input.i1} && "
        "snpEff {params} -v {REFERENCE_NAME} {input.i1}  > {output}"
        #-t {threads}


rule snpeff_sample_snippy:
    input:
        i1="align_samples/{sample}/snippy/snps.vcf",
        i2="align_samples/{sample}/snp_ready.txt",
    output:
        "align_samples/{sample}/snippy/sample__{sample}_snpeff.vcf",
    conda:
        "../envs/snpeff.yaml"
    threads: 12
    params:
        "-no-downstream -no-upstream -no-intergenic -no-utr -noStats -c ../workflow/db/snpeff.config",
    shell:
        "{replace} {input.i1} && "
        "snpEff {params} -v {REFERENCE_NAME} {input.i1}  > {output}"
        #-t {threads}


"align_samples/{sample}/iVar/{sample}_freebayes.vcf",


rule freebayes_snpeff_sample_ivar:
    input:
        i1="align_samples/{sample}/iVar/sample__{sample}_freebayes.vcf",
        i2="align_samples/{sample}/snp_ready.txt",
    output:
        "align_samples/{sample}/iVar/sample__{sample}_freebayes_snpeff.vcf",
    conda:
        "../envs/snpeff.yaml"
    threads: 12
    params:
        "-no-downstream -no-upstream -no-intergenic -no-utr -noStats -c ../workflow/db/snpeff.config",
    shell:
        "{replace} {input.i1} && "
        "snpEff {params} -v {REFERENCE_NAME} {input.i1}  > {output}"
        #-t {threads}


rule freebayes_snpeff_sample_snippy:
    input:
        i1="align_samples/{sample}/snippy/sample__{sample}_freebayes.vcf",
        i2="align_samples/{sample}/snp_ready.txt",
    output:
        "align_samples/{sample}/snippy/sample__{sample}_freebayes_snpeff.vcf",
    conda:
        "../envs/snpeff.yaml"
    threads: 12
    params:
        "-no-downstream -no-upstream -no-intergenic -no-utr -noStats -c ../workflow/db/snpeff.config",
    shell:
        "{replace} {input.i1} && "
        "snpEff {params} -v {REFERENCE_NAME} {input.i1}  > {output}"
        #-t {threads}
