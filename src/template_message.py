
def start():
    return """
        Bem vindo ao sistema E-SIC Bot... \nSelecione uma das opções abaixo:
    /novo_pedido - Para fazer um novo pedido
    /consultar_pedido - Para consultar um pedido
    """
    
def novo_pedido_cidade():
    text = "Qual cidade?"
    cidades = ["Rio Branco", "Florianópolis"]
    return {text: cidades}


def novo_pedido_assunto():
    text = "Qual assunto?"
    assuntos = ["Saúde", "Educação", "Segurança", "Transporte"]
    return {text: assuntos}

def novo_pedido_descricao():
    text = "Descreva o pedido:"
    return text

def novo_pedido_conclusao(cidade: str, assunto: str, descricao: str):
    text = f"""
    Novo pedido registrado com sucesso!
    Cidade: {cidade}
    Assunto: {assunto}
    Descrição: {descricao}\n
    /novo_pedido - Para fazer um novo pedido
    /consultar_pedidos - Para consultar os pedidos realizados
    """
    return text


def retornar_pedidos(user):
    
    qtd_pedidos = user.get_qtd_pedidos()
        
    if qtd_pedidos == 0:
        return "Você não possui pedidos!\n/novo_pedido - Para fazer um novo pedido"
        
    text = f"Você possui {qtd_pedidos} pedidos\n"    
    text += "Pedidos:\n"
    for pedido in user.pedidos:
        text += f"""
        ID: {pedido.id}
        Cidade: {pedido.city}
        Assunto: {pedido.subject}
        Descrição: {pedido.description}\n
        """
    return text