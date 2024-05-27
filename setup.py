from setuptools import setup, find_packages

setup(
    name='utilityai',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'onnxruntime-genai==0.2.0rc7',
        'numpy',
    ],
    author='Navid Matin Moghaddam',
    author_email='navid.matinmo@gmail.com',
    description='UtilityAI package for python',
    url='https://github.com/navid-matinmo/utilityai',
)