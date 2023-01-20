rule generate_reads:
    output:
        "../user/reads/{folder}/{sample}_1.fq",
        "../user/reads/{folder}/{sample}_2.fq",
    conda:
        "../envs/art.yaml"
    shell:
        "art_illumina -p -i {REFERENCE_TO_CREATE}  -l 150 -f {COVERAGE} -m 290 -s 140  -o ../user/reads/{FOLDER_NAME}/{wildcards.sample}_"


rule gzip_reads:
    input:
        read_1="../user/reads/{folder}/{sample}_1.fq",
        read_2="../user/reads/{folder}/{sample}_2.fq",
    output:
        read_1="../user/reads/{folder}/{sample}_1.fastq.gz",
        read_2="../user/reads/{folder}/{sample}_2.fastq.gz",
    shell:
        "gzip -c {input.read_1} > {output.read_1} && "
        "gzip -c {input.read_2} > {output.read_2}"
