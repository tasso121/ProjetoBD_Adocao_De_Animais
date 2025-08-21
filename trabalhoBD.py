"""
Trabalho Prático de Banco de Dados

Este script demonstra a conexão com um banco de dados PostgreSQL,
executando transações com os fluxos de COMMIT (sucesso) e ROLLBACK (falha).

É necessário ter o Python 3 e a biblioteca 'psycopg2' instalados.
$ sudo apt install python3-psycopg2

Para executar o script, abra um terminal na pasta onde este arquivo está salvo e
use o comando:
$ python3 seu_arquivo.py
"""

import psycopg2
from psycopg2 import sql

# Configurações de acesso ao banco de dados
DB_HOST = "atividade-db.c2lqlzv5lrvj.us-east-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "professor"
DB_PASS = "professor"
DB_SCHEMA = "projeto_bd"

def conectar():
    "Estabelece a conexão com o banco de dados."
    try:
        conn = psycopg2.connect(
            host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
        )
        print("Conexão com o banco de dados bem-sucedida.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Falha na conexão com o banco de dados: {e}")
        return None

def cadastrar_usuario(conn, cpf, nome, email, telefone):
    " Cadastra um novo usuário e seu telefone em uma única transação."
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")

            print("\nIniciando transação para cadastrar novo usuário.")
            
            # Insere o usuário e retorna o ID gerado
            query_usuario = sql.SQL(
                "INSERT INTO Usuario (CPF, Email, Nome, Senha, DataNascimento) VALUES (%s, %s, %s, %s, %s) RETURNING idUsuario"
            )
            cursor.execute(query_usuario, (cpf, email, nome, 'senha_padrao', '2000-01-01'))
            id_usuario = cursor.fetchone()[0]

            # Insere o telefone usando o ID do usuário
            query_telefone = sql.SQL(
                "INSERT INTO Telefone (Telefone, Usuario_idUsuario) VALUES (%s, %s)"
            )
            cursor.execute(query_telefone, (telefone, id_usuario))
            
            # TESTE:
            # Ponto de teste para o ROLLBACK (descomente a linha abaixo para testar a falha)
            # cursor.execute(query_telefone, (telefone, id_usuario))

            conn.commit()
            print(f"COMMIT efetuado: Usuário '{nome}' (ID: {id_usuario}) salvo com sucesso.")

        except (Exception, psycopg2.Error) as error:
            print(f"\nERRO na transação: {error}")
            print("ROLLBACK efetuado: Nenhuma alteração foi salva no banco.")
            conn.rollback()

def listar_usuarios(conn):
    """Consulta e exibe os usuários mais recentes no banco."""
    with conn.cursor() as cursor:
        try:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            
            query = sql.SQL("SELECT idUsuario, Nome, Email FROM Usuario ORDER BY idUsuario DESC LIMIT 5")
            cursor.execute(query)
            
            records = cursor.fetchall()
            
            print("\nUsuários salvos:")
            if not records:
                print("Nenhum usuário encontrado na base de dados.")
            else:
                for row in records:
                    print(f"  ID: {row[0]} | Nome: {row[1]} | Email: {row[2]}")

        except (Exception, psycopg2.Error) as error:
            print(f"Erro ao consultar usuários: {error}")

def main():
    conn = conectar()
    if not conn:
        return

    try:
        # 1. Mostra o estado inicial do banco
        listar_usuarios(conn)

        # 2. Define os dados fixos para o cadastro
        # Para testar usuários diferentes basta trocar os valores abaixo,
        # visto que o banco de dados já possui alguns como teste(principalemnte para testes de ROLLBACK)
        dados_novo_usuario = {
            "cpf": "11122233355",
            "nome": "Maria Oliveira",
            "email": "maria.oliveira@email.com",
            "telefone": "79987654321"
        }
        
        # 3. Executa a rotina de cadastro com os dados definidos
        cadastrar_usuario(
            conn,
            dados_novo_usuario["cpf"],
            dados_novo_usuario["nome"],
            dados_novo_usuario["email"],
            dados_novo_usuario["telefone"]
        )
        
        # 4. Mostra o estado final para verificação
        listar_usuarios(conn)

    finally:
        # Garante que a conexão seja sempre fechada
        if conn:
            conn.close()
            print("\nConexão com o banco de dados fechada.")

if __name__ == "__main__":
    main()