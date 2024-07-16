[linkedin-url]: https://www.linkedin.com/in/mateus-colares/

[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

  <h3 align="center">Analisador de logs nginx</h3>

  <p align="center">
    Prezando pela seguranca do seu servidor
    <br />

  </p>
</div>




<!-- ABOUT THE PROJECT -->
## Sobre o projeto


O Analisador de logs nginx é uma ferramenta extremamente necessária quando se tem um servidor NGINX rodando no seu próprio projeto

O aplicativo irá varrer logs do nginx e extrair informações pertinentes como: ip da requisição, tipo de requisição, horário da requisição, localização do ip e etc.

Após a varredura caso tenha alguma atividade suspeita será disparado um email para os administradores cadastrados, tendo, ou não, alguma atividade suspeita a informação será armazenada no banco de dados mysql.

Os parâmetros para análise de segurança do log são totalmente customizáveis, pois algumas questões podem variar dependendo da situação do projeto.

**Como funciona**: Um container sera executado juntamente com um crontab para automatizar a execucao, fazendo com que o scraping de log seja executado de 5 em 5 minutos todos os dias, armazenando todos os dados novos no mysql, que tambem esta rodando em um container separadamente.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Preparando a Execução

### Pré-requisitos

-   Docker e docker-compose instalados na máquina:
    
-   Será necessário uma conta no MaxMind e gerar uma LICENSE KEY para poder usar a biblioteca geoip2 gratuitamente:
	- Apos gerar a key ela nao estara mais visivel, entao **GUARDE ELA**.
	- Seguir o passo a passo no site oficial da MaxMind: [https://support.maxmind](https://support.maxmind.com/hc/en-us/articles/4407111582235-Generate-a-License-Key)

-   Também será necessário ter uma conta no gmail e criar uma app key para o funcionamento do disparo de emails para os admins:
	- Abra sua [Conta do Google.](https://myaccount.google.com/)
	-   Selecione **Segurança.**
	-   Ir para a barra de pesquisa e pesquisar "Senhas de app". Se você não tiver essa opção, pode ser porque:
	    1.  a verificação em duas etapas não está configurada na sua conta;
	    2.  a verificação em duas etapas está configurada apenas para chaves de segurança;
	    3.  você usa uma conta do trabalho, da escola ou de outra organização;
	    4.  você ativou o Proteção Avançada.
	-   Apos inserir o nome do app aperte em "Criar".
	-   Ira aprecer um pop-up com a senha, **GUARDE ELA**.
	-   Toque em **Concluído**.


### Preparando o ambiente
- Apos realizar o clone:
	```shell
	cd nginx_log_analyzer
	```
- Tendo as informações do tópico anterior em mãos e ja estando no diretorio principal do projeto criar o arquivo .env dentro do diretorio app:
	```shell
	touch app/.env
	```
-  Abra esse arquivo no seu editor favorito (VsCode, Nano, NotePad, Vim...) e adicione as seguintes linhas:
	- Lembrando que e possivel inserir seu proprio email na lista de admins para teste
	 ```
	 ACCOUNT_ID_GEOIP = '<your_max_mind_account_id>'
	LICENSE_KEY_GEOIP = '<your_max_mind_account_key>'
	EMAIL_SENDER = '<your_email_sender>'
	EMAIL_PASSWORD = '<your_email_app_key>'
	EMAILS_ADMINS = '<email_admin1>@gmail.com', '<email_admin2>@gmail.com'
	 ```


## Subir os Containers:
### Importante:
- Voltar para o diretorio principal do projeto:
	```shell
	cd ..
	```
- Os logs do scraping estaram disponiveis em app_log/app.log
- Antes de subir os containers e necessario ter a nocao de 3 possiveis formas de varreduras diponiveis para esse projeto:
	- **Cenario 1**: Varrer os fake_logs, aonde procurei o maximo de cenarios possiveis para poder testar a minha aplicacao
	- **Cenario 2**: Varrer os logs da maquina local, se essa maquina estiver com um servidor nginx rodando
	- **Cenario 3**: Varrer os logs a partir da execucao de um container rodando um nginx, no qual tem um docker-compose disponivel no projeto
	- 
### Subindo os containers em cada cenario:
- **Cenario 1:**
```shell
PATH_ACCESS_LOG=./fake_logs_for_test/access.log PATH_ERROR_LOG=./fake_logs_for_test/error.log docker-compose up -d
```
- **Cenario 2:**
	- Para executar esse cenario e necessario lembrar que o seu usuario linux precisa ter acesso ao diretorio e aos arquivos de log
```shell
sudo PATH_ACCESS_LOG=<directory_path>/access.log PATH_ERROR_LOG=<directory_path>/error.log docker-compose up -d
```
- **Cenario 3:**
	- Antes de subir os containers para o python e mysql sera necessario subir o container do nginx, sendo possivel realizar com os seguintes comandos: 
```shell
docker-compose -f nginx/docker-compose.yaml up -d && PATH_ACCESS_LOG=./nginx/logs/access.log PATH_ERROR_LOG=./nginx/logs/error.log docker-compose up -d
```

### Parando os containers em cada cenario:
- **Cenario 1:**
```shell
docker-compose down
```
- **Cenario 2:**
	- Para executar esse cenario e necessario lembrar que o seu usuario linux precisa ter acesso ao diretorio e aos arquivos de log
```shell
docker-compose down
```
- **Cenario 3:**
	- Antes de subir os containers para o python e mysql sera necessario subir o container do nginx, sendo possivel realizar com os seguintes comandos: 
```shell
docker-compose -f nginx/docker-compose.yaml down && docker-compose up down
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contatos

C0lares - [LinkedIn](https://www.linkedin.com/in/mateus-colares/) - mcolaresc@gmail.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
