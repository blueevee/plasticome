from plasticome.services.genbank_service import search_fungi_id_by_name


def search_fungi_by_name(fungi_name: str):
    genbank_accession, refseq_accession = search_fungi_id_by_name(fungi_name)
    if genbank_accession or refseq_accession:
        return {'genbank_assembly_accession': genbank_accession, 'refseq_assembly_accession': refseq_accession}, 200
    return {'message': 'Genome not found'}, 404
