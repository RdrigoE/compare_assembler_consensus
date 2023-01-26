rule iVar_align_pe:
    input:
        reads_1="samples/{sample}/trimmed_reads/{sample}_1.trimmed.fastq.gz",
        reads_2="samples/{sample}/trimmed_reads/{sample}_2.trimmed.fastq.gz",
    output:
        bam="align_samples/{sample}/iVar/pre_snps.bam",
    conda:
        "../envs/ivar.yaml"
    log:
        "logs/align_samples/{sample}/iVar/mapping.log",
    shell:
        "mkdir align_samples/{wildcards.sample}/reference -p && "
        "cp {REFERENCE_FASTA} align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta && "
        "bwa index align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta && "
        "bwa mem align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta {input.reads_1} {input.reads_2} | "
        "samtools view -u -T align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta -q 20 | "
        "samtools sort --reference align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta > {output}"


rule primers_bam:
    input:
        pre_snps="align_samples/{sample}/iVar/pre_snps.bam",
    output:
        snps="align_samples/{sample}/iVar/snps.bam",
    conda:
        "../envs/ivar.yaml"
    params:
        "align_samples/{wildcards.sample}/iVar/snps",
    log:
        "logs/align_samples/{sample}/iVar/primers.log",
    shell:
        "samtools sort -o {input.pre_snps}.sorted {input.pre_snps} "
        "&& ivar trim -b {PRIMERS} -i {input.pre_snps}.sorted -m 35 -s 5  -p {output} -e "
        "&& samtools sort -o {output} {output}"


rule call_variant:
    input:
        bam="align_samples/{sample}/iVar/snps.bam",
    output:
        tsv_file="align_samples/{sample}/iVar/snps.tsv",
    conda:
        "../envs/ivar.yaml"
    log:
        "logs/align_samples/{sample}/iVar/call_variants.log",
    shell:
        "samtools mpileup -A -d 600000 -B -Q 0 {input.bam} --reference align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta | "
        "ivar variants -p align_samples/{wildcards.sample}/iVar/snps -q 20 -t 0.51  align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta "


rule generate_consensus:
    input:
        bam="align_samples/{sample}/iVar/snps.bam",
    output:
        consensus="align_samples/{sample}/iVar/snps.consensus.fa",
    conda:
        "../envs/ivar.yaml"
    params:
        "snps.consensus",
    log:
        "logs/align_samples/{sample}/iVar/generate_consensus.log",
    shell:
        "samtools mpileup -aa -A -Q 0 {input.bam} --reference align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta | ivar consensus -p align_samples/{wildcards.sample}/iVar/{params} -q 20 -t 0.51 -n N"


rule get_depth:
    input:
        i="align_samples/{sample}/iVar/snps.bam",
        consensus="align_samples/{sample}/iVar/snps.consensus.fa",
    output:
        only_depth="align_samples/{sample}/iVar/snps.depth.gz",
        depth="align_samples/{sample}/iVar/snps.depth",
        ind="align_samples/{sample}/iVar/snps.depth.gz.tbi",
    conda:
        "../envs/snippy.yaml"
    params:
        "-aa -q 20",
    log:
        "logs/align_samples/{sample}/iVar/get_depth.log",
    shell:
        "samtools depth {params} {input.i} | bgzip -c > {output.only_depth} "
        "&& tabix -p vcf {output.only_depth} && gunzip -c {output.only_depth}  > {output.depth} "


rule iVar_depth_1_2:
    input:
        consensus="align_samples/{sample}/iVar/snps.consensus.fa",
        depth="align_samples/{sample}/iVar/snps.depth",
    output:
        consensus="align_samples/{sample}/iVar/new_snps.consensus.fa",
    log:
        "logs/align_samples/{sample}/iVar/depth_1_2.log",
    shell:
        "python ../workflow/scripts/split_consensus.py {input.consensus} {input.depth} {REFERENCE_GB} {output.consensus}"


rule iVar_depth_step_2:
    input:
        zipped="align_samples/{sample}/iVar/snps.depth",
    output:
        unzipped="align_samples/{sample}/iVar/{seg}.depth",
    log:
        "logs/align_samples/{sample}/iVar/depth_step_2/{seg}.log",
    shell:
        "python ../workflow/scripts/split_depth_file.py {input.zipped} {REFERENCE_GB}"


rule create_align_file_iVar:
    input:
        first_consensus="align_samples/{sample}/iVar/new_snps.consensus.fa",
    output:
        align_file=temp("align_samples/{sample}/iVar/iVar_align_{seg}.fasta"),
    log:
        "logs/align_samples/{sample}/iVar/create_align_file/{seg}.log",
    shell:
        "python ../workflow/scripts/mask_consensus_by_deep.py align_samples/{wildcards.sample}/reference/{REFERENCE_NAME}.fasta {input.first_consensus} {output.align_file} {wildcards.seg}"


rule align_mafft_iVar:
    input:
        align_file="align_samples/{sample}/iVar/iVar_align_{seg}.fasta",
    output:
        aligned_file=temp("align_samples/{sample}/iVar/iVar_aligned_{seg}.fasta"),
    conda:
        "../envs/mafft.yaml"
    threads: 12
    params:
        "--preservecase",
    log:
        "logs/align_samples/{sample}/iVar/align_mafft/{seg}.log",
    shell:
        "mafft --thread {threads} {params} {input.align_file} > {output.aligned_file}"


rule msa_masker_iVar:
    input:
        align_file="align_samples/{sample}/iVar/iVar_aligned_{seg}.fasta",
        depth="align_samples/{sample}/iVar/{seg}.depth",
    output:
        temp("align_samples/{sample}/iVar/consensus_aligned_{seg}.fasta"),
    conda:
        "../envs/msa_masker.yaml"
    params:
        "--c " + str(software_parameters["mincov"] - 1),
    log:
        "logs/align_samples/{sample}/iVar/msa_masker/{seg}.log",
    shell:
        "python ../workflow/scripts/msa_masker.py -i {input.align_file} -df {input.depth} -o {output} {params}"


rule get_masked_consensus_iVar:
    input:
        lambda wildcards: expand(
            "align_samples/{sample}/iVar/consensus_aligned_{seg}.fasta",
            sample=wildcards.sample,
            seg=get_locus(REFERENCE_GB),
        ),
    output:
        final_consensus="align_samples/{sample}/iVar/pre_{sample}_consensus.fasta",
    log:
        "logs/align_samples/{sample}/iVar/get_masked_consensus.log",
    shell:
        "python ../workflow/scripts/get_consensus_medaka.py '{input}' {output}"


rule mask_regions_consensus_iVar:
    input:
        consensus="align_samples/{sample}/iVar/pre_{sample}_consensus.fasta",
        tsv_file="align_samples/{sample}/iVar/snps.tsv",
    output:
        final_consensus="align_samples/{sample}/iVar/{sample}_consensus.fasta",
        vcf_file="align_samples/{sample}/iVar/snps.vcf",
    params:
        mask_regions_parameters(software_parameters),
    log:
        "logs/align_samples/{sample}/iVar/mask_regions_consensus.log",
    shell:
        "python ../workflow/scripts/mask_regions.py {input.consensus} {output.final_consensus} {params} "
        " && "
        "python ../workflow/scripts/convert_vcf.py {input.tsv_file} {output.vcf_file} "
