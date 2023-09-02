import subprocess
import os
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

    # local_mount_dir = local_mount_dir.replace('\\', '/')
    command = f'docker run --name dbcan-sub -v "{local_mount_dir}:/app/{docker_mount}" -it haidyi/run_dbcan:latest ./{docker_mount}/{input_file} protein --out_dir ./{docker_mount}/{output_folder_name}'
    print('========================',command)
    # docker run --name dbcan2 -v C:/Users/evelyn.ferreira/Documents/eevee/estudos/FACULDADE/TCC/plasticome/plasticome/genomes:/app/genomes -it haidyi/run_dbcan:latest ./genomes/123.faa protein --out_dir ./genomes/output

    try:
        subprocess.run(command, shell=True, check=True)
        return output_folder
    except subprocess.CalledProcessError as e:
        return f'Error to execute command: {e}'
    except Exception as e:
        return f'Unexpected error: {e}'

