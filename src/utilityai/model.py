import os
import json
from typing import Optional
from huggingface_hub import hf_hub_download

def download(option: Optional[int] = None):

    module_dir = os.path.dirname(os.path.realpath(__file__))

    models_folder = os.path.join(module_dir, "models")
    if not os.path.exists(models_folder):
        os.makedirs(models_folder)

    if os.name == "nt":
        models_folder_hf = "\\\\?\\" + os.path.abspath(models_folder)
    else:
        models_folder_hf = models_folder

    info_repo_id = "navid-matinmo/utilityai"
    info_filename = "info.json"
    hf_hub_download(repo_id=info_repo_id, filename=info_filename, local_dir=models_folder_hf)
    info_filename = "config.json"
    hf_hub_download(repo_id=info_repo_id, filename=info_filename, local_dir=models_folder_hf)

    file_path = os.path.join(models_folder, "info.json")
    with open(file_path, 'r') as file:
        info = json.load(file)

    if not info: 
        print("The model is not currently available")
        return
    
    if option:
        if len(info) == 1:
            if not isinstance(option, int) or option != 1:
                raise ValueError("Only option 1 is available")
        else:
            if not isinstance(option, int) or option > len(info) or option < 1:
                options = ", ".join(str(i) for i in range(1, len(info) + 1))
                raise ValueError(f"option must be an integer either {options}")
    else:
        option = 1

    model_folder = os.path.join(models_folder, "model_"+str(option))
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)

    if os.name == "nt":
        model_folder_hf = "\\\\?\\" + os.path.abspath(model_folder)
    else:
        model_folder_hf = model_folder

    repo_id = info[option-1]["repo_id"]
    filenames = info[option-1]["filenames"]
    for filename in filenames:
        hf_hub_download(repo_id=repo_id, filename=filename, local_dir=model_folder_hf)