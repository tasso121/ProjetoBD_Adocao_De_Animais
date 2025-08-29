import db_postgresql as pg
import db_mongodb as mg
from datetime import date, datetime

def pausar_e_verificar(mensagem="continuar"):
    """Função para pausar o script e pedir verificação."""
    input(f"\n✅ VERIFIQUE OS BANCOS. Pressione Enter para {mensagem}...")

def demonstrar_crud_usuario(conn_pg, db_mongo):
    """Executa a demonstração para a entidade Usuario."""
    print("\n" + "="*50)
    print("--- DEMONSTRAÇÃO DO CRUD DE USUÁRIO ---")
    print("="*50)
    
    ids_pg, ids_mongo = {}, {}

    # --- CREATE ---
    print("\n[CREATE] Criando 'João Doador' e 'Ana Adotante'...")
    ids_pg['joao'] = pg.criar_usuario_pg(conn_pg, '11122233344', 'João Doador', 'joao@email.com', 'senha123', date(1990, 5, 15))
    ids_mongo['joao'] = mg.criar_usuario_mongo(db_mongo, '11122233344', 'João Doador', 'joao@email.com', 'senha123', date(1990, 5, 15))
    ids_pg['ana'] = pg.criar_usuario_pg(conn_pg, '55566677788', 'Ana Adotante', 'ana@email.com', 'senha456', date(1992, 10, 20))
    ids_mongo['ana'] = mg.criar_usuario_mongo(db_mongo, '55566677788', 'Ana Adotante', 'ana@email.com', 'senha456', date(1992, 10, 20))
    
    pausar_e_verificar("o READ inicial")

    # --- READ ---
    print("\n[READ] Lendo usuários de ambos os bancos:")
    for u in pg.ler_usuarios_pg(conn_pg): print(f"  [PG] -> {u}")
    for u in mg.ler_usuarios_mongo(db_mongo): print(f"  [MONGO] -> {u}")

    pausar_e_verificar("o UPDATE")

    # --- UPDATE ---
    print("\n[UPDATE] Atualizando 'Ana Adotante' para 'Ana Adotante Silva'...")
    pg.atualizar_usuario_pg(conn_pg, ids_pg['ana'], 'Ana Adotante Silva', 'ana.silva@email.com')
    mg.atualizar_usuario_mongo(db_mongo, ids_mongo['ana'], 'Ana Adotante Silva', 'ana.silva@email.com')

    pausar_e_verificar("o DELETE")

    # --- DELETE ---
    print("\n[DELETE] Para demonstrar a deleção, vamos primeiro criar um novo usuário 'Carlos Para Deletar'...")
    id_temp_pg = pg.criar_usuario_pg(conn_pg, '99988877766', 'Carlos Para Deletar', 'carlos@email.com', 'senhatemp', date(2000, 1, 1))
    id_temp_mongo = mg.criar_usuario_mongo(db_mongo, '99988877766', 'Carlos Para Deletar', 'carlos@email.com', 'senhatemp', date(2000, 1, 1))
    
    print("\n[READ] Verificando que 'Carlos Para Deletar' foi criado:")
    for u in pg.ler_usuarios_pg(conn_pg): print(f"  [PG] -> {u}")
    for u in mg.ler_usuarios_mongo(db_mongo): print(f"  [MONGO] -> {u}")
    
    pausar_e_verificar("DELETAR o usuário 'Carlos'")

    print("\n[DELETE] Agora, deletando 'Carlos Para Deletar'...")
    if id_temp_pg: pg.deletar_usuario_pg(conn_pg, id_temp_pg)
    if id_temp_mongo: mg.deletar_usuario_mongo(db_mongo, id_temp_mongo)

    pausar_e_verificar("ver o resultado final")

    # --- READ FINAL ---
    print("\n[READ] Lendo usuários no estado final (note que João e Ana continuam aqui):")
    for u in pg.ler_usuarios_pg(conn_pg): print(f"  [PG] -> {u}")
    for u in mg.ler_usuarios_mongo(db_mongo): print(f"  [MONGO] -> {u}")
    
    print("\n--- FIM DA DEMONSTRAÇÃO DE USUÁRIO ---")
    return ids_pg, ids_mongo

