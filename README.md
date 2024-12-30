## **Análise de Logs Web com Apache Spark**
Este projeto foi desenvolvido como parte de um desafio para a análise de logs de acesso a servidores web utilizando o framework Apache Spark. O objetivo principal é processar e extrair informações valiosas a partir de dados de log no formato Web Server Access Log, auxiliando a empresa a monitorar a performance do sistema, identificar padrões de uso e detectar possíveis problemas de segurança.

A análise foi feita utilizando as capacidades de processamento distribuído do Apache Spark para manipular e responder às perguntas definidas no desafio. As respostas foram geradas com base em um arquivo de log contendo registros de vários dias de acessos ao servidor.


## **Perguntas do desafio**
1. **Identifique as 10 maiores origens de acesso (Client IP) por quantidade de acessos.**
2. **Liste os 6 endpoints mais acessados, desconsiderando aqueles que representam arquivos.**
3. **Qual a quantidade de Client IPs distintos?**
4. **Quantos dias de dados estão representados no arquivo?**
5. **Com base no tamanho (em bytes) do conteúdo das respostas, faça a seguinte análise:**
   - O volume total de dados retornado.
   - O maior volume de dados em uma única resposta.
   - O menor volume de dados em uma única resposta.
   - O volume médio de dados retornado.
6. **Qual o dia da semana com o maior número de erros do tipo "HTTP Client Error"?**

## Estrutura do Projeto
A organização do projeto está estruturada em pastas e arquivos que atendem diferentes necessidades, desde a análise de logs, configurações de contêineres até testes unitários. Abaixo está uma visão geral da estrutura do projeto:

```bash 
├── logs/
│   ├── __pycache__/             # Cache do Python gerado automaticamente
│   ├── access_log.txt           # Arquivo de log principal utilizado na análise
│   ├── test_access_log.txt      # Arquivo de log de teste utilizado nos testes
├── src/
│   ├── bd_connection.py         # Script responsável por interações com o banco de dados
│   ├── processed_logs.csv       # Saída processada dos logs em formato CSV
│   ├── test_unitario.py         # Testes unitários para validar o código
├── .dockerignore                # Arquivos a serem ignorados no contexto Docker
├── .gitattributes               # Configurações de atributos Git
├── .gitignore                   # Arquivos e pastas a serem ignorados pelo Git
├── docker-compose.yml           # Configuração para orquestrar contêineres Docker
├── Dockerfile                   # Configuração para criar a imagem Docker do projeto
├── LICENSE                      # Licença do projeto
├── README.md                    # Documentação principal do projeto
├── requirements.txt             # Dependências Python necessárias para o projeto
├── run_all.py                   # Script principal para executar todo o pipeline do projeto
```
## Códigos no Diretório src/

#### acess_log.py

Este código contém a lógica principal para processar os logs brutos (access_log.txt).
Ele inclui:
* A leitura e a limpeza dos dados de log.
* Processamento dos logs com o Apache Spark.
* Transformações e cálculos para responder às perguntas do desafio.
* Exportação dos resultados para o arquivo processed_logs.csv.


#### test_unitario.py

Este arquivo contém testes unitários para validar as funcionalidades desenvolvidas no arquivo acess_log.py.
Ele utiliza bibliotecas como unittest ou pytest para verificar se as funções do projeto estão retornando os resultados esperados.


#### bd_connection.py
Este arquivo é responsável por gerenciar a conexão com um banco de dados. 
Ele inclui:
* Configurações de conexão (credenciais, URL do banco, etc.).
* Criação de tabelas específicas para logs
* Inserção dos dados processados a partir do arquivo processed_logs.csv.

Para o armazenamento dos resultados processados, foi utilizado o PostgreSQL, um banco de dados relacional amplamente conhecido por sua confiabilidade e desempenho. A conexão e o gerenciamento do banco de dados foram realizados com o PGAdmin, enquanto a infraestrutura do banco foi provisionada por meio do Aiven, um provedor de banco de dados gerenciado em nuvem.


### Motivação para Escolha do PostgreSQL

O PostgreSQL foi escolhido por ser uma ferramenta já familiar, baseada em experiências anteriores bem-sucedidas, e por suas reconhecidas capacidades para armazenar e gerenciar grandes volumes de dados de forma eficiente. Sua robustez e desempenho tornam-no ideal para aplicações que exigem alta confiabilidade e escalabilidade.

Dados no Banco de dados:
![Texto alternativo]("C:/Users/anna.b.pereira.lima/Downloads/WhatsApp Image 2024-12-30 at 18.49.41.jpeg")


### Configurando o Banco de Dados
Antes de rodar os códigos, é necessário que ajuste as informações de conexão no arquivo Python bd_connection.py, para que funcione e conecte com o banco de dados PostgreSQL. Caso você ainda não possua um banco de dados configurado, siga as etapas abaixo:

