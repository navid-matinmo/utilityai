from setuptools import setup, find_packages

def get_model_folder():
    import os
    module_dir = os.path.dirname(__file__)
    model_folder = os.path.join(module_dir, "model")
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
    return model_folder

def download_model():
    from huggingface_hub import hf_hub_download
    import json
    import os
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

download_model()

setup(
    name='utilityai',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'utilityai': ["model/*"],
    },
    install_requires=[
        'onnxruntime-genai==0.2.0rc7',
        'numpy',
    ],
    setup_requires=[
        'huggingface_hub',
    ],
    author='Navid Matin Moghaddam',
    author_email='navid.matinmo@gmail.com',
    description='UtilityAI package for python',
    url='https://github.com/navid-matinmo/utilityai',
)




