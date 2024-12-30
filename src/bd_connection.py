# -*- coding: utf-8 -*-
import pandas as pd
import psycopg2


# Configuração do banco de dados
def get_db_config():
    return psycopg2.connect(
        host="*****",
        port="*****",
        dbname="*****",
        user="*****",
        password="*****",
        sslmode="*****"
    )


def create_or_update_table(cursor):
    # Alterar a tabela se já existir
    alter_table_query = """
    ALTER TABLE logs
    ALTER COLUMN endpoint TYPE TEXT;
    """

    create_table_query = """
    CREATE TABLE IF NOT EXISTS logs (
        client_ip VARCHAR(50),
        timestamp DATE,
        method VARCHAR(10),
        endpoint TEXT,
        status_code INT,
        response_size INT
    );
    """

    try:
        cursor.execute(create_table_query)
        cursor.execute(alter_table_query)
    except psycopg2.errors.UndefinedColumn:
        pass  # Caso a coluna já esteja no tipo correto, ignore o erro


def validate_and_clean_csv(path_csv: str) -> str:
    try:
        # Ler o CSV
        df = pd.read_csv(path_csv, dtype=str, on_bad_lines='skip', sep=',')

        # Garantir que as colunas correspondam à tabela
        expected_columns = ["client_ip", "timestamp", "method", "endpoint", "status_code", "response_size"]
        if list(df.columns) != expected_columns:
            print("Aviso: As colunas do CSV não correspondem ao esperado. Corrigindo...")
            df = df[expected_columns]

        # Salvar o CSV limpo em um arquivo temporário
        clean_csv_path = "./cleaned_logs.csv"
        df.to_csv(clean_csv_path, index=False)
        return clean_csv_path
    except Exception as e:
        print(f"Erro ao validar e limpar o CSV: {e}")
        raise


def load_csv_to_db(path_csv: str, table_name: str) -> None:
    conn = get_db_config()
    cursor = conn.cursor()

    create_or_update_table(cursor)

    # Validar e limpar o CSV antes do carregamento
    clean_csv_path = validate_and_clean_csv(path_csv)

    copy_sql = f""" 
    COPY {table_name} FROM STDIN 
    WITH CSV HEADER 
    DELIMITER AS ',' 
    """

    try:
        with open(clean_csv_path, "r", encoding="utf-8") as f:
            cursor.copy_expert(sql=copy_sql, file=f)

        conn.commit()
        print(f"Dados carregados para a tabela '{table_name}' com sucesso.")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao carregar dados: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
        print("Conexão encerrada.")


if __name__ == "__main__":
    try:
        # Caminho do arquivo CSV
        csv_path = "/app/src/processed_logs.csv"
        table_name = "logs"

        # Carregar CSV para o banco de dados
        load_csv_to_db(csv_path, table_name)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
