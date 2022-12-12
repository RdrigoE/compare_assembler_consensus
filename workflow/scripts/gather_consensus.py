"""Join consensus sequences from multiple files into one file."""
import sys
from Bio import SeqIO


def join_consensus(input_consensus: list[str], output_file: str) -> None:
    """Join consensus sequences from multiple files into one file."""
    with open(output_file, "w", encoding="utf-8") as handle_fasta_out_align:
        for consensus_file in input_consensus:
            with open(consensus_file, "r", encoding="utf-8") as handle_fasta:
                for record in SeqIO.parse(handle_fasta, "fasta"):
                    SeqIO.write(record, handle_fasta_out_align, "fasta")


if __name__ == "__main__":
    input_files = sys.argv[1].split(" ")
    OUTPUT_FILE = sys.argv[2]
    join_consensus(input_files, OUTPUT_FILE)
