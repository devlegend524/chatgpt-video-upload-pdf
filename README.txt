1-) Verificar a versão do python
    python --version
2-) Criar ambiente virtual
    python -m venv ai
3-) Ativar o ambiente criado
    ai\Scripts\Activate.bat
4-) Instalar as dependencias
    pip install -r requirements.txt
5-) Instalar Pytorch + cuda (caso de usar GPU) verificar a versao cuda instalada
    pip install torch==1.12.1+cu113 --extra-index-url https://download.pytorch.org/whl/cu113
6-) Renomear .env_modelo para .env informando sua chave de API do OpenAi.


Rodar a aplicacao
streamlit run app.py

Acessar
Local URL: http://localhost:8501