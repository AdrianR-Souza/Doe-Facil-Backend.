novo = "matheus@gmail.com"
dominios_validos = ['@yahoo.com', '@gmail.com', '@hotmail.com', '@icloud.com']
dominio_user = "@" + novo.split("@")[1]
if dominio_user not in dominios_validos:
    print({"Email": "O retorno (email) não tem dominio válido."})
else:
    print("Email válido! dominio:", dominio_user)