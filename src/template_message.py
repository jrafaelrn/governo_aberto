from pedido import Pedido

def start():
    return """
    ℹ Bem vindo ao E-SIC Bot! \n
Selecione uma das opções abaixo:
➕ /novo_pedido - Para fazer um novo pedido
🔍 /consultar_pedidos - Para consultar um pedido
    """
    
def novo_pedido_cidade():
    text = "🏭 Qual cidade?"
    cidades = ["Rio Branco", "Florianópolis"]
    return {text: cidades}


def novo_pedido_assunto():
    text = "📚 Qual assunto?"
    assuntos = ["Saúde", "Educação", "Segurança", "Transporte"]
    return {text: assuntos}


def novo_pedido_descricao():
    text = "📄 Descreva o pedido:"
    return text


def novo_pedido_conclusao(cidade: str, assunto: str, descricao: str):
    text = f"""
    ✅ Novo pedido registrado com sucesso!\n
    Cidade: {cidade}
    Assunto: {assunto}
    Descrição: {descricao}\n
➕ /novo_pedido - Para fazer um novo pedido
🔍 /consultar_pedidos - Para consultar os pedidos realizados
    """
    return text


def retornar_pedidos(user):
    
    qtd_pedidos = user.get_qtd_pedidos()
        
    if qtd_pedidos == 0:
        return "Você não possui pedidos!\n➕ /novo_pedido - Para fazer um novo pedido"
        
    text = f"Você possui {qtd_pedidos} pedido(s)\n"    
    
    for pedido in user.pedidos:
        text += f"""
👉 ID: {pedido.id}
    Cidade: {pedido.city}
    Assunto: {pedido.subject}
    Descrição: {pedido.description}
    Status: {pedido.last_status}
        """
    return text


#####################################
#           NOTIFICAÇÕES            #
#####################################

tipos_notificacao = ['troca_responsavel', 'prazo_expirado', 'resposta', 'conclusao']

def gerar_notificacao(user):
    
    text = f'🔔 Atualização do seu pedido:'

    for pedido in user.pedidos:
        if pedido.last_notification != "conclusao":
            text += f'\n\n👉 ID: {pedido.id}\n'
            text += gerar_proximo_passo(pedido)
        
    return text
        

def gerar_proximo_passo (pedido: Pedido):
    
    if pedido.last_notification == None:
        pedido.last_notification = "troca_responsavel"
        pedido.last_status = f'⤴ Seu pedido foi enviado da Central E-SIC da Prefeitura de {pedido.city} para a Secretária de {pedido.subject} de {pedido.city}.\n\n⏰ O prazo de atendimento é de 4 minutos.'
    
    elif pedido.last_notification == "troca_responsavel":
        pedido.last_notification = "prazo_expirado"
        pedido.last_status = f'😬 O prazo para resposta do seu pedido expirou.\n Ele está sendo enviado para a Ouvidoria da Prefeitura de {pedido.city}.\n\n⏰ O prazo de atendimento é de 5 minutos.'
    
    elif pedido.last_notification == "prazo_expirado":
        pedido.last_notification = "resposta"
        pedido.last_status = f"""🎉 Sua solicitação foi respondida:
Os documentos solicitados podem ser encontrados no link: https://www.e-sic-bot.com.br/documentos/{pedido.id}
    """
    
    elif pedido.last_notification == "resposta":
        pedido.last_notification = "conclusao"
        pedido.last_status = f"""✅ Seu pedido foi concluído com sucesso!
Caso queira avaliar o atendimento, acesse o link: https://www.e-sic-bot.com.br/avaliacao/{pedido.id}

Para realizar um novo pedido, clique em: /novo_pedido"""
    
    return pedido.last_status