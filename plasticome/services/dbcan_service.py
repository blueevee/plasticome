import os
import subprocess

from ..config.celery_config import celery_app


# @celery_app.task
def run_dbcan_container(absolute_mount_dir):

    """
    This function executes dbcan on a docker container to analyze a file, and create an output folder with the complete analyzes.

    Parameters:
        absolute_mount_dir (str): Absolute path where the choosen file is located.
    """

    input_file = os.path.basename(absolute_mount_dir)
    local_mount_dir = os.path.dirname(absolute_mount_dir)
    docker_mount = os.path.basename(local_mount_dir)

    output_folder_name = 'dbcan_output'
    output_folder = os.path.join(local_mount_dir, output_folder_name)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    command = f'docker run -v "{local_mount_dir}:/app/{docker_mount}" -it haidyi/run_dbcan:latest ./{docker_mount}/{input_file} protein --out_dir ./{docker_mount}/{output_folder_name}'

    try:
        subprocess.run(command, shell=True, check=True)
        return output_folder, False
    except subprocess.CalledProcessError as e:
        return False, f'Error to execute command: {e}'
    except Exception as e:
        return False, f'[DBCAN STEP] - Unexpected error: {e}'
