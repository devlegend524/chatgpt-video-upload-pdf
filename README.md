
# gptMyContent

Plataforma de criacao de chatBot que usa como conteudo de aprendizado videos youtube, url da web e documentos PDF, consolidados em uma base de conhecimento.


## Screenshots

![App Screenshot](https://github.com/leonardonhesi/gptMyContent/blob/main/exemplos/tela_01.png?raw=true)

![App Screenshot](https://github.com/leonardonhesi/gptMyContent/blob/main/exemplos/tela_02.png?raw=true)

![App Screenshot](https://github.com/leonardonhesi/gptMyContent/blob/main/exemplos/chat01.png?raw=true)

![App Screenshot](https://github.com/leonardonhesi/gptMyContent/blob/main/exemplos/chat02.png?raw=true)

![App Screenshot](https://github.com/leonardonhesi/gptMyContent/blob/main/exemplos/chat3.png?raw=true)


## Instalação

1-) Verificar a versão do python
```bash
  python --version
```
2-) Criar ambiente virtual
```bash
    python -m venv ai
```
3-) Ativar o ambiente criado
```bash
    ai\Scripts\Activate.bat
```
4-) Instalar as dependencias
 ```bash
pip install -r requirements.txt
```
5-) Instalar Pytorch + cuda (caso de usar GPU) verificar a versao cuda instalada
```bash
    pip install torch==1.12.1+cu113 --extra-index-url https://download.pytorch.org/whl/cu113
```
6-) Renomear 
```bash
    .env_modelo para .env informando sua chave de API do OpenAi.
```


Rodar a aplicacao
streamlit run app.py

Acessar
Local URL: http://localhost:8501


    
## Demonstração

Exemplos

https://youtu.be/robuw_oU0fk

https://youtu.be/d5TVYNQYsrc

## Autores

- [@Leonardo Bolognesi](https://github.com/leonardonhesi)

