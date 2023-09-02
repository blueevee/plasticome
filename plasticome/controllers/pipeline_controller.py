from plasticome.services.genbank_service import download_fasta_sequence_by_id

def execute_main_pipeline(data: dict):
    try:
        if data.get('user_email', False) and data.get('user_name', False) and data.get('fungi_id', False):
            file_path, error, file_status = download_fasta_sequence_by_id(data['fungi_id'])
            if error:
                return {'error': error}, file_status
            return {'msg': file_path}, 200
            # result, error = store_enzyme(**data)
            # if error:
            #     return {'error': str(error)}, 500
            # return result, 201
        else:
            return {
                'error': 'Incomplete model, you must have to send a valid email: `user_email`, a valid name: `user_name` and a valid fungi genbank id: `fungi_id`'
            }, 422
    except Exception as e:
        return {'error': f'Invalid data: {e}'}, 400
#     # FAZER O DOWNLOAD DA SEQUENCIA VIA GENBANK
#     # ABORTAR SE NÂO CONSEGUIR BAIXAR A SEQUENCIA, RETORNAR ERRO

#     # [CELERY] RODAR O DBCAN COM CELERY
#     output_folder = run_dbcan_container(response)
#     print(output_folder)
#     # [CELERY] SIMULTANEO RODAR O DEEPEC

#     # [CELERY] SIMULTANEO RODAR O BLAST COM O PLASTICOME-ENZYMES E A SEQUENCIA

#     # APÓS ISSO ENVIAR EMAIL COM O RESULTADO
#     return {
#         'message': 'Analysis is in progress, the result will be sent by email'
#     }, 200
