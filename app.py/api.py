from flask_cors import CORS  
import json
from flask import Flask, request, jsonify
import threading
pedido_lock = threading.Lock()

app = Flask(__name__)
CORS(app)  


def load_function (path_file):
    with open(path_file, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
    
def save_function(path_file, save):
    with open (path_file,'w', encoding="utf-8") as f:
        json.dump(save, f, indent=4)
        

@app.get('/produto/<int:id>')
def pedar_id_produto(id):
    save = load_function("produtos.json")
    
    for i in save:
        if i.get('id') == id:
            return jsonify(i), 200
        
    return jsonify({"error" : "Id não encontrado na rota determinada."}), 404 

@app.get('/produto')
def listar_produtos():
    with open("produtos.json", "r", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)
        
    nome = request.args.get('nome')
    tipo = request.args.get('tipo')
        
    resultado = []

    for produto in produtos:
        if nome and nome in produto.get('nome', ''):
            resultado.append(produto)
        elif tipo and tipo in produto.get('tipo', ''):
            resultado.append(produto)

    if nome or tipo:
        produtos = resultado
    return jsonify(produtos), 200
 
@app.post('/produto')
def add_produto():
    produtos = load_function("produtos.json")
        
    novo = request.get_json()
    
    if not novo.get('nome'):
        return jsonify({"erro": "Campo 'nome' é obrigatório"}), 400
    if not isinstance(novo.get('nome'), str):
        return jsonify({"error": "O retorno (nome )não é o tipo de dados necessário."}), 422
    
    tipo_volume = ['kg', 'g', 'l', 'ml']
    if novo.get('tipoVolume') not in tipo_volume:
        return jsonify({"mensagem" : "O tipo de volume informado não é valido"}), 422
    if not isinstance(novo.get('tipoVolume'), str):
        return jsonify({"error": "O retorno (tipoVolume) não é o tipo de dados necessário."}), 422
    
    tipo_produto = ['perecível', 'não perecível']
    if novo.get('tipo') not in tipo_produto:
        return jsonify({"mensagem" : "O tipo do produto não é valido."}), 422
    if not isinstance(novo.get('tipo'), str):
        return jsonify({"error": "O retorno (tipo_produto) não é o tipo de dados necessário."}), 422
    
    if not novo.get('preco'):
        return jsonify({"error" : "Falta o campo preço."}), 400
    if not isinstance(novo.get('preco'), float) or novo.get('preco') == 0:
        return jsonify({"error": "O retorno (preço) não é o tipo de dados necessário."}), 422
    
    ultimo_id = produtos[-1]["id"] if produtos else 0
    novo["id"] = ultimo_id + 1
    produtos.append(novo)
    save_function("produtos.json", produtos)
    
    return jsonify(novo), 201
 
@app.put('/produto/<int:id>')
def atualizar_produto(id):
      produtos = load_function("produtos.json")
      dados = request.get_json()
      
      for produto in produtos:
            if produto.get("id") == id:
                produto.update(dados)
                produto["id"] = id
                save_function("produtos.json", produtos)
                return jsonify({"mensagem" : "O atualizar produtos foi feito com sucesso."}), 200
           
      return jsonify({"erro" : "Produto não encontrado."}), 404
                
@app.delete('/produto/<int:id>')
def deletar(id):
    produtos = load_function("produtos.json")
    validar_produto = load_function("cad_pedido.json")
    
    for produto in validar_produto:
        if id == produto["id_produto"]:
            return jsonify({"error": "O produto selecionado não pode ser deletado, pois está vinculado a uma doação."}), 422
    
    for produto in produtos:
        if id == produto["id"]:
            produtos.remove(produto)
            save_function("produtos.json", produtos)
            return jsonify({"mensagem" : "Produto deletado com sucesso!"}), 204
           
    return jsonify({"error": "produto não encontrado."}), 404
        

@app.get('/instituicoes/<int:id>')
def pegar_id_instituicoes(id):
    save = load_function("cad_inst.json")
    
    for i in save:
        if i.get('id') == id:
            return jsonify(i), 200
        
    return jsonify({"error" : "Id não encontrado na rota determinada."}), 404 

@app.get('/instituicoes')
def cad_instituicao():
    with open("cad_inst.json", "r", encoding="utf-8") as arquivo:
         cadastro_inst = json.load(arquivo)
         
    razao_social = request.args.get('razao_social')
    nome_fantasia = request.args.get('nome_fantasia')
    cnpj = request.args.get('cnpj')
        
    resultado = []

    for instituicao in cadastro_inst:
        if razao_social and razao_social in instituicao.get('razao_social', ''):
            resultado.append(instituicao)
        elif nome_fantasia and nome_fantasia in instituicao.get('nome_fantasia', ''):
            resultado.append(instituicao)
        elif cnpj and cnpj in str(instituicao.get('cnpj', '')):
            resultado.append(instituicao)

    if razao_social or nome_fantasia or cnpj:
        return jsonify(resultado),200
    
    return jsonify(cadastro_inst),200

@app.post('/instituicoes')
def add_instituicoes():
    instituicoes = load_function("cad_inst.json")
    novo = request.get_json()  
    
    if not novo.get('razao_social'):
        return jsonify({"error": "No cadastro, falta a Razão Social da instituição:"}), 400
    if not isinstance(novo.get('razao_social'), str):
        return jsonify({"error": "O retorno (razao_social) não é o tipo de dados necessário."}), 422
    
    if not novo.get('nome_fantasia'):
        return jsonify({"error": "No cadastro, falta o Nome Fantasia da instituição:"}), 400
    if not isinstance(novo.get('nome_fantasia'), str):
        return jsonify({"error": "O retorno (nome_fantasia) não é o tipo de dados necessário."}), 422
    
    if not novo.get('cnpj'):
        return jsonify({"error": "No cadastro, falta o CNPJ da instituição:"}), 400
    if not isinstance(novo.get('cnpj'), int):
        return jsonify({"error": "O retorno (cnpj) não é o tipo de dados necessário."}), 422
    
    if not novo.get('endereco'):
        return jsonify({"error": "No cadastro, falta o Endereço da instituição:"}), 400
    if not isinstance(novo.get('endereco'), str):
        return jsonify({"error": "O retorno (endereco) não é o tipo de dados necessário."}), 422
    
    if not novo.get('contato'):
        return jsonify({"error": "No cadastro, falta o Contato da instituição:"}), 400
    if not isinstance(novo.get('contato'), str):
        return jsonify({"error": "O retorno (contato) não é o tipo de dados necessário."}), 422
    
    if not novo.get('email'):
        return jsonify({"error": "No cadastro, falta o Email da instituição:"}), 400
    if not isinstance(novo.get('email'), str):
        return jsonify({"error": "O retorno (email) não é o tipo de dados necessário."}), 422
    dominios_validos = ['@yahoo.com', '@gmail.com', '@hotmail.com', '@icloud.com']
    dominio_user = "@" + novo.get('email').split("@")[1]
    if dominio_user not in dominios_validos:
        return jsonify({"error": "O retorno (email) não tem dominio válido."}), 422
            
    ultimo_id = instituicoes[-1]["id"] if instituicoes else 0
    novo["id"] = ultimo_id + 1
    instituicoes.append(novo)
    save_function("cad_inst.json", instituicoes )
    
    return jsonify(novo), 201

@app.put('/instituicoes/<int:id>')
def atualizar_dados(id):
    instituicoes = load_function("cad_inst.json")
    dados = request.get_json()
    
    for inst in instituicoes:
        if inst.get("id") == id:
            inst.update(dados)
            inst["id"] = id
            save_function("cad_inst.json", instituicoes)
            return jsonify({"mensagem": "O atualizar instituições foi feito com sucesso."}), 200
        
    return jsonify({"error": "Instituição não encontrado."}), 404

@app.delete('/instituicoes/<int:id>')
def delete_instituicoes(id):
    instituicoes = load_function("cad_inst.json")
    pedidos = load_function("cad_pedido.json")
    
    for valid_id in pedidos:
        if id == valid_id["id_instituicao"]:
            return jsonify({"error": "A instituição desejada não pode ser deletada por estar vinculada a um pedido."}), 422
    
    for inst in instituicoes:
        if id == inst["id"]:
            instituicoes.remove(inst)
            save_function("cad_inst.json", instituicoes) 
            return jsonify({"mensagem": "Instituição deletada."}), 204
       
    return jsonify({"error": "Instituição não encontrada."}), 404   

@app.get('/doador/<int:id>')
def pegar_id_doador(id):
    save = load_function("cad_doador.json")
    
    for i in save:
        if i.get('id') == id:
            return jsonify(i), 200
        
    return jsonify({"error" : "Id não encontrado na rota determinada."}), 404 

@app.get('/doador')
def cad_doador():
    with open("cad_doador.json", "r", encoding="utf-8") as arquivo:
         cadastro_doador = json.load(arquivo)
      
    nome = request.args.get('nome')
    tipo_doador = request.args.get('tipo_doador')
    
    resultado = []

    for doador in cadastro_doador:
        if nome and nome in doador.get('nome', ''):
            resultado.append(doador)
        elif tipo_doador and tipo_doador in doador.get('tipo_doador', ''):
            resultado.append(doador)
    
    if nome or tipo_doador:
        return jsonify(resultado), 200
    return jsonify(cadastro_doador), 200

@app.post('/doador')
def add_doador():
    doador = load_function("cad_doador.json")
    novo = request.get_json()
    
    if not novo.get('nome'):
        return jsonify({"error": "O atributo Nome não foi encontrado."}), 400
    if not isinstance(novo.get('nome'), str):
        return jsonify({"error" : "O retorno (nome) não é do tipo dados necessário."}), 422
    
    tipo_doador = ['cpf', 'cnpj']
    if novo.get('tipo_doador') not in tipo_doador:
        return jsonify({"error": "O tipo do cliente não foi encontrado (CPF , CNPJ)"}), 422
    if not isinstance(novo.get('tipo_doador'), str):
        return jsonify({"error" : "O retorno (tipo_doador) não é do tipo dados necessário."}), 422
    
    if not novo.get('endereco'):
         return jsonify({"error": "No cadastro, falta o Endereço do doador:"}), 400
    if not isinstance(novo.get('endereco'), str):
        return jsonify({"error" : "O retorno (endereco) não é do tipo dados necessário."}), 422
    
    if not novo.get('telefone'):
        return jsonify({"error": "No cadastro, falta o Contato do doador:"}), 400
    if not isinstance(novo.get('telefone'), str):
        return jsonify({"error" : "O retorno (telefone) não é do tipo dados necessário."}), 422
    
    if not novo.get('cidade'):
        return jsonify({"error": "No cadastro, falta o Endereço do doador:"}), 400
    if not isinstance(novo.get('cidade'), str):
        return jsonify({"error" : "O retorno (cidade) não é do tipo dados necessário."}), 422
    
    if not novo.get('cep'):
        return jsonify({"error": "No cadastro, falta o CEP do doador:"}), 400
    if not isinstance(novo.get('cep'), str):
        return jsonify({"error" : "O retorno (cep) não é do tipo dados necessário."}), 422
    
    if not novo.get('email'):
        return jsonify({"error": "No cadastro, falta o Email da instituição:"}), 400
    if not isinstance(novo.get('email'), str):
        return jsonify({"error": "O retorno (email) não é o tipo de dados necessário."}), 422
    dominios_validos = ['@yahoo.com', '@gmail.com', '@hotmail.com', '@icloud.com']
    dominio_user ="@" + novo.get('email').split("@")[1]
    if dominio_user not in dominios_validos:
        return jsonify({"error": "O retorno (email) não tem dominio válido."}), 422
         
    ultimo_id = doador[-1]["id"] if doador else 0
    novo["id"] = ultimo_id + 1
    doador.append(novo)
    save_function("cad_doador.json", doador)
    
    return jsonify(novo), 201

@app.put('/doador/<int:id>')
def atualizar_doador(id):
    doadores = load_function("cad_doador.json")
    novo = request.get_json()
    
    for doador in doadores:
        if doador["id"] == id:
            doador.update(novo)
            doador["id"] == id
            save_function("cad_doador.json", doadores)
            return jsonify({"mensagem": "/doador atualizado com sucesso."}), 200
        
    return jsonify({"error": "Doador não encontrado."}), 404
        
@app.delete('/doador/<int:id>')
def delete_doador(id):
    doadores = load_function("cad_doador.json")
    lista_validar = load_function("cad_pedido.json")
    
    for pedido in lista_validar:
        if id == pedido["id_doador"]:
            return jsonify({"error": "O doador não pode não ser deletado."}), 422
        
        for doador in doadores:
            if id == doador["id"]:
                doadores.remove(doador)
                save_function("cad_doador.json", doadores)
                return jsonify({"mensagem": "Doador deletado com sucesso!"}), 204
            
        return jsonify({"error": "Doador não encontrado."}), 404
        

@app.get('/pedido/<int:id>')
def pegar_id_pedido(id):
    save = load_function("cad_pedido.json")
    
    for i in save:
        if i.get('id') == id:
            return jsonify(i), 200
        
    return jsonify({"error" : "Id não encontrado na rota determinada."}), 404 

@app.get('/pedido')
def cad_pedido():
    with open("cad_pedido.json", "r", encoding="utf-8") as arquivo:
        cadastro_pedido = json.load(arquivo)

    id_doador = request.args.get('id_doador')
    id_instituicao = request.args.get('id_instituicao')
        
    resultado = []

    for pedidos in cadastro_pedido:
        if id_doador and int(id_doador) == pedidos.get('id_doador', ''):
            resultado.append(pedidos)
        elif id_instituicao and int(id_instituicao) == pedidos.get('id_instituicao', ''):
            resultado.append(pedidos)

    if id_doador or id_instituicao:
        return jsonify(resultado), 200
    
    return jsonify(cadastro_pedido),200

@app.post('/pedido')
def add_pedido():
    novo = request.get_json()

    if not novo.get('id_doador'):
        return jsonify({"error": "No pedido, falta o id_doador:"}), 400
    if not isinstance(novo.get('id_doador'), int):
        return jsonify({"error": "O retorno (id_doador) não é do tipo dados necessário."}), 422

    if not novo.get('id_produtos') or not isinstance(novo.get('id_produtos'), list):
        return jsonify({"error": "No pedido, falta a lista id_produtos:"}), 400

    if not novo.get('id_instituicao'):
        return jsonify({"error": "No pedido, falta o id_instituicao:"}), 400
    if not isinstance(novo.get('id_instituicao'), int):
        return jsonify({"error": "O retorno (id_instituicao) não é do tipo dados necessário."}), 422

    if not novo.get('id_metodo_pgto'):
        return jsonify({"error": "No pedido, falta o id_metodo_pgto:"}), 400
    if not isinstance(novo.get('id_metodo_pgto'), int):
        return jsonify({"error": "O retorno (id_metodo_pgto) não é do tipo dados necessário."}), 422

    doadores    = load_function("cad_doador.json")
    instituicoes = load_function("cad_inst.json")
    produtos    = load_function("produtos.json")
    metodos     = load_function("metodo_pgto.json")

    ids_doadores     = [i["id"] for i in doadores]
    ids_instituicoes = [i["id"] for i in instituicoes]
    ids_produtos     = [i["id"] for i in produtos]
    ids_metodos      = [i["id"] for i in metodos]

    if novo.get("id_doador") not in ids_doadores:
        return jsonify({"error": "id_doador não cadastrado."}), 404
    if novo.get("id_instituicao") not in ids_instituicoes:
        return jsonify({"error": "id_instituicao não cadastrado."}), 404
    if novo.get("id_metodo_pgto") not in ids_metodos:
        return jsonify({"error": "id_metodo_pgto não cadastrado."}), 404

    for id_prod in novo.get("id_produtos"):
        if id_prod not in ids_produtos:
            return jsonify({"error": f"id_produto {id_prod} não cadastrado."}), 404

    with pedido_lock:
        pedido = load_function("cad_pedido.json")
        ultimo_id = pedido[-1]["id"] if pedido else 0
        novo["id"] = ultimo_id + 1
        pedido.append(novo)
        save_function("cad_pedido.json", pedido)

    return jsonify(novo), 201

@app.put('/pedido/<int:id>')
def atualizar_pedido(id):
    pedidos = load_function("cad_pedido.json")
    dados = request.get_json()
    
    for pedido in pedidos:
        if id == pedido["id"]:
            pedido.update(dados)
            pedido["id"] = id
            save_function("cad_pedido.json", pedidos)
            return jsonify({"mensagem": f"O pedido {id} foi atualizado com sucesso!"}), 200
            
    return jsonify({"error": "Pedido não encontrado."}), 404
    
@app.get('/metodo_pgto')
def metodo_pgto():
    metodos = load_function("metodo_pgto.json")
    return jsonify(metodos)

@app.post("/metodo_pgto")
def confirmar_pgto():
    confirmar_pgto = load_function("metodo_pgto.json")
    novos_dados = request.get_json()
    
    id_metodos_pgto = [1,2,3]
    
    metodos_pgto_validos = [
        (1,"pix"),
        (2 ,"cartão de credito"),
        (3, "boleto")
    ]
    id_escolhido = novos_dados.get("id_metodo_pgto")

    if id_escolhido not in id_metodos_pgto:
        return jsonify({"error": "Metodo de pagamento nao encontrado."}), 404
    elif id_escolhido == 1:
        return jsonify({"mensagem": f"Pagamento via {metodos_pgto_validos[0][1]} confirmado!"}), 200
    elif id_escolhido == 2:
        return jsonify({"mensagem": f"Pagamento via {metodos_pgto_validos[1][1]} confirmado!"}), 200
    elif id_escolhido == 3:
        return jsonify({"mensagem": f"Pagamento via {metodos_pgto_validos[2][1]} confirmado!"}), 200
        
app.run()
 