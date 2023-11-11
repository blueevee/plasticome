import csv
import os

import matplotlib.pyplot as plt
from dotenv import load_dotenv

from plasticome.config.celery_config import celery_app
from plasticome.services.plasticome_metadata_service import (
    get_all_enzymes,
    get_all_plastic_types_by_enzyme,
    get_all_plastics_with_enzymes,
)

load_dotenv(override=True)


def get_enzymes_info():
    enzymes_info, error = get_all_enzymes(
        os.getenv('PLASTICOME_USER'), os.getenv('PLASTICOME_PASSWORD')
    )
    if error:
        return {}
    print()
    enzyme_dict = {}
    for item in enzymes_info:
        cazy_family = item['cazy_family']
        ec_number = item['ec_number']
        if cazy_family not in enzyme_dict:
            enzyme_dict[cazy_family] = item['id']
        if ec_number not in enzyme_dict:
            enzyme_dict[ec_number] = item['id']

    return enzyme_dict


def get_plastics_info():
    plastics_info, error = get_all_plastics_with_enzymes(
        os.getenv('PLASTICOME_USER'), os.getenv('PLASTICOME_PASSWORD')
    )
    if error:
        return set()
    return set(item['plastic_acronym'] for item in plastics_info)


def create_result_graphic(
    absolute_dir: str, aimed_enzymes: dict, all_plastics_set: set
):

    enzyme_names = list(aimed_enzymes.keys())
    plastics_relations = [aimed_enzymes[enzyme] for enzyme in aimed_enzymes]

    _, ax = plt.subplots(figsize=(12, int(len(enzyme_names) / 5 * 1.4) + 1.5))
    colors = {
        plastic: plt.cm.viridis(i / len(all_plastics_set))
        for i, plastic in enumerate(all_plastics_set)
    }

    for i, plastics in enumerate(plastics_relations):
        y_pos = [i] * len(plastics)
        ax.scatter(
            plastics,
            y_pos,
            color=[colors[p] for p in plastics],
            s=100,
            label=enzyme_names[i],
        )

    ax.set_yticks(range(len(enzyme_names)))
    ax.set_yticklabels(enzyme_names)
    ax.set_xlabel('Plásticos com possibilidade de degradação')

    handles = [
        plt.Line2D(
            [0],
            [0],
            marker='o',
            color='w',
            markerfacecolor=colors[p],
            markersize=10,
            label=p,
        )
        for p in all_plastics_set
    ]
    ax.legend(
        handles=handles,
        title='Tipos de plástico testados',
        loc='center left',
        bbox_to_anchor=(1, 0.5),
    )

    plt.title(
        'Relação de enzimas que podem ser candidatas à degradação de plásticos.',
        loc='right',
    )

    image_path = os.path.join(absolute_dir, 'plasticome_result.png')
    plt.savefig(image_path, format='png', bbox_inches='tight', dpi=100)
    plt.close()

    return image_path


@celery_app.task
def create_result(ec_pred_output: tuple):
    absolute_dir, _ = ec_pred_output
    enzymes_info = get_enzymes_info()
    all_plastics_set = get_plastics_info()
    aimed_enzymes = {}

    ####### INIT: [LENDO RESULTADOS EC_PRED]
    for filename in os.listdir(absolute_dir):
        if filename.endswith('.tsv'):
            ec_pred_file_path = os.path.join(absolute_dir, filename)
    with open(
        ec_pred_file_path, mode='r', newline='', encoding='utf-8'
    ) as file_ec_pred:
        reader = csv.DictReader(file_ec_pred, delimiter='\t')

        for row in reader:
            protein_id = row['Protein ID']
            ec_number = row['EC Number']
            aimed_enzymes[protein_id] = []
            if ec_number in enzymes_info.keys():
                plastic_types, _ = get_all_plastic_types_by_enzyme(
                    os.getenv('PLASTICOME_USER'),
                    os.getenv('PLASTICOME_PASSWORD'),
                    enzymes_info[ec_number],
                )
                aimed_enzymes[protein_id].extend(plastic_types)
    ####### END: [LENDO RESULTADOS EC_PRED]

    clean_enzymes_data = {
        key: value for key, value in aimed_enzymes.items() if value
    }
    if len(clean_enzymes_data) < 1:
        negative_result = f"""
            Gostaríamos de informar que concluímos a análise das enzimas em relação à degradação de plásticos, até o momento, nossa análise está focada nos seguintes tipos de plástico: {all_plastics_set}.

            Dito isso, nesta análise, não encontramos nenhuma enzima que tenha uma relação identificável com esses tipos específicos de plástico. Embora isso possa ser desapontador, é importante destacar que a pesquisa nesse campo continua evoluindo, e novas descobertas podem surgir no futuro.

            Agradecemos por usar nossos serviços e estamos à disposição para futuras análises e pesquisas.
        """
        return absolute_dir, negative_result

    image_path = create_result_graphic(
        absolute_dir, clean_enzymes_data, all_plastics_set
    )
    return image_path, False
