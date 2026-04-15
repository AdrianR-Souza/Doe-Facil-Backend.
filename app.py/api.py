import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def load_function ():
    with open("produtos.json", "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)
    
    
def save_function(save):
    with open ('produtos.json','w', encoding="utf-8") as f:
        json.dump(save, f, indent=4)

#localhost/rota/id
@app.get('/produtos/<int:id>')
def get_id(id):
    save = load_function()
    
    for i in save:
        if i.get('id') == id:
            return jsonify(i), 200
        
    return jsonify({"error" : "Id não encontrado na rota determinada."}), 404 

    
    

#para add os jsons dinamicamente
def ler_json(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []

def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        
###############################################################################
#                     produtos

#rota cadastro de produtos
@app.route('/produto', methods=["GET"])
def listar_produtos():
   with open("produtos.json", "r", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)
   return jsonify(produtos), 200
 
 # metodo POST que recebe o JSON do front-end e add dinamicamente
@app.route('/produto', methods=["POST"])
def add_produto():
    produtos = ler_json("produtos.json")
        
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
    #estava implementando os isistance
    
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
    salvar_json("produtos.json", produtos)
    
    return jsonify(novo), 201
 
 
 #metodo PUT- ainda não está funcinando
@app.route('/produto/<int:id>', methods=["PUT"])
def atualizar_produto(id):
      produtos = ler_json("produtos.json")
      
      for produto in produtos:
             if produto["id"] == id:
                  dados_novos = request.get_json()
                  produto.update(dados_novos)
                  produto["id"] = id
                  
                  if dados_novos is None:
                         return jsonify ({"error" : "JSON inválido ou ausente."})
                  
                  salvar_json("produtos.json", produtos)
                  return jsonify(produto), 200
            
      return jsonify({"erro" : "Produto não encontrado."}), 404


      
###############################################################################
#                     instituições

#rota cadastro de instituições que irão receber as doações diretamente
@app.route('/instituicoes', methods=["GET"])
def cad_instituicao():
   with open("cad_inst.json", "r", encoding="utf-8") as arquivo:
         cadastro_inst = json.load(arquivo)
   return jsonify(cadastro_inst),200

#post instituições
@app.route('/instituicoes', methods=["POST"])
def add_instituicoes():
    instituicoes = ler_json("cad_inst.json")
    
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
    #if not novo.get('email') == '@':
    
    
    
    # pega o último ID e incrementa
    ultimo_id = instituicoes[-1]["id"] if instituicoes else 0
    novo["id"] = ultimo_id + 1
    
    instituicoes.append(novo)
    salvar_json("cad_inst.json", instituicoes )
    
    return jsonify(novo), 201

###############################################################################
#                            DOADOR
#rota GET cadastro de doadores
@app.route('/doador', methods=["GET"])
def cad_doador():
   with open("cad_doador.json", "r", encoding="utf-8") as arquivo:
         cadastro_doador = json.load(arquivo)
      
   return jsonify(cadastro_doador)

#post do doador
@app.route('/doador', methods=["POST"])
def add_doador():
    doador = ler_json("cad_doador.json")
    
    novo = request.get_json()
    
    if not novo.get('nome'):
        return jsonify({"error": "O atributo Nome não foi encontrado."}), 400
    if not isinstance(novo.get('nome'), str):
        return jsonify({"error" : "O retorno (nome) não é do tipo dados necessário."}), 422
    
    tip_doador = ['cpf', 'cnpj']
    if novo.get('tipo_doador') not in tip_doador:
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
    
    
    ultimo_id = doador[-1]["id"] if doador else 0
    
    novo["id"] = ultimo_id + 1
    
    doador.append(novo)
    salvar_json("cad_doador.json", doador)
    
    return jsonify(novo), 201


##############################################################################
#Rota /pedido

@app.route('/pedido', methods=["GET"])
def cad_pedido():
    with open("cad_pedido.json", "r", encoding="utf-8") as arquivo:
        cadastro_pedido = json.load(arquivo)
        
    return jsonify(cadastro_pedido),200

@app.route('/pedido', methods=["POST"])
def add_pedido():
    
    pedido = ler_json("cad_pedido.json")
    novo = request.get_json()
    #ver c o diego sobre esse post
    
   
    if not novo.get('id_doador'):
        return jsonify({"error": "No pedido, falta o id_doador:"}), 400
    if not isinstance(novo.get('id_doador'), int):
        return jsonify({"error" : "O retorno (id_doador) não é do tipo dados necessário."}), 422
    
    if not novo.get('id_produto'):
        return jsonify({"error": "No pedido, falta o id_produto:"}), 400
    if not isinstance(novo.get('id_produto'), int):
        return jsonify({"error" : "O retorno (id_produto) não é do tipo dados necessário."}), 422
    
    if not novo.get('id_instituicao'):
        return jsonify({"error": "No pedido, falta o id_instituicao:"}), 400
    if not isinstance(novo.get('id_instituicao'), int):
        return jsonify({"error" : "O retorno (id_instituicao) não é do tipo dados necessário."}), 422
    
    if not novo.get('id_metodo_pgto'):
        return jsonify({"error": "No pedido, falta o iid_metodo_pgto:"}), 400
    if not isinstance(novo.get('id_metodo_pgto'), int):
        return jsonify({"error" : "O retorno (id_metodo_pgto) não é do tipo dados necessário."}), 422
    
#validação apra ver se os ids para o pedido já foram cadastrados anteriormente
    doadores = ler_json("cad_doador.json")
    instituicoes = ler_json("cad_inst.json")
    produtos = ler_json("produtos.json")
    metodos = ler_json("metodo_pgto.json")

    ids_doadores = []
    for i in doadores:
        ids_doadores.append(i["id"])

    ids_instituicoes = []
    for i in instituicoes:
        ids_instituicoes.append(i["id"])

    ids_produtos = []
    for i in produtos:
        ids_produtos.append(i["id"])

    ids_metodos = []
    for i in metodos:
        ids_metodos.append(i["id"])

    if novo.get("id_doador") not in ids_doadores:
        return jsonify({"error": "id_doador não cadastrado."}), 422
    if novo.get("id_instituicao") not in ids_instituicoes:
        return jsonify({"error": "id_instituicao não cadastrado."}), 422
    if novo.get("id_produto") not in ids_produtos:
        return jsonify({"error": "id_produto não cadastrado."}), 422
    if novo.get("id_metodo_pgto") not in ids_metodos:
        return jsonify({"error": "id_metodo_pgto não cadastrado."}), 422
            
            
    

    
    ultimo_id = pedido[-1]["id"] if pedido else 0
    
    novo["id"] = ultimo_id + 1
    
    pedido.append(novo)
    salvar_json("cad_pedido.json", pedido)
    
    return jsonify(novo), 201

###############################################################################
#                         metodo pag


@app.route('/metodo_pgto', methods=["GET"])
def metodo_pgto():
   with open("metodo_pgto.json", "r", encoding="utf-8") as arquivo:
         metodo_pgto = json.load(arquivo)
         
   return jsonify(metodo_pgto)
  
app.run()




#metodo de pago, pix, deb, cred, boleto
#get para retornar as met de pago, depois um POST para confirmar o pag