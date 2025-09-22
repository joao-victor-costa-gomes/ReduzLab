### Rodando com ambiente virtual 

Na raiz do projeto, crie um ambiente virtual e baixe os requisitos com os comandos abaixo:

```bash
python3 -m venv reduzlab_env

reduzlab_env\Scripts\activate

pip install -r requirements.txt
```

Renomeie o arquivo `.env.example` apenas para `.env` e copie esse texto dentro dele:

```bash
# Flask App Configuration
SECRET_KEY="your-super-secret-and-random-key-here"
MAX_CONTENT_LENGTH=209715200 # 200MB
```

Em seguida rode a aplicação:

```bash
python run.py
```

A aplicação estará rodando em http://127.0.0.1:5000

