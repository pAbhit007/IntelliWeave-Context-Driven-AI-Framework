from setuptools import setup, find_packages

setup(
    name="ai_engineer_assignment",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'langchain',
        'langgraph==0.0.17',
        'google-generativeai',
        'python-dotenv',
        'requests',
        'streamlit',
        'qdrant-client',
        'pypdf',
        'langchain-google-genai'
    ],
)
