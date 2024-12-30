# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, sum, avg, max, min, to_date, dayofweek, when
import os
import shutil


# Criar a sessão do Spark
def create_spark_session():
    return SparkSession.builder.appName("WebLogAnalysis").getOrCreate()

def process_logs(log_file_path, spark):
    """Funcão criada para processar e ajustar o arquivo log.
        Divide as linhas do log em colunas com base em espaços.
        Filtra linhas válidas e organiza os dados em um DataFrame com as colunas necessárias"""
    try:
        if not os.path.exists(log_file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {log_file_path}")

        logs_rdd = spark.read.text(log_file_path).rdd
        
        if logs_rdd.isEmpty():
            raise ValueError(f"O arquivo {log_file_path} está vazio.")

        logs_split = logs_rdd.map(lambda row: row.value.split(" "))

        valid_logs = logs_split.filter(lambda cols: len(cols) > 9)
        invalid_logs = logs_split.filter(lambda cols: len(cols) <= 9)

        invalid_count = invalid_logs.count()
        if invalid_count > 0:
            print(f"Encontradas {invalid_count} linhas inválidas no arquivo de log:")

        if valid_logs.isEmpty():
            raise ValueError("Nenhuma linha válida encontrada no arquivo de log.")

        # Processar as linhas válidas
        logs_df = valid_logs.map(lambda cols: (
            cols[0],  # client_ip
            cols[3][1:],  # timestamp (remover o primeiro colchete)
            cols[5][1:],  # method (remover aspas iniciais)
            cols[6],  # endpoint
            int(cols[8]) if cols[8].isdigit() else None,  # status_code
            int(cols[9]) if cols[9].isdigit() else None   # response_size
        )).toDF(["client_ip", "timestamp", "method", "endpoint", "status_code", "response_size"])

        return logs_df.withColumn("timestamp", to_date(col("timestamp"), "dd/MMM/yyyy:HH:mm:ss"))

    except FileNotFoundError as fnf_error:
        print(f"Erro: {fnf_error}")
        raise
    except ValueError as ve_error:
        print(f"Erro: {ve_error}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao processar os logs: {e}")
        raise

# Análise 1: Identificar as 10 maiores origens de acesso
def analyze_most_accessed_ips(logs_df):
    return logs_df.groupBy("client_ip").count().orderBy(col("count").desc()).limit(10)

# Análise 2: Listar os 6 endpoints mais acessados
def analyze_most_accessed_endpoints(logs_df):
    return logs_df.filter(~col("endpoint").rlike("\\.(jpg|png|css|js|ico)$")) \
                  .groupBy("endpoint").count().orderBy(col("count").desc()).limit(6)

# Análise 3: Quantidade de Client IPs distintos
def analyze_distinct_ips(logs_df):
    return logs_df.select("client_ip").distinct().count()

# Análise 4: Quantidade de dias representados
def analyze_days_count(logs_df):
    return logs_df.select("timestamp").distinct().count()

# Análise 5: Análise de tamanho das respostas
def analyze_response_size(logs_df):
    return logs_df.select(
        sum("response_size").alias("total_data"),
        max("response_size").alias("max_data"),
        min("response_size").alias("min_data"),
        avg("response_size").alias("avg_data")
    )

# Listar tamanhos de respostas detalhados
def analyze_response_sizes_detailed(logs_df):
    return logs_df.select("response_size").orderBy(col("response_size").desc())

# Análise 6: Erros HTTP por dia da semana
def analyze_errors_by_day(logs_df):
    return logs_df.filter((col("status_code") >= 400) & (col("status_code") < 500)) \
                  .withColumn("day_of_week", dayofweek(col("timestamp"))) \
                  .withColumn("day_name", when(col("day_of_week") == 1, "Sunday")
                                         .when(col("day_of_week") == 2, "Monday")
                                         .when(col("day_of_week") == 3, "Tuesday")
                                         .when(col("day_of_week") == 4, "Wednesday")
                                         .when(col("day_of_week") == 5, "Thursday")
                                         .when(col("day_of_week") == 6, "Friday")
                                         .when(col("day_of_week") == 7, "Saturday")
                                         .otherwise("Unknown")) \
                  .groupBy("day_of_week", "day_name").count().orderBy(col("day_of_week").asc())

# Dia com maior número de erros
def analyze_day_with_most_errors(errors_by_day):
    return errors_by_day.orderBy(col("count").desc()).limit(1)

def transform_load(logs_df):
    """Funcão para transformar o DF/RDD em CSV para ser mais fácil passar as informacoes para o banco de dados
    Como no Pyspark não é gerado o CSV direto,foi necessário tratar para gerar somente o arquivo desejado
    """
    # Escreve os dados em uma única partição
    logs_df.coalesce(1).write.csv("./processed_logs_temp", header=True, mode="overwrite")
    
    # Localizar o arquivo CSV gerado
    temp_folder = "./processed_logs_temp"
    output_file = None
    for file in os.listdir(temp_folder):
        if file.endswith(".csv"):
            output_file = "./processed_logs.csv"
            shutil.move(os.path.join(temp_folder, file), output_file)
            break
    
    # Remover a pasta temporária
    shutil.rmtree(temp_folder)
    
    # Retornar o caminho do arquivo gerado
    return output_file

# Fluxo principal
if __name__ == "__main__":
    try:
        spark = create_spark_session()
        spark.sparkContext.setLogLevel("ERROR")

        log_file_path = "/app/src/access_log.txt"
        logs_df = process_logs(log_file_path, spark)

        # Realizar análises
        most_accessed_ips = analyze_most_accessed_ips(logs_df)
        most_accessed_endpoints = analyze_most_accessed_endpoints(logs_df)
        distinct_ips_count = analyze_distinct_ips(logs_df)
        days_count = analyze_days_count(logs_df)
        response_analysis = analyze_response_size(logs_df)
        response_sizes = analyze_response_sizes_detailed(logs_df)
        errors_by_day = analyze_errors_by_day(logs_df)
        max_errors_by_day = analyze_day_with_most_errors(errors_by_day)
        processed_logs = transform_load(logs_df)

        # Exibir resultados
        print("=" * 50)
        print("10 maiores origens de acesso:")
        most_accessed_ips.show(truncate=False)

        print("=" * 50)
        print("6 endpoints mais acessados:")
        most_accessed_endpoints.show(truncate=False)

        print("=" * 50)
        print(f"Quantidade de Client IPs distintos: {distinct_ips_count}")
        print(f"Quantidade de dias representados: {days_count}")

        print("=" * 50)
        print("Tamanho das respostas em bytes (detalhado):")
        response_sizes.show(20, truncate=False)

        print("=" * 50)
        print("Análise do tamanho das respostas:")
        response_analysis.show(truncate=False)

        print("=" * 50)
        print("Número de erros HTTP Client por dia da semana:")
        errors_by_day.show(truncate=False)

        print("=" * 50)
        print("Dia com maior número de erros HTTP Client:")
        max_errors_by_day.show(truncate=False)

        print("Análise concluída.")
    except Exception as main_error:
        print(f"Erro fatal: {main_error}")
    finally:
        spark.stop()