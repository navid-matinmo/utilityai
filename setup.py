from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess

class PostInstallCommand(install):
    def run(self):
        install.run(self)
        subprocess.call(['huggingface-cli', 'download', 'microsoft/Phi-3-mini-4k-instruct-onnx', 'cpu_and_mobile/cpu-int4-rtn-block-32-acc-level-4/phi3-mini-4k-instruct-cpu-int4-rtn-block-32-acc-level-4.onnx', '--local-dir', './sth'])

setup(
    name='utilityai',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'onnxruntime-genai==0.2.0rc7',
        'numpy',
        'huggingface_hub[cli]'
    ],
    author='Navid Matin Moghaddam',
    author_email='navid.matinmo@gmail.com',
    description='UtilityAI package for python',
    url='https://github.com/navid-matinmo/utilityai',
)