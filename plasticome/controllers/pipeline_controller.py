from plasticome.services.dbcan_service import run_dbcan_container
from plasticome.services.genbank_service import download_fasta_sequence_by_id


def execute_main_pipeline(data: dict):
    try:
        if (
            data.get('user_email', False)
            and data.get('user_name', False)
            and data.get('fungi_id', False)
        ):
            # TODO Validar se esse email é email msm
            # TODO TRATAR ESSE RETONRO
            file_path, file_error = download_fasta_sequence_by_id(
                data['fungi_id']
            )
            if file_error:
                return {'error': file_error}, 500

            # TODO [CELERY] RODAR O DBCAN COM CELERY
            output_folder, dbcan_error = run_dbcan_container(file_path)
            if dbcan_error:
                return {'error': dbcan_error}, 500
            return {'msg': output_folder}, 200
            # TODO [CELERY] SIMULTANEO RODAR O DEEPEC

            # TODO [CELERY] SIMULTANEO RODAR O BLAST COM O PLASTICOME-ENZYMES E A SEQUENCIA
            # TODO VER COMO TRATAR OS DADOS... ENVIAR EMAIL COM O RESULTADO???
            # return {
            # 'message': 'Analysis is in progress, the result will be sent by email'
            # }, 200
        else:
            return {
                'ValidationError': 'Incomplete model, you must have to send a valid email: `user_email`, a valid name: `user_name` and a valid fungi genbank id: `fungi_id`'
            }, 422
    except Exception as e:
        return {'error': f'[EXECUTE PIPELINE] - {e}'}, 400