#### Crie uma conta no Aiven:
* Acesse o site oficial do [Aiven](https://aiven.io/ "Título opcional").
* Crie uma conta e configure um novo banco de dados PostgreSQL seguindo as instruções fornecidas pelo Aiven.

#### Obtenha as credenciais de conexão:
Após criar o banco de dados, copie as informações de conexão, incluindo:

* Host
* Porta
* Nome do banco de dados
* Usuário
* Senha
* SSL mode

#### Configure no projeto:
Substitua os valores de conexão no arquivo de configuração bd_connection.py.
```python
def get_db_config():
    return psycopg2.connect(
        host="********",
        port="********",
        dbname="**********",
        user="*****",
        password="*****",
        sslmode="*******"
    )
```

#### Conecte ao PGAdmin:
Utilize o PGAdmin para gerenciar o banco de dados.
Configure uma nova conexão no PGAdmin utilizando as credenciais do banco criadas no Aiven.
Verifique se a conexão foi estabelecida com sucesso e se o banco está acessível.


Ao concluir essas etapas, o banco de dados estará pronto para armazenar os resultados processados pela análise de logs. Se surgir qualquer dúvida durante o processo, consulte a documentação oficial do Aiven e do PGAdmin ou entre em contato com as equipes de suporte.

#### run_all.py

Script principal que orquestra a execução de todo o pipeline.
Ele é feito, para quando criar toda a execução com o docker, chamar todos os scripts em python.

## Execução com Docker

O projeto foi configurado para ser executado em contêineres Docker, facilitando a reprodução do ambiente e garantindo consistência entre diferentes sistemas. Siga os passos abaixo para executar os arquivos utilizando Docker:

Certifique-se de ter o Docker instalado:

Instale o [Docker](https://www.docker.com/ "Título opcional") em seu sistema.

#### Construa a imagem Docker do projeto:
No diretório raiz do projeto, execute o seguinte comando:
``` cmd
docker-compose build
```

Saída do terminal ao executar o comando, ele irá realizar o build da imagem Docker e mostrará o processo:
``` cmd
PS C:\Users\anna.b.pereira.lima\Downloads\Project_acess_log\Project_acess_log> docker-compose build
[+] Building 11.3s (14/14) FINISHED                                                                        docker:desktop-linux
 => [analiselog internal] load build definition from Dockerfile                                                            0.0s
 => => transferring dockerfile: 877B                                                                                       0.0s
 => [analiselog internal] load metadata for docker.io/bitnami/spark:latest                                                 4.3s
 => [analiselog internal] load .dockerignore                                                                               0.0s
 => => transferring context: 409B                                                                                          0.0s
 => [analiselog 1/8] FROM docker.io/bitnami/spark:latest@sha256:7eec09bee6ff8b363d528a49ad6cc23536334e68ce394fe0689bf92ad  0.0s 
 => [analiselog internal] load build context                                                                               0.0s 
 => => transferring context: 7.18kB                                                                                        0.0s 
 => CACHED [analiselog 2/8] RUN apt-get update && apt-get install -y python3 python3-pip                                   0.0s 
 => CACHED [analiselog 3/8] COPY requirements.txt .                                                                        0.0s 
 => CACHED [analiselog 4/8] RUN python3 -m pip install --upgrade pip                                                       0.0s 
 => CACHED [analiselog 5/8] RUN pip3 install --no-cache-dir -r requirements.txt                                            0.0s 
 => CACHED [analiselog 6/8] WORKDIR /app                                                                                   0.0s 
 => [analiselog 7/8] COPY . /app                                                                                           2.5s 
 => [analiselog 8/8] COPY ./src /app/src                                                                                   2.5s
 => [analiselog] exporting to image                                                                                        1.6s
 => => exporting layers                                                                                                    1.5s 
 => => writing image sha256:8717828817daae97e994ba01b0ae8a733183155a23be13bd4545ca650a2b12c0                               0.0s
 => => naming to docker.io/library/analiselog                                                                              0.0s 
 => [analiselog] resolving provenance for metadata file                                                                    0.0s 
```
#### Inicie os contêineres com o Docker Compose:
Use o arquivo docker-compose.yml para iniciar o ambiente completo:

```cmd
docker-compose up
```
Utilizando o docker-compose up além dele inicar os conteiners, ele vai utilizar o script do arquivo run_all.py para rodar o projeto automaticamente, além de imprimir já no terminal o retorno das respostas do acess_log.py, os testes do arquivo de teste unitário e o processo de banco de dados. 

```cmd
PS C:\Users\anna.b.pereira.lima\Downloads\Project_acess_log\Project_acess_log> docker-compose up
[+] Running 1/1
 ✔ Container project_acess_log-analiselog-1  Recreated                                                                     0.2s 
Attaching to analiselog-1
analiselog-1  | spark 20:30:06.67 INFO  ==>
analiselog-1  | spark 20:30:06.67 INFO  ==> Welcome to the Bitnami spark container
analiselog-1  | spark 20:30:06.67 INFO  ==> Subscribe to project updates by watching https://github.com/bitnami/containers      
analiselog-1  | spark 20:30:06.67 INFO  ==> Did you know there are enterprise versions of the Bitnami catalog? For enhanced secure software supply chain features, unlimited pulls from Docker, LTS support, or application customization, see Bitnami Premium or Tanzu Application Catalog. See https://www.arrow.com/globalecs/na/vendors/bitnami/ for more information.
analiselog-1  | spark 20:30:06.67 INFO  ==> 
analiselog-1  |                                                                                                                 
analiselog-1  | Executando src/acess_log.py...   
```

## Resultados

Abaixo tem os resultados obtidos e que devem aparecer em seu terminal, quando for rodar todos os arquivos, respondendo 

``` cmd
analiselog-1  | Saída de src/acess_log.py:
analiselog-1  | ==================================================
analiselog-1  | 10 maiores origens de acesso:
analiselog-1  | +--------------+------+                                                                                         
analiselog-1  | |client_ip     |count |
analiselog-1  | +--------------+------+                                                                                         
analiselog-1  | |10.216.113.172|158614|                                                                                         
analiselog-1  | |10.220.112.1  |51942 |
analiselog-1  | |10.173.141.213|47503 |                                                                                         
analiselog-1  | |10.240.144.183|43592 |                                                                                         
analiselog-1  | |10.41.69.177  |37554 |                                                                                         
analiselog-1  | |10.169.128.121|22516 |                                                                                         
analiselog-1  | |10.211.47.159 |20866 |
analiselog-1  | |10.96.173.111 |19667 |                                                                                         
analiselog-1  | |10.203.77.198 |18878 |                                                                                         
analiselog-1  | |10.31.77.18   |18721 |                                                                                         
analiselog-1  | +--------------+------+
analiselog-1  |                                                                                                                 
analiselog-1  | ==================================================                                                              
analiselog-1  | 6 endpoints mais acessados:                                                                                     
analiselog-1  | +------------------------------------------------------+-----+                                                  
analiselog-1  | |endpoint                                              |count|                                                  
analiselog-1  | +------------------------------------------------------+-----+                                                  
analiselog-1  | |/                                                     |99303|
analiselog-1  | |/robots.txt                                           |51975|                                                  
analiselog-1  | |/assets/img/search-button.gif                         |38990|                                                  
analiselog-1  | |/images/filmmediablock/290/Harpoon_2d.JPG             |32533|
analiselog-1  | |/assets/img/x.gif                                     |29377|                                                  
analiselog-1  | |/images/filmpics/0000/1421/RagingPhoenix_2DSleeve.jpeg|29243|                                                  
analiselog-1  | +------------------------------------------------------+-----+
analiselog-1  |                                                                                                                 
analiselog-1  | ==================================================                                                              
analiselog-1  | Quantidade de Client IPs distintos: 333923                                                                      
analiselog-1  | Quantidade de dias representados: 792                                                                           
analiselog-1  | ==================================================
analiselog-1  | Tamanho das respostas em bytes (detalhado):                                                                     
analiselog-1  | +-------------+                                                                                                 
analiselog-1  | |response_size|                                                                                                 
analiselog-1  | +-------------+                                                                                                 
analiselog-1  | |80215074     |
analiselog-1  | |71572786     |                                                                                                 
analiselog-1  | |70297395     |                                                                                                 
analiselog-1  | |64237267     |                                                                                                 
analiselog-1  | |64237267     |
analiselog-1  | |64237036     |                                                                                                 
analiselog-1  | |64237036     |                                                                                                 
analiselog-1  | |64237036     |
analiselog-1  | |64237036     |                                                                                                 
analiselog-1  | |64237036     |
analiselog-1  | |64237036     |                                                                                                 
analiselog-1  | |64237036     |
analiselog-1  | |64237036     |                                                                                                 
analiselog-1  | |64237036     |
analiselog-1  | |64237036     |                                                                                                 
analiselog-1  | |64237036     |
analiselog-1  | |64237036     |
analiselog-1  | |64237036     |                                                                                                 
analiselog-1  | |64237036     |
analiselog-1  | |64237036     |
analiselog-1  | +-------------+                                                                                                 
analiselog-1  | only showing top 20 rows
analiselog-1  |                                                                                                                 
analiselog-1  | ==================================================
analiselog-1  | Análise do tamanho das respostas:                                                                               
analiselog-1  | +------------+--------+--------+------------------+                                                             
analiselog-1  | |total_data  |max_data|min_data|avg_data          |
analiselog-1  | +------------+--------+--------+------------------+                                                             
analiselog-1  | |805218428578|80215074|1       |195015.55065153854|                                                             
analiselog-1  | +------------+--------+--------+------------------+                                                             
analiselog-1  |                                                                                                                 
analiselog-1  | ==================================================
analiselog-1  | Número de erros HTTP Client por dia da semana:                                                                  
analiselog-1  | +-----------+---------+-----+                                                                                   
analiselog-1  | |day_of_week|day_name |count|                                                                                   
analiselog-1  | +-----------+---------+-----+
analiselog-1  | |1          |Sunday   |10642|                                                                                   
analiselog-1  | |2          |Monday   |12409|                                                                                   
analiselog-1  | |3          |Tuesday  |11639|                                                                                   
analiselog-1  | |4          |Wednesday|12685|
analiselog-1  | |5          |Thursday |11919|                                                                                   
analiselog-1  | |6          |Friday   |14785|                                                                                   
analiselog-1  | |7          |Saturday |10897|                                                                                   
analiselog-1  | +-----------+---------+-----+
analiselog-1  |                                                                                                                 
analiselog-1  | ==================================================                                                              
analiselog-1  | Dia com maior número de erros HTTP Client:                                                                      
analiselog-1  | +-----------+--------+-----+
analiselog-1  | |day_of_week|day_name|count|                                                                                    
analiselog-1  | +-----------+--------+-----+                                                                                    
analiselog-1  | |6          |Friday  |14785|                                                                                    
analiselog-1  | +-----------+--------+-----+                                                                                    
analiselog-1  | 
analiselog-1  | Análise concluída.                                                                                              
analiselog-1  |                                                                                                                 
analiselog-1  | Executando src/test_unitario.py...                                                                              
analiselog-1  | Saída de src/test_unitario.py:
analiselog-1  | Inicializando sessão Spark...
analiselog-1  | Processando arquivo de log...                                                                                   
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:
analiselog-1  | Executando: test_analyze_day_with_most_errors                                                                   
analiselog-1  | Processando arquivo de log...                                                                                   
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:                                                               
analiselog-1  | Executando: test_analyze_days_count                                                                             
analiselog-1  | Processando arquivo de log...
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:                                                               
analiselog-1  | Executando: test_analyze_distinct_ips                                                                           
analiselog-1  | Processando arquivo de log...                                                                                   
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:                                                               
analiselog-1  | Executando: test_analyze_errors_by_day                                                                          
analiselog-1  | Processando arquivo de log...
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:                                                               
analiselog-1  | Executando: test_analyze_most_accessed_endpoints                                                                
analiselog-1  | Processando arquivo de log...                                                                                   
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:                                                               
analiselog-1  | Executando: test_analyze_most_accessed_ips                                                                      
analiselog-1  | Processando arquivo de log...
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:                                                               
analiselog-1  | Executando: test_analyze_response_size                                                                          
analiselog-1  | Processando arquivo de log...                                                                                   
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:                                                               
analiselog-1  | Executando: test_process_logs                                                                                   
analiselog-1  | Processando arquivo de log...
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:                                                               
analiselog-1  | Executando: test_process_logs_empty_file                                                                        
analiselog-1  | Erro: O arquivo /app/src/empty_file.txt está vazio.
analiselog-1  | Processando arquivo de log...
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:
analiselog-1  | Executando: test_process_logs_file_not_found
analiselog-1  | Erro: Arquivo não encontrado: /app/src/non_existent_file.txt
analiselog-1  | Processando arquivo de log...
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:
analiselog-1  | Executando: test_process_logs_invalid_lines
analiselog-1  | Encontradas 2 linhas inválidas no arquivo de log:
analiselog-1  | Erro: Nenhuma linha válida encontrada no arquivo de log.
analiselog-1  | Processando arquivo de log...
analiselog-1  | Encontradas 1 linhas inválidas no arquivo de log:
analiselog-1  | Executando: test_process_logs_no_valid_lines
analiselog-1  | Encontradas 2 linhas inválidas no arquivo de log:
analiselog-1  | Erro: Nenhuma linha válida encontrada no arquivo de log.
analiselog-1  | Encerrando sessão Spark...
analiselog-1  |
analiselog-1  | Executando src/bd_connection.py...
analiselog-1  | Saída de src/bd_connection.py:
analiselog-1  | Dados carregados para a tabela 'logs' com sucesso.
analiselog-1  | Conexão encerrada.
analiselog-1  |
analiselog-1  | Todos os scripts foram executados com sucesso!
analiselog-1 exited with code 0
```