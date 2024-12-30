import subprocess

def run_script(script_name, is_test=False):
    """
    Função para executar scripts ou testes.
    
    :param script_name: Nome do arquivo do script a ser executado.
    :param is_test: Indica se o script é um teste unitário (True) ou um script normal (False).
    """
    print(f"Executando {script_name}...")

    # Define o comando com base no tipo de execução
    if is_test:
        # Comando para rodar testes com unittest, ignorando warnings
        command = ["python", "-W", "ignore", "-m", "unittest", script_name]
    else:
        # Comando padrão para rodar scripts normais
        command = ["python", script_name]

    # Executa o comando e captura a saída
    result = subprocess.run(command, capture_output=True, text=True)

    # Verifica o resultado
    if result.returncode == 0:
        print(f"Saída de {script_name}:\n{result.stdout}")
    else:
        print(f"Erro ao executar {script_name}:\n{result.stderr}")
        exit(1)

if __name__ == "__main__":
    # Lista de scripts para execução
    scripts_to_run = [
        {"name": "src/acess_log.py", "is_test": False},  # Script normal
        {"name": "src/test_unitario.py", "is_test": True},  # Teste unitário
        {"name": "src/bd_connection.py", "is_test": False},  # Script normal
    ]

    # Iterar sobre a lista de scripts e executá-los
    for script in scripts_to_run:
        run_script(script["name"], is_test=script["is_test"])

    print("Todos os scripts foram executados com sucesso!")
