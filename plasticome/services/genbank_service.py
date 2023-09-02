import os
from Bio import Entrez, SeqIO
from Bio.Seq import UndefinedSequenceError
from dotenv import load_dotenv

load_dotenv()

Entrez.email = os.getenv('ENTREZ_EMAIL')


def search_fungi_id_by_name(especie: str):
    handle = Entrez.esearch(db='protein', term=especie)
    record = Entrez.read(handle)
    handle.close()

    return record


def download_fasta_sequence_by_id(fungi_id: str):
    try:
        handle = Entrez.efetch(
            db='protein', id=fungi_id, rettype='gb', retmode='text'
        )

        gene_record = SeqIO.read(handle, 'genbank')
        handle.close()

        genomes_folder = os.path.join(os.getcwd(), 'temp_genomes')
        if not os.path.exists(genomes_folder):
            os.makedirs(genomes_folder)

        fasta_file = os.path.join(genomes_folder, str(fungi_id))
        with open(fasta_file, 'w') as f:
            SeqIO.write(gene_record, f, 'fasta')

        if os.path.exists(fasta_file) and os.path.getsize(fasta_file) > 0:
            return fasta_file, False
        else:
            return False, 'An error occured try again latter', 503

    except UndefinedSequenceError:
        return False, f'{gene_record.name} = Gene Sequence is undefined.', 404
    except Exception as e:
        return False, f'[DOWNLOAD FASTA ERROR]: {e}', 400


# print(search_fungi_by_name("Fusarium oxysporum mitochondrion" ))

# download_fasta_sequence_by_id(search_fungi_by_name("Fusarium oxysporum mitochondrion" )[0]['fungi_id'])
