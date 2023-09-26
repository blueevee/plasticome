import docker
import os

from ..config.celery_config import celery_app


@celery_app.task
def run_dbcan_container(absolute_mount_dir):

    input_file = os.path.basename(absolute_mount_dir)
    local_mount_dir = os.path.dirname(absolute_mount_dir)
    docker_mount = os.path.basename(local_mount_dir)

    output_folder_name = f'{input_file.split(".")[0]}_dbcan_output'
    output_folder = os.path.join(local_mount_dir, output_folder_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    client = docker.from_env()

    container_params = {
        'image': 'haidyi/run_dbcan:latest',
        'volumes': {local_mount_dir: {'bind': f'/app/{docker_mount}', 'mode': 'rw'}},
        'working_dir': '/app',
        'command': [f'./{docker_mount}/{input_file}', 'protein', '--out_dir', f'./{docker_mount}/{output_folder_name}'],
        'remove': True,
    }
    try:
        client.containers.run(**container_params)
        return output_folder, False
    except Exception as e:
        return False, f'[DBCAN STEP] - Unexpected error: {e}'