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


O Analisador de logs nginx � uma ferramenta extremamente necess�ria quando se tem um servidor NGINX rodando no seu pr�prio projeto

O aplicativo ir� varrer logs do nginx e extrair informa��es pertinentes como: ip da requisi��o, tipo de requisi��o, hor�rio da requisi��o, localiza��o do ip e etc.

Ap�s a varredura caso tenha alguma atividade suspeita ser� disparado um email para os administradores cadastrados, tendo, ou n�o, alguma atividade suspeita a informa��o ser� armazenada no banco de dados mysql.

Os par�metros para an�lise de seguran�a do log s�o totalmente customiz�veis, pois algumas quest�es podem variar dependendo da situa��o do projeto.

**Como funciona**: Um container ser� executado juntamente com um crontab para automatizar a execu��o, fazendo com que o scraping de log seja executado de minuto em minuto todos os dias, armazenando todos os dados novos no mysql, que tamb�m est� rodando em um container separadamente.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Preparando a Execu��o

### Pr�-requisitos

-   Docker e docker-compose instalados na m�quina:
    
-   Ser� necess�rio uma conta no MaxMind e gerar uma LICENSE KEY para poder usar a biblioteca geoip2 gratuitamente:
	- Ap�s gerar a key ela n�o estar� mais vis�vel, ent�o **GUARDE ELA**.
	- Seguir o passo a passo no site oficial da MaxMind: [https://support.maxmind](https://support.maxmind.com/hc/en-us/articles/4407111582235-Generate-a-License-Key)

-   Tamb�m ser� necess�rio ter uma conta no gmail e criar uma app key para o funcionamento do disparo de emails para os admins:
	- Abra sua [Conta do Google.](https://myaccount.google.com/)
	-   Selecione **Seguran�a.**
	-   Ir para a barra de pesquisa e pesquisar "Senhas de app". Se voc� n�o tiver essa op��o, pode ser porque:
	    1.  a verifica��o em duas etapas n�o est� configurada na sua conta;
	    2.  a verifica��o em duas etapas est� configurada apenas para chaves de seguran�a;
	    3.  voc� usa uma conta do trabalho, da escola ou de outra organiza��o;
	    4.  voc� ativou o Prote��o Avan�ada.
	-   Ap�s inserir o nome do app aperte em "Criar".
	-   Ira aparecer um pop-up com a senha, **GUARDE ELA**.
	-   Toque em **Conclu�do**.


### Preparando o ambiente
- Ap�s realizar o clone:
	```shell
	cd nginx_log_analyzer
	```
- Tendo as informa��es do t�pico anterior em m�os e j� estando no diret�rio principal do projeto criar o arquivo .env dentro do diret�rio app:
	```shell
	cd app && touch .env
	```
-  Abra esse arquivo no seu editor favorito (VsCode, Nano, NotePad, Vim...) e adicione as seguintes linhas:
	- Lembrando que � poss�vel inserir seu pr�prio email na lista de admins para teste
	 ```
	 ACCOUNT_ID_GEOIP = <your_max_mind_account_id>
	LICENSE_KEY_GEOIP = '<your_max_mind_account_key>'
	EMAIL_SENDER = '<your_email_sender>'
	EMAIL_PASSWORD = '<your_email_app_key>'
	EMAILS_ADMINS = '<email_admin1>@gmail.com,<email_admin2>@gmail.com'
	 ```


## Subir os Containers:
### Importante:
- Voltar para o diret�rio principal do projeto:
	```shell
	cd ..
	```
- Os logs do scraping estar�o dispon�veis em app_log/app.log
- Antes de subir os containers � necess�rio ter a no��o de 3 poss�veis varreduras dispon�veis para esse projeto:
	- **Cen�rio 1**: Varrer os fake_logs, onde procurei o m�ximo de cen�rios poss�veis para poder testar a minha aplica��o.
	- **Cen�rio 2**: Varrer os logs da maquina local, se essa maquina estiver com um servidor nginx rodando.
	- **Cen�rio 3**: Varrer os logs a partir da execu��o de um container rodando um nginx, no qual tem um docker-compose dispon�vel no projeto.
	- 
### Subindo os containers em cada Cen�rio:
- **Cen�rio 1:**
```shell
PATH_ACCESS_LOG=./fake_logs_for_test/access.log PATH_ERROR_LOG=./fake_logs_for_test/error.log docker-compose up -d
```
- **Cen�rio 2:**
	- Para executar esse cen�rio � necess�rio lembrar que o seu usu�rio linux precisa ter acesso ao diret�rio e aos arquivos de log
```shell
sudo PATH_ACCESS_LOG=<directory_path>/access.log PATH_ERROR_LOG=<directory_path>/error.log docker-compose up -d
```
- **Cen�rio 3:**
	- Antes de subir os containers para o python e mysql ser� necess�rio subir o container do nginx, sendo poss�vel realizar com os seguintes comandos:
	- O servidor nginx vai estar dispon�vel na url: [Welcome nginx](http://localhost:8080/)
```shell
docker-compose -f nginx/docker-compose.yaml up -d && PATH_ACCESS_LOG=./nginx/logs/access.log PATH_ERROR_LOG=./nginx/logs/error.log docker-compose up -d
```

### Acessar os dados inseridos:
� poss�vel acessar tanto por interface gr�fica(PhpMyAdmin) quanto por linha de comando.
Lembrando que os dados ser�o populados apenas ap�s a primeira execu��o do c�digo
- Para acessar a interface gr�fica: [PhpMyAdmin](http://localhost:81)
	- user: root
	- password:bp1234
- Para acessar por linha de comando:
```shell
docker exec -it mysql /bin/bash
```
Dentro do container:
```shel
mysql -u root -p
```
password:bp1234

### Parando os containers em cada cen�rio:
- **Cen�rio 1:**
```shell
PATH_ACCESS_LOG=./fake_logs_for_test/access.log PATH_ERROR_LOG=./fake_logs_for_test/error.log docker-compose down
```
- **Cen�rio 2:**
	- Para executar esse cen�rio e necess�rio lembrar que o seu usuario linux precisa ter acesso ao diret�rio e aos arquivos de log
```shell
sudo PATH_ACCESS_LOG=<directory_path>/access.log PATH_ERROR_LOG=<directory_path>/error.log docker-compose down
```
- **Cen�rio 3:**
	- Antes de subir os containers para o python e mysql ser� necess�rio subir o container do nginx, sendo poss�vel realizar com os seguintes comandos:
```shell
docker-compose -f nginx/docker-compose.yaml down && PATH_ACCESS_LOG=./nginx/logs/access.log PATH_ERROR_LOG=./nginx/logs/error.log docker-compose down
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Observa��o:
Caso queira executar mais de um cen�rio, sempre verificar se os containers e as images ainda est�o no seu ambiente:
```shell
docker ps -a
docker image ls
```
Caso ainda estejam presentes:
```shell
docker rm python-scraper
docker image rm nginx_log_analyzer_python
```
Tamb�m ser� necess�rio limpar o arquivo app/app_log/app.log:
```shell
rm -f app/app_log/app.log && touch app/app_log/app.log
```

<!-- CONTACT -->
## Contatos

C0lares - [LinkedIn](https://www.linkedin.com/in/mateus-colares/) - mcolaresc@gmail.com

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
