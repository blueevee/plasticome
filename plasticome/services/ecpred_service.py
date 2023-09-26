import docker
import os

from ..config.celery_config import celery_app


@celery_app.task
def run_ecpred_container(absolute_mount_dir):

    input_file = os.path.basename(absolute_mount_dir)
    local_mount_dir = os.path.dirname(absolute_mount_dir)
    docker_mount = os.path.basename(local_mount_dir)

    output_folder_name = f'{input_file.split(".")[0]}_ecpred_output'
    output_file_path = os.path.join(local_mount_dir, output_folder_name, f'{output_folder_name}.tsv')

    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))

    client = docker.from_env()

    container_params = {
        'image': 'blueevee/ecpred:latest',
        'volumes': {local_mount_dir: {'bind': f'/app/{docker_mount}', 'mode': 'rw'}},
        'working_dir': '/app',
        'command': ['spmap', f'./{docker_mount}/{input_file}', './', '/temp', f'./{docker_mount}/{output_folder_name}/{output_folder_name}.tsv'],
        'remove': True,
    }
    try:
        client.containers.run(**container_params)
        return output_file_path, False
    except Exception as e:
        return False, f'[ECPRED STEP] - Unexpected error: {e}'