def demonstrar_crud_animal(conn_pg, db_mongo):
    """Executa a demonstração para a entidade Animal."""
    print("\n" + "="*50)
    print("--- DEMONSTRAÇÃO DO CRUD DE ANIMAL ---")
    print("="*50)
    
    ids_pg, ids_mongo = {}, {}

    # --- CREATE ---
    print("\n[CREATE] Criando 'Rex'...")
    ids_pg['rex'] = pg.criar_animal_pg(conn_pg, 'Rex', 'PET', 'Vira-lata')
    ids_mongo['rex'] = mg.criar_animal_mongo(db_mongo, 'Rex', 'PET', 'Vira-lata')

    pausar_e_verificar("o READ")
    
    # --- READ ---
    print("\n[READ] Lendo animais:")
    for a in pg.ler_animais_pg(conn_pg): print(f"  [PG] -> {a}")
    for a in mg.ler_animais_mongo(db_mongo): print(f"  [MONGO] -> {a}")

    pausar_e_verificar("o UPDATE")

    # --- UPDATE ---
    print("\n[UPDATE] Atualizando 'Rex' para 'Rex Junior'...")
    pg.atualizar_animal_pg(conn_pg, ids_pg['rex'], 'Rex Junior', 'Vira-lata Caramelo')
    mg.atualizar_animal_mongo(db_mongo, ids_mongo['rex'], 'Rex Junior', 'Vira-lata Caramelo')

    pausar_e_verificar("o DELETE")

    # --- DELETE ---
    print("\n[DELETE] Para demonstrar, vamos criar e depois deletar 'Mimi Para Deletar'...")
    id_temp_pg = pg.criar_animal_pg(conn_pg, 'Mimi Para Deletar', 'PET', 'Gato')
    id_temp_mongo = mg.criar_animal_mongo(db_mongo, 'Mimi Para Deletar', 'PET', 'Gato')

    print("\n[READ] Verificando que 'Mimi Para Deletar' foi criada:")
    for a in pg.ler_animais_pg(conn_pg): print(f"  [PG] -> {a}")
    for a in mg.ler_animais_mongo(db_mongo): print(f"  [MONGO] -> {a}")

    pausar_e_verificar("DELETAR a 'Mimi'")

    print("\n[DELETE] Agora, deletando 'Mimi Para Deletar'...")
    if id_temp_pg: pg.deletar_animal_pg(conn_pg, id_temp_pg)
    if id_temp_mongo: mg.deletar_animal_mongo(db_mongo, id_temp_mongo)

    pausar_e_verificar("ver o resultado final")

    # --- READ FINAL ---
    print("\n[READ] Lendo animais no estado final (note que Rex continua aqui):")
    for a in pg.ler_animais_pg(conn_pg): print(f"  [PG] -> {a}")
    for a in mg.ler_animais_mongo(db_mongo): print(f"  [MONGO] -> {a}")

    print("\n--- FIM DA DEMONSTRAÇÃO DE ANIMAL ---")
    return ids_pg, ids_mongo

