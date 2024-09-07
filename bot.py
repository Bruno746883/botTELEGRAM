import requests
import time
import json
import os

class TelegramBot:
    def __init__(self):
        token = '7204871992:AAGpdDS1bBQK22FAnZxSIUIRPN2qcl1H7f4'
        self.url_base = f"https://api.telegram.org/bot{token}/"

    def Iniciar(self):
        update_id = None
        while True:
            try:
                atualizacao = self.obter_mensagens(update_id)
                if atualizacao and 'result' in atualizacao:
                    mensagens = atualizacao['result']
                    if mensagens:
                        for mensagem in mensagens:
                            update_id = mensagem['update_id']
                            chat_id = mensagem['message']['from']['id']
                            eh_primeira_mensagem = mensagem['message']['message_id'] == 1
                            resposta = self.criar_resposta(mensagem, eh_primeira_mensagem)
                            self.responder(resposta, chat_id)
            except Exception as e:
                print(f"Erro: {e}")
                time.sleep(5)

    def obter_mensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        if resultado.status_code == 200:
            return json.loads(resultado.content)
        return None

    def criar_resposta(self, mensagem, eh_primeira_mensagem):
        mensagem_texto = mensagem['message']['text']
        if eh_primeira_mensagem or mensagem_texto.lower() == 'menu':
            return f'''Olá, bem-vindo à nossa lanchonete! Digite o número do lanche que deseja pedir:{os.linesep}1 - X-Burguer{os.linesep}2 - X-Salada{os.linesep}3 - X-Tudo'''
        if mensagem_texto == '1':
            return f'X-Burguer pedido!{os.linesep}Deseja pedir mais alguma coisa?'
        if mensagem_texto == '2':
            return f'X-Salada pedido!{os.linesep}Deseja pedir mais alguma coisa?'
        if mensagem_texto == '3':
            return f'X-Tudo pedido!{os.linesep}Deseja pedir mais alguma coisa?'
        else:
            return 'Desculpe, não entendi. Gostaria de acessar o menu? Digite "menu".'

    def responder(self, resposta, chat_id):
        link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
        requests.get(link_de_envio)


bot = TelegramBot()
bot.Iniciar()
