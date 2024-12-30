import unittest
from pyspark.sql import SparkSession
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from acess_log import (
    process_logs,
    analyze_most_accessed_ips,
    analyze_most_accessed_endpoints,
    analyze_distinct_ips,
    analyze_days_count,
    analyze_response_size,
    analyze_errors_by_day,
    analyze_day_with_most_errors,
)
import os


class TestAccessLogAnalysis(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Inicializando sessão Spark...")
        cls.spark = SparkSession.builder.master("local[1]").appName("AccessLogTest").getOrCreate()
        cls.spark.sparkContext.setLogLevel("ERROR")
        cls.log_file_path = "/app/src/test_access_log.txt"

    @classmethod
    def tearDownClass(cls):
        print("Encerrando sessão Spark...")
        cls.spark.stop()

    def setUp(self):
        print("Processando arquivo de log...")
        try:
            self.logs_df = process_logs(self.log_file_path, self.spark)
        except Exception as e:
            print(f"Erro ao processar logs: {e}")
            raise

    def test_process_logs(self):
        print("Executando: test_process_logs")
        try:
            self.assertIsNotNone(self.logs_df)
            self.assertEqual(
                set(self.logs_df.columns),
                {"client_ip", "timestamp", "method", "endpoint", "status_code", "response_size"}
            )
        except AssertionError as e:
            print(f"Falha em test_process_logs: {e}")
            raise

    def test_analyze_most_accessed_ips(self):
        print("Executando: test_analyze_most_accessed_ips")
        try:
            result = analyze_most_accessed_ips(self.logs_df)
            ips = [row.client_ip for row in result.collect()]
            self.assertIn("10.43.29.24", ips)
            self.assertEqual(result.collect()[0]["count"], 7)
        except AssertionError as e:
            print(f"Falha em test_analyze_most_accessed_ips: {e}")
            raise

    def test_analyze_most_accessed_endpoints(self):
        print("Executando: test_analyze_most_accessed_endpoints")
        try:
            result = analyze_most_accessed_endpoints(self.logs_df)
            endpoints = [row.endpoint for row in result.collect()]
            self.assertIn("/login", endpoints)
            self.assertEqual(len(endpoints), 6)
        except AssertionError as e:
            print(f"Falha em test_analyze_most_accessed_endpoints: {e}")
            raise

    def test_analyze_distinct_ips(self):
        print("Executando: test_analyze_distinct_ips")
        try:
            result = analyze_distinct_ips(self.logs_df)
            self.assertEqual(result, 10)
        except AssertionError as e:
            print(f"Falha em test_analyze_distinct_ips: {e}")
            raise

    def test_analyze_days_count(self):
        print("Executando: test_analyze_days_count")
        try:
            result = analyze_days_count(self.logs_df)
            self.assertEqual(result, 9)
        except AssertionError as e:
            print(f"Falha em test_analyze_days_count: {e}")
            raise

    def test_analyze_response_size(self):
        print("Executando: test_analyze_response_size")
        try:
            result = analyze_response_size(self.logs_df).collect()[0]
            self.assertEqual(result["total_data"], 45854)
            self.assertEqual(result["max_data"], 18432)
            self.assertEqual(result["min_data"], 0)
            self.assertAlmostEqual(result["avg_data"], 2697.29, places=2)
        except AssertionError as e:
            print(f"Falha em test_analyze_response_size: {e}")
            raise

    def test_analyze_errors_by_day(self):
        print("Executando: test_analyze_errors_by_day")
        try:
            result = analyze_errors_by_day(self.logs_df)
            errors = result.collect()
            self.assertEqual(len(errors), 4)
            day_counts = {row.day_name: row["count"] for row in errors}
            self.assertEqual(day_counts["Thursday"], 7)
            self.assertIn("Tuesday", day_counts)
        except AssertionError as e:
            print(f"Falha em test_analyze_errors_by_day: {e}")
            raise

    def test_analyze_day_with_most_errors(self):
        print("Executando: test_analyze_day_with_most_errors")
        try:
            errors_by_day = analyze_errors_by_day(self.logs_df)
            result = analyze_day_with_most_errors(errors_by_day)
            top_error_day = result.collect()[0]
            self.assertEqual(top_error_day["day_name"], "Thursday")
            self.assertEqual(top_error_day["count"], 7)
        except AssertionError as e:
            print(f"Falha em test_analyze_day_with_most_errors: {e}")
            raise

    def test_process_logs_file_not_found(self):
        print("Executando: test_process_logs_file_not_found")
        with self.assertRaises(FileNotFoundError):
            process_logs("/app/src/non_existent_file.txt", self.spark)

    def test_process_logs_empty_file(self):
        print("Executando: test_process_logs_empty_file")
        empty_file_path = "/app/src/empty_file.txt"
        # Criar um arquivo vazio para teste
        with open(empty_file_path, "w") as f:
            pass
        try:
            with self.assertRaises(ValueError):
                process_logs(empty_file_path, self.spark)
        finally:
            os.remove(empty_file_path)  # Limpar o arquivo após o teste

    def test_process_logs_invalid_lines(self):
        print("Executando: test_process_logs_invalid_lines")
        invalid_file_path = "/app/src/invalid_lines_file.txt"
        # Criar um arquivo com linhas inválidas
        with open(invalid_file_path, "w") as f:
            f.write("Linha inválida sem colunas suficientes\n")
            f.write("Outra linha inválida\n")
        try:
            with self.assertRaises(ValueError):
                process_logs(invalid_file_path, self.spark)
        finally:
            os.remove(invalid_file_path)  # Limpar o arquivo após o teste

    def test_process_logs_no_valid_lines(self):
        print("Executando: test_process_logs_no_valid_lines")
        no_valid_lines_file_path = "/app/src/no_valid_lines_file.txt"
        # Criar um arquivo com linhas inválidas que não são processáveis
        with open(no_valid_lines_file_path, "w") as f:
            f.write("Linha inválida sem colunas suficientes\n")
            f.write("Outra linha inválida\n")
        try:
            with self.assertRaises(ValueError):
                process_logs(no_valid_lines_file_path, self.spark)
        finally:
            os.remove(no_valid_lines_file_path)  # Limpar o arquivo após o teste


if __name__ == "__main__":
    unittest.main()
