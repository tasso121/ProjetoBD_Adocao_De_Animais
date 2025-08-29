from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# IMPORTANTE: COLOQUE SUA CONNECTION STRING AQUI 
MONGO_CONNECTION_STRING = "mongodb://professor:professor@3.84.92.46:27017/?authSource=admin"
DB_NAME = "projeto_bd_nosql"

def conectar_mongo():
    try:
        client = MongoClient(MONGO_CONNECTION_STRING)
        client.admin.command('ping')
        db = client[DB_NAME]
        return db
    except Exception as e:
        print(f"Erro na conexão com o MongoDB: {e}")
        return None

# --- CRUD Usuario ---
def criar_usuario_mongo(db, cpf, nome, email, senha, data_nascimento):
    try:
        usuario_doc = {"cpf": cpf, "nome": nome, "email": email, "senha": senha, "dataNascimento": datetime.combine(data_nascimento, datetime.min.time())}
        result = db.usuarios.insert_one(usuario_doc)
        print(f"[MONGO] Usuário '{nome}' criado (ID: {result.inserted_id}).")
        return result.inserted_id
    except Exception as e:
        print(f"[MONGO] Erro ao criar usuário: {e}")
        return None

def ler_usuarios_mongo(db):
    try:
        return list(db.usuarios.find({}))
    except Exception as e:
        print(f"[MONGO] Erro ao ler usuários: {e}")
        return []

def atualizar_usuario_mongo(db, id_usuario, novo_nome, novo_email):
    try:
        result = db.usuarios.update_one({"_id": ObjectId(id_usuario)}, {"$set": {"nome": novo_nome, "email": novo_email}})
        if result.modified_count > 0:
            print(f"[MONGO] Usuário ID {id_usuario} atualizado.")
            return True
        return False
    except Exception as e:
        print(f"[MONGO] Erro ao atualizar usuário: {e}")
        return False

def deletar_usuario_mongo(db, id_usuario):
    try:
        result = db.usuarios.delete_one({"_id": ObjectId(id_usuario)})
        if result.deleted_count > 0:
            print(f"[MONGO] Usuário ID {id_usuario} deletado.")
            return True
        return False
    except Exception as e:
        print(f"[MONGO] Erro ao deletar usuário: {e}")
        return False

def ler_usuario_por_nome_mongo(db, nome):
    """Lê um usuário do MongoDB pelo nome."""
    try:
        return db.usuarios.find_one({"nome": nome})
    except Exception as e:
        print(f"[MONGO] Erro ao ler usuário por nome: {e}")
        return None

# --- CRUD Animal ---
def criar_animal_mongo(db, nome, tipo_animal, raca):
    try:
        animal_doc = {"nome": nome, "tipoAnimal": tipo_animal, "raca": raca, "historicoMedico": {}}
        result = db.animais.insert_one(animal_doc)
        print(f"[MONGO] Animal '{nome}' criado (ID: {result.inserted_id}).")
        return result.inserted_id
    except Exception as e:
        print(f"[MONGO] Erro ao criar animal: {e}")
        return None

def ler_animais_mongo(db):
    try:
        return list(db.animais.find({}))
    except Exception as e:
        print(f"[MONGO] Erro ao ler animais: {e}")
        return []

def atualizar_animal_mongo(db, id_animal, novo_nome, nova_raca):
    try:
        result = db.animais.update_one({"_id": ObjectId(id_animal)}, {"$set": {"nome": novo_nome, "raca": nova_raca}})
        if result.modified_count > 0:
            print(f"[MONGO] Animal ID {id_animal} atualizado.")
            return True
        return False
    except Exception as e:
        print(f"[MONGO] Erro ao atualizar animal: {e}")
        return False

def deletar_animal_mongo(db, id_animal):
    try:
        result = db.animais.delete_one({"_id": ObjectId(id_animal)})
        if result.deleted_count > 0:
            print(f"[MONGO] Animal ID {id_animal} deletado.")
            return True
        return False
    except Exception as e:
        print(f"[MONGO] Erro ao deletar animal: {e}")
        return False

# --- CRUD Doacao ---
def criar_doacao_mongo(db, id_doador_mongo, id_adotante_mongo, id_animal_mongo):
    try:
        doacao_doc = {"data": datetime.now(), "doador_id": id_doador_mongo, "adotante_id": id_adotante_mongo, "animal_id": id_animal_mongo}
        result = db.doacoes.insert_one(doacao_doc)
        print(f"[MONGO] Doação registrada (ID: {result.inserted_id}).")
        return result.inserted_id
    except Exception as e:
        print(f"[MONGO] Erro ao criar doação: {e}")
        return None

def ler_doacoes_mongo(db):
    try:
        return list(db.doacoes.find({}))
    except Exception as e:
        print(f"[MONGO] Erro ao ler doações: {e}")
        return []

def atualizar_doacao_mongo(db, id_doacao, nova_data):
    try:
        result = db.doacoes.update_one({"_id": ObjectId(id_doacao)}, {"$set": {"data": nova_data}})
        if result.modified_count > 0:
            print(f"[MONGO] Doação ID {id_doacao} atualizada.")
            return True
        return False
    except Exception as e:
        print(f"[MONGO] Erro ao atualizar doação: {e}")
        return False

def deletar_doacao_mongo(db, id_doacao):
    try:
        result = db.doacoes.delete_one({"_id": ObjectId(id_doacao)})
        if result.deleted_count > 0:
            print(f"[MONGO] Doação ID {id_doacao} deletada.")
            return True
        return False
    except Exception as e:
        print(f"[MONGO] Erro ao deletar doação: {e}")
        return False