from plasticome.services.dbcan_service import run_dbcan_container
from plasticome.services.ecpred_service import run_ecpred_container
from plasticome.services.email_service import send_email_with_results
from plasticome.services.Helpers import validate_email
from plasticome.services.genbank_service import download_fasta_sequence_by_id
from celery import chain


def execute_main_pipeline(data: dict):
    try:
        if (
            data.get('user_email', False)
            and data.get('user_name', False)
            and data.get('fungi_id', False)
        ):
            user_email = data['user_email']
            if not validate_email(user_email):
                return {'ValidationError': 'You must have to send a valid email'}, 422

            user_name = data['user_name']
            file_path, file_error = download_fasta_sequence_by_id.delay(
                data['fungi_id']
            )
            if file_error:
                return {'error': file_error}, 500

            chain(run_ecpred_container.si(file_path),run_dbcan_container.si(file_path) , send_email_with_results.s(user_email, user_name))()

            # TODO [CELERY] SIMULTANEO RODAR O BLAST COM O PLASTICOME-ENZYMES E A SEQUENCIA
            return {
            'message': 'Analysis is in progress, the result will be sent by email'
            }, 200
        else:
            return {
                'ValidationError': 'Incomplete model, you must have to send a valid email: `user_email`, a valid name: `user_name` and a valid fungi genbank id: `fungi_id`'
            }, 422
    except Exception as e:
        return {'error': f'[EXECUTE PIPELINE] - {e}'}, 400
