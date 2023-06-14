
def start():
    return """
        Bem vindo ao sistema E-SIC Bot... \nSelecione uma das opções abaixo:
    /novo_pedido - Para fazer um novo pedido
    /consultar_pedido - Para consultar um pedido
    """
    
def novo_pedido_cidade():
    text = "Qual cidade?"
    cidades = ["Rio Branco", "Florianópolis"]
    return text, cidades


def novo_pedido_assunto():
    text = "Qual assunto?"
    assuntos = ["Saúde", "Educação", "Segurança", "Transporte"]
    return text, assuntos