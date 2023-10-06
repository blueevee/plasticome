import gzip
import os
import shutil
import urllib.request
from ftplib import FTP
from urllib.parse import urlparse

from Bio import Entrez
from dotenv import load_dotenv

load_dotenv()

Entrez.email = os.getenv('ENTREZ_EMAIL')


def search_fungi_id_by_name(especie: str):
    seacrh_term = f'"{especie}"[Organism] AND (latest[filter] AND all[filter] NOT anomalous[filter])'
    handle = Entrez.esearch(db='assembly', term=seacrh_term, retmax=1)
    record = Entrez.read(handle)
    handle.close()

    if record['Count'] > '0':
        assembly_id = record['IdList'][0]

        handle = Entrez.esummary(db='assembly', id=assembly_id)
        record = Entrez.read(handle)
        handle.close()

        genbank_assembly_accession = record['DocumentSummarySet'][
            'DocumentSummary'
        ][0]['AssemblyAccession']
        refseq_assembly_accession = record['DocumentSummarySet'][
            'DocumentSummary'
        ][0]['Synonym']['RefSeq']

        return genbank_assembly_accession, refseq_assembly_accession

    else:
        return None, None


def check_ftp_file_existence(ftp_url, file_name):
    url_parts = urlparse(ftp_url)
    server_address = url_parts.netloc
    file_path = url_parts.path
    try:
        ftp = FTP(server_address)
        ftp.login()

        ftp.cwd(file_path)
        file_list = ftp.nlst()
        file_exists = file_name in file_list

        ftp.quit()

        return file_exists

    except Exception as e:
        print(f'Error checking FTP file existence: {e}')
        return False


def download_fasta_sequence_by_id(acession_number: str):
    try:
        temp_genomes_path = os.path.join(os.getcwd(), 'temp_genomes')

        if not os.path.exists(temp_genomes_path):
            os.makedirs(temp_genomes_path)

        handle = Entrez.esearch(
            db='assembly',
            term=f'{acession_number}[Assembly Accession]',
            retmax=1,
        )

        record = Entrez.read(handle)
        handle.close()
        if not record['IdList']:
            raise ValueError(
                'Assembly not found for the given accession number.'
            )

        assembly_id = record['IdList'][0]

        handle = Entrez.esummary(db='assembly', id=assembly_id)
        record = Entrez.read(handle)
        handle.close()

        ftp_url = record['DocumentSummarySet']['DocumentSummary'][0].get(
            'FtpPath_RefSeq'
        )
        if not ftp_url:
            ftp_url = record['DocumentSummarySet']['DocumentSummary'][0].get(
                'FtpPath_GenBank'
            )
            if not ftp_url:
                raise ValueError(
                    'No FTP path found for the given accession number.'
                )

        fasta_file = ftp_url.split('/')[-1] + '_protein.faa.gz'
        fasta_url = ftp_url + '/' + fasta_file

        if not check_ftp_file_existence(ftp_url=ftp_url, file_name=fasta_file):
            raise ValueError(f'File {fasta_file} not found on the FTP server.')

        fasta_folder_path = os.path.join(
            temp_genomes_path, f'{acession_number}.fasta.gz'
        )

        if not os.path.exists(fasta_folder_path):
            urllib.request.urlretrieve(fasta_url, fasta_folder_path)

        fasta_output_path = os.path.join(
            temp_genomes_path, f'{acession_number}.faa'
        )

        with gzip.open(fasta_folder_path, 'rb') as f_in:
            with open(fasta_output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(fasta_folder_path)

        return fasta_output_path, False

    except Exception as error:
        return False, error
