rule generate_alt_ref:
    output:
        "../user/alt_ref/{sample}.fasta",
    shell:
        "python ../workflow/scripts/create_new_references_spike.py {output}"
