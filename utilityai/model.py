import os
import json
from typing import Optional
from huggingface_hub import hf_hub_download

def download(option: Optional[int] = None):

    def get_model_folder():
        module_dir = os.path.dirname(os.path.realpath(__file__))
        model_folder = os.path.join(module_dir, "model")
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)
        return model_folder

    local_dir = get_model_folder()

    info_repo_id = "navid-matinmo/utilityai"
    info_filename = "info.json"
    hf_hub_download(repo_id=info_repo_id, filename=info_filename, local_dir=local_dir, use_auth_token="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")
    
    file_path = os.path.join(local_dir, "info.json")
    with open(file_path, 'r') as file:
        info = json.load(file)

    repo_id = info["repo_id"]
    filenames = info["filenames"]
    for filename in filenames:
        hf_hub_download(repo_id=repo_id, filename=filename, local_dir=local_dir, use_auth_token="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")