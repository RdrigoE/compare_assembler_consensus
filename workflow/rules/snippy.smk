# configfile: "../config/threads.yaml"


rule snippy_pe:
    input:
        reads_1="samples/{sample}/trimmed_reads/{sample}_1.trimmed.fastq.gz",
        reads_2="samples/{sample}/trimmed_reads/{sample}_2.trimmed.fastq.gz",
    output:
        depth="align_samples/{sample}/snippy/snps.depth.gz",
        bam="align_samples/{sample}/snippy/snps.bam",
        tab="align_samples/{sample}/snippy/snps.tab",
        consensus="align_samples/{sample}/snippy/snps.consensus.fa",
        vcf="align_samples/{sample}/snippy/snps.vcf",
    conda:
        "../envs/snippy.yaml"
    threads: 6  #config["snippy_threads"]
    params:
        get_snippy_parameters(software_parameters),
    shell:
        "rm -r align_samples/{wildcards.sample}/snippy/ && "

        "snippy --cpus {threads} --pe1 {input.reads_1} --pe2 {input.reads_2} --ref {REFERENCE_FASTA} --outdir align_samples/{wildcards.sample}/snippy/ {params}"


rule snippy_se:
    input:
        read="samples/{sample}/trimmed_reads/{sample}.trimmed.fastq.gz",
    output:
        depth="align_samples/{sample}/snippy/snps.depth.gz",
        bam="align_samples/{sample}/snippy/snps.bam",
        tab="align_samples/{sample}/snippy/snps.tab",
        consensus="align_samples/{sample}/snippy/snps.consensus.fa",
    threads: 6  #config["snippy_threads"]
    conda:
        "../envs/snippy.yaml"
    params:
        get_snippy_parameters(software_parameters),
    shell:
        "rm -r align_samples/{wildcards.sample}/snippy/ && "
        "snippy --cpus {threads} --se {input.read} --ref {REFERENCE_FASTA} --outdir align_samples/{wildcards.sample}/snippy/ {params}"


ruleorder: snippy_pe > snippy_se


rule snippy_depth_step_1:
    input:
        zipped="align_samples/{sample}/snippy/snps.depth.gz",
    output:
        unzipped="align_samples/{sample}/snippy/depth/snps.depth",
    shell:
        "gunzip -c {input.zipped} > {output.unzipped}"


rule snippy_depth_step_2:
    input:
        zipped="align_samples/{sample}/snippy/depth/snps.depth",
    output:
        unzipped="align_samples/{sample}/snippy/depth/{seg}.depth",
    shell:
        "python3 ../workflow/scripts/split_depth_file.py align_samples/{wildcards.sample}/snippy/depth/snps.depth {REFERENCE_GB} "
        "&& touch {output.unzipped}"


rule create_align_file_snippy:
    input:
        first_consensus="align_samples/{sample}/snippy/snps.consensus.fa",
    output:
        align_file=temp("align_samples/{sample}/snippy/snippy_align_{seg}.fasta"),
    shell:
        "python ../workflow/scripts/mask_consensus_by_deep.py {REFERENCE_FASTA} {input.first_consensus} {output.align_file} {wildcards.seg}"


rule align_mafft_snippy:
    input:
        align_file="align_samples/{sample}/snippy/snippy_align_{seg}.fasta",
    output:
        aligned_file=temp("align_samples/{sample}/snippy/snippy_aligned_{seg}.fasta"),
    conda:
        "../envs/mafft.yaml"
    threads: 6  #config["mafft_threads"]
    params:
        "--preservecase",
    shell:
        "mafft --thread {threads} {params} {input.align_file} > {output.aligned_file}"


rule msa_masker_snippy:
    input:
        align_file="align_samples/{sample}/snippy/snippy_aligned_{seg}.fasta",
        depth="align_samples/{sample}/snippy/depth/{seg}.depth",
    output:
        temp("align_samples/{sample}/snippy/consensus_aligned_{seg}.fasta"),
    conda:
        "../envs/msa_masker.yaml"
    params:
        "--c " + str(software_parameters["msa_masker"]),
    shell:
        "python ../workflow/scripts/msa_masker.py -i {input.align_file} -df {input.depth} -o {output} {params}"


rule get_masked_consensus_snippy:
    input:
        lambda wildcards: expand(
            "align_samples/{sample}/snippy/consensus_aligned_{seg}.fasta",
            sample=wildcards.sample,
            seg=get_locus(REFERENCE_GB),
        ),
    output:
        final_consensus="align_samples/{sample}/snippy/pre_{sample}_consensus.fasta",
    shell:
        "python ../workflow/scripts/get_consensus_medaka.py '{input}' {output}"


rule mask_regions_consensus_snippy:
    input:
        consensus="align_samples/{sample}/snippy/pre_{sample}_consensus.fasta",
    output:
        final_consensus="align_samples/{sample}/snippy/{sample}_consensus.fasta",
    params:
        mask_regions_parameters(software_parameters),
    shell:
        "python ../workflow/scripts/mask_regions.py {input} {output} {params}"
