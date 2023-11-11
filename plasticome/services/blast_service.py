import os
import re

import pandas as pd
from Bio import SeqIO
from dotenv import load_dotenv
from Bio.Blast.NCBIWWW import makeblastdb
from Bio.Blast.Applications import NcbimakeblastdbCommandline

from plasticome.config.celery_config import celery_app
from plasticome.services.plasticome_metadata_service import get_all_enzymes

load_dotenv(override=True)


def get_protein_sequences():
    enzymes_info, error = get_all_enzymes(
        os.getenv('PLASTICOME_USER'), os.getenv('PLASTICOME_PASSWORD')
    )
    if error:
        return set()
    return set(item['protein_sequence'] for item in enzymes_info)


def protein_sequences_to_fasta(protein_list, output_file):
    with open(output_file, 'w') as fasta_file:
        for sequence in protein_list:
            match = re.match(r'(>.*?)([A-Z ]{10,})$', sequence)
            if match:
                header, sequence = match.groups()
                fasta_file.write(header + '\n')
                fasta_file.write(sequence.strip() + '\n')


def make_blastdb_biopython(blast_path):
    # 1. Verificar se já existe um fasta, se não criar
    # 2. Verificar se já existe um blast db, se não criar
    # 3. Se já existe os dois, verificar quantas proteinas tem no banco e quantas tem no fasta, se valor for diferente, recria o fasta e recria o blastdb
    all_reported_proteins = get_protein_sequences()
    full_fasta_path = os.path.join(blast_path, 'proteins_to_db.fasta')

    for filename in os.listdir(blast_path):
        if not filename.endswith('.fasta'):
            protein_sequences_to_fasta(
                all_reported_proteins,
                full_fasta_path
            )

    makeblastdb_cline = NcbimakeblastdbCommandline(
        input_file=full_fasta_path,
        dbtype='prot',
        output_file=os.path.join(blast_path, 'plasticome_protein_db'),
    )
    makeblastdb_cline.run()


# makeblastdb('my_proteins.fasta', 'my_protein_db', 'prot')
# # Crie uma base de dados de proteínas chamada 'my_protein_db' a partir do arquivo 'my_proteins.fasta'