def demonstrar_crud_doacao(conn_pg, db_mongo, ids_usuarios_pg, ids_animais_pg, ids_usuarios_mongo, ids_animais_mongo):
    """Executa a demonstração para o relacionamento Doacao."""
    print("\n" + "="*50)
    print("--- DEMONSTRAÇÃO DO CRUD DE DOACAO ---")
    print("="*50)

    # --- SETUP ---
    print("\n[SETUP] Definindo papéis de Doador e Adotante no PostgreSQL...")
    pg.definir_role_usuario_pg(conn_pg, ids_usuarios_pg['joao'], 'doador')
    pg.definir_role_usuario_pg(conn_pg, ids_usuarios_pg['ana'], 'adotante')

    pausar_e_verificar("o CREATE da Doação")

    # --- CREATE ---
    print("\n[CREATE] Registrando uma doação...")
    id_doacao_pg = pg.criar_doacao_pg(conn_pg, ids_usuarios_pg['joao'], ids_usuarios_pg['ana'], ids_animais_pg['rex'])
    id_doacao_mongo = mg.criar_doacao_mongo(db_mongo, ids_usuarios_mongo['joao'], ids_usuarios_mongo['ana'], ids_animais_mongo['rex'])

    pausar_e_verificar("o READ da Doação")
    
    # --- READ ---
    print("\n[READ] Lendo doações:")
    for d in pg.ler_doacoes_pg(conn_pg): print(f"  [PG] -> {d}")
    for d in mg.ler_doacoes_mongo(db_mongo): print(f"  [MONGO] -> {d}")

    pausar_e_verificar("o UPDATE da Doação")

    # --- UPDATE ---
    print("\n[UPDATE] Atualizando data da doação...")
    nova_data = date(2025, 9, 15)
    if id_doacao_pg: pg.atualizar_doacao_pg(conn_pg, id_doacao_pg, nova_data)
    if id_doacao_mongo: mg.atualizar_doacao_mongo(db_mongo, id_doacao_mongo, datetime.combine(nova_data, datetime.min.time()))

    pausar_e_verificar("o DELETE da Doação")
    
    # --- DELETE ---
    print("\n[DELETE] Deletando a doação...")
    if id_doacao_pg: pg.deletar_doacao_pg(conn_pg, id_doacao_pg)
    if id_doacao_mongo: mg.deletar_doacao_mongo(db_mongo, id_doacao_mongo)

    pausar_e_verificar("ver o resultado final")

    # --- READ FINAL ---
    print("\n[READ] Lendo doações no estado final:")
    for d in pg.ler_doacoes_pg(conn_pg): print(f"  [PG] -> {d}")
    for d in mg.ler_doacoes_mongo(db_mongo): print(f"  [MONGO] -> {d}")

    print("\n--- FIM DA DEMONSTRAÇÃO DE DOAÇÃO ---")

def main():
    """Função principal que gerencia o menu interativo."""
    conn_pg = pg.conectar_pg()
    db_mongo = mg.conectar_mongo()
    
    if not conn_pg or not db_mongo:
        print("Encerrando o programa por falha em uma das conexões.")
        return

    ids_usuarios_pg, ids_usuarios_mongo = {}, {}
    ids_animais_pg, ids_animais_mongo = {}, {}

    while True:
        print("\n" + "="*25)
        print("MENU DE DEMONSTRAÇÃO")
        print("="*25)
        print("1. CRUD de Usuário")
        print("2. CRUD de Animal")
        print("3. CRUD de Doação")
        print("0. Sair")
        
        opcao = input("Escolha uma opção para demonstrar: ")

        if opcao == '1':
            ids_usuarios_pg, ids_usuarios_mongo = demonstrar_crud_usuario(conn_pg, db_mongo)
        elif opcao == '2':
            ids_animais_pg, ids_animais_mongo = demonstrar_crud_animal(conn_pg, db_mongo)
        elif opcao == '3':
            if not ids_usuarios_pg or not ids_animais_pg:
                print("\nAVISO: Execute o CRUD de Usuário (1) e Animal (2) primeiro para gerar os dados.")
            else:
                demonstrar_crud_doacao(conn_pg, db_mongo, ids_usuarios_pg, ids_animais_pg, ids_usuarios_mongo, ids_animais_mongo)
        elif opcao == '0':
            break
        else:
            print("\nOpção inválida. Tente novamente.")

    if conn_pg:
        conn_pg.close()
        print("\nConexão com o PostgreSQL fechada.")

if __name__ == "__main__":
    main()