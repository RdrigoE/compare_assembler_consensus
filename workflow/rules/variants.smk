rule variant_validated_iVar:
    input:
        expand(
            "align_samples/{sample}/iVar/sample__{sample}_snpeff.vcf",
            sample=config_user["samples"],
        ),
    output:
        "{project}/validated_variants_iVar.csv",
    shell:
        "python ../workflow/scripts/variants.py '{input}' '{output}' validated_variants"


rule variant_validated_snippy:
    input:
        expand(
            "align_samples/{sample}/snippy/sample__{sample}_snpeff.vcf",
            sample=config_user["samples"],
        ),
    output:
        "{project}/validated_variants_snippy.csv",
    shell:
        "python ../workflow/scripts/variants.py '{input}' '{output}' validated_variants"


rule snpeff_concat_iVar:
    input:
        expand(
            "align_samples/{sample}/iVar/sample__{sample}_freebayes_snpeff.vcf",
            sample=config_user["samples"],
        ),
    output:
        "{project}/validated_minor_iSNVs_iVar.csv",
    shell:
        "python ../workflow/scripts/variants.py '{input}' {output} minor_iSNVs"


rule snpeff_concat_snippy:
    input:
        expand(
            "align_samples/{sample}/snippy/sample__{sample}_freebayes_snpeff.vcf",
            sample=config_user["samples"],
        ),
    output:
        "{project}/validated_minor_iSNVs_snippy.csv",
    shell:
        "python ../workflow/scripts/variants.py '{input}' {output} minor_iSNVs"


rule snpeff_concat_indels_iVar:
    input:
        expand(
            "align_samples/{sample}/iVar/sample__{sample}_freebayes_snpeff.vcf",
            sample=config_user["samples"],
        ),
    output:
        "{project}/validated_minor_iSNVs_inc_indels_iVar.csv",
    shell:
        "python ../workflow/scripts/variants.py '{input}' {output} minor_iSNVs_inc_indels"


rule snpeff_concat_indels_snippy:
    input:
        expand(
            "align_samples/{sample}/snippy/sample__{sample}_freebayes_snpeff.vcf",
            sample=config_user["samples"],
        ),
    output:
        "{project}/validated_minor_iSNVs_inc_indels_snippy.csv",
    shell:
        "python ../workflow/scripts/variants.py '{input}' {output} minor_iSNVs_inc_indels"


rule proportions_iSNVs_graph_iVar:
    input:
        expand(
            "align_samples/{sample}/iVar/sample__{sample}_freebayes_snpeff.vcf",
            sample=config_user["samples"],
        ),
    output:
        out_file="{project}/proportions_iSNVs_graph_iVar.csv",
    shell:
        "python ../workflow/scripts/proportions_iSNVs_graph.py '{input}' {output.out_file}"


rule proportions_iSNVs_graph_snippy:
    input:
        expand(
            "align_samples/{sample}/snippy/sample__{sample}_freebayes_snpeff.vcf",
            sample=config_user["samples"],
        ),
    output:
        out_file="{project}/proportions_iSNVs_graph_snippy.csv",
    shell:
        "python ../workflow/scripts/proportions_iSNVs_graph.py '{input}' {output.out_file}"
