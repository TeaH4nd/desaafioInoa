# Desafio Inoa

Programa desenvolvido para o processo seletivo da [INOA](https://www.inoa.com.br/)

# Objetivo

Auxiliar um investidor nas suas decisões de comprar/vender ativos. Para tal, ele deve registrar periodicamente a cotação atual de ativos da B3 e também avisar, via e-mail, caso haja oportunidade de negociação.

# Requisitos

- Obter periodicamente as cotações de alguma fonte pública qualquer e armazená-las, em uma periodicidade configurável, para consulta posterior
- Expor uma interface web para permitir consultar os preços armazenados, configurar os ativos a serem monitorados e parametrizar os túneis de preço de cada ativo
- Enviar e-mail para o investidor sugerindo Compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior, e sugerindo Venda sempre que o preço de um ativo monitorado cruzar o seu limite superior
- Sistema seja feito em **Python** com **Django**

### Bibliotecas e Api's
- [Django](https://www.djangoproject.com/) - High-level Python Web framework!
- [Background-tasks](https://django-background-tasks.readthedocs.io/en/latest/) - Django Background Task is a databased-backed work queue
- [Bootstrap 5](https://getbootstrap.com/) - The world’s most popular front-end open source toolkit
- [yahoo-fin](https://theautomatic.net/yahoo_fin-documentation/) - Api designed to scrape historical stock price data
- [yfinance](https://pypi.org/project/yfinance/) - Download historical market data from Yahoo! finance.

### Instalação

O projeto utiliza [Django](https://www.djangoproject.com/) v3+

Baixe o projeto e instale as dependencias e migre a database
```sh
$ git clone https://github.com/TeaH4nd/desafioInoa.git
$ cd desafioInoa
$ pip install -r "requirements.txt"
$ python3 manage.py migrate
```
Crie um arquivo _.env_
```sh
$ touch .env
```
Adicione seus credenciais para mandar email
>EMAIL_HOST = 'smtp.gmail.com'
>EMAIL_USE_TLS = True
>EMAIL_PORT = 587
>EMAIL_HOST_USER = 'SEU_EMAIL'
>EMAIL_HOST_PASSWORD = 'SUA_SENHA'

Depois de configurado inicie o servidor
```sh
$ python3 manage.py runserver
```
Para iniciar o script do Background-tasks
```sh
$ python3 manage.py process_tasks
```