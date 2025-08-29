
import psycopg2
from psycopg2 import sql
from datetime import date

# Credenciais para o PostgreSQL
DB_HOST = "atividade-db.c2lqlzv5lrvj.us-east-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "professor"
DB_PASS = "professor"
DB_SCHEMA = "projeto_bd"

def conectar_pg():
    """Estabelece a conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Erro na conexão com o PostgreSQL: {e}")
        return None

# --- CRUD Usuario ---
def criar_usuario_pg(conn, cpf, nome, email, senha, data_nascimento):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("INSERT INTO Usuario (CPF, Email, Nome, Senha, DataNascimento) VALUES (%s, %s, %s, %s, %s) RETURNING idUsuario")
            cursor.execute(query, (cpf, email, nome, senha, data_nascimento))
            id_usuario = cursor.fetchone()[0]
            conn.commit()
            print(f"[PG] Usuário '{nome}' criado (ID: {id_usuario}).")
            return id_usuario
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao criar usuário: {error}")
        conn.rollback()
        return None

def ler_usuarios_pg(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            cursor.execute("SELECT idUsuario, Nome, Email, CPF FROM Usuario ORDER BY idUsuario")
            return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao ler usuários: {error}")
        return []

def atualizar_usuario_pg(conn, id_usuario, novo_nome, novo_email):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("UPDATE Usuario SET Nome = %s, Email = %s WHERE idUsuario = %s")
            cursor.execute(query, (novo_nome, novo_email, id_usuario))
            conn.commit()
            print(f"[PG] Usuário ID {id_usuario} atualizado.")
            return True
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao atualizar usuário: {error}")
        conn.rollback()
        return False

def deletar_usuario_pg(conn, id_usuario):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("DELETE FROM Usuario WHERE idUsuario = %s")
            cursor.execute(query, (id_usuario,))
            conn.commit()
            print(f"[PG] Usuário ID {id_usuario} deletado.")
            return True
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao deletar usuário: {error}")
        conn.rollback()
        return False
    
def definir_role_usuario_pg(conn, id_usuario, role):
    if role not in ['doador', 'adotante']:
        print(f"Role '{role}' inválido.")
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("INSERT INTO {} (Usuario_idUsuario) VALUES (%s)").format(sql.Identifier(role))
            cursor.execute(query, (id_usuario,))
            conn.commit()
            print(f"[PG] Usuário ID {id_usuario} definido como '{role}'.")
            return True
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao definir role '{role}': {error}")
        conn.rollback()
        return False

# --- CRUD Animal ---
def criar_animal_pg(conn, nome, tipo_animal, raca):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("INSERT INTO Animal (Nome, TipoAnimal, Raca) VALUES (%s, %s, %s) RETURNING idAnimal")
            cursor.execute(query, (nome, tipo_animal, raca))
            id_animal = cursor.fetchone()[0]
            conn.commit()
            print(f"[PG] Animal '{nome}' criado (ID: {id_animal}).")
            return id_animal
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao criar animal: {error}")
        conn.rollback()
        return None

def ler_animais_pg(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            cursor.execute("SELECT idAnimal, Nome, TipoAnimal, Raca FROM Animal ORDER BY idAnimal")
            return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao ler animais: {error}")
        return []

def atualizar_animal_pg(conn, id_animal, novo_nome, nova_raca):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("UPDATE Animal SET Nome = %s, Raca = %s WHERE idAnimal = %s")
            cursor.execute(query, (novo_nome, nova_raca, id_animal))
            conn.commit()
            print(f"[PG] Animal ID {id_animal} atualizado.")
            return True
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao atualizar animal: {error}")
        conn.rollback()
        return False

def deletar_animal_pg(conn, id_animal):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("DELETE FROM Animal WHERE idAnimal = %s")
            cursor.execute(query, (id_animal,))
            conn.commit()
            print(f"[PG] Animal ID {id_animal} deletado.")
            return True
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao deletar animal: {error}")
        conn.rollback()
        return False

# --- CRUD Doacao ---
def criar_doacao_pg(conn, id_doador, id_adotante, id_animal):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("INSERT INTO Doacao (Data, Doador_Usuario_idUsuario, Adotante_Usuario_idUsuario, Animal_idAnimal) VALUES (%s, %s, %s, %s) RETURNING idDoacao")
            cursor.execute(query, (date.today(), id_doador, id_adotante, id_animal))
            id_doacao = cursor.fetchone()[0]
            conn.commit()
            print(f"[PG] Doação registrada (ID: {id_doacao}).")
            return id_doacao
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao criar doação: {error}")
        conn.rollback()
        return None

def ler_doacoes_pg(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            cursor.execute("SELECT idDoacao, Data, Doador_Usuario_idUsuario, Adotante_Usuario_idUsuario, Animal_idAnimal FROM Doacao ORDER BY idDoacao")
            return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao ler doações: {error}")
        return []

def atualizar_doacao_pg(conn, id_doacao, nova_data):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("UPDATE Doacao SET Data = %s WHERE idDoacao = %s")
            cursor.execute(query, (nova_data, id_doacao))
            conn.commit()
            print(f"[PG] Doação ID {id_doacao} atualizada.")
            return True
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao atualizar doação: {error}")
        conn.rollback()
        return False

def deletar_doacao_pg(conn, id_doacao):
    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SET search_path TO {DB_SCHEMA}")
            query = sql.SQL("DELETE FROM Doacao WHERE idDoacao = %s")
            cursor.execute(query, (id_doacao,))
            conn.commit()
            print(f"[PG] Doação ID {id_doacao} deletada.")
            return True
    except (Exception, psycopg2.Error) as error:
        print(f"[PG] Erro ao deletar doação: {error}")
        conn.rollback()
        return False