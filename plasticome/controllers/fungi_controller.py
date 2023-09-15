from plasticome.services.genbank_service import search_fungi_id_by_name


def search_fungi_by_name(fungi_name: str):
    response = search_fungi_id_by_name(fungi_name)

    if int(response['Count']) == 0:
        return {'message': 'Genome not found'}, 404
    return {'fungi_id': response['IdList'][0]}, 200
