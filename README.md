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

**Como funciona**: Um container será executado juntamente com um crontab para automatizar a execução, fazendo com que o scraping de log seja executado de minuto em minuto todos os dias, armazenando todos os dados novos no mysql, que também está rodando em um container separadamente.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Preparando a Execução

### Pré-requisitos

-   Docker e docker-compose instalados na máquina:
    
-   Será necessário uma conta no MaxMind e gerar uma LICENSE KEY para poder usar a biblioteca geoip2 gratuitamente:
	- Após gerar a key ela não estará mais visível, então **GUARDE ELA**.
	- Seguir o passo a passo no site oficial da MaxMind: [https://support.maxmind](https://support.maxmind.com/hc/en-us/articles/4407111582235-Generate-a-License-Key)

-   Também será necessário ter uma conta no gmail e criar uma app key para o funcionamento do disparo de emails para os admins:
	- Abra sua [Conta do Google.](https://myaccount.google.com/)
	-   Selecione **Segurança.**
	-   Ir para a barra de pesquisa e pesquisar "Senhas de app". Se você não tiver essa opção, pode ser porque:
	    1.  a verificação em duas etapas não está configurada na sua conta;
	    2.  a verificação em duas etapas está configurada apenas para chaves de segurança;
	    3.  você usa uma conta do trabalho, da escola ou de outra organização;
	    4.  você ativou o Proteção Avançada.
	-   Após inserir o nome do app aperte em "Criar".
	-   Ira aparecer um pop-up com a senha, **GUARDE ELA**.
	-   Toque em **Concluído**.


### Preparando o ambiente
- Após realizar o clone:
	```shell
	cd nginx_log_analyzer
	```
- Tendo as informações do tópico anterior em mãos e já estando no diretório principal do projeto criar o arquivo .env dentro do diretório app:
	```shell
	cd app && touch .env
	```
-  Abra esse arquivo no seu editor favorito (VsCode, Nano, NotePad, Vim...) e adicione as seguintes linhas:
	- Lembrando que é possível inserir seu próprio email na lista de admins para teste
	 ```
	 ACCOUNT_ID_GEOIP = <your_max_mind_account_id>
	LICENSE_KEY_GEOIP = '<your_max_mind_account_key>'
	EMAIL_SENDER = '<your_email_sender>'
	EMAIL_PASSWORD = '<your_email_app_key>'
	EMAILS_ADMINS = '<email_admin1>@gmail.com,<email_admin2>@gmail.com'
	 ```


## Subir os Containers:
### Importante:
- Voltar para o diretório principal do projeto:
	```shell
	cd ..
	```
- Os logs do scraping estarão disponíveis em app_log/app.log
- Antes de subir os containers é necessário ter a noção de 3 possíveis varreduras disponíveis para esse projeto:
	- **Cenário 1**: Varrer os fake_logs, onde procurei o máximo de cenários possíveis para poder testar a minha aplicação.
	- **Cenário 2**: Varrer os logs da maquina local, se essa maquina estiver com um servidor nginx rodando.
	- **Cenário 3**: Varrer os logs a partir da execução de um container rodando um nginx, no qual tem um docker-compose disponível no projeto.
	- 
### Subindo os containers em cada Cenário:
- **Cenário 1:**
```shell
PATH_ACCESS_LOG=./fake_logs_for_test/access.log PATH_ERROR_LOG=./fake_logs_for_test/error.log docker-compose up -d
```
- **Cenário 2:**
	- Para executar esse cenário é necessário lembrar que o seu usuário linux precisa ter acesso ao diretório e aos arquivos de log
```shell
sudo PATH_ACCESS_LOG=<directory_path>/access.log PATH_ERROR_LOG=<directory_path>/error.log docker-compose up -d
```
- **Cenário 3:**
	- Antes de subir os containers para o python e mysql será necessário subir o container do nginx, sendo possível realizar com os seguintes comandos:
	- O servidor nginx vai estar disponível na url: [Welcome nginx](http://localhost:8080/)
```shell
docker-compose -f nginx/docker-compose.yaml up -d && PATH_ACCESS_LOG=./nginx/logs/access.log PATH_ERROR_LOG=./nginx/logs/error.log docker-compose up -d
```

### Acessar os dados inseridos:
É possível acessar tanto por interface gráfica(PhpMyAdmin) quanto por linha de comando.
Lembrando que os dados serão populados apenas após a primeira execução do código
- Para acessar a interface gráfica: [PhpMyAdmin](http://localhost:81)
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

### Parando os containers em cada cenário:
- **Cenário 1:**
```shell
PATH_ACCESS_LOG=./fake_logs_for_test/access.log PATH_ERROR_LOG=./fake_logs_for_test/error.log docker-compose down
```
- **Cenário 2:**
	- Para executar esse cenário e necessário lembrar que o seu usuario linux precisa ter acesso ao diretório e aos arquivos de log
```shell
sudo PATH_ACCESS_LOG=<directory_path>/access.log PATH_ERROR_LOG=<directory_path>/error.log docker-compose down
```
- **Cenário 3:**
	- Antes de subir os containers para o python e mysql será necessário subir o container do nginx, sendo possível realizar com os seguintes comandos:
```shell
docker-compose -f nginx/docker-compose.yaml down && PATH_ACCESS_LOG=./nginx/logs/access.log PATH_ERROR_LOG=./nginx/logs/error.log docker-compose down
```
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Observação:
Caso queira executar mais de um cenário, sempre verificar se os containers e as images ainda estão no seu ambiente:
```shell
docker ps -a
docker image ls
```
Caso ainda estejam presentes:
```shell
docker rm python-scraper
docker image rm nginx_log_analyzer_python
```
Também será necessário limpar o arquivo app/app_log/app.log:
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
