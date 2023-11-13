import os
import re
from glob import glob

from Bio import SeqIO
from Bio.Blast.Applications import (
    NcbiblastpCommandline,
    NcbimakeblastdbCommandline,
)
from dotenv import load_dotenv

from plasticome.config.celery_config import celery_app
from plasticome.services.plasticome_metadata_service import get_all_enzymes

load_dotenv(override=True)


def get_protein_sequences():
    """
    The function `get_protein_sequences` retrieves protein sequences for all
    enzymes using credentials and returns all unique sequences.
    :return: a set of protein sequences.
    """
    enzymes_info, error = get_all_enzymes(
        os.getenv('PLASTICOME_USER'), os.getenv('PLASTICOME_PASSWORD')
    )
    if error:
        return set()
    return set(item['protein_sequence'] for item in enzymes_info)


def protein_sequences_to_fasta(protein_list: list, output_path: str):

    output_file = os.path.join(output_path, 'proteins_to_db.fasta')
    with open(output_file, 'w') as fasta_file:
        for sequence in protein_list:
            match = re.match(r'(>.*?)([A-Z ]{10,})$', sequence)
            if match:
                header, sequence = match.groups()
                fasta_file.write(header + '\n')
                fasta_file.write(sequence.strip() + '\n')
        if os.path.exists(output_file):
            return output_file
        return None


def make_blastdb_biopython(blast_dir_path):
    try:
        all_reported_proteins = get_protein_sequences()
        fasta_file_path = None

        fasta_files = glob(os.path.join(blast_dir_path, '*.fasta'))

        if fasta_files:
            fasta_file_path = fasta_files[0]

            with open(fasta_file_path, 'r') as file:
                records = list(SeqIO.parse(file, 'fasta'))
                if len(records) != len(all_reported_proteins):
                    fasta_file_path = protein_sequences_to_fasta(
                        all_reported_proteins, blast_dir_path
                    )
        else:
            fasta_file_path = protein_sequences_to_fasta(
                all_reported_proteins, blast_dir_path
            )

        blast_db_path = os.path.join(blast_dir_path, 'plasticome_protein_db')
        mod_time_fasta_file = os.path.getmtime(fasta_file_path)

        if os.path.exists(f'{blast_db_path}.phr'):
            mod_time_blast_db_file = os.path.getmtime(f'{blast_db_path}.phr')

            if mod_time_blast_db_file < mod_time_fasta_file:
                makeblastdb_cline = NcbimakeblastdbCommandline(
                    cmd=os.getenv('BLAST_PATH'),
                    input_file=fasta_file_path,
                    dbtype='prot',
                    out=blast_db_path,
                )
                makeblastdb_cline()
        else:
            makeblastdb_cline = NcbimakeblastdbCommandline(
                cmd=f'{os.getenv("BLAST_PATH")}\makeblastdb',
                input_file=fasta_file_path,
                dbtype='prot',
                out=blast_db_path,
            )
            makeblastdb_cline()

        return blast_db_path, None
    except Exception as error:
        return None, f'CREATE BLASTDB ERROR: {str(error)}'


@celery_app.task
def align_with_blastdb(query_file: str):
    current_script_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    blast_dir_path = os.path.join(
        current_script_root, 'blastdb', 'plasticome_protein_db'
    )

    if not os.path.exists(blast_dir_path):
        os.makedirs(blast_dir_path)
    blast_db_path, error = make_blastdb_biopython(blast_dir_path)

    if error:
        return False, error

    results_path = os.path.join(
        os.path.dirname(query_file), 'blast_results.tsv'
    )
    try:
        blastp_cline = NcbiblastpCommandline(
            cmd=f'{os.getenv("BLAST_PATH")}\\blastp',
            query=query_file,
            db=os.path.dirname(blast_db_path),
            out=os.path.join(os.path.dirname(query_file), 'blast_results.tsv'),
            outfmt=6,
        )
        blastp_cline()
        return results_path, False
    except Exception as error:
        return False, f'ALIGN WITH BLASTDB: {str(error)}'
