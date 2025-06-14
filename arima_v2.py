# Core Python imports
import os
import sys
import json
import math
import random
import socket
import ssl
import signal
import time  # Added this line back
import threading
import traceback
import webbrowser
from collections import deque, OrderedDict
from datetime import datetime, timedelta
from functools import wraps, lru_cache
from threading import Lock
# Data processing & scientific libraries
import numpy as np
import pandas as pd
import talib
from numba import jit

# Async libraries
import asyncio
from asyncio import Semaphore
import aiohttp
import websocket

# HTTP & Networking
import requests
import urllib.request

# GUI & Media
import pygame
import dearpygui.dearpygui as dpg
from PIL import Image

# Windows specific
import pythoncom
import win32com.client

# Multiprocessing
import multiprocessing

# Logging
import logging

# Custom modules
from deriv_api_v2 import BinaryAPI
from language_manager import LanguageManager
from mt45receiver import MT4SignalReceiver
from checkUpdates import UpdateManager
from masaniello_api import MasanielloAPI
from dataclasses import dataclass
from telethon import TelegramClient, events
from telethon.tl.types import Channel, User
import asyncio
from datetime import datetime
from ml_strategy import initialize_strategies, get_ml_signal, trading_strategies
from telegram_interface import TelegramInterface
from telegram_signal_manager import TelegramSignalManager
from shared_state import set_order_in_progress
import shared_state
from abr import ABRStrategy




abr_strategy_active = False
SequenciaMinima = 7
SequenciaMaxima = 13
Winrate = 60
abr_strategy = ABRStrategy(min_sequence=SequenciaMinima, max_sequence=SequenciaMaxima, analysis_candles=400, min_success_rate=Winrate)

telegram_pending_signals = []
telegram_interface = None
telegram_manager = None
ml_strategy_active = False
last_symbol = None
cached_optimal_params = {}
last_optimization_times = {}
optimization_interval = 3600  # 1 hora em segundos
modo_gale = "normal"
default_expiration = 1
modo_entrada = "tempo_fixo"
fim_da_vela_time = "M1"
default_expiration = 1
hedge_active = False
alvoresete = False
gerenciamento_ativo = "Masaniello"  # Valor padrão
configuracoes_gerenciamentos = {}
modo_antiloss = "global"  # "global" ou "restrito"
pares_verificados_antiloss = {}  # {symbol: total_losses}
kicker_active = False
kicker_priority = True  # Se True, ignora outras confirmações quando Kicker está presente
pressao_compradora_min = 0.65  # valor padrão
pressao_vendedora_min = 0.65   # valor padrão
fluxo_active = False
antiloss_em_andamento = False
ultimo_resultado_antiloss = None
VerificaSeAntlossEstavaAtivo = False
price_action_active = False
volume_profile_active = False
ws_manager = None
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
style = "Normal"  # Valor padrão
stop_message_sent = False
websocket_semaphore = Semaphore(1)  # Permite uma operação WebSocket por vez
antiloss_ativado = False
required_losses = 2
ultimo_par_negociado = None
NumeroDeGales = 1
last_sample_run = 0
transactions = []  # Para a interface do bot
statistics_transactions = []  # Para as estatísticas
retracao_ativada = True  # Ou False, dependendo da configuração padrão desejada
telegram_ativado = False
should_send_orders = False
# Definir seu token do bot e chat ID
bot_token = "7631380155:AAFZ58yJE9hOXYX1dj3NWSO5RWBVLgKPzRs"
chat_id_value = ""
row_id = None  # Inicializa a variável row_id como None no escopo global
bot_running = False
ultima_vela_analisada = None
api_autorizada = False
lucro_total = 0.0  # Initialize to 0
api = None
gales = 0
volatilidade_selecionada = "Media"  # Valor padrão
velas_selecionadas = "20 Velas"  # Valor padrão
first_initialization = True
volume_atual = 0
em_espera = False  # Indica se o bot está esperando sair da zona de rompimento
tipo_ordem_anterior = None  # Para rastrear o tipo de ordem anterior (CALL ou PUT)
TOKEN_FILE = "token.json"  # Nome do arquivo onde o token será salvo
APP_ID = '35317'
URL = f"wss://ws.derivws.com/websockets/v3?app_id={APP_ID}"
api_token = None
cached_stake = None
ultimo_sinal = None  # Armazena o último sinal para controlar as novas entradas
filtro_rsi = True
reversao_value = False
retracao_value = False
max_repeticoes_loss = 3  # Número máximo de repetições após uma perda
repeticoes_atuais_loss = 0  # Contador de repetições atuais
usar_ticks = False  # Falso por padrão, usa segundos
websocket_client = None  # Initialize globally
tick_data = []
ultimo_tempo = None
tick_buffer = []
numero_ticks_para_sinal = 3
risco = 35.0  # Valor inicial padrão para o risco
total_operations = 12  # Valor inicial padrão para total de operações
wins = 3  # Valor inicial padrão para número de wins
payout = 1.94  # Valor inicial padrão para payout
min_entry = 0.35  # Valor inicial padrão para entrada mínima
tipo = 1  # Valor inicial padrão para tipo (1 = Normal, 0 = Progressivo)
style = "Normal"  # Valor inicial padrão para estilo (Normal ou Composto)
STOP_WIN = 500  # Example value for Stop Win (in dollars)
STOP_LOSS = 300  # Example value for Stop Loss (in dollars)
usar_ticks = False  # Sempre usa segundos
estrategia_atual = "Rise/Fall"  # Estratégia fixa
numero_confluencias = 1
VOLUME_COMPRA = 100
VOLUME_VENDA = 100
duracao_estrategia = 18
total_wins = 0
total_losses = 0
previous_num_transactions = 0
volatilidade_deque = deque(maxlen=000)
media_deque = deque(maxlen=100)
APOSTA_INICIAL = 1.0  # Valor padrão
FACTOR_GALE = 2.0  # Fator padrão de Martingale
RSI_ATIVADO = False
VOLUME_ATIVADO = False
operacao_real = False
is_running = False
is_shutting_down = False
stop_event = threading.Event()
estrategias_combinadas = 1  # Inicializando com o valor padrão, ajuste conforme necessário
ultima_chamada_velas = 0  # Variável global para armazenar o tempo da última chamada
velas = {}
dpg.create_context()
retracao = False
saldo_atual = 0  # Inicialize com 0 ou outro valor padrão
initial_balance = 0  # Inicialize também o saldo inicial
websocket_client = None
is_running = False
reconnect_delay = 5
max_reconnect_delay = 60
mt4_receiver = None  # No início do arquivo com outras variáveis globais
show_antiloss_rows = True  # Estado inicial - mostrar linhas de antiloss
is_maintenance = False

symbols = ["R_10", "R_25", "R_50", "R_75", "R_100", "1HZ10V", "1HZ25V",
           "1HZ50V", "1HZ75V", "1HZ100V" , "JD10" , "JD25" , "JD50" , "JD75" , "JD100",
          "stpRNG","stpRNG2","stpRNG3","stpRNG4","stpRNG5","RDBEAR","RDBULL"]


SYMBOL_DISPLAY_NAMES = {
    "RDBEAR": "Bear Market",
    "RDBULL": "Bull Market",


    "R_10": "Volatility 10",
    "R_25": "Volatility 25",
    "R_50": "Volatility 50",
    "R_75": "Volatility 75",
    "R_100": "Volatility 100",

    # Volatility Index (1s)
    "1HZ10V": "Volatility 10 (1s)",
    "1HZ25V": "Volatility 25 (1s)",
    "1HZ50V": "Volatility 50 (1s)",
    "1HZ75V": "Volatility 75 (1s)",
    "1HZ100V": "Volatility 100 (1s)",

    # Jump Indices
    "JD10": "Jump 10",
    "JD25": "Jump 25",
    "JD50": "Jump 50",
    "JD75": "Jump 75",
    "JD100": "Jump 100",

    # Step Index
    "stpRNG": "Step 100",
    "stpRNG2": "Step 200",
    "stpRNG3": "Step 300",
    "stpRNG4": "Step 400",
    "stpRNG5": "Step 500"
}

language_manager = LanguageManager()  # Cria a instância
CURRENT_VERSION = "3.52.7"

update_manager = UpdateManager(
    server_address=('45.230.238.11', 5544),
    current_version="3.52.7",
    language_manager=language_manager
)


def open_youtube_video():
    import webbrowser
    video_url = "https://t.me/Binaryelitevip"
    webbrowser.open(video_url)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bot_log.txt',  # Opcional: salva logs em um arquivo
    filemode='a'  # Anexa novos logs ao arquivo existente
)

parametros_globais = {
    "periodo_rsi": 14,
    "periodo_stoch": 14,
    "periodo_cci": 14,
    "bb_period": 22,
    "rsi_nivel_compra": 30,     # Aumentado de 30
    "rsi_nivel_venda": 70,      # Reduzido de 70
    "stoch_nivel_compra": 20,   # Aumentado de 20
    "stoch_nivel_venda": 80,    # Reduzido de 80
    "cci_nivel_compra": -100,    # Aumentado de -100
    "cci_nivel_venda": 100,      # Reduzido de 100
}

# Defina os pesos para os indicadores
pesos = {
    'rsi': 1.25,
    'macd': 1.25,
    'stoch': 1.15,
    'cci': 1.15,
    'bb': 1.25,
    'value_charts': 1.6,
    'fibo': 1.7,
    'momentum': 1.1,
    'adx': 1.2,
    'rvi': 1.2,
    'price_action': 1.6,
    'volume_profile': 1.8
}

def download_connector():
    import webbrowser
    video_url = "http://204.12.203.216:8000/Connectores.rar"
    webbrowser.open(video_url)


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def robust_execution(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            logging.debug(f"Starting execution of {func.__name__}")
            result = await func(*args, **kwargs)
            logging.debug(f"Execution of {func.__name__} completed successfully")
            return result
        except Exception as e:
            logging.error(f"Error in execution of {func.__name__}: {str(e)}")
            logging.error(traceback.format_exc())
            # Here you can implement additional recovery logic if needed
    return wrapper

def open_site():
    import webbrowser
    video_url = "https://t.me/Binaryelitevip"
    webbrowser.open(video_url)



def start_update_check_thread():
    """Inicia thread separada para verificar atualizações"""
    try:
        def check_updates():
            try:
                print("\n=== Verificando atualizações ===")
                asyncio.run(update_manager.verificar_atualizacoes())
            except Exception as e:
                print(f"Erro ao verificar atualizações: {e}")
                import traceback
                traceback.print_exc()

        # Inicia a verificação em uma thread separada
        update_thread = threading.Thread(
            target=check_updates,
            daemon=True,
            name="UpdateChecker"
        )
        update_thread.start()
        print("✅ Thread de verificação de atualizações iniciada")

    except Exception as e:
        print(f"❌ Erro ao iniciar thread de atualizações: {e}")
        import traceback
        traceback.print_exc()

async def enviar_mensagem_telegram(mensagem, chat_id_value, bot_token):
    global telegram_ativado

    if not telegram_ativado:
        print("Envio para Telegram desativado. Mensagem não enviada.")
        return

    if not chat_id_value or not bot_token:
        print("Erro: chat_id_value ou bot_token está vazio. Não é possível enviar a mensagem.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id_value,
        "text": mensagem
    }

    max_retries = 3
    retry_delay = 5  # segundos

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, data=data, timeout=10) as response:
                    if response.status == 200:
                        print("Mensagem enviada com sucesso para o Telegram!")
                        return
                    else:
                        text = await response.text()
                        print(f"Erro ao enviar mensagem. Status code: {response.status}")
                        print(f"Detalhes do erro: {text}")
        except Exception as e:
            print(f"Erro de conexão ao enviar mensagem para o Telegram: {e}")

        if attempt < max_retries - 1:
            print(f"Tentando novamente em {retry_delay} segundos...")
            await asyncio.sleep(retry_delay)

    print("Falha ao enviar mensagem após várias tentativas.")

def save_transactions():
    try:
        if not statistics_transactions:
            print("Nenhuma transação para salvar.")
            return True

        # Remove duplicatas usando Contract_ID
        unique_transactions = []
        seen_contracts = set()

        for transaction in statistics_transactions:
            contract_id = transaction.get('Contract_ID')
            if contract_id and contract_id not in seen_contracts:
                seen_contracts.add(contract_id)
                unique_transactions.append(transaction)

        # Salva em arquivo temporário
        temp_file = 'transactions_history.temp.json'
        with open(temp_file, 'w') as f:
            json.dump(unique_transactions, f, default=str, indent=2)

        # Move para arquivo final
        if os.path.exists('transactions_history.json'):
            os.replace('transactions_history.json', 'transactions_history.json.bak')
        os.replace(temp_file, 'transactions_history.json')

        print(f"\n=== Histórico salvo com sucesso ===")
        print(f"Total de transações únicas: {len(unique_transactions)}")
        print("=================================\n")

        return True

    except Exception as e:
        print(f"Erro ao salvar transações: {e}")
        traceback.print_exc()
        return False

def load_all_configurations():
   """Carrega todas as configurações do bot ao iniciar"""
   global masaniello, risco, total_operations, wins, payout, min_entry, tipo, style
   global numero_confluencias, simbolos_ativos, volatilidade_selecionada, velas_selecionadas
   global retracao_value, reversao_value, antiloss_ativado, required_losses
   global modo_entrada, default_expiration, fim_da_vela_time, modo_gale
   global hedge_active, alvoresete, kicker_active, kicker_priority
   global pressao_compradora_min, pressao_vendedora_min, fluxo_active
   global price_action_active, volume_profile_active, modo_antiloss
   global abr_strategy_active, SequenciaMinima, SequenciaMaxima, Winrate, STOP_WIN, STOP_LOSS, NumeroDeGales
   global ml_strategy_active

   try:
       print("\n=== Carregando todas as configurações ===")

       # Primeiro carrega o tipo de gerenciamento
       load_gerenciamento_tipo()

       config_dir = get_config_directory()
       config_file = os.path.join(config_dir, "bot_config.json")

       # Carrega o arquivo principal de configurações
       if os.path.exists(config_file):
           with open(config_file, 'r') as f:
               config = json.load(f)

           # Carrega configurações do Masaniello
           m_config = config.get('masaniello', {})
           risco = float(m_config.get('risco', 35.0))
           total_operations = int(m_config.get('total_operations', 12))
           wins = int(m_config.get('wins', 3))
           payout = float(m_config.get('payout', 1.94))
           min_entry = float(m_config.get('min_entry', 0.35))
           STOP_WIN = float(m_config.get('STOP_WIN', 500))
           STOP_LOSS = float(m_config.get('STOP_LOSS', 300))
           NumeroDeGales = int(m_config.get('NumeroDeGales', 1))
           tipo = int(m_config.get('tipo', 1))
           style = str(m_config.get('style', "Normal"))

           # Carrega configurações de estratégias
           e_config = config.get('estrategias', {})
           numero_confluencias = int(e_config.get('numero_confluencias', 1))
           simbolos_ativos.update(e_config.get('simbolos_ativos', {symbol: True for symbol in symbols}))
           volatilidade_selecionada = str(e_config.get('volatilidade_selecionada', "Media"))
           velas_selecionadas = str(e_config.get('velas_selecionadas', "20 Velas"))
           retracao_value = bool(e_config.get('retracao_value', False))
           reversao_value = bool(e_config.get('reversao_value', False))
           antiloss_ativado = bool(e_config.get('antiloss_ativado', False))
           required_losses = int(e_config.get('required_losses', 2))

           # Carrega configurações ABR Strategy
           abr_config = e_config.get('abr_strategy', {})
           abr_strategy_active = bool(abr_config.get('active', False))
           SequenciaMinima = int(abr_config.get('sequencia_minima', 7))
           SequenciaMaxima = int(abr_config.get('sequencia_maxima', 13))
           Winrate = int(abr_config.get('winrate', 60))

           # Carrega configurações de modo de entrada
           entrada_config = config.get('modo_entrada', {})
           print(f"\n🔍 DEBUG carregamento modo_entrada:")
           print(f"   entrada_config completo: {entrada_config}")
           
           modo_entrada = entrada_config.get('tipo', 'tempo_fixo')
           modo_gale = entrada_config.get('modo_gale', 'normal')
           
           expiracao_config = entrada_config.get('expiracao', {})
           print(f"   expiracao_config: {expiracao_config}")
           
           default_expiration = expiracao_config.get('tempo_fixo', 1)
           fim_da_vela_time = expiracao_config.get('fim_da_vela', 'M1')
           
           print(f"   CARREGADO - modo_entrada: '{modo_entrada}'")
           print(f"   CARREGADO - default_expiration: {default_expiration}")
           print(f"   CARREGADO - fim_da_vela_time: '{fim_da_vela_time}'")
           print(f"   CARREGADO - modo_gale: '{modo_gale}'")
           print(f"🔍 FIM DEBUG carregamento\n")

           # Carrega outras configurações de estratégias
           outras_config = config.get('outras_estrategias', {})
           hedge_active = bool(outras_config.get('hedge_active', False))
           alvoresete = bool(outras_config.get('alvoresete', False))
           kicker_active = bool(outras_config.get('kicker_active', False))
           kicker_priority = bool(outras_config.get('kicker_priority', True))
           pressao_compradora_min = float(outras_config.get('pressao_compradora_min', 0.65))
           pressao_vendedora_min = float(outras_config.get('pressao_vendedora_min', 0.65))
           fluxo_active = bool(outras_config.get('fluxo_active', False))
           price_action_active = bool(outras_config.get('price_action_active', False))
           volume_profile_active = bool(outras_config.get('volume_profile_active', False))
           modo_antiloss = str(outras_config.get('modo_antiloss', 'global'))
           ml_strategy_active = bool(outras_config.get('ml_strategy_active', False))

           # Inicializa o Masaniello com as configurações carregadas
           masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)

           print("\n=== Configurações carregadas com sucesso ===")
           print("\nMasaniello:")
           print(f"Risco: ${risco}")
           print(f"Total Operações: {total_operations}")
           print(f"Wins: {wins}")
           print(f"Payout: {payout}")
           print(f"Min Entry: ${min_entry}")
           print(f"Stop Win: ${STOP_WIN}")
           print(f"Stop Loss: ${STOP_LOSS}")
           print(f"Gales: {NumeroDeGales}")
           print(f"Tipo: {'Normal' if tipo == 1 else 'Progressivo'}")
           print(f"Style: {style}")

           print("\nEstratégias:")
           print(f"Confluências: {numero_confluencias}")
           print(f"Pares Ativos: {len([s for s, v in simbolos_ativos.items() if v])}")
           print(f"Volatilidade: {volatilidade_selecionada}")
           print(f"Velas: {velas_selecionadas}")
           print(f"Retração: {'Ativada' if retracao_value else 'Desativada'}")
           print(f"Reversão: {'Ativada' if reversao_value else 'Desativada'}")
           print(f"Antiloss: {'Ativado' if antiloss_ativado else 'Desativado'} ({required_losses} losses)")

           print("\nABR Strategy:")
           print(f"Ativo: {'Sim' if abr_strategy_active else 'Não'}")
           print(f"Sequência Mínima: {SequenciaMinima}")
           print(f"Sequência Máxima: {SequenciaMaxima}")
           print(f"Winrate: {Winrate}%")

           print("\nModo de Entrada:")
           print(f"Tipo: {modo_entrada}")
           print(f"Expiração Tempo Fixo: {default_expiration} minutos")
           print(f"Timeframe Fim da Vela: {fim_da_vela_time}")
           print(f"Modo Gale: {modo_gale}")

           print("\nOutras Estratégias:")
           print(f"Hedge: {'Ativo' if hedge_active else 'Inativo'}")
           print(f"Alvoresete: {'Ativo' if alvoresete else 'Inativo'}")
           print(f"Kicker: {'Ativo' if kicker_active else 'Inativo'}")
           print(f"Fluxo: {'Ativo' if fluxo_active else 'Inativo'}")
           print(f"Price Action: {'Ativo' if price_action_active else 'Inativo'}")
           print(f"Volume Profile: {'Ativo' if volume_profile_active else 'Inativo'}")
           print(f"ML Strategy: {'Ativo' if ml_strategy_active else 'Inativo'}")

       else:
           print("Arquivo de configurações não encontrado. Usando valores padrão")
           masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)

       # Carrega configurações do Telegram
       load_telegram_settings()

       # Atualiza a interface após carregar todas as configurações
       update_interface_after_load()

       print("\n=== Carregamento de configurações concluído ===")

   except Exception as e:
       print(f"Erro ao carregar configurações: {e}")
       import traceback
       traceback.print_exc()
       # Se houver erro, inicializa com valores padrão
       masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)

def load_transactions():
    """Carrega o histórico de transações com validação rigorosa"""
    global statistics_transactions, total_wins, total_losses, lucro_total, saldo_atual, initial_balance

    try:
        with open('transactions_history.json', 'r') as f:
            loaded_transactions = json.load(f)

        # Reseta os contadores antes de processar
        statistics_transactions = []
        total_wins = 0
        total_losses = 0
        lucro_total = 0

        # Conjunto para rastrear transações já processadas (evita duplicação)
        processed_transactions = set()

        for transaction in loaded_transactions:
            # Cria uma chave única para cada transação
            transaction_key = (
                str(transaction.get('Hora de Abertura', '')),
                transaction.get('Par', ''),
                str(transaction.get('W/L', '')),
                str(transaction.get('Profit', '')),
                str(transaction.get('Gales', 0))
            )

            # Verifica se a transação já foi processada
            if transaction_key in processed_transactions:
                print(f"Transação duplicada ignorada: {transaction}")
                continue

            processed_transactions.add(transaction_key)

            # Converte data se necessário
            if 'Hora de Abertura' in transaction:
                if isinstance(transaction['Hora de Abertura'], str):
                    transaction['Hora de Abertura'] = datetime.strptime(
                        transaction['Hora de Abertura'],
                        "%Y-%m-%d %H:%M:%S.%f"
                    )

            statistics_transactions.append(transaction)

            # Atualiza contadores apenas se W/L estiver definido
            if transaction.get('W/L') == 'Win':
                total_wins += 1
            elif transaction.get('W/L') == 'Loss':
                total_losses += 1

            try:
                lucro_total += float(transaction.get('Profit', 0))
            except (ValueError, TypeError):
                print(f"Erro ao processar lucro da transação: {transaction}")
                continue

        # Atualiza saldo inicial apenas se necessário
        if not initial_balance or initial_balance == 0:
            initial_balance = saldo_atual - lucro_total if saldo_atual else 0

        saldo_atual = initial_balance + lucro_total if initial_balance is not None else 0

        print(f"\n=== Transações Carregadas ===")
        print(f"Total de transações: {len(statistics_transactions)}")
        print(f"Total de vitórias: {total_wins}")
        print(f"Total de derrotas: {total_losses}")
        print(f"Lucro total: ${lucro_total:.2f}")
        print(f"Saldo atual: ${saldo_atual:.2f}")
        print("=============================\n")

        update_status()  # Atualiza interface

    except FileNotFoundError:
        print("Nenhum histórico de transações encontrado. Iniciando com lista vazia.")
        statistics_transactions = []
    except json.JSONDecodeError:
        print("Erro ao decodificar arquivo JSON. O arquivo pode estar corrompido.")
        statistics_transactions = []
    except Exception as e:
        print(f"Erro ao carregar transações: {e}")
        traceback.print_exc()
        statistics_transactions = []

def update_numero_confluencias(sender, app_data):
    global numero_confluencias
    novo_valor = int(app_data)
    if novo_valor != numero_confluencias:
        numero_confluencias = novo_valor
        print(f"Número de confluências atualizado para: {numero_confluencias}")
        save_configurations()  # Salva imediatamente quando o valor muda


def on_open(ws):
    print("WebSocket connection opened")
    asyncio.run(subscribe_to_all_symbols(ws))


async def start_websocket_async():
    global websocket_client, is_running
    try:
        websocket.enableTrace(False)
        ws = websocket.WebSocketApp(URL,
                                  on_open=on_open,
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
        websocket_client = ws
        is_running = True

        def run_forever_wrapper():
            try:
                ws.run_forever(
                    ping_interval=30,
                    ping_timeout=10,
                    sslopt={"cert_reqs": ssl.CERT_NONE}
                )
            except Exception as e:
                print(f"Erro no run_forever: {e}")

        # Executa o WebSocket em uma thread separada
        ws_thread = threading.Thread(target=run_forever_wrapper, daemon=True)
        ws_thread.start()

        # Aguarda a conexão ser estabelecida
        for _ in range(10):
            if websocket_client and websocket_client.sock and websocket_client.sock.connected:
                print("✅ WebSocket conectado com sucesso")
                await subscribe_to_all_symbols(websocket_client)
                break
            await asyncio.sleep(0.5)
        else:
            print("❌ Timeout ao aguardar conexão WebSocket")

    except Exception as e:
        print(f"❌ Erro ao iniciar WebSocket: {e}")
        if is_running:
            await reconnect_websocket()

async def subscribe_to_all_symbols(ws):
    """Inscreve em todos os símbolos para receber dados."""
    print("\n=== Iniciando Subscrições ===")
    for symbol in symbols:
        try:
            # Inscrição para ticks
            tick_request = {
                "ticks": symbol,
                "subscribe": 1
            }
            await send_websocket_request(ws, tick_request)
            print(f"✅ Inscrito nos ticks de {symbol}")

            # Inscrição para velas
            candle_request = {
                "ticks_history": symbol,
                "adjust_start_time": 1,
                "count": 600,
                "end": "latest",
                "start": 1,
                "style": "candles",
                "subscribe": 1
            }
            await send_websocket_request(ws, candle_request)
            print(f"✅ Inscrito nas velas de {symbol}")

            await asyncio.sleep(0.5)  # Pequena pausa entre subscrições

        except Exception as e:
            print(f"❌ Erro ao inscrever em {symbol}: {e}")


async def send_websocket_request(ws, request):
    """Envia requisição para o WebSocket."""
    try:
        await asyncio.get_event_loop().run_in_executor(
            None,
            ws.send,
            json.dumps(request)
        )
        print(f"📤 Requisição enviada: {request.get('ticks', request.get('ticks_history'))}")
    except Exception as e:
        print(f"❌ Erro ao enviar requisição: {e}")


def adicionar_nova_vela(candle, symbol):
    """Função síncrona para adicionar nova vela apenas para pares ativos"""
    global velas
    try:
        # Verifica se o símbolo está ativo
        if not simbolos_ativos.get(symbol, False):
            return False

        VELAS_MINIMAS = 500

        if symbol not in velas:
            velas[symbol] = deque(maxlen=600)

        vela_validada = {
            'open': float(candle['open']),
            'high': float(candle['high']),
            'low': float(candle['low']),
            'close': float(candle['close']),
            'epoch': float(candle['epoch'])
        }

        velas[symbol].append(vela_validada)

        total_velas = len(velas[symbol])
        if total_velas >= VELAS_MINIMAS:
            print(f"✅ {symbol}: {total_velas} velas disponíveis para análise")
        else:
            print(f"⚠️ {symbol}: Aguardando mais velas ({total_velas}/{VELAS_MINIMAS})")

        if abr_strategy_active and symbol in velas and len(velas[symbol]) > 0:
            abr_strategy.update_current_sequences(symbol, vela_validada)

        return True

    except Exception as e:
        print(f"Erro ao adicionar nova vela para {symbol}: {e}")
        return False



def on_message(ws, message):
    global last_candle_update
    try:
        if not message:
            print("Mensagem vazia recebida")
            return

        data = json.loads(message)

        # Processa heartbeat/ping
        if "ping" in data:
            ws.send(json.dumps({"pong": data["ping"]}))
            return

        if 'ohlc' in data:
            candle = data['ohlc']
            symbol = candle.get('symbol')
            if symbol in symbols:
                epoch = float(candle['epoch'])
                timeframe = default_expiration * 60
                granularity = timeframe

                # Verifica se é uma nova vela baseado na granularidade
                if epoch % granularity == 0:
                    print(f"\n=== Nova vela fechada de {granularity}s para {symbol} ===")
                    # Esta é uma vela fechada, podemos adicionar e atualizar ABR
                    adicionar_nova_vela(candle, symbol)
                else:
                    # Esta é uma vela em andamento, apenas atualizamos sem afetar ABR
                    atualizar_vela_atual(candle, symbol)

    except json.JSONDecodeError:
        print("Erro ao decodificar mensagem JSON")
    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
        if "close frame received" in str(e).lower():
            threading.Thread(target=lambda: asyncio.run(reconnect_websocket()), daemon=True).start()


def atualizar_vela_atual(candle, symbol):
    """Função síncrona para atualizar a vela atual"""
    global velas
    try:
        if symbol not in velas or len(velas[symbol]) == 0:
            return

        vela_atual = velas[symbol][-1]
        epoch_atual = float(candle['epoch'])

        # Se ainda estamos na mesma vela (mesmo minuto)
        if epoch_atual - float(vela_atual['epoch']) < 60:
            vela_atual.update({
                'high': max(float(candle['high']), float(vela_atual['high'])),
                'low': min(float(candle['low']), float(vela_atual['low'])),
                'close': float(candle['close'])
            })

    except Exception as e:
        print(f"Erro ao atualizar vela atual para {symbol}: {e}")


def show_velas_error_popup():
    """Shows loading status popup with real-time updates and friendly names"""
    if dpg.does_item_exist("velas_error_popup"):
        dpg.delete_item("velas_error_popup")

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    window_width = 400
    window_height = 300
    pos_x = (viewport_width - window_width) // 2
    pos_y = (viewport_height - window_height) // 2

    with dpg.window(label="JANELA CARREGAMENTO", modal=True, no_close=True,
                    tag="velas_error_popup", width=window_width, height=window_height,
                    pos=[pos_x, pos_y]):
        dpg.add_text("Iniciando Carregamento De Velas!", color=(255, 0, 0))
        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_text("Status do carregamento:", color=(255, 215, 0))

        # Create status indicators with friendly names and timeframes
        with dpg.group(tag="status_group"):
            for symbol in symbols:
                # Define o timeframe para exibição
                timeframe_display = "M15" if symbol.startswith("stpRNG") else f"M{default_expiration}"
                friendly_name = f"{get_display_name(symbol)} ({timeframe_display})"
                dpg.add_text(f"{friendly_name}: Aguardando...", tag=f"status_{symbol}", color=(255, 255, 255))

        dpg.add_separator()
        dpg.add_text("Janela Fecha Automatica Ao Carregar!", color=(255, 0, 0))


async def update_symbol_status(symbol, status, color=(0, 255, 0)):
    """Updates the status for a specific symbol with friendly name"""
    if dpg.does_item_exist(f"status_{symbol}"):
        friendly_name = get_display_name(symbol)
        dpg.set_value(f"status_{symbol}", f"{friendly_name}: {status}")
        dpg.configure_item(f"status_{symbol}", color=color)


async def inicializar_velas():
    """Inicializa velas com verificação adequada e status em tempo real usando nomes amigáveis"""
    global velas

    try:
        print("\n=== Iniciando Inicialização de Velas ===")
        velas = {}
        show_velas_error_popup()

        for symbol in symbols:
            # Define o timeframe e seu display name
            timeframe =  default_expiration * 60
            timeframe_display = "M15" if symbol.startswith("stpRNG") else f"M{default_expiration}"

            if not simbolos_ativos.get(symbol, True):
                friendly_name = f"{get_display_name(symbol)} ({timeframe_display})"
                await update_symbol_status(symbol, "Desativado", (150, 150, 150))
                print(f"{friendly_name}: Desativado")
                continue

            await update_symbol_status(symbol, "Loading...", (255, 165, 0))
            friendly_name = f"{get_display_name(symbol)} ({timeframe_display})"
            print(f"Carregando {friendly_name}...")

            try:
                candles = await api.ticks_history({
                    "ticks_history": symbol,
                    "end": "latest",
                    "start": 1,
                    "count": 600,
                    "style": "candles",
                    "granularity": timeframe
                })

                if 'candles' in candles:
                    velas[symbol] = deque(candles['candles'], maxlen=600)
                    if len(velas[symbol]) >= 600:
                        await update_symbol_status(symbol, "Sucess Ok", (0, 255, 0))
                        print(f"{friendly_name}: Carregado com sucesso")
                    else:
                        await update_symbol_status(symbol, f"Insuficiente ({len(velas[symbol])}/600)", (255, 0, 0))
                        print(f"{friendly_name}: Dados insuficientes")
                        return False
                else:
                    await update_symbol_status(symbol, "Falha ao carregar", (255, 0, 0))
                    print(f"{friendly_name}: Falha ao carregar dados")
                    return False

            except Exception as e:
                await update_symbol_status(symbol, f"Erro: {str(e)}", (255, 0, 0))
                print(f"{friendly_name}: Erro - {str(e)}")
                return False

            await asyncio.sleep(0.5)

        await asyncio.sleep(1)
        if dpg.does_item_exist("velas_error_popup"):
            dpg.delete_item("velas_error_popup")

        print("✅ Inicialização concluída com sucesso")
        return True

    except Exception as e:
        print(f"❌ Erro na inicialização de velas: {e}")
        return False


async def robust_connect_api(max_retries=3, base_delay=2):
    """Tenta conectar à API com retry exponencial"""
    global api, api_token

    for attempt in range(max_retries):
        try:
            print(f"\n=== Tentativa de conexão {attempt + 1}/{max_retries} ===")

            # Limpa conexão anterior se existir
            if api:
                try:
                    await api.logout()
                    await asyncio.sleep(1)
                except:
                    pass
                api = None

            # Verifica token
            if not api_token:
                print("Token não fornecido")
                return None

            # Cria nova instância da API
            api = BinaryAPI(api_token)

            # Tenta iniciar (sem await pois não é assíncrono)
            status, message = api.start()

            if status:
                print("✅ API conectada com sucesso")

                # Verifica se pode obter saldo como teste
                try:
                    async with asyncio.timeout(10):
                        balance = api.get_balance()
                        if balance is not None:
                            print(f"✅ Conexão verificada com sucesso (Saldo: ${float(balance):.2f})")
                            return api
                        else:
                            print("❌ Não foi possível obter saldo")
                            continue
                except asyncio.TimeoutError:
                    print("⚠️ Timeout ao verificar saldo")
                    continue
                except Exception as e:
                    print(f"❌ Erro ao verificar saldo: {e}")
                    continue
            else:
                print(f"❌ Falha na conexão: {message}")
                continue

        except websocket.WebSocketConnectionClosedException:
            print("⚠️ Conexão WebSocket fechada prematuramente")
        except Exception as e:
            print(f"❌ Erro na conexão: {e}")
            import traceback
            traceback.print_exc()

        # Calcula delay exponencial
        delay = base_delay * (2 ** attempt)
        print(f"Aguardando {delay}s antes da próxima tentativa...")
        await asyncio.sleep(delay)

    print("❌ Todas as tentativas de conexão falharam")
    return None


async def verify_api_connection(api_instance, timeout=10):
    """Verifica se a conexão com a API está funcionando"""
    try:
        start_time = time.time()

        # Tenta obter saldo
        balance = api_instance.get_balance()
        if balance is not None:
            print(f"✅ Saldo obtido: ${float(balance):.2f}")
            print(f"⚡ Tempo de resposta: {(time.time() - start_time) * 1000:.0f}ms")
            return True

        print("❌ Não foi possível obter saldo")
        return False

    except Exception as e:
        print(f"❌ Erro ao verificar conexão: {e}")
        return False


async def inicializar_api():
    global api, api_autorizada, api_token

    try:
        if not api_autorizada:
            print("\n=== Inicializando conexão com API ===")

            # Verifica configurações de rede
            if not update_manager.check_network_config():
                update_manager.show_network_error_popup()

            # Tenta conexão robusta
            api = await robust_connect_api()
            if not api:
                print("❌ Falha ao conectar com API")
                return None

            # Verifica conexão
            if not await verify_api_connection(api):
                print("❌ Falha na verificação de conexão")
                return None

            api_autorizada = True
            print("\n=== Conexão estabelecida ===")

            # Atualiza saldo inicial
            saldo = await atualizar_saldo(api)
            if saldo is not None:
                print(f"💰 Saldo inicial: ${saldo:.2f}")
                return api
            else:
                print("❌ Falha ao obter saldo inicial")
                return None

        return api

    except Exception as e:
        print(f"❌ Erro ao inicializar API: {e}")
        import traceback
        traceback.print_exc()
        return None




async def cleanup_connections():
    global api, websocket_client

    if api:
        try:
            await api.logout()
        except:
            pass
        api = None

    if websocket_client:
        try:
            await websocket_client.close()
        except:
            pass
        websocket_client = None




async def verificar_api_autorizada():
    """Função auxiliar para verificar se a API está autorizada"""
    global api, api_autorizada

    if not api or not api_autorizada:
        api = await inicializar_api()
        if not api:
            print("Falha ao reconectar com a API")
            return False
    return True



async def enviar_sticker_telegram(sticker_id, chat_id_value, bot_token):
    if not telegram_ativado:
        print("Envio para Telegram desativado. Mensagem não enviada.")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendSticker"
    data = {
        "chat_id": chat_id_value,
        "sticker": sticker_id
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    print("Sticker enviado com sucesso para o Telegram!")
                else:
                    text = await response.text()
                    print(f"Erro ao enviar sticker. Status code: {response.status}")
                    print(f"Detalhes do erro: {text}")
    except Exception as e:
        print(f"Erro ao enviar sticker para o Telegram: {e}")


def main():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


def controlar_seletor_ativo(ativo):
    if ativo:
        dpg.enable_item("token_mode")  # Ativa o seletor Demo/Real
    else:
        dpg.disable_item("token_mode")  # Desativa o seletor Demo/Real


@jit(nopython=True)
def calcular_atr(high, low, close, periodo=14):
    """
    Calcula o ATR otimizado com numba
    """
    if len(high) <= periodo:
        return 0.0

    tr = np.zeros(len(high) - 1, dtype=np.float64)
    for i in range(1, len(high)):
        hl = high[i] - low[i]
        hc = abs(high[i] - close[i - 1])
        lc = abs(low[i] - close[i - 1])
        tr[i - 1] = max(hl, hc, lc)

    return np.mean(tr[-periodo:])


async def filtrar_volatilidade(api, symbol, sinal, volatilidade_valor, num_velas):
    """Filtro de volatilidade aprimorado"""
    try:
        timeframe =  default_expiration * 60
        candles = await api.ticks_history({
            "ticks_history": symbol,
            "end": "latest",
            "start": 1,
            "style": "candles",
            "granularity": timeframe,
            "count": num_velas
        })

        if 'candles' not in candles or len(candles['candles']) < num_velas:
            print(f"❌ Dados insuficientes para {symbol}")
            return None

        # Convertendo dados
        highs = np.array([float(candle['high']) for candle in candles['candles']])
        lows = np.array([float(candle['low']) for candle in candles['candles']])
        closes = np.array([float(candle['close']) for candle in candles['candles']])

        # 1. Cálculo de ATR
        atr = calcular_atr(highs, lows, closes)
        atr_percentual = atr / closes[-1]

        # 2. Análise de Gaps
        gaps = np.abs(closes[1:] - closes[:-1]) / closes[:-1]
        gaps_anormais = np.sum(gaps > 0.005)  # Gaps > 0.5%

        # 3. Análise de Momentum
        roc = talib.ROC(closes, timeperiod=10)
        momentum_forte = abs(roc[-1]) > 2.0  # Movimento > 2%

        # 4. Consistência de Movimento
        direcao_consistente = True
        if sinal == "CALL":
            direcao_consistente = closes[-1] > closes[-2] > closes[-3]
        elif sinal == "PUT":
            direcao_consistente = closes[-1] < closes[-2] < closes[-3]

        # Decisão baseada em múltiplos fatores
        volatilidade_adequada = True

        # Verifica volatilidade excessiva
        if atr_percentual > 0.015:  # > 1.5%
            print(f"❌ {symbol}: Volatilidade muito alta (ATR: {atr_percentual:.4f})")
            volatilidade_adequada = False

        # Verifica gaps anormais
        if gaps_anormais > 2:
            print(f"❌ {symbol}: Muitos gaps anormais ({gaps_anormais})")
            volatilidade_adequada = False

        # Verifica momentum excessivo
        if momentum_forte and not direcao_consistente:
            print(f"❌ {symbol}: Momentum forte sem consistência")
            volatilidade_adequada = False

        if volatilidade_adequada:
            print(f"✅ {symbol}: Volatilidade adequada para operação")
            print(f"ATR%: {atr_percentual:.4f}")
            print(f"Gaps anormais: {gaps_anormais}")
            print(f"Momentum: {'Forte' if momentum_forte else 'Normal'}")
            print(f"Direção consistente: {'Sim' if direcao_consistente else 'Não'}")
            return sinal

        return None

    except Exception as e:
        print(f"❌ Erro ao filtrar volatilidade para {symbol}: {e}")
        return None



def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end-start:.2f} seconds")
        return result
    return wrapper

@measure_time
async def analisar_estrategias_e_filtros(api, symbols, tick_data, volume_atual, estrategias_combinadas):
    """
    Analisa estratégias continuamente, independente do tempo de execução
    """
    global parametros_globais, velas, tipo_ordem_anterior, numero_confluencias, stop_event

    if stop_event.is_set():
        print("Robô foi parado. Cancelando análise.")
        return {}

    resultados = {}
    VELAS_MINIMAS = 500

    async def processar_symbol(symbol):
        try:
            # Primeiro verifica se o símbolo está ativo
            if not simbolos_ativos.get(symbol, False):
                print(f"❌ {symbol}: Par desativado - ignorando análise")
                return symbol, None

            # Só então tenta acessar os dados das velas
            if symbol not in velas or len(velas[symbol]) < VELAS_MINIMAS:
                print(f"❌ {symbol}: Quantidade insuficiente de velas ({len(velas.get(symbol, []))}/{VELAS_MINIMAS})")
                return symbol, None

            # Realizar análise contínua independente do tempo
            indicadores = await analisar_symbol(symbol, velas[symbol], parametros_globais)
            if indicadores:
                # Define threshold baseado no número de confluências requerido
                threshold = numero_confluencias * 1.35
                sinal = analisar_sinal(indicadores, pesos, threshold)

                print(f"\n=== Análise Contínua {symbol} ===")
                print(f"RSI: {indicadores['rsi']:.2f}")
                print(f"MACD: {indicadores.get('macd', 0):.6f}")
                if sinal:
                    print(f"✅ Sinal detectado: {sinal}")
                    return symbol, sinal
                else:
                    print("ℹ️ Nenhum sinal válido no momento")

        except Exception as exc:
            print(f'❌ {symbol} gerou uma exceção: {exc}')
            traceback.print_exc()
        return symbol, None

    # Processa todos os símbolos continuamente
    tarefas = [processar_symbol(symbol) for symbol in symbols]
    resultados_processados = await asyncio.gather(*tarefas)

    for symbol, sinal in resultados_processados:
        if sinal:
            resultados[symbol] = sinal

    return resultados




@robust_execution
async def analisar_symbol(symbol, velas_symbol, parametros):
   """
   Análise completa incluindo detecção de manipulação, qualidade de mercado e todos indicadores
   """
   try:
       # Inicializa dicionário de indicadores
       indicadores = {}

       # Validação inicial
       if len(velas_symbol) < 600:
           print(f"❌ {symbol}: Quantidade insuficiente de velas ({len(velas_symbol)}/600)")
           return None

       # Validação de temporalidade
       ultima_vela = velas_symbol[-1]
       tempo_atual = datetime.now().timestamp()

       # Converte dados para arrays numpy com proteção - MOVIDO PARA O INÍCIO
       try:
           closes = np.array([float(vela['close']) for vela in velas_symbol], dtype=np.float64)
           highs = np.array([float(vela['high']) for vela in velas_symbol], dtype=np.float64)
           lows = np.array([float(vela['low']) for vela in velas_symbol], dtype=np.float64)
           opens = np.array([float(vela['open']) for vela in velas_symbol], dtype=np.float64)
       except (ValueError, TypeError) as e:
           print(f"❌ {symbol}: Erro na conversão de dados: {e}")
           return None

       # Análise de Manipulação
       range_values = highs - lows

       # Adiciona proteção contra divisão por zero
       mask = range_values != 0
       wicks_superiores = np.zeros_like(range_values)
       wicks_inferiores = np.zeros_like(range_values)

       # Calcula apenas onde range_values não é zero
       wicks_superiores[mask] = (highs[mask] - np.maximum(opens[mask], closes[mask])) / range_values[mask]
       wicks_inferiores[mask] = (np.minimum(opens[mask], closes[mask]) - lows[mask]) / range_values[mask]

       # Calcula a média das diferenças de forma segura
       wick_ratio = np.mean(np.abs(wicks_superiores - wicks_inferiores))

       # === ANÁLISE DE QUALIDADE DE MERCADO ===
       market_quality = 1.0
       mensagens_qualidade = []

       # 1. Análise de Volatilidade (ATR)
       atr = talib.ATR(highs, lows, closes, timeperiod=8)[-1]
       volatilidade = atr / np.mean(closes)
       if volatilidade > 0.003:
           market_quality *= 0.8
           mensagens_qualidade.append("Alta volatilidade")

       # 2. Verificação de Gaps
       gaps = np.abs(closes[1:] - closes[:-1]) / closes[:-1]
       gaps_anormais = np.sum(gaps > 0.003)
       if gaps_anormais > 2:
           market_quality *= 0.85
           mensagens_qualidade.append(f"Gaps anormais: {gaps_anormais}")

       # 3. Análise de Manipulação
       range_values = highs - lows
       wicks_superiores = np.where(range_values != 0, (highs - np.maximum(opens, closes)) / range_values, 0)
       wicks_inferiores = np.where(range_values != 0, (np.minimum(opens, closes) - lows) / range_values, 0)
       wick_ratio = np.mean(np.abs(wicks_superiores - wicks_inferiores))
       if wick_ratio > 0.6:
           market_quality *= 0.9
           mensagens_qualidade.append("Possível manipulação")

       # 4. Consistência de Movimento
       direcoes = np.sign(np.diff(closes))
       reversoes_bruscas = np.sum(np.abs(np.diff(direcoes))) / len(direcoes)
       if reversoes_bruscas > 0.5:
           market_quality *= 0.9
           mensagens_qualidade.append("Movimento errático")

       # 5. Força da Tendência
       ema_curta = talib.EMA(closes, timeperiod=8)
       ema_longa = talib.EMA(closes, timeperiod=21)
       tendencia_force = abs(ema_curta[-1] - ema_longa[-1]) / ema_longa[-1]

       # === CÁLCULO DE INDICADORES TÉCNICOS ===
       preco_atual = float(ultima_vela['close'])

       # RSI
       rsi = talib.RSI(closes, timeperiod=14)
       rsi_nivel_compra = parametros.get('rsi_nivel_compra', 30)
       rsi_nivel_venda = parametros.get('rsi_nivel_venda', 70)

       # MACD
       macd, signal, hist = talib.MACD(closes, fastperiod=12, slowperiod=26, signalperiod=9)
       macd_strength = abs(macd[-1] - signal[-1]) / preco_atual

       # Bollinger Bands
       upper, middle, lower = talib.BBANDS(closes, timeperiod=20, nbdevup=2, nbdevdn=2)

       # Stochastic
       stoch_k, stoch_d = talib.STOCH(highs, lows, closes,
                                     fastk_period=14,
                                     slowk_period=3,
                                     slowd_period=3)

       # ADX e DMI
       adx = talib.ADX(highs, lows, closes, timeperiod=14)
       plus_di = talib.PLUS_DI(highs, lows, closes, timeperiod=14)
       minus_di = talib.MINUS_DI(highs, lows, closes, timeperiod=14)

       # CCI
       cci = talib.CCI(highs, lows, closes, timeperiod=14)

       # Verifica se todos os indicadores foram calculados
       if any(x is None for x in [rsi, macd, signal, stoch_k, stoch_d, adx, plus_di, minus_di, cci]):
           print(f"❌ {symbol}: Falha no cálculo de indicadores")
           return None

       # Sistema de Confluências com pesos ajustados pela qualidade
       confluences = {
           'rsi': {
               'bullish': rsi[-1] < rsi_nivel_compra,
               'bearish': rsi[-1] > rsi_nivel_venda,
               'weight': 1.3 * market_quality
           },
           'macd': {
               'bullish': macd[-1] > signal[-1] and macd_strength > 0.001,
               'bearish': macd[-1] < signal[-1] and macd_strength > 0.001,
               'weight': 1.2 * market_quality
           },
           'bollinger': {
               'bullish': preco_atual < lower[-1],
               'bearish': preco_atual > upper[-1],
               'weight': 1.1 * market_quality
           },
           'stochastic': {
               'bullish': stoch_k[-1] < 20 and stoch_d[-1] < 20 and stoch_k[-1] > stoch_d[-1],
               'bearish': stoch_k[-1] > 80 and stoch_d[-1] > 80 and stoch_k[-1] < stoch_d[-1],
               'weight': 1.2 * market_quality
           },
           'adx_dmi': {
               'bullish': adx[-1] > 25 and plus_di[-1] > minus_di[-1],
               'bearish': adx[-1] > 25 and plus_di[-1] < minus_di[-1],
               'weight': 1.3 * market_quality
           },
           'cci': {
               'bullish': cci[-1] < -100,
               'bearish': cci[-1] > 100,
               'weight': 1.1 * market_quality
           }
       }

       # Consolida todos os indicadores
       indicadores = {
           'rsi': rsi[-1],
           'macd': macd[-1],
           'signal': signal[-1],
           'stoch_k': stoch_k[-1],
           'stoch_d': stoch_d[-1],
           'cci': cci[-1],
           'preco_atual': preco_atual,
           'banda_superior': upper[-1],
           'banda_inferior': lower[-1],
           'banda_media': middle[-1],
           'adx': adx[-1],
           'plus_di': plus_di[-1],
           'minus_di': minus_di[-1],
           'market_quality': market_quality,
           'qualidade_mensagens': mensagens_qualidade,
           'atr': atr,
           'volatilidade': volatilidade,
           'confluences': confluences
       }

       # Log detalhado
       print(f"\n=== Análise Completa para {symbol} ===")
       print(f"Qualidade do Mercado: {market_quality:.2f}")
       if mensagens_qualidade:
           print("Alertas:", ", ".join(mensagens_qualidade))
       print(f"Preço Atual: {preco_atual:.5f}")
       print(f"RSI: {rsi[-1]:.2f}")
       print(f"MACD: {macd[-1]:.6f} Signal: {signal[-1]:.6f}")
       print(f"Stochastic K/D: {stoch_k[-1]:.2f}/{stoch_d[-1]:.2f}")
       print(f"ADX: {adx[-1]:.2f} +DI: {plus_di[-1]:.2f} -DI: {minus_di[-1]:.2f}")
       print("=======================================")

       return indicadores

   except Exception as e:
       print(f"❌ Erro ao analisar {symbol}: {e}")
       import traceback
       traceback.print_exc()
       return None



def analisar_sinal(indicadores, pesos, threshold):
    """
    Análise completa de sinais incluindo todas as estratégias
    """
    try:
        print("\n=== Iniciando Análise de Sinais ===")
        print(f"Número de confluências necessárias: {numero_confluencias}")
        print(f"Threshold base: {threshold:.2f}")

        # Validação inicial
        if not indicadores or indicadores.get('market_quality', 1.2) < 0.6:
            print("❌ Qualidade de mercado insuficiente")
            return None

        score_compra = 0
        score_venda = 0
        confluencias_compra = 0
        confluencias_venda = 0
        debug_info = []

        # Análise das confluências dos indicadores
        for indicator, data in indicadores['confluences'].items():
            if data['bullish']:
                score_compra += data['weight']
                confluencias_compra += 1
            elif data['bearish']:
                score_venda += data['weight']
                confluencias_venda += 1

        # 1. RSI
        if all(k in indicadores for k in ['rsi', 'rsi_nivel_compra', 'rsi_nivel_venda']):
            rsi = indicadores['rsi']
            rsi_nivel_compra = indicadores['rsi_nivel_compra']
            rsi_nivel_venda = indicadores['rsi_nivel_venda']

            rsi_strength = abs(50 - rsi) / 50
            peso_rsi = pesos['rsi'] * (1 + rsi_strength)

            if rsi < rsi_nivel_compra:
                score_compra += peso_rsi
                confluencias_compra += 1
                debug_info.append(f"RSI: Compra ({rsi:.2f} < {rsi_nivel_compra}) | Peso: {peso_rsi:.2f}")
            elif rsi > rsi_nivel_venda:
                score_venda += peso_rsi
                confluencias_venda += 1
                debug_info.append(f"RSI: Venda ({rsi:.2f} > {rsi_nivel_venda}) | Peso: {peso_rsi:.2f}")

        # 2. MACD
        if all(k in indicadores for k in ['macd', 'linha_sinal']):
            macd = indicadores['macd']
            signal = indicadores['linha_sinal']
            macd_diff = macd - signal

            macd_strength = abs(macd_diff / signal) if signal != 0 else 0
            peso_macd = pesos['macd'] * (1 + min(macd_strength, 1.0))

            if macd_diff > 0:
                score_compra += peso_macd
                confluencias_compra += 1
                debug_info.append(f"MACD: Compra (diff: {macd_diff:.4f}) | Peso: {peso_macd:.2f}")
            elif macd_diff < 0:
                score_venda += peso_macd
                confluencias_venda += 1
                debug_info.append(f"MACD: Venda (diff: {macd_diff:.4f}) | Peso: {peso_macd:.2f}")

        # 3. Bollinger Bands
        if all(k in indicadores for k in ['preco_atual', 'banda_inferior', 'banda_superior']):
            preco = indicadores['preco_atual']
            bb_inf = indicadores['banda_inferior']
            bb_sup = indicadores['banda_superior']

            bb_peso = pesos['bb']

            dist_inf = (preco - bb_inf) / bb_inf if bb_inf != 0 else 0
            dist_sup = (bb_sup - preco) / preco if preco != 0 else 0

            if preco < bb_inf:
                peso_bb = bb_peso * (1 + abs(dist_inf))
                score_compra += peso_bb
                confluencias_compra += 1
                debug_info.append(f"BB: Compra ({preco:.4f} < {bb_inf:.4f}) | Peso: {peso_bb:.2f}")
            elif preco > bb_sup:
                peso_bb = bb_peso * (1 + abs(dist_sup))
                score_venda += peso_bb
                confluencias_venda += 1
                debug_info.append(f"BB: Venda ({preco:.4f} > {bb_sup:.4f}) | Peso: {peso_bb:.2f}")

        # 4. Value Charts Dinâmico
        if 'value_charts' in indicadores:
            vc_value = indicadores['value_charts']
            vc_peso = pesos.get('value_charts', 1.6)

            if 'atr' in indicadores:
                atr_atual = indicadores['atr']
                nivel_vc = ajustar_nivel_value_charts(atr_atual)
            else:
                nivel_vc = 9.2

            if vc_value < -nivel_vc:
                vc_score = vc_peso * (1 + abs(vc_value / nivel_vc))
                score_compra += vc_score
                confluencias_compra += 1
                debug_info.append(f"Value Charts: Compra ({vc_value:.2f}) | Peso: {vc_score:.2f}")
            elif vc_value > nivel_vc:
                vc_score = vc_peso * (1 + abs(vc_value / nivel_vc))
                score_venda += vc_score
                confluencias_venda += 1
                debug_info.append(f"Value Charts: Venda ({vc_value:.2f}) | Peso: {vc_score:.2f}")

        # 5. Análise Fibonacci
        if 'fibo_levels' in indicadores:
            fibo_levels = indicadores['fibo_levels']
            fibo_peso = pesos.get('fibo', 1.6)
            preco_atual = indicadores['preco_atual']

            if fibo_levels['trend'] == 'up':
                # Análise para tendência de alta
                if preco_atual <= fibo_levels['fibo_23_6']:
                    fibo_score = fibo_peso * 1.5
                    score_compra += fibo_score
                    confluencias_compra += 1
                    debug_info.append(f"Fibonacci: Forte Compra - 23.6% | Peso: {fibo_score:.2f}")
                elif fibo_levels['fibo_38_2'] <= preco_atual <= fibo_levels['fibo_50']:
                    fibo_score = fibo_peso * 1.1
                    score_compra += fibo_score
                    confluencias_compra += 1
                    debug_info.append(f"Fibonacci: Compra Moderada - 38.2-50% | Peso: {fibo_score:.2f}")
            else:  # Tendência de baixa
                if preco_atual >= fibo_levels['fibo_78_6']:
                    fibo_score = fibo_peso * 1.5
                    score_venda += fibo_score
                    confluencias_venda += 1
                    debug_info.append(f"Fibonacci: Forte Venda - 78.6% | Peso: {fibo_score:.2f}")
                elif fibo_levels['fibo_50'] <= preco_atual <= fibo_levels['fibo_61_8']:
                    fibo_score = fibo_peso * 1.2
                    score_venda += fibo_score
                    confluencias_venda += 1
                    debug_info.append(f"Fibonacci: Venda Moderada - 50-61.8% | Peso: {fibo_score:.2f}")

        # 6. Volume Profile (se ativado)
        if 'volume_profile' in indicadores:
            vp_data = indicadores.get('volume_profile')
            if vp_data and vp_data.get('dentro_value_area'):
                vp_peso = pesos.get('volume_profile', 1.8)

                if vp_data['tendencia'] == 'up' and vp_data['pressao_compradora'] > 0.6:
                    score_compra += vp_peso
                    confluencias_compra += 1
                    debug_info.append(f"Volume Profile: Suporte compra | Peso: {vp_peso:.2f}")
                elif vp_data['tendencia'] == 'down' and vp_data['pressao_vendedora'] > 0.6:
                    score_venda += vp_peso
                    confluencias_venda += 1
                    debug_info.append(f"Volume Profile: Suporte venda | Peso: {vp_peso:.2f}")

        # 7. Price Action (se ativado)
        if 'price_patterns' in indicadores:
            patterns = indicadores['price_patterns']
            pa_peso = pesos.get('price_action', 1.6)

            if patterns.get('bullish_pattern'):
                score_compra += pa_peso
                confluencias_compra += 1
                debug_info.append(f"Price Action: Padrão de alta | Peso: {pa_peso:.2f}")
            elif patterns.get('bearish_pattern'):
                score_venda += pa_peso
                confluencias_venda += 1
                debug_info.append(f"Price Action: Padrão de baixa | Peso: {pa_peso:.2f}")

        # Ajuste final do threshold baseado nas confluências
        threshold_ajustado = threshold * (numero_confluencias / 3)


        print("\n=== Resumo da Análise ===")
        print(f"Score Compra: {score_compra:.2f} ({confluencias_compra} confluências)")
        print(f"Score Venda: {score_venda:.2f} ({confluencias_venda} confluências)")
        print(f"Threshold Ajustado: {threshold_ajustado:.2f}")
        print("\nSinais Detectados:")
        for info in debug_info:
            print(f"- {info}")

        # Decisão final considerando confluências e scores
        if score_compra > score_venda and score_compra >= threshold_ajustado and  confluencias_compra > confluencias_venda :
            print(f"\n✅ Sinal CALL gerado (Score: {score_compra:.2f}, Confluências: {confluencias_compra})")
            return "CALL"
        elif score_venda > score_compra and score_venda >= threshold_ajustado and confluencias_venda > confluencias_compra :
            print(f"\n✅ Sinal PUT gerado (Score: {score_venda:.2f}, Confluências: {confluencias_venda})")
            return "PUT"

        print("❌ Nenhum sinal válido gerado")
        return None

    except Exception as e:
        print(f"\n❌ Erro na análise de sinais: {e}")
        import traceback
        traceback.print_exc()
        return None


def analisar_retracao_correta(velas_symbol, num_velas_analise=50):
    """
    Análise CORRETA de retração baseada na definição real:
    - Retração é movimento CONTRA a tendência predominante
    - Identifica áreas de resistência/suporte através de pavios
    - Opera CONTRA a cor da vela atual (se verde, sinal PUT; se vermelha, sinal CALL)
    - Busca por pullbacks em áreas de acúmulo de pavios
    """
    try:
        print(f"[DEBUG] analisar_retracao_correta chamada com {len(velas_symbol)} velas")
        
        if len(velas_symbol) < num_velas_analise:
            print(f"[DEBUG] Poucas velas: {len(velas_symbol)} < {num_velas_analise}")
            return None
            
        # Usa as últimas velas para análise
        velas_recentes = list(velas_symbol)[-num_velas_analise:]
        vela_atual = velas_recentes[-1]
        
        # Dados da vela atual
        preco_atual = float(vela_atual['close'])
        abertura_atual = float(vela_atual['open'])
        alta_atual = float(vela_atual['high'])
        baixa_atual = float(vela_atual['low'])
        
        # Determina se a vela atual é verde ou vermelha
        vela_atual_verde = preco_atual > abertura_atual
        
        print(f"\n=== ANÁLISE DE RETRAÇÃO CORRETA ===")
        print(f"Vela atual: {'VERDE' if vela_atual_verde else 'VERMELHA'}")
        print(f"Preço: {preco_atual:.5f}")
        
        # 1. IDENTIFICAR ÁREAS DE ACÚMULO DE PAVIOS
        areas_resistencia = []  # Onde há muitos pavios superiores
        areas_suporte = []      # Onde há muitos pavios inferiores
        
        # Analisa cada nível de preço para encontrar acúmulo de pavios
        for i in range(len(velas_recentes) - 10):  # Deixa margem para análise
            vela = velas_recentes[i]
            high = float(vela['high'])
            low = float(vela['low'])
            open_price = float(vela['open'])
            close = float(vela['close'])
            
            # Identifica pavios significativos
            corpo_vela = abs(close - open_price)
            pavio_superior = high - max(open_price, close)
            pavio_inferior = min(open_price, close) - low
            
            # Se o pavio é significativo em relação ao corpo
            if corpo_vela > 0:  # Evita divisão por zero
                ratio_pavio_superior = pavio_superior / (corpo_vela + 0.00001)
                ratio_pavio_inferior = pavio_inferior / (corpo_vela + 0.00001)
                
                # Considera pavio significativo se > 30% do corpo
                if ratio_pavio_superior > 0.3:
                    areas_resistencia.append({
                        'preco': high,
                        'forca': ratio_pavio_superior,
                        'indice': i
                    })
                    
                if ratio_pavio_inferior > 0.3:
                    areas_suporte.append({
                        'preco': low,
                        'forca': ratio_pavio_inferior,
                        'indice': i
                    })
        
        # 2. IDENTIFICAR TENDÊNCIA PREDOMINANTE
        # Analisa as últimas 20 velas para tendência
        velas_tendencia = velas_recentes[-20:]
        precos_fechamento = [float(v['close']) for v in velas_tendencia]
        
        # Calcula média móvel simples para determinar tendência
        if len(precos_fechamento) >= 10:
            media_inicial = sum(precos_fechamento[:10]) / 10
            media_final = sum(precos_fechamento[-10:]) / 10
            tendencia_alta = media_final > media_inicial
        else:
            tendencia_alta = precos_fechamento[-1] > precos_fechamento[0]
        
        print(f"Tendência: {'ALTA' if tendencia_alta else 'BAIXA'}")
        
        # 3. IDENTIFICAR PROXIMIDADE DE ÁREAS DE RESISTÊNCIA/SUPORTE
        proximidade_resistencia = False
        proximidade_suporte = False
        
        # Verifica se o preço atual está próximo de alguma área de resistência/suporte
        for area in areas_resistencia:
            distancia = abs(preco_atual - area['preco']) / preco_atual
            if distancia <= 0.001:  # Dentro de 0.1% do preço (mais flexível para testes)
                proximidade_resistencia = True
                print(f"Próximo de resistência: {area['preco']:.5f} (força: {area['forca']:.2f})")
                
        for area in areas_suporte:
            distancia = abs(preco_atual - area['preco']) / preco_atual
            if distancia <= 0.001:  # Dentro de 0.1% do preço (mais flexível para testes)
                proximidade_suporte = True
                print(f"Próximo de suporte: {area['preco']:.5f} (força: {area['forca']:.2f})")
        
        # 4. LÓGICA DE RETRAÇÃO (CONTRA A COR DA VELA)
        sinal = None
        confianca = 0
        motivo = ""
        
        # Se vela verde (alta) E próximo de resistência E tendência de alta
        # = Possível retração para baixo = PUT
        if vela_atual_verde and proximidade_resistencia and tendencia_alta:
            sinal = "PUT"
            confianca = 0.75
            motivo = "Vela verde rejeitada em resistência (retração esperada)"
            print("🔴 SINAL PUT: Vela verde rejeitada em resistência (retração esperada)")
            
        # Se vela vermelha (baixa) E próximo de suporte E tendência de baixa
        # = Possível retração para cima = CALL
        elif not vela_atual_verde and proximidade_suporte and not tendencia_alta:
            sinal = "CALL"
            confianca = 0.75
            motivo = "Vela vermelha rejeitada em suporte (retração esperada)"
            print("🟢 SINAL CALL: Vela vermelha rejeitada em suporte (retração esperada)")
            
        # Casos de força menor (sem confluência de tendência)
        elif vela_atual_verde and proximidade_resistencia:
            sinal = "PUT"
            confianca = 0.6
            motivo = "Vela verde em resistência (sem confluência de tendência)"
            print("🔴 SINAL PUT (menor força): Vela verde em resistência")
            
        elif not vela_atual_verde and proximidade_suporte:
            sinal = "CALL"
            confianca = 0.6
            motivo = "Vela vermelha em suporte (sem confluência de tendência)"
            print("🟢 SINAL CALL (menor força): Vela vermelha em suporte")
        
        if sinal:
            return {
                'sinal': sinal,
                'confianca': confianca,
                'motivo': motivo,
                'tipo': 'retracao_correta',
                'vela_atual_verde': vela_atual_verde,
                'tendencia_alta': tendencia_alta,
                'proximidade_resistencia': proximidade_resistencia,
                'proximidade_suporte': proximidade_suporte,
                'em_area_resistencia': proximidade_resistencia,  # Compatibilidade com teste
                'em_area_suporte': proximidade_suporte,          # Compatibilidade com teste
                'areas_resistencia': len(areas_resistencia),
                'areas_suporte': len(areas_suporte)
            }
        
        return None
        
    except Exception as e:
        print(f"❌ Erro em analisar_retracao_correta: {e}")
        import traceback
        traceback.print_exc()
        return None


def calcular_volume_profile(velas_symbol, num_profiles=20):
    """
    Calcula o Volume Profile com tratamento robusto dos dados das velas.
    """
    try:
        print("\n=== Debug Volume Profile ===")
        print(f"Tipo de velas_symbol: {type(velas_symbol)}")

        # Converter deque para lista se necessário
        velas_list = list(velas_symbol) if hasattr(velas_symbol, 'maxlen') else velas_symbol

        print(f"Total de velas: {len(velas_list)}")
        if velas_list:
            print(f"Amostra primeira vela: {velas_list[0]}")

        # Usar últimas 80 velas ou todas disponíveis se menor que 80
        velas_analise = velas_list[-20:] if len(velas_list) > 20 else velas_list

        precos = []
        volumes = []
        total_volume = 0

        for vela in velas_analise:
            try:
                # Garantir que todos os valores são float
                high = float(str(vela['high']).replace("'", ""))
                low = float(str(vela['low']).replace("'", ""))
                close = float(str(vela['close']).replace("'", ""))
                open_price = float(str(vela['open']).replace("'", ""))

                # Calcular volume sintético baseado no range e movimento da vela
                range_vela = high - low
                movimento = abs(close - open_price)
                volume = (range_vela + movimento) * 100  # Volume sintético

                # Calcular preço médio ponderado da vela
                preco_medio = (high + low + close + open_price) / 4

                if preco_medio > 0 and not math.isnan(preco_medio):
                    precos.append(preco_medio)
                    volumes.append(volume)
                    total_volume += volume

            except (KeyError, ValueError, TypeError) as e:
                print(f"⚠️ Erro ao processar vela: {e}")
                continue

        if not precos:
            print("❌ Nenhum preço válido processado")
            return None

        print(f"✅ Processados {len(precos)} preços válidos")

        # Cálculo dos níveis de preço
        preco_min = min(precos)
        preco_max = max(precos)

        if preco_max <= preco_min:
            print("❌ Range de preços inválido")
            return None

        step = (preco_max - preco_min) / num_profiles
        niveis = []

        # Análise por nível
        for i in range(num_profiles):
            nivel_min = preco_min + (i * step)
            nivel_max = nivel_min + step

            volume_nivel = sum(v for p, v in zip(precos, volumes)
                               if nivel_min <= p < nivel_max)

            if volume_nivel > 0:
                niveis.append({
                    'preco_medio': (nivel_min + nivel_max) / 2,
                    'volume': volume_nivel,
                    'volume_relativo': volume_nivel / total_volume if total_volume else 0
                })

        if not niveis:
            print("❌ Nenhum nível de preço calculado")
            return None

        # Ordenar níveis por volume
        niveis_ordenados = sorted(niveis, key=lambda x: x['volume'], reverse=True)

        # Point of Control (POC)
        poc_preco = niveis_ordenados[0]['preco_medio']

        # Value Area Analysis (70% do volume)
        volume_acumulado = 0
        value_area_niveis = []

        for nivel in niveis_ordenados:
            volume_acumulado += nivel['volume']
            value_area_niveis.append(nivel)
            if volume_acumulado >= total_volume * 0.75:
                break

        # Calcular pressão compradora/vendedora
        ultimos_precos = precos[-20:]  # Últimos 10 preços
        pressao_compradora = sum(1 for p in ultimos_precos if p > poc_preco) / len(ultimos_precos)
        pressao_vendedora = 1 - pressao_compradora

        # Determinar tendência
        preco_atual = precos[-1] if precos else 0
        tendencia = 'up' if preco_atual > poc_preco else 'down'
        forca_tendencia = abs(preco_atual - poc_preco) / (preco_max - preco_min)

        resultado = {
            'poc': poc_preco,
            'value_area_high': max(n['preco_medio'] for n in value_area_niveis),
            'value_area_low': min(n['preco_medio'] for n in value_area_niveis),
            'tendencia': tendencia,
            'forca_tendencia': forca_tendencia,
            'pressao_compradora': pressao_compradora,
            'pressao_vendedora': pressao_vendedora,
            'dentro_value_area': True,  # Será atualizado depois
            'volume_anormal': False,  # Será atualizado depois
            'distribuicao': {
                'acima_poc': sum(n['volume'] for n in niveis if n['preco_medio'] > poc_preco),
                'abaixo_poc': sum(n['volume'] for n in niveis if n['preco_medio'] < poc_preco)
            }
        }

        print(f"Volume Profile calculado com sucesso para {len(precos)} preços")
        return resultado

    except Exception as e:
        print(f"Erro ao calcular Volume Profile: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def usar_volume_profile_na_analise(velas_symbol, preco_atual):

    try:
        # Obter dados do Volume Profile
        vp_data = calcular_volume_profile(velas_symbol)
        if not vp_data:
            print("❌ Dados do Volume Profile insuficientes")
            return None

        print("\n=== Análise Volume Profile ===")

        sinais = {
            'sinal': None,
            'forca': 0,
            'confirmacoes': [],
            'detalhes': {}
        }

        # 1. Análise da Value Area (70% do volume)
        preco_dentro_va = vp_data['value_area_low'] <= preco_atual <= vp_data['value_area_high']
        distancia_poc = abs(preco_atual - vp_data['poc']) / vp_data['poc'] * 100

        sinais['detalhes']['value_area'] = {
            'dentro': preco_dentro_va,
            'distancia_poc': distancia_poc
        }

        if preco_dentro_va:
            if distancia_poc < 0.25:  # Muito próximo ao POC
                sinais['confirmacoes'].append('Preço próximo ao POC - área de decisão importante')
                sinais['forca'] += 0.35
            if vp_data['pressao_compradora'] > 0.75:
                sinais['confirmacoes'].append('Alta pressão compradora na Value Area')
                sinais['forca'] += 0.45
            elif vp_data['pressao_vendedora'] > 0.75:
                sinais['confirmacoes'].append('Alta pressão vendedora na Value Area')
                sinais['forca'] += 0.45

        # 2. Análise da Distribuição de Volume
        vol_ratio = vp_data['distribuicao']['acima_poc'] / vp_data['distribuicao']['abaixo_poc']
        sinais['detalhes']['volume_ratio'] = vol_ratio

        if vol_ratio > 1.55:  # Volume significativamente maior acima do POC
            sinais['confirmacoes'].append('Acumulação significativa acima do POC')
            sinais['forca'] += 0.35
        elif vol_ratio < 0.67:  # Volume significativamente maior abaixo do POC
            sinais['confirmacoes'].append('Acumulação significativa abaixo do POC')
            sinais['forca'] += 0.35

        # 3. Análise de Momentum e Tendência
        if vp_data['forca_tendencia'] > 0.65:
            if vp_data['tendencia'] == 'up':
                sinais['confirmacoes'].append(f"Forte tendência de alta (força: {vp_data['forca_tendencia']:.2f})")
                sinais['forca'] += 0.45
            else:
                sinais['confirmacoes'].append(f"Forte tendência de baixa (força: {vp_data['forca_tendencia']:.2f})")
                sinais['forca'] += 0.45

        # 4. Volume Anormal
        if vp_data['volume_anormal']:
            sinais['confirmacoes'].append('Volume anormal detectado')
            sinais['forca'] += 0.25

        # 5. Análise de Pressão
        pressao = max(vp_data['pressao_compradora'], vp_data['pressao_vendedora'])
        sinais['detalhes']['pressao'] = pressao

        if pressao > 0.85:
            direcao = "compradora" if vp_data['pressao_compradora'] > vp_data['pressao_vendedora'] else "vendedora"
            sinais['confirmacoes'].append(f"Forte pressão {direcao}: {pressao:.2f}")
            sinais['forca'] += 0.35

        # Decisão Final
        if sinais['forca'] >= 0.65:
            if (preco_atual < vp_data['poc'] and vp_data['tendencia'] == 'up' and
                    vp_data['pressao_compradora'] > vp_data['pressao_vendedora']):
                sinais['sinal'] = 'CALL'
                sinais['confirmacoes'].append('Sinal de CALL confirmado por múltiplos fatores')

            elif (preco_atual > vp_data['poc'] and vp_data['tendencia'] == 'down' and
                  vp_data['pressao_vendedora'] > vp_data['pressao_compradora']):
                sinais['sinal'] = 'PUT'
                sinais['confirmacoes'].append('Sinal de PUT confirmado por múltiplos fatores')

        # Log detalhado
        print(f"\nForça total acumulada: {sinais['forca']:.2f}")
        print("\nConfirmações encontradas:")
        for conf in sinais['confirmacoes']:
            print(f"- {conf}")
        if sinais['sinal']:
            print(f"\nSinal gerado: {sinais['sinal']}")
        print("============================")

        return sinais

    except Exception as e:
        print(f"❌ Erro na análise do Volume Profile: {str(e)}")
        import traceback
        traceback.print_exc()
        return None





async def validar_price_action(symbol, sinal, velas_symbol):
    """
    Valida padrões de price action incluindo todos os padrões originais e novas validações.

    Args:
        symbol (str): Símbolo sendo analisado
        sinal (str): Direção do sinal ("CALL" ou "PUT")
        velas_symbol (list/deque): Lista ou deque das últimas velas do símbolo

    Returns:
        bool: True se o padrão de price action confirma o sinal, False caso contrário
    """
    try:
        # Converter para lista se não for
        velas_list = list(velas_symbol) if hasattr(velas_symbol, '__iter__') else []

        if len(velas_list) < 5:
            print(f"❌ {symbol}: Dados insuficientes para análise de Price Action ({len(velas_list)} velas)")
            return False

        # Pegar as últimas 5 velas para análise mais completa
        ultimas_velas = velas_list[-5:]
        print(f"Analisando {len(ultimas_velas)} velas para {symbol}")

        velas_processadas = []
        for vela in ultimas_velas:
            try:
                vela_dados = {
                    'open': float(vela['open']),
                    'high': float(vela['high']),
                    'low': float(vela['low']),
                    'close': float(vela['close']),
                    'body_size': abs(float(vela['close']) - float(vela['open'])),
                    'upper_shadow': float(vela['high']) - max(float(vela['open']), float(vela['close'])),
                    'lower_shadow': min(float(vela['open']), float(vela['close'])) - float(vela['low']),
                    'is_bullish': float(vela['close']) > float(vela['open']),
                    'is_bearish': float(vela['close']) < float(vela['open'])
                }
                velas_processadas.append(vela_dados)
            except (KeyError, ValueError) as e:
                print(f"❌ Erro ao processar vela: {e}")
                continue

        if len(velas_processadas) < 3:
            print(f"❌ {symbol}: Dados processados insuficientes")
            return False

        # === Análise para CALL ===
        if sinal == "CALL":
            # 1. Padrão de reversão de baixa
            reversao_baixa = (
                    all(not v['is_bullish'] for v in velas_processadas[-4:-1]) and  # 3 velas de baixa
                    velas_processadas[-1]['is_bullish'] and  # Última vela de alta
                    velas_processadas[-1]['body_size'] > sum(v['body_size'] for v in velas_processadas[-4:-1]) / 3
            # Força relativa
            )

            # 2. Martelo (hammer)
            martelo = (
                    velas_processadas[-1]['lower_shadow'] > 2 * velas_processadas[-1]['body_size'] and
                    velas_processadas[-1]['upper_shadow'] < velas_processadas[-1]['body_size'] * 0.3 and
                    not velas_processadas[-2]['is_bullish']  # Confirmação com vela anterior de baixa
            )

            # 3. Padrão de engolfo de alta
            engolfo_alta = (
                    not velas_processadas[-2]['is_bullish'] and  # Vela anterior de baixa
                    velas_processadas[-1]['is_bullish'] and  # Vela atual de alta
                    velas_processadas[-1]['open'] < velas_processadas[-2]['close'] and  # Abre abaixo
                    velas_processadas[-1]['close'] > velas_processadas[-2]['open']  # Fecha acima
            )

            # 4. Three white soldiers (3 soldados brancos)
            three_white_soldiers = (
                    len(velas_processadas) >= 3 and
                    all(v['is_bullish'] for v in velas_processadas[-3:]) and
                    all(v['upper_shadow'] < v['body_size'] * 0.3 for v in velas_processadas[-3:]) and
                    all(v['lower_shadow'] < v['body_size'] * 0.3 for v in velas_processadas[-3:])
            )

            if reversao_baixa or martelo or engolfo_alta or three_white_soldiers:
                print(f"✅ {symbol}: Padrão de alta confirmado")
                if reversao_baixa: print("- Reversão de baixa identificada")
                if martelo: print("- Martelo identificado")
                if engolfo_alta: print("- Engolfo de alta identificado")
                if three_white_soldiers: print("- Three white soldiers identificado")
                return True

        # === Análise para PUT ===
        elif sinal == "PUT":
            # 1. Padrão de reversão de alta
            reversao_alta = (
                    all(v['is_bullish'] for v in velas_processadas[-4:-1]) and  # 3 velas de alta
                    velas_processadas[-1]['is_bearish'] and  # Última vela de baixa
                    velas_processadas[-1]['body_size'] > sum(v['body_size'] for v in velas_processadas[-4:-1]) / 3
            # Força relativa
            )

            # 2. Shooting star (estrela cadente)
            shooting_star = (
                    velas_processadas[-1]['upper_shadow'] > 2 * velas_processadas[-1]['body_size'] and
                    velas_processadas[-1]['lower_shadow'] < velas_processadas[-1]['body_size'] * 0.3 and
                    velas_processadas[-2]['is_bullish']  # Confirmação com vela anterior de alta
            )

            # 3. Padrão de engolfo de baixa
            engolfo_baixa = (
                    velas_processadas[-2]['is_bullish'] and  # Vela anterior de alta
                    velas_processadas[-1]['is_bearish'] and  # Vela atual de baixa
                    velas_processadas[-1]['open'] > velas_processadas[-2]['close'] and  # Abre acima
                    velas_processadas[-1]['close'] < velas_processadas[-2]['open']  # Fecha abaixo
            )

            # 4. Three black crows (3 corvos negros)
            three_black_crows = (
                    len(velas_processadas) >= 3 and
                    all(not v['is_bullish'] for v in velas_processadas[-3:]) and
                    all(v['upper_shadow'] < v['body_size'] * 0.3 for v in velas_processadas[-3:]) and
                    all(v['lower_shadow'] < v['body_size'] * 0.3 for v in velas_processadas[-3:])
            )

            if reversao_alta or shooting_star or engolfo_baixa or three_black_crows:
                print(f"✅ {symbol}: Padrão de baixa confirmado")
                if reversao_alta: print("- Reversão de alta identificada")
                if shooting_star: print("- Shooting star identificado")
                if engolfo_baixa: print("- Engolfo de baixa identificado")
                if three_black_crows: print("- Three black crows identificado")
                return True

        print(f"❌ {symbol}: Nenhum padrão de Price Action confirmado para {sinal}")
        return False

    except Exception as e:
        print(f"❌ Erro na validação de Price Action para {symbol}: {e}")
        import traceback
        traceback.print_exc()
        return False



@jit(nopython=True)
def ajustar_nivel_value_charts(atr, atr_min=0.01, atr_max=0.1):
    """Ajusta nível do Value Charts baseado no ATR"""
    atr = max(atr_min, min(atr, atr_max))
    atr_porcentagem = (atr - atr_min) / (atr_max - atr_min)
    return 9.2 + (12.2 - 9.2) * atr_porcentagem




def calculate_sr_levels(velas, lookback=60, threshold=0.001):
    """
    Calcula os níveis de Suporte e Resistência usando os últimos N períodos.
    """
    try:
        # Converter velas para lista caso não seja
        velas_list = list(velas) if not isinstance(velas, list) else velas

        # Garantir dados suficientes
        if len(velas_list) < lookback:
            print("Dados insuficientes para cálculo de SR")
            return {"suportes": [], "resistencias": [], "zone_size": 0.0}

        # Extrair últimas velas para análise
        recent_velas = velas_list[-lookback:] if len(velas_list) >= lookback else velas_list

        # Converter dados para arrays numpy com proteção contra erros
        try:
            highs = []
            lows = []
            closes = []

            for vela in recent_velas:
                try:
                    highs.append(float(vela['high']))
                    lows.append(float(vela['low']))
                    closes.append(float(vela['close']))
                except (ValueError, TypeError, KeyError) as e:
                    print(f"Erro ao processar vela: {e}")
                    continue

            if not highs or not lows or not closes:
                print("Nenhum dado válido encontrado nas velas")
                return {"suportes": [], "resistencias": [], "zone_size": 0.0}

            highs = np.array(highs)
            lows = np.array(lows)
            closes = np.array(closes)

        except Exception as e:
            print(f"Erro na conversão de dados: {e}")
            return {"suportes": [], "resistencias": [], "zone_size": 0.0}

        # Calcula média do range para definir zonas
        avg_range = np.mean(highs - lows)
        zone_size = avg_range * threshold

        # Encontra picos e vales
        resistencias = []
        suportes = []

        # Usar loop tradicional para evitar problemas de indexação
        for i in range(2, len(highs) - 2):
            # Resistência: Ponto mais alto entre dois pontos mais baixos em cada lado
            if (highs[i] > highs[i - 1] and highs[i] > highs[i - 2] and
                    highs[i] > highs[i + 1] and highs[i] > highs[i + 2]):
                resistencias.append(float(highs[i]))

            # Suporte: Ponto mais baixo entre dois pontos mais altos em cada lado
            if (lows[i] < lows[i - 1] and lows[i] < lows[i - 2] and
                    lows[i] < lows[i + 1] and lows[i] < lows[i + 2]):
                suportes.append(float(lows[i]))

        # Remove níveis muito próximos
        if resistencias:
            resistencias = merge_close_levels(resistencias, zone_size)
        if suportes:
            suportes = merge_close_levels(suportes, zone_size)

        result = {
            "suportes": suportes,
            "resistencias": resistencias,
            "zone_size": float(zone_size)
        }

        print(f"\n=== Níveis SR calculados ===")
        print(f"Total de velas analisadas: {len(recent_velas)}")
        if suportes:
            print(f"Zonas de Suporte: {', '.join([f'{s:.2f}' for s in suportes])}")
        if resistencias:
            print(f"Zonas de Resistência: {', '.join([f'{r:.2f}' for r in resistencias])}")
        print(f"Tamanho da zona: {zone_size:.4f}")

        return result

    except Exception as e:
        print(f"Erro ao calcular níveis SR: {e}")
        import traceback
        traceback.print_exc()
        return {"suportes": [], "resistencias": [], "zone_size": 0.0}


def validate_sr_signal(preco_atual, velas, sinal, sr_levels):
    """
    Valida um sinal baseado nos níveis de SR e confirmação de rompimento.
    """
    try:
        if len(velas) < 3:
            return False, "Dados insuficientes"

        zone_size = float(sr_levels.get('zone_size', 0.0))
        suportes = sr_levels.get('suportes', [])
        resistencias = sr_levels.get('resistencias', [])

        # Se não há níveis SR, o sinal é válido
        if not suportes and not resistencias:
            return True, "Sem níveis SR definidos"

        # Converte velas para lista se necessário
        velas_list = list(velas) if not isinstance(velas, list) else velas

        # Extrai últimas velas para análise
        vela_atual = velas_list[-1]
        vela_anterior = velas_list[-2]
        vela_anterior2 = velas_list[-3]

        print(f"\n=== Validação SR para preço {preco_atual:.2f} ===")

        # Verifica proximidade com níveis SR
        for nivel in suportes + resistencias:
            distancia = abs(preco_atual - nivel)
            if distancia <= zone_size * 2:
                print(f"Preço próximo ao nível {nivel:.2f} (distância: {distancia:.4f})")

                # Verifica rompimento para CALL
                if sinal == "CALL" and nivel in suportes:
                    rompimento = verifica_rompimento_alta(vela_atual, vela_anterior, vela_anterior2, nivel)
                    if rompimento:
                        print(f"✅ Rompimento de suporte confirmado em {nivel:.2f}")
                        return True, "Rompimento de suporte confirmado"
                    print(f"❌ Sem confirmação de rompimento de suporte em {nivel:.2f}")
                    return False, "Muito próximo ao suporte sem rompimento"

                # Verifica rompimento para PUT
                elif sinal == "PUT" and nivel in resistencias:
                    rompimento = verifica_rompimento_baixa(vela_atual, vela_anterior, vela_anterior2, nivel)
                    if rompimento:
                        print(f"✅ Rompimento de resistência confirmado em {nivel:.2f}")
                        return True, "Rompimento de resistência confirmado"
                    print(f"❌ Sem confirmação de rompimento de resistência em {nivel:.2f}")
                    return False, "Muito próximo à resistência sem rompimento"

                print("❌ Muito próximo a nível SR sem confirmação")
                return False, "Muito próximo a nível de SR"

        print("✅ Preço longe dos níveis SR")
        return True, "Longe de níveis SR"

    except Exception as e:
        print(f"Erro ao validar sinal SR: {e}")
        import traceback
        traceback.print_exc()
        return False, f"Erro na validação: {str(e)}"


def merge_close_levels(levels, threshold):
    """
    Combina níveis que estão muito próximos usando a média.
    """
    if not levels:
        return []

    levels = sorted(levels)
    merged = []
    current_group = [levels[0]]

    for level in levels[1:]:
        if abs(level - current_group[-1]) <= threshold:
            current_group.append(level)
        else:
            merged.append(float(np.mean(current_group)))
            current_group = [level]

    merged.append(float(np.mean(current_group)))
    return merged


def verifica_rompimento_alta(vela_atual, vela_anterior, vela_anterior2, nivel):
    """
    Verifica se houve rompimento de alta confirmado.
    """
    try:
        # Converte valores para float com segurança
        def get_float(vela, key):
            try:
                return float(vela[key])
            except (ValueError, TypeError):
                return 0.0

        # Pega os valores das velas
        atual_open = get_float(vela_atual, 'open')
        atual_close = get_float(vela_atual, 'close')
        anterior_open = get_float(vela_anterior, 'open')
        anterior_close = get_float(vela_anterior, 'close')

        # Verifica se são velas de alta (verdes)
        vela_atual_verde = atual_close > atual_open
        vela_anterior_verde = anterior_close > anterior_open

        # Verifica se fecharam acima do nível
        fechou_acima_atual = atual_close > nivel
        fechou_acima_anterior = anterior_close > nivel

        return (vela_atual_verde and vela_anterior_verde and
                fechou_acima_atual and fechou_acima_anterior)

    except Exception as e:
        print(f"Erro ao verificar rompimento de alta: {e}")
        return False


def verifica_rompimento_baixa(vela_atual, vela_anterior, vela_anterior2, nivel):
    """
    Verifica se houve rompimento de baixa confirmado.
    """
    try:
        # Converte valores para float com segurança
        def get_float(vela, key):
            try:
                return float(vela[key])
            except (ValueError, TypeError):
                return 0.0

        # Pega os valores das velas
        atual_open = get_float(vela_atual, 'open')
        atual_close = get_float(vela_atual, 'close')
        anterior_open = get_float(vela_anterior, 'open')
        anterior_close = get_float(vela_anterior, 'close')

        # Verifica se são velas de baixa (vermelhas)
        vela_atual_vermelha = atual_close < atual_open
        vela_anterior_vermelha = anterior_close < anterior_open

        # Verifica se fecharam abaixo do nível
        fechou_abaixo_atual = atual_close < nivel
        fechou_abaixo_anterior = anterior_close < nivel

        return (vela_atual_vermelha and vela_anterior_vermelha and
                fechou_abaixo_atual and fechou_abaixo_anterior)

    except Exception as e:
        print(f"Erro ao verificar rompimento de baixa: {e}")
        return False


def on_error(ws, error):
    print(f"Error occurred: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"Connection closed: {close_status_code} - {close_msg}")



def connect_websocket():
    global websocket_client, is_running
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(URL,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    websocket_client = ws
    is_running = True
    ws.run_forever()


async def start_websocket():
    global websocket_client, is_running, reconnect_delay

    while is_running:
        try:
            print("\n=== Iniciando conexão WebSocket ===")
            websocket.enableTrace(False)
            ws = websocket.WebSocketApp(
                URL,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )

            websocket_client = ws

            # Executa o WebSocket em uma thread separada
            ws_thread = threading.Thread(
                target=lambda: ws.run_forever(
                    ping_interval=30,
                    ping_timeout=10,
                    sslopt={"cert_reqs": ssl.CERT_NONE}
                ),
                daemon=True
            )
            ws_thread.start()

            # Aguarda a conexão ser estabelecida
            for _ in range(10):  # 5 segundos de timeout
                if websocket_client and websocket_client.sock and websocket_client.sock.connected:
                    print("✅ WebSocket conectado com sucesso")
                    reconnect_delay = 5  # Reset delay após sucesso
                    await subscribe_to_all_symbols(websocket_client)
                    break
                await asyncio.sleep(0.5)
            else:
                print("❌ Timeout ao aguardar conexão WebSocket")
                continue

            # Mantém a thread viva enquanto estiver rodando
            while is_running and websocket_client and websocket_client.sock and websocket_client.sock.connected:
                await asyncio.sleep(1)

            if not is_running:
                print("Bot pausado, encerrando WebSocket...")
                break

        except Exception as e:
            print(f"Erro na conexão WebSocket: {e}")

        finally:
            if websocket_client:
                try:
                    websocket_client.close()
                except:
                    pass
                websocket_client = None

        print(f"Tentando reconexão em {reconnect_delay} segundos...")
        await asyncio.sleep(reconnect_delay)
        reconnect_delay = min(reconnect_delay * 2, 60)  # Aumenta o delay até 60 segundos

    print("WebSocket encerrado")


async def reconnect_websocket():
    """Reconecta o WebSocket com retry exponencial"""
    global websocket_client, reconnect_delay

    print(f"Tentando reconexão em {reconnect_delay} segundos...")
    await asyncio.sleep(reconnect_delay)

    try:
        # Fecha conexão existente se houver
        if websocket_client:
            try:
                websocket_client.close()
            except:
                pass
            websocket_client = None
            await asyncio.sleep(1)

        # Inicia nova conexão
        await start_websocket_async()

        # Reseta delay se conexão bem sucedida
        reconnect_delay = 5

    except Exception as e:
        print(f"Erro na reconexão: {e}")
        # Aumenta delay até o máximo
        reconnect_delay = min(reconnect_delay * 2, 60)
        await reconnect_websocket()



def debounce(wait):
    """
    Decorator para limitar a frequência de chamadas de uma função

    Args:
        wait (float): Tempo mínimo (em segundos) entre chamadas
    """

    def decorator(fn):
        last_call = [0]
        lock = threading.Lock()

        @wraps(fn)
        def debounced(*args, **kwargs):
            with lock:
                current_time = time.time()
                if current_time - last_call[0] >= wait:
                    last_call[0] = current_time
                    return fn(*args, **kwargs)

        return debounced

    return decorator


class StatsCache:
    """
    Cache para estatísticas do bot para evitar atualizações desnecessárias da interface
    """

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.lucro = 0.0
        self.saldo = 0.0
        self.last_update = 0
        self.lock = threading.Lock()

    def needs_update(self, wins, losses, lucro, saldo):
        """
        Verifica se é necessário atualizar a interface

        Args:
            wins (int): Número atual de vitórias
            losses (int): Número atual de derrotas
            lucro (float): Lucro atual
            saldo (float): Saldo atual

        Returns:
            bool: True se necessário atualizar, False caso contrário
        """
        with self.lock:
            if time.time() - self.last_update < 0.1:  # Limita atualizações a cada 100ms
                return False

            return (
                    wins != self.wins or
                    losses != self.losses or
                    abs(lucro - self.lucro) > 0.001 or  # Tolerância para valores float
                    abs(saldo - self.saldo) > 0.001
            )

    def update(self, wins, losses, lucro, saldo):
        """
        Atualiza os valores em cache

        Args:
            wins (int): Novo número de vitórias
            losses (int): Novo número de derrotas
            lucro (float): Novo valor de lucro
            saldo (float): Novo valor de saldo
        """
        with self.lock:
            self.wins = wins
            self.losses = losses
            self.lucro = lucro
            self.saldo = saldo
            self.last_update = time.time()


# Instância global do cache
stats_cache = StatsCache()

@debounce(0.1)
def update_status():
    """Atualiza o status mantendo lucro baseado apenas no lucro_total global"""
    global total_wins, total_losses, lucro_total, stats_cache, saldo_atual

    try:
        total_wins = max(0, int(total_wins))
        total_losses = max(0, int(total_losses))
        total_trades = total_wins + total_losses

        # Verifica se precisa atualizar
        if not stats_cache.needs_update(total_wins, total_losses, lucro_total, saldo_atual):
            return

        # Calcula winrate
        winrate = (total_wins / total_trades * 100) if total_trades > 0 else 0

        # Atualiza interface usando sempre lucro_total
        updates = [
            {
                "tag": "saldo_text",
                "value": f"$ {saldo_atual:.2f}",
                "validator": lambda x: isinstance(x, (int, float)) and x >= 0,
                "raw_value": saldo_atual
            },
            {
                "tag": "wins_text",
                "value": f"{total_wins}",
                "validator": lambda x: isinstance(x, int) and x >= 0,
                "raw_value": total_wins
            },
            {
                "tag": "losses_text",
                "value": f"{total_losses}",
                "validator": lambda x: isinstance(x, int) and x >= 0,
                "raw_value": total_losses
            },
            {
                "tag": "winrate_text",
                "value": f"{winrate:.2f}%",
                "validator": lambda x: isinstance(x, (int, float)) and 0 <= x <= 100,
                "raw_value": winrate
            },
            {
                "tag": "pnl_text",
                "value": f"$ {lucro_total:.2f}",  # Usa sempre lucro_total
                "validator": lambda x: isinstance(x, (int, float)),
                "raw_value": lucro_total
            }
        ]

        for update in updates:
            try:
                if dpg.does_item_exist(update["tag"]):
                    if update["validator"](update["raw_value"]):
                        dpg.set_value(update["tag"], update["value"])

                        # Configura cor do lucro
                        if update["tag"] == "pnl_text":
                            dpg.configure_item(
                                update["tag"],
                                color=(0, 255, 0) if lucro_total >= 0 else (255, 0, 0)
                            )
            except Exception as e:
                print(f"Erro ao atualizar {update['tag']}: {e}")
                continue

        # Atualiza cache com os valores corretos
        stats_cache.update(total_wins, total_losses, lucro_total, saldo_atual)

        print("\n=== Status Atualizado ===")
        print(f"Wins: {total_wins}")
        print(f"Losses: {total_losses}")
        print(f"Lucro Total: ${lucro_total:.2f}")
        print(f"Saldo Atual: ${saldo_atual:.2f}")
        print("=======================\n")

    except Exception as e:
        print(f"Erro ao atualizar status: {e}")
        traceback.print_exc()



def abrir_popup_token():
    global telegram_ativado
    demo_token, real_token = carregar_tokens()

    if dpg.does_item_exist("token_popup"):
        dpg.delete_item("token_popup")

    # Obter o tamanho da viewport
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    # Calcular a posição central
    window_width = 300
    window_height = 300  # Aumentado um pouco para acomodar o novo layout
    pos_x = (viewport_width - window_width) // 2
    pos_y = (viewport_height - window_height) // 2

    with dpg.window(label="Inserir Tokens", tag="token_popup", width=window_width, height=window_height,
                    no_resize=True, no_collapse=True, pos=[pos_x, pos_y]):
        dpg.add_spacer(height=10)
        dpg.add_text(language_manager.get_text("TOKENS_INSIRA"), color=(255, 255, 0),tag="tokensinriratext")
        dpg.add_separator()
        dpg.add_spacer(height=10)

        with dpg.group():
            dpg.add_text("Token Demo")
            dpg.add_input_text(tag="demo_token_input", password=True, default_value=demo_token or "", width=280)
            dpg.add_spacer(height=10)
            dpg.add_text("Token Real")
            dpg.add_input_text(tag="real_token_input", password=True, default_value=real_token or "", width=280)

        dpg.add_spacer(height=20)

        with dpg.group(horizontal=True):
            dpg.add_button(label=language_manager.get_text("TOKENS_SALVAR"), width=135, height=20, callback=salvar_tokens,tag="tokenssalvartext")
            dpg.add_button(label=language_manager.get_text("TOKENS_CANCELAR"), width=135, height=20,
                           callback=lambda: dpg.delete_item("token_popup"),tag="tokenscancelartext")



    # Aplicar tema personalizado
    with dpg.theme() as theme_token:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 70, 70))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 120, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)

    dpg.bind_item_theme("token_popup", theme_token)




def on_account_change(sender, app_data):
    global api_token, demo_token, real_token, api

    mode = dpg.get_value("token_mode")
    print(f"Modo selecionado: {mode}")

    # Carregar tokens se ainda não estiverem definidos
    if not demo_token or not real_token:
        carregar_tokens()

    if mode == "Demo":
        api_token = demo_token
        print(f"Token Demo selecionado: {api_token}")
    elif mode == "Real":
        api_token = real_token
        print(f"Token Real selecionado: {api_token}")

    # Verifica se há um token válido para a nova conta
    if not api_token or api_token.strip() == "":
        print(f"Por favor, insira o token para o modo {mode} antes de continuar.")
        abrir_popup_token()
        return

    # Rodar o switch_account de forma não bloqueante, com verificação de loop
    print("Reconectando com o novo token...")

    # Verificar se há um loop de eventos ativo, caso contrário usar create_task
    try:
        loop = asyncio.get_running_loop()
        asyncio.create_task(switch_account(mode))  # Usa create_task em vez de run_until_complete
    except RuntimeError:
        # Se não houver um loop de eventos ativo, executa em uma nova thread
        threading.Thread(target=lambda: asyncio.run(switch_account(mode)), daemon=True).start()


async def switch_account(mode):
    global api, api_token, saldo_atual, initial_balance, lucro_total

    # Desativar o botão de iniciar e o seletor de modo
    dpg.disable_item("toggle_button")
    dpg.disable_item("token_mode")

    # Exibir a mensagem de conexão em andamento
    dpg.set_value("success_message", f"Conectando a conta {mode}...")
    dpg.show_item("success_message")

    try:
        # Tenta fazer logout
        if api is not None:
            try:
                await api.logout()
            except Exception as e:
                print(f"Erro durante o logout: {e}")
                api = None

        # Reconecta com o novo token
        await unified_reconnect("all", force=True)

        # Atualizar saldo e reinicializar variáveis
        await atualizar_saldo(api)
        initial_balance = saldo_atual
        lucro_total = 0

        print(f"Conectado a conta {mode} com sucesso!")
        dpg.set_value("success_message", f"Conectado a conta {mode}!")

        # Atualizar a interface
        update_status()

    except Exception as e:
        print(f"Erro ao trocar para a conta {mode}: {e}")
        dpg.set_value("success_message", f"Erro ao conectar a conta {mode}")

    finally:
        # Reativar controles após um curto delay
        await asyncio.sleep(1)
        dpg.enable_item("toggle_button")
        dpg.enable_item("token_mode")

        # Esconder a mensagem de sucesso após um breve momento
        await asyncio.sleep(2)
        dpg.hide_item("success_message")




def get_display_name(symbol):
    """
    Retorna o nome amigável do símbolo para exibição.
    Se o símbolo não estiver mapeado, retorna o símbolo original.
    """
    return SYMBOL_DISPLAY_NAMES.get(symbol, symbol)




def add_open_order_to_table(hora_abertura, entrada, par, direcao, duracao, gale_count, is_retracao, is_antiloss=False,
                            row_tag=None):
    global row_id, modo_gale
    row_tag = f"row_{hora_abertura.replace(':', '')}"
    fechamento_tag = f"fechamento_{row_tag}"
    tipo_sinal_tag = f"tipo_sinal_{row_tag}"
    w_l_tag = f"wl_{row_tag}"
    gale_tag = f"gale_{row_tag}"
    comentario_tag = f"comentario_{row_tag}"
    antiloss_tag = f"antiloss_{row_tag}"

    # Converte o símbolo para o nome de exibição
    display_symbol = get_display_name(par)

    # Define o texto do gale
    gale_text = "Sem Gale" if gale_count == 0 else f"Gale {gale_count}" if modo_gale == "zigzag" else f"Gale {gale_count}"

    rows = dpg.get_item_children("transactions_table", 1)

    if duracao == 15:  # Para pares STEP
        duracao_display = "15S"
    else:
        duracao_display = f"M{default_expiration}"

    if row_id is None or gale_count == 0:
        row_id = f"row_{hora_abertura.replace(':', '')}"

        tipo_sinal_text = (
            "Externo" if mt4_receiver and mt4_receiver.is_processing_order else
            "Fluxo" if fluxo_active else
            "PPONetwork" if ml_strategy_active else
            "ABR" if abr_strategy_active else
            "Retracao" if is_retracao else "Reversao"
        )
        antiloss_text = "Checking AntLoss" if is_antiloss else ""
        entrada_text = f"${entrada:.2f}"

        if rows:
            first_row = rows[0]
            with dpg.table_row(parent="transactions_table", tag=row_tag, before=first_row) as row:
                if is_antiloss:
                    dpg.set_item_user_data(row, "antiloss_row")
                    show_antiloss = dpg.get_item_user_data("toggle_antiloss_visibility")
                    if not show_antiloss:
                        dpg.hide_item(row_tag)

                dpg.add_text(hora_abertura)
                dpg.add_text("", tag=fechamento_tag)
                dpg.add_text(tipo_sinal_text)
                dpg.add_text(entrada_text)
                dpg.add_text(display_symbol)
                dpg.add_text(gale_text, tag=gale_tag)
                dpg.add_text(direcao, tag=f"direcao_{row_tag}")  # Adicionei tag para a direção
                dpg.add_text(duracao_display)
                dpg.add_text("", tag=w_l_tag)
                dpg.add_text(antiloss_text, tag=antiloss_tag)
                dpg.add_text("", tag=comentario_tag)
        else:
            with dpg.table_row(parent="transactions_table", tag=row_tag) as row:
                if is_antiloss:
                    dpg.set_item_user_data(row, "antiloss_row")
                    show_antiloss = dpg.get_item_user_data("toggle_antiloss_visibility")
                    if not show_antiloss:
                        dpg.hide_item(row_tag)

                dpg.add_text(hora_abertura)
                dpg.add_text("", tag=fechamento_tag)
                dpg.add_text(tipo_sinal_text)
                dpg.add_text(entrada_text)
                dpg.add_text(display_symbol)
                dpg.add_text(gale_text, tag=gale_tag)
                dpg.add_text(direcao, tag=f"direcao_{row_tag}")  # Adicionei tag para a direção
                dpg.add_text(duracao_display)
                dpg.add_text("", tag=w_l_tag)
                dpg.add_text(antiloss_text, tag=antiloss_tag)
                dpg.add_text("", tag=comentario_tag)

    else:
        children = dpg.get_item_children(row_id, slot=1)
        if children:
            dpg.set_value(children[0], hora_abertura)
            dpg.set_value(children[3], f"${entrada:.2f}")
            dpg.set_value(children[4], display_symbol)
            dpg.set_value(children[5], gale_text)
            dpg.set_value(children[6], direcao)  # Atualiza a direção com o novo valor
            dpg.set_value(children[7], duracao_display)
            dpg.set_value(children[8], "")
            dpg.set_value(children[9], "Checando AntLoss" if is_antiloss else "")
            dpg.set_value(children[10], "")

            if is_antiloss:
                show_antiloss = dpg.get_item_user_data("toggle_antiloss_visibility")
                if not show_antiloss:
                    dpg.hide_item(row_id)

    print(f"Ordem {'adicionada' if row_id is None else 'atualizada'} com row_id: {row_id}")
    print(f"Gale atual: {gale_text}")
    print(f"Direção atual: {direcao}")
    return row_id


def update_order_in_table(row_id, hora_fechamento, duracao, resultado, comentario=""):
    """Atualiza a ordem na tabela com melhor tratamento de erros"""
    try:
        if not dpg.does_item_exist(row_id):
            print(f"Row {row_id} não encontrada na tabela")
            return

        children = dpg.get_item_children(row_id, slot=1)
        if not children:
            return

        if duracao == 15:  # Para pares STEP
            duracao_display = "15S"
        else:
            duracao_display = f"M{default_expiration}"

        # Lista de atualizações com verificações
        updates = [
            (1, hora_fechamento),
            (7, duracao_display)
        ]

        for idx, value in updates:
            try:
                if idx < len(children):
                    dpg.set_value(children[idx], value)
            except Exception as e:
                print(f"Erro ao atualizar coluna {idx}: {e}")

        # Cores específicas para Antiloss
        CYAN = (0, 255, 255)      # Azul claro para antiloss fechado
        MAGENTA = (255, 0, 255)   # Magenta para antiloss em andamento

        # Verifica se é uma operação de antiloss
        is_antiloss = "AntLoss" in str(comentario) if comentario else False

        # Atualiza resultado e comentário
        if is_antiloss:
            # Extrai os números do formato "AntLoss X/Y"
            import re
            match = re.search(r'AntLoss (\d+)/(\d+)', str(comentario))
            if match:
                current, total = map(int, match.groups())
                # Antiloss em andamento
                if current < total:
                    if len(children) > 8:
                        dpg.set_value(children[8], resultado)
                        dpg.configure_item(children[8], color=MAGENTA)
                    if len(children) > 9:
                        dpg.set_value(children[9], comentario)
                        dpg.configure_item(children[9], color=CYAN)
                # Antiloss completado
                else:
                    if len(children) > 8:
                        dpg.set_value(children[8], resultado)
                        dpg.configure_item(children[8], color=MAGENTA)
                    if len(children) > 9:
                        dpg.set_value(children[9], comentario)
                        dpg.configure_item(children[9], color=CYAN)
            else:
                # Caso especial para "Resetando AntLoss" ou outros textos de antiloss
                if len(children) > 8:
                    dpg.set_value(children[8], resultado)
                    dpg.configure_item(children[8], color=MAGENTA)
                if len(children) > 9:
                    dpg.set_value(children[9], comentario)
                    dpg.configure_item(children[9], color=CYAN)
        else:
            # Comportamento normal para operações não-antiloss
            if resultado.upper() in ["WIN", "LOSS"]:
                is_win = resultado.upper() == "WIN"
                cor = (0, 255, 0) if is_win else (255, 0, 0)
                dpg.set_value(children[8], resultado)
                dpg.configure_item(children[8], color=cor)
            if len(children) > 9:
                dpg.set_value(children[9], comentario)

    except Exception as e:
        print(f"Erro ao atualizar tabela: {e}")
        import traceback
        traceback.print_exc()


async def start_countdown(row_id, duracao, contract_id, api):
    """Função que atualiza o countdown na interface no formato MM:SS"""
    try:
        start_time = time.time()
        end_time = start_time + duracao

        while time.time() < end_time:
            tempo_restante = max(0, int(end_time - time.time()))

            # Converte segundos para formato MM:SS
            horas = tempo_restante // 3600  # Divide por 3600 (segundos em 1 hora)
            minutos = (tempo_restante % 3600) // 60  # Pega o resto da divisão por 3600 e divide por 60
            segundos = tempo_restante % 60  # Pega o resto da divisão por 60
            tempo_formatado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"

            # Atualiza cor baseado no tempo restante
            if tempo_restante <= 4:
                cor = (255, 0, 0)  # Vermelho
            elif tempo_restante <= 11:
                cor = (240, 172, 4)  # Laranja
            else:
                cor = (51, 236, 0)  # Verde

            # Atualiza o contador na interface
            if dpg.does_item_exist(f"fechamento_{row_id}"):
                dpg.configure_item(f"fechamento_{row_id}", color=cor)
                dpg.set_value(f"fechamento_{row_id}", tempo_formatado)

            # Verifica status do contrato
            resultado, _ = api.check_win(contract_id, False)
            if resultado:
                break

            await asyncio.sleep(1)

        # Finaliza mostrando hora de fechamento
        if dpg.does_item_exist(f"fechamento_{row_id}"):
            hora_fechamento = datetime.now().strftime("%H:%M:%S")
            dpg.set_value(f"fechamento_{row_id}", hora_fechamento)
            dpg.configure_item(f"fechamento_{row_id}", color=(255, 255, 255))

    except Exception as e:
        logger.error(f"Erro no countdown: {e}")



async def start_rgb_effect_during_sample():
    tag = "bot_status_text"
    hue = 0

    while True:  # Mudado para loop infinito
        try:
            if not should_send_orders:
                # Quando pausado, define uma cor estática e aguarda
                dpg.configure_item(tag, color=(255, 255, 255))  # Cor branca quando pausado
                dpg.set_value(tag, "Bot Pausado")
                await asyncio.sleep(0.7)
                continue

            # Se o bot está ativo, continua com o efeito RGB
            r = int(127 * (math.sin(hue) + 1))
            g = int(127 * (math.sin(hue + 2 * math.pi / 3) + 1))
            b = int(127 * (math.sin(hue + 4 * math.pi / 3) + 1))

            dpg.configure_item(tag, color=(r, g, b))
            dpg.set_value(tag, f"BINARY ELITE BOT V{CURRENT_VERSION}")

            hue += 0.1
            await asyncio.sleep(0.1)

        except Exception as e:
            print(f"Erro no efeito RGB: {e}")
            await asyncio.sleep(0.7)


class TimedCache:
    def __init__(self, maxsize=100, ttl=1):
        self.maxsize = maxsize
        self.ttl = ttl
        self.cache = OrderedDict()

    async def get_or_set(self, key, func):
        now = time.time()
        if key in self.cache:
            result, timestamp = self.cache[key]
            if now - timestamp <= self.ttl:
                return result

        result = await func()
        self.cache[key] = (result, now)
        if len(self.cache) > self.maxsize:
            self.cache.popitem(last=False)
        return result


proposal_cache = TimedCache(maxsize=100, ttl=1)


async def check_connection_health():
    while is_running:
        if not api or not api.check_connect or not websocket_client or not websocket_client.sock or not websocket_client.sock.connected:
            await unified_reconnect("all")
        await asyncio.sleep(30)



class LucroMonitor:
    def __init__(self):
        self.ultimo_lucro = 0.0
        self.contagem_igual = 0
        self.max_contagem_igual = 3  # Número máximo de vezes que o lucro pode permanecer igual
        self._travado = False

    @property
    def travado(self):
        return self._travado

    def verificar_atualizacao(self, novo_lucro):
        """
        Verifica se o lucro está atualizando corretamente.
        Retorna True se estiver ok, False se estiver travado.
        """
        try:
            if abs(novo_lucro - self.ultimo_lucro) < 0.0001:  # Considera valores muito próximos como iguais
                self.contagem_igual += 1
                print(f"Lucro permanece em ${novo_lucro:.2f} - Contagem: {self.contagem_igual}")

                if self.contagem_igual >= self.max_contagem_igual:
                    if not self._travado:
                        print(f"⚠️ Alerta: Lucro travado em ${novo_lucro:.2f}")
                        self._travado = True
                    return False
            else:
                # Lucro mudou, resetar contagem
                print(f"Lucro atualizado: ${self.ultimo_lucro:.2f} -> ${novo_lucro:.2f}")
                self.contagem_igual = 0
                self._travado = False

            self.ultimo_lucro = novo_lucro
            return True

        except Exception as e:
            print(f"Erro ao verificar atualização do lucro: {e}")
            return False

    def forcar_atualizacao(self):
        """
        Tenta forçar uma atualização do saldo quando travado
        """
        self.contagem_igual = 0
        self._travado = False
        print("Forçando atualização do lucro...")


lucro_monitor = LucroMonitor()


@robust_execution
async def process_order_result(api, contract_id, current_row_id, duration, symbol, signal):
    """Process order results with improved timeout and error handling - VERSÃO ML INTEGRADA"""
    global saldo_atual, lucro_total, row_id, cached_stake
    global should_send_orders, stop_message_sent, total_wins, total_losses
    global ml_strategy_active, trading_strategies, gales, tipo_sinal_original
    global antiloss_em_andamento, statistics_transactions

    # Add a set to track processed contracts if it doesn't exist
    if not hasattr(process_order_result, 'processed_contracts'):
        process_order_result.processed_contracts = set()

    # Check if this contract was already processed
    if contract_id in process_order_result.processed_contracts:
        print(f"Contract {contract_id} already processed - skipping")
        return True, "Already Processed"

    try:
        countdown_task = asyncio.create_task(
            start_countdown(current_row_id, duration, contract_id, api)
        )

        start_time = time.time()
        timeout = duration + 5
        check_interval = 0.2
        last_check = 0

        while time.time() - start_time < timeout:
            current_time = time.time()
            if current_time - last_check >= check_interval:
                result, profit = api.check_win(contract_id, False)
                last_check = current_time

                if result:
                    # Mark this contract as processed
                    process_order_result.processed_contracts.add(contract_id)

                    hora_fechamento = datetime.now().strftime('%H:%M:%S')
                    status = "Win" if profit > 0 else "Loss"
                    is_win = profit > 0

                    # =============================================
                    # INTEGRAÇÃO ML CORRIGIDA
                    # =============================================
                    if ml_strategy_active:
                        try:
                            # Importar as funções ML necessárias
                            from ml_strategy import process_ml_feedback, trading_strategies
                            
                            # Verificar se temos a estratégia para este símbolo
                            if symbol in trading_strategies:
                                print(f"🤖 Processando feedback ML para {symbol}")
                                
                                # Determinar o tipo de ação baseado no sinal original
                                action_type = None
                                if hasattr(signal, 'upper'):
                                    action_type = signal.upper()  # 'CALL' ou 'PUT'
                                elif tipo_sinal_original:
                                    action_type = tipo_sinal_original.upper()
                                
                                # Se ainda não temos o tipo, tentar inferir do profit
                                if not action_type:
                                    action_type = "CALL" if profit > 0 else "PUT"
                                
                                # Determinar se foi uma recuperação de gale
                                gale_recovery = gales > 0 and is_win
                                
                                # Obter dados das velas para o feedback
                                # Nota: Você pode precisar ajustar esta parte dependendo de como
                                # você armazena os dados das velas
                                velas_data = None
                                if hasattr(api, 'velas_data') and symbol in api.velas_data:
                                    velas_data = api.velas_data[symbol]
                                
                                # Processar feedback ML
                                if velas_data and len(velas_data) > 0:
                                    success = process_ml_feedback(
                                        symbol=symbol,
                                        win=is_win,
                                        velas_data=velas_data,
                                        action_type=action_type,
                                        gale_level=gales,
                                        gale_recovery=gale_recovery
                                    )
                                    
                                    if success:
                                        print(f"✅ Feedback ML processado para {symbol}: {status}")
                                        if gale_recovery:
                                            print(f"🎯 Recuperação em Gale {gales} registrada")
                                    else:
                                        print(f"⚠️ Falha ao processar feedback ML para {symbol}")
                                else:
                                    print(f"⚠️ Dados de velas não disponíveis para feedback ML: {symbol}")
                                    
                                    # Alternativa: usar dados básicos do contrato
                                    # Criar dados dummy baseados no resultado
                                    dummy_velas = create_dummy_velas_from_contract(
                                        contract_id, symbol, profit, start_time
                                    )
                                    
                                    if dummy_velas:
                                        success = process_ml_feedback(
                                            symbol=symbol,
                                            win=is_win,
                                            velas_data=dummy_velas,
                                            action_type=action_type,
                                            gale_level=gales,
                                            gale_recovery=gale_recovery
                                        )
                                        print(f"📊 Feedback ML com dados estimados: {symbol}")
                            else:
                                print(f"⚠️ Estratégia ML não encontrada para {symbol}")
                                
                        except Exception as ml_error:
                            print(f"❌ Erro no processamento ML para {symbol}: {ml_error}")
                            import traceback
                            traceback.print_exc()

                    # =============================================
                    # PROCESSAMENTO NORMAL CONTINUA
                    # =============================================
                    if not antiloss_em_andamento:
                        lucro_total += profit

                        new_transaction = {
                            "Par": symbol,
                            "W/L": status,
                            "Tipo Sinal": tipo_sinal_original if gales == 0 else f"Gale {gales}",
                            "Profit": profit,
                            "Hora de Abertura": datetime.now(),
                            "Gales": gales,
                            "Entrada": cached_stake,
                            "Contract_ID": contract_id,
                        }

                        if not any(t.get("Contract_ID") == contract_id for t in statistics_transactions):
                            statistics_transactions.append(new_transaction)
                            save_transactions()

                    update_order_in_table(current_row_id, hora_fechamento, duration, status)
                    update_status()

                    # Handle stops
                    if lucro_total >= STOP_WIN and not stop_message_sent:
                        await handle_stop_win(symbol, tipo_sinal_original, lucro_total)
                        await enviar_stop_telegram(True)
                    elif lucro_total <= -STOP_LOSS and not stop_message_sent:
                        await handle_stop_loss(symbol, tipo_sinal_original, lucro_total)
                        await enviar_stop_telegram(False)

                    # Cleanup
                    if contract_id in api.resultados:
                        del api.resultados[contract_id]
                    api.active_subscriptions.discard(f"proposal_open_contract_{contract_id}")

                    return True, status

            await asyncio.sleep(0.1)

        print(f"Timeout waiting for contract {contract_id} result")
        return False, None

    except Exception as e:
        print(f"Error processing order result: {e}")
        traceback.print_exc()
        return False, None


def create_dummy_velas_from_contract(contract_id, symbol, profit, start_time):
    """
    Cria dados de velas dummy baseados no resultado do contrato
    quando dados reais não estão disponíveis
    """
    try:
        # Simular dados de velas básicos
        base_price = 1.0  # Preço base
        
        # Gerar dados de velas dummy para os últimos 100 períodos
        dummy_velas = []
        
        for i in range(100):
            # Simular movimento de preço
            variation = (i - 50) * 0.0001  # Variação gradual
            
            open_price = base_price + variation
            close_price = open_price + (0.0001 if profit > 0 else -0.0001)
            high_price = max(open_price, close_price) + 0.0002
            low_price = min(open_price, close_price) - 0.0002
            
            vela = {
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': 1000
            }
            
            dummy_velas.append(vela)
        
        return dummy_velas
        
    except Exception as e:
        print(f"❌ Erro ao criar dados dummy: {e}")
        return None


# =============================================
# FUNÇÃO AUXILIAR PARA INTEGRAÇÃO
# =============================================

def ensure_ml_integration():
    """
    Garante que a integração ML está funcionando corretamente
    """
    try:
        from ml_strategy import trading_strategies, get_strategy_stats
        
        if trading_strategies:
            print(f"🤖 ML Integration Status: {len(trading_strategies)} strategies active")
            
            # Mostrar estatísticas básicas
            stats = get_strategy_stats()
            if stats and 'overall' in stats:
                overall = stats['overall']
                print(f"📊 Overall ML Stats: {overall['total_trades']} trades, "
                      f"{overall['win_rate']:.1f}% win rate")
            
            return True
        else:
            print("⚠️ No ML strategies found")
            return False
            
    except ImportError:
        print("❌ ML strategy module not available")
        return False
    except Exception as e:
        print(f"❌ Error checking ML integration: {e}")
        return False


# =============================================
# EXEMPLO DE USO NO INÍCIO DO BOT
# =============================================

async def initialize_bot_with_ml():
    """
    Exemplo de como inicializar o bot com integração ML
    """
    try:
        # Verificar integração ML
        ml_available = ensure_ml_integration()
        
        if ml_available:
            print("✅ Bot inicializado com suporte ML completo")
            global ml_strategy_active
            ml_strategy_active = True
        else:
            print("⚠️ Bot inicializado sem suporte ML")
            ml_strategy_active = False
            
        return ml_available
        
    except Exception as e:
        print(f"❌ Erro na inicialização ML: {e}")
        return False


async def handle_stop_win(symbol, tipo_sinal, lucro_total):
    """Função auxiliar para processar Stop Win"""
    add_stop_line_to_table(symbol, tipo_sinal, True, lucro_total)
    if telegram_ativado and chat_id_value and bot_token:
        await enviar_stop_telegram(True)  # Adicionar aqui
    should_send_orders = False
    stop_message_sent = True
    dpg.configure_item("toggle_button", label="INICIAR")
    update_button_image("toggle_button", "play.png")
    dpg.set_value("bot_status_text", "Bot Pausado - Take Profit Atingido")
    controlar_seletor_ativo(True)

async def handle_stop_loss(symbol, tipo_sinal, lucro_total):
    """Função auxiliar para processar Stop Loss"""
    add_stop_line_to_table(symbol, tipo_sinal, False, abs(lucro_total))
    if telegram_ativado and chat_id_value and bot_token:
        await enviar_stop_telegram(False)  # Adicionar aqui
    should_send_orders = False
    stop_message_sent = True
    dpg.configure_item("toggle_button", label="INICIAR")
    update_button_image("toggle_button", "play.png")
    dpg.set_value("bot_status_text", "Bot Pausado - Stop Loss Atingido")
    controlar_seletor_ativo(True)

def add_stop_line_to_table(symbol, tipo_sinal, is_win, lucro_atual):
    """Adiciona linha de STOP WIN/LOSS no topo da tabela e interrompe as ordens"""
    global should_send_orders, stop_message_sent, is_running, total_wins, total_losses, initial_balance

    try:
        hora_atual = datetime.now().strftime('%H:%M:%S')
        stop_text = language_manager.get_text("STOP_WIN_ATINGIDO") if is_win else language_manager.get_text("STOP_LOSS_ATINGIDO")
        stop_text = stop_text.format(abs(lucro_atual))
        stop_color = (0, 255, 0) if is_win else (255, 0, 0)

        # Interrompe as ordens imediatamente
        should_send_orders = False
        stop_message_sent = True

        # Atualiza interface
        dpg.configure_item("toggle_button", label=language_manager.get_text("INICIAR"))
        update_button_image("toggle_button", "play.png")
        dpg.set_value("bot_status_text", language_manager.get_text("BOT_PAUSADO") + " - Stop Atingido")
        controlar_seletor_ativo(True)

        # Pega a primeira linha da tabela para inserir antes dela
        rows = dpg.get_item_children("transactions_table", 1)
        first_row = rows[0] if rows else None

        with dpg.table_row(parent="transactions_table", before=first_row):
            dpg.add_text(hora_atual, color=stop_color)  # Hora
            dpg.add_text(hora_atual, color=stop_color)  # Hora fechamento
            dpg.add_text(tipo_sinal, color=stop_color)  # Tipo sinal
            dpg.add_text("---", color=stop_color)  # Entrada
            dpg.add_text("---", color=stop_color)  # Par
            dpg.add_text("---", color=stop_color)  # Gales
            dpg.add_text("---", color=stop_color)  # Direção
            dpg.add_text("---", color=stop_color)  # Duração
            dpg.add_text("---", color=stop_color)  # Win/Loss
            dpg.add_text(stop_text, color=stop_color)  # Comentário

        # Envia mensagem para o Telegram de forma assíncrona
        if telegram_ativado:
            total_operacoes = total_wins + total_losses
            winrate = (total_wins / total_operacoes * 100) if total_operacoes > 0 else 0
            hora_atual = datetime.now().strftime('%H:%M:%S')

            if is_win:
                mensagem = (
                    f"🎯{language_manager.get_text('STOP_WIN_ATINGIDO')}: $ {abs(lucro_atual):.2f}\n\n"
                    f"⏰{language_manager.get_text('HORA_ATUAL')}: {hora_atual}\n"
                    f"💰{language_manager.get_text('LUCRO_ATUAL')}: $ {abs(lucro_atual):.2f}\n\n"
                    f"📊{language_manager.get_text('ESTATISTICAS')}:\n"
                    f"✅{language_manager.get_text('WINS')}: {total_wins}\n"
                    f"❌{language_manager.get_text('LOSSES')}: {total_losses}\n"
                    f"📈{language_manager.get_text('WINRATE')}: {winrate:.1f}%\n\n"
                    f"💵{language_manager.get_text('SALDO_INICIAL')}: $ {initial_balance:.2f}\n"
                    f"💵{language_manager.get_text('SALDO_ATUAL')}: $ {saldo_atual:.2f}\n\n"
                    f"💵{language_manager.get_text('PARABENS')}! {language_manager.get_text('META_LUCRO_ATINGIDA')}!"
                )
            else:
                mensagem = (
                    f"🛑{language_manager.get_text('STOP_LOSS_ATINGIDO')}: $ {abs(lucro_atual):.2f}\n\n"
                    f"⏰{language_manager.get_text('HORA_ATUAL')}: {hora_atual}\n"
                    f"💸{language_manager.get_text('PERDA_TOTAL')}: $ {abs(lucro_atual):.2f}\n\n"
                    f"📊{language_manager.get_text('ESTATISTICAS')}:\n"
                    f"✅{language_manager.get_text('WINS')}: {total_wins}\n"
                    f"❌{language_manager.get_text('LOSSES')}: {total_losses}\n"
                    f"📈{language_manager.get_text('WINRATE')}: {winrate:.1f}%\n\n"
                    f"💵{language_manager.get_text('SALDO_INICIAL')}: $ {initial_balance:.2f}\n"
                    f"💵{language_manager.get_text('SALDO_ATUAL')}: $ {saldo_atual:.2f}\n\n"
                    f"⚠️{language_manager.get_text('LIMITE_PERDA_ATINGIDO')}. {language_manager.get_text('ENCERRANDO_OPERACOES')}."
                )

            # Cria uma task para enviar a mensagem de forma assíncrona
            asyncio.create_task(enviar_mensagem_telegram(mensagem, chat_id_value, bot_token))

            # Envia sticker apropriado
            sticker_id = (
                "CAACAgEAAxkBAAENS5NnVfROJrTNnr5KAQSrCJSKetnUFwACBQQAAn7ngAK73FMZOonu0DYE" if is_win
                else "CAACAgQAAxkBAAENS5dnVfTk4WVsM3hzKtJZY-dwkFKxKQAChwsAAvg9UFBvYUEMvlcVLTYE"
            )
            asyncio.create_task(enviar_sticker_telegram(sticker_id, chat_id_value, bot_token))

        print(f"Nova linha de {language_manager.get_text('STOP_WIN_ATINGIDO') if is_win else language_manager.get_text('STOP_LOSS_ATINGIDO')} adicionada à tabela")

        # Salva as transações após adicionar a linha
        save_transactions()

        return True
    except Exception as e:
        print(f"Erro ao adicionar linha de stop: {e}")
        traceback.print_exc()
        return False


def reset_stop_message():
    """Reseta o estado da mensagem de stop"""
    global stop_message_sent
    stop_message_sent = False


async def check_stop_conditions():
    """Verifica condições de stop win/loss usando apenas lucro dos contratos"""
    global should_send_orders, lucro_total

    try:
        # Usa diretamente o lucro_total que já está sendo calculado pelos contratos
        if lucro_total >= STOP_WIN:
            print(f"Stop Win atingido - Lucro: ${lucro_total:.2f}")
            should_send_orders = False
            return True
        elif lucro_total <= -STOP_LOSS:
            print(f"Stop Loss atingido - Perda: ${abs(lucro_total):.2f}")
            should_send_orders = False
            return True

        # Log periódico do lucro
        print(f"\n=== Verificação de Stops ===")
        print(f"Lucro atual: ${lucro_total:.2f}")
        print(f"Stop Win: ${STOP_WIN:.2f}")
        print(f"Stop Loss: ${STOP_LOSS:.2f}")
        print("==========================\n")

        return False

    except Exception as e:
        print(f"❌ Erro ao verificar condições de stop: {e}")
        traceback.print_exc()
        return False


async def periodic_stop_check():
    """Verifica stops periodicamente"""
    while is_running:
        try:
            if await check_stop_conditions():
                print("Condição de stop atingida - parando operações")
                should_send_orders = False
            await asyncio.sleep(14)
        except Exception as e:
            print(f"Erro na verificação periódica de stops: {e}")
            await asyncio.sleep(14)


async def enviar_resultados_telegram(resultado):
    """Envia resultados profissionais para o Telegram com símbolos universais"""
    global total_wins, total_losses, lucro_total, chat_id_value, bot_token, last_symbol

    try:
        if not telegram_ativado or not chat_id_value or not bot_token:
            return

        # Calcula winrate de forma segura
        total_operacoes = total_wins + total_losses
        winrate = (total_wins / total_operacoes * 100) if total_operacoes > 0 else 0

        # Obtém o nome amigável do par com tratamento de erro
        symbol_display = "Unknown"
        if 'last_symbol' in globals() and last_symbol:
            symbol_display = get_display_name(last_symbol)



        # Emojis universais
        if resultado == "Win":
            mensagem = (
                f"✅ TRADE WIN \n\n"
                f"📊 TRADING STATS:\n"
                f"📈 PAIR: {symbol_display}\n"
                f"🎯 WINS: {total_wins}\n"
                f"❌ LOSS: {total_losses}\n"
                f"📊 WINRATE: {winrate:.1f}%\n"
                f"💰 PROFIT: ${lucro_total:.2f}\n\n"
                f"🕒 {datetime.now().strftime('%H:%M:%S')}"
            )
        else:
            mensagem = (
                f"⛔️ TRADE LOSS \n\n"
                f"📊 TRADING STATS:\n"
                f"📈 PAIR: {symbol_display}\n"
                f"🎯 WINS: {total_wins}\n"
                f"❌ LOSS: {total_losses}\n"
                f"📊 WINRATE: {winrate:.1f}%\n"
                f"💰 PROFIT: ${lucro_total:.2f}\n\n"
                f"🕒 {datetime.now().strftime('%H:%M:%S')}"
            )


        await enviar_mensagem_telegram(mensagem, chat_id_value, bot_token)

        print(f"✅ Resultado enviado ao Telegram: {resultado}")

    except Exception as e:
        print(f"❌ Erro ao enviar resultados para Telegram: {e}")
        traceback.print_exc()

async def enviar_stop_telegram(is_win):
    """Envia mensagem de Stop Win/Loss para o Telegram"""
    try:
        total_operacoes = total_wins + total_losses
        winrate = (total_wins / total_operacoes * 100) if total_operacoes > 0 else 0
        hora_atual = datetime.now().strftime('%H:%M:%S')

        if is_win:
            mensagem = (
                f"🎯 TAKE PROFIT REACHED!\n\n"
                f"📊 FINAL STATS:\n"
                f"✅ WINS: {total_wins}\n"
                f"❌ LOSS: {total_losses}\n"
                f"📈 WINRATE: {winrate:.1f}%\n"
                f"💰 TOTAL PROFIT: ${abs(lucro_total):.2f}\n\n"
                f"💵 INITIAL BALANCE: ${initial_balance:.2f}\n"
                f"💵 FINAL BALANCE: ${saldo_atual:.2f}\n\n"
                f"🎉 CONGRATULATIONS! TARGET REACHED!\n"
                f"🕒 {hora_atual}"
            )

        else:
            mensagem = (
                f"🛑 STOP LOSS REACHED!\n\n"
                f"📊 FINAL STATS:\n"
                f"✅ WINS: {total_wins}\n"
                f"❌ LOSS: {total_losses}\n"
                f"📈 WINRATE: {winrate:.1f}%\n"
                f"💸 TOTAL LOSS: ${abs(lucro_total):.2f}\n\n"
                f"💵 INITIAL BALANCE: ${initial_balance:.2f}\n"
                f"💵 FINAL BALANCE: ${saldo_atual:.2f}\n\n"
                f"⚠️ LOSS LIMIT REACHED - STOPPING OPERATIONS\n"
                f"🕒 {hora_atual}"
            )


        await enviar_sticker_telegram(sticker_id, chat_id_value, bot_token)
        await enviar_mensagem_telegram(mensagem, chat_id_value, bot_token)

    except Exception as e:
        print(f"Erro ao enviar mensagem de stop: {e}")
        traceback.print_exc()

# Função para atualizar saldo com retry
async def update_gui_after_login(mode):
    """Atualiza a interface após o login com tratamento robusto do saldo"""
    global saldo_atual, initial_balance, lucro_total

    try:
        # Atualiza texto de conexão
        if dpg.does_item_exist("success_message"):
            dpg.set_value("success_message", f"Conectado com sucesso na conta {mode}!")
            dpg.show_item("success_message")

        # Atualiza botões e controles
        if dpg.does_item_exist("logar_button"):
            dpg.configure_item("logar_button", label="Logado", enabled=False)

        if dpg.does_item_exist("toggle_button"):
            dpg.enable_item("toggle_button")

        if dpg.does_item_exist("token_mode"):
            dpg.enable_item("token_mode")

        # Atualiza saldo e lucro na interface
        if dpg.does_item_exist("saldo_text"):
            dpg.set_value("saldo_text", f"$ {saldo_atual:.2f}")
            print(f"Saldo atualizado na interface: ${saldo_atual:.2f}")

        if dpg.does_item_exist("pnl_text"):
            dpg.set_value("pnl_text", f"$ {lucro_total:.2f}")
            dpg.configure_item("pnl_text", color=(0, 255, 0) if lucro_total >= 0 else (255, 0, 0))
            print(f"Lucro atualizado na interface: ${lucro_total:.2f}")

        print("Interface gráfica atualizada com sucesso após o login.")

        # Esconder a mensagem após 3 segundos
        await asyncio.sleep(2)
        dpg.hide_item("success_message")

    except Exception as e:
        print(f"Erro ao atualizar a interface gráfica após o login: {e}")
        import traceback
        traceback.print_exc()


async def atualizar_saldo(api):
    """Atualiza apenas o saldo, sem modificar o lucro"""
    global saldo_atual

    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            if not api or not api.check_connect:
                print("API desconectada - tentando reconexão")
                api = await unified_reconnect("all", force=True)
                if not api:
                    continue

            # Força reinscrição no saldo
            json_data = json.dumps({"forget_all": "balance"})
            api.ws.send(json_data)
            await asyncio.sleep(0.5)

            # Nova subscrição
            json_data = json.dumps({"balance": 1, "subscribe": 1})
            api.ws.send(json_data)

            # Aguarda resposta com timeout
            timeout = 10
            start_time = time.time()
            while time.time() - start_time < timeout:
                balance = api.get_balance()
                if balance is not None:
                    saldo_atual = float(balance)

                    # Atualiza apenas display de saldo, não o lucro
                    if dpg.does_item_exist("saldo_text"):
                        dpg.set_value("saldo_text", f"$ {saldo_atual:.2f}")

                    print(f"Saldo atualizado: ${saldo_atual:.2f}")
                    return saldo_atual

                await asyncio.sleep(0.5)

            print(f"Timeout na tentativa {attempt + 1} de atualizar saldo")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2

        except Exception as e:
            print(f"Erro ao atualizar saldo (tentativa {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
                retry_delay *= 2

    print("Todas as tentativas de atualização de saldo falharam")
    return None


# Monitor dedicado para lucro
async def monitor_profit():
    """Monitor dedicado para lucro e saldo"""
    global lucro_monitor, saldo_atual, initial_balance, lucro_total

    while is_running:
        try:
            # Atualiza saldo
            new_balance = await update_balance_safe()
            if new_balance is not None:
                # Calcula novo lucro
                new_profit = new_balance - initial_balance

                # Verifica se o lucro está atualizando corretamente
                if not lucro_monitor.verificar_atualizacao(new_profit):
                    print("⚠️ Possível travamento do lucro detectado")
                    await unified_reconnect("api", force=True)
                else:
                    lucro_total = new_profit
                    # Atualiza interface
                    update_status()

            await asyncio.sleep(15)  # Verifica a cada 15 segundos

        except Exception as e:
            print(f"❌ Erro no monitor de lucro: {e}")
            await asyncio.sleep(5)


async def start_bot():
    global api_token, symbols, velas, ultimas_velas, first_initialization
    global stop_event, is_running, is_shutting_down, ws_manager, should_send_orders
    global api, cached_stake, masaniello, saldo_atual, initial_balance
    global telegram_interface, telegram_manager  # Importante declarar ambos como global

    if not api_token:
        print("Por favor, insira o token antes de iniciar o bot.")
        abrir_popup_token()
        return

    try:
        print("\n=== Iniciando Bot ===")

        # Inicialização da API
        api = await inicializar_api()
        if not api:
            print("❌ Falha ao inicializar API")
            return

        print("\n=== Verificando estado do Telegram ===")
        print(f"Interface Telegram: {'Presente' if telegram_interface else 'Ausente'}")
        print(f"Manager Telegram: {'Presente' if telegram_manager else 'Ausente'}")

        telegram_success = await initialize_telegram()
        if not telegram_success:
            print("⚠️ Aviso: Falha ao inicializar Telegram")

        # Se não tiver telegram_manager, tenta recuperar
        if not telegram_manager and telegram_interface:
            telegram_manager = telegram_interface.get_telegram_manager()
            print(f"Manager recuperado: {'Sim' if telegram_manager else 'Não'}")

        # Garante estado inicial correto
        if not inicializar_estado_bot():
            print("❌ Falha ao inicializar estado do bot")
            return



        # Atualização inicial do saldo
        await atualizar_saldo(api)
        initial_balance = saldo_atual
        lucro_total = 0.0

        # Configuração inicial do stake
        if cached_stake is None:
            if gerenciamento_ativo == "Masaniello":
                cached_stake = masaniello.getStake()
            else:  # Ciclos
                matriz = configuracoes_gerenciamentos["Ciclos"]["matriz_ciclos"]
                cached_stake = float(matriz[0][0])

        print(f"✅ Saldo inicial: ${initial_balance:.2f}")
        print(f"✅ Stake inicial: ${cached_stake:.2f}")

        # Iniciar conexões e verificações
        is_running = True
        should_send_orders = True
        stop_event.clear()

        # Iniciar tasks de monitoramento
        tasks = [
            asyncio.create_task(check_connection_health()),
            asyncio.create_task(start_rgb_effect_during_sample()),
            asyncio.create_task(periodic_stop_check()),
            asyncio.create_task(monitor_profit()),
            asyncio.create_task(monitor_telegram_queue()),
        ]

        print("🔄 Iniciando loop principal do bot...")
        await sample_calls()

    except Exception as e:
        print(f"❌ Erro durante a execução do bot: {e}")
        import traceback
        traceback.print_exc()
        is_running = False
        stop_event.set()
    finally:
        update_gui_state(is_running)
        # Cancela todas as tasks pendentes
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()


async def verify_connection_before_order(api):
    """
    Verifica a conexão da API antes de enviar uma ordem.

    Args:
        api: Instância da API
    Returns:
        bool: True se a conexão está ok, False caso contrário
    """
    try:
        if not api or not api.check_connect:
            print("\n=== Verificando Conexão API ===")
            success = await unified_reconnect("api")
            if not success:
                print("❌ Falha ao reconectar API")
                return False

        # Verifica saldo como teste de conexão
        saldo = await atualizar_saldo(api)
        if saldo is None:
            print("❌ Falha ao verificar saldo")
            return False

        return True

    except Exception as e:
        print(f"❌ Erro ao verificar conexão: {e}")
        import traceback
        traceback.print_exc()
        return False


def validate_operation(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if not should_send_orders or stop_event.is_set():
            return None
        return await func(*args, **kwargs)
    return wrapper


def get_line_max_gales(linha_atual):
    """
    Determina o número máximo de gales disponíveis para uma linha específica da matriz.
    O número de gales é calculado dinamicamente baseado nos valores não-zero após a entrada inicial.

    Args:
        linha_atual (int): Índice da linha atual na matriz (0-4)

    Returns:
        int: Número máximo de gales disponíveis para a linha
    """
    try:
        matriz = configuracoes_gerenciamentos["Ciclos"]["matriz_ciclos"]

        if linha_atual < 0 or linha_atual >= len(matriz):
            print(f"Erro: Linha {linha_atual} fora dos limites da matriz")
            return 0

        linha = matriz[linha_atual]

        # Conta quantos valores maiores que zero existem após o valor de entrada
        gales_disponiveis = 0
        for valor in linha[1:]:  # Começando do segundo valor
            if isinstance(valor, (int, float)) and valor > 0:
                gales_disponiveis += 1
            else:
                break  # Para quando encontrar um valor zero ou inválido

        print(f"\n=== Análise de Gales da Linha {linha_atual + 1} ===")
        print(f"Entrada inicial: {linha[0]}")
        print(f"Valores de gale disponíveis: {[linha[i] for i in range(1, gales_disponiveis + 1)]}")
        print(f"Número máximo de gales: {gales_disponiveis}")

        return gales_disponiveis

    except Exception as e:
        print(f"Erro ao calcular máximo de gales para linha {linha_atual}: {e}")
        import traceback
        traceback.print_exc()
        return 0


def calculate_candle_expiration(timeframe):
    try:
        now = datetime.now()
        current_minute = now.minute
        current_second = now.second

        minutes = int(timeframe)
        current_candle_start = (current_minute // minutes) * minutes
        next_candle_start = current_candle_start + minutes

        remaining_minutes = next_candle_start - current_minute - 1
        remaining_seconds = 60 - current_second

        total_seconds = (remaining_minutes * 60) + remaining_seconds - 2

        print(f"\n=== Cálculo de Expiração ===")
        print(f"Hora atual: {now.strftime('%H:%M:%S')}")
        print(f"Minuto atual: {current_minute}")
        print(f"Segundo atual: {current_second}")
        print(f"Próxima vela: {next_candle_start}:00")
        print(f"Tempo restante: {total_seconds}s")

        if total_seconds < 15:
            print("⚠️ Tempo insuficiente, mínimo de 15s necessário")
            return None

        return total_seconds

    except Exception as e:
        print(f"❌ Erro ao calcular expiração: {e}")
        return None



@validate_operation
async def sample_calls():
    """Analisa estratégias continuamente para todos os símbolos ativos."""
    global gales, total_wins, total_losses, saldo_atual, initial_balance, lucro_total, cached_stake
    global symbols, api_token, masaniello, transactions, statistics_transactions, last_symbol, last_signal, NumeroDeGales
    global stop_event, row_id, api, last_sample_run, antiloss_ativado, should_send_orders, antiloss_em_andamento
    global is_running, tipo_sinal_original, fluxo_active, mt4_receiver, stop_message_sent, symbol, sinal
    global ultimo_par_negociado, gerenciamento_ativo, default_expiration, modo_entrada, fim_da_vela_time, modo_gale

    try:
        print("\n=== Iniciando sample_calls ===")
        if not velas or any(len(velas.get(symbol, [])) < 100 for symbol in symbols):
            success = await inicializar_velas()
            if not success:
                return

        api = await inicializar_api()
        if not api:
            return

        await atualizar_saldo(api)
        initial_balance = saldo_atual if not initial_balance else initial_balance
        verificar_velas_antiloss.current_losses = 0

        print(f"✅ Saldo inicial: ${initial_balance:.2f}")
        print(f"✅ Stake inicial: ${cached_stake:.2f}")
        print(f"✅ Modo de entrada: {modo_entrada}")
        print(f"✅ Timeframe: M{default_expiration}")
        print(f"✅ Modo de gale: {modo_gale}")

        while not stop_event.is_set():
            try:
                if not should_send_orders or stop_message_sent:
                    await asyncio.sleep(1)
                    continue

                await asyncio.sleep(1)

                # Determina o stake atual baseado no gerenciamento
                if gerenciamento_ativo == "Masaniello":
                    current_stake = max(cached_stake or 1.0, 0.35)
                else:
                    config = configuracoes_gerenciamentos["Ciclos"]
                    linha_atual = config["linha_atual"]
                    coluna_atual = config["coluna_atual"]
                    matriz = config["matriz_ciclos"]
                    current_stake = float(matriz[linha_atual][coluna_atual])
                    if current_stake <= 0:
                        await asyncio.sleep(0.5)
                        continue

                # Processamento de gales
                # Processamento de gales
                if gales > 0 and last_symbol and last_signal:
                    symbol = last_symbol
                    if modo_gale == "zigzag":
                        sinal = "PUT" if last_signal == "CALL" else "CALL"
                        print(f"✨ Gale {gales} - Modo ZigZag - Invertendo sinal de {last_signal} para {sinal}")
                    else:
                        sinal = last_signal
                        print(f"✨ Gale {gales} - Modo Normal - Mantendo sinal {sinal}")

                    sinal_info = (symbol, sinal)

                    # MODIFICAÇÃO PARA PRESERVAR DURAÇÃO DO TELEGRAM
                    # Verifica se há uma duração específica do último sinal
                    if hasattr(verificar_e_enviar_sinais,
                               'last_signal_info') and 'duration' in verificar_e_enviar_sinais.last_signal_info:
                        duracao = verificar_e_enviar_sinais.last_signal_info['duration']
                        duration_unit = "s"
                        print(f"✨ Gale preservando duração do Telegram: {duracao}s")
                    else:
                        # Fallback para o método padrão
                        if modo_entrada == "fim_da_vela":
                            duracao = calculate_candle_expiration(default_expiration)
                            if duracao is None:
                                print("❌ Tempo insuficiente para gale")
                                await asyncio.sleep(0.5)
                                continue
                            duration_unit = "s"
                        else:
                            if symbol.startswith("stpRNG"):
                                duracao = 2
                                duration_unit = "t"
                            else:
                                duracao = default_expiration * 60 - 2
                                duration_unit = "s"

                    print(f"✅ Gale com duração: {duracao}{duration_unit}")

                    antiloss_ativado_local = False

                # Processamento de novos sinais
                else:
                    result = await verificar_e_enviar_sinais(api, symbols)
                    if not result:
                        await asyncio.sleep(0.5)
                        continue

                    sinal_info, is_retracao, duracao_padrao, antiloss_ativado_local, row_id = result
                    if not sinal_info:
                        continue

                    symbol, sinal = sinal_info
                    last_symbol = symbol  # Atualiza o símbolo atual
                    last_signal = sinal   # Atualiza o sinal atual

                    # Cálculo da duração para novas entradas
                    if modo_entrada == "fim_da_vela":
                        print("\n=== Processando Nova Ordem no Modo Fim da Vela ===")
                        duracao = calculate_candle_expiration(default_expiration)
                        if duracao is None:
                            print("❌ Tempo insuficiente para entrada")
                            if mt4_receiver and mt4_receiver.is_processing_order:
                                mt4_receiver.mark_order_complete()
                            await asyncio.sleep(0.5)
                            continue
                        print(f"✅ Entrada com {duracao}s até o fim da vela")
                        duration_unit = "s"
                    else:
                        if symbol.startswith("stpRNG"):
                            duracao = 2
                            duration_unit = "t"
                        else:
                            duracao = default_expiration * 60 - 2
                            duration_unit = "s"
                        print(f"✅ Entrada com duração: {duracao}{duration_unit}")

                # Prepara informações para a ordem
                tipo_sinal_original = (
                    "Externo" if mt4_receiver and mt4_receiver.is_processing_order else
                    "Fluxo" if fluxo_active else  "PPONetwork" if ml_strategy_active  else  "ABR" if abr_strategy_active else "Retracao"  if is_retracao else "Reversao"
                )

                hora_abertura = datetime.now().strftime("%H:%M:%S")
                duracao_display = "2T" if symbol.startswith("stpRNG") else f"M{default_expiration}"

                # Adiciona ordem na tabela
                row_id = add_open_order_to_table(
                    hora_abertura,
                    current_stake,
                    symbol,
                    sinal,
                    duracao_display,
                    gales,
                    is_retracao if not gales else False,
                    antiloss_ativado_local
                )

                try:
                    # Verifica conexão antes de enviar ordem
                    await verify_connection_before_order(api)

                    print(f"\n=== Enviando Ordem ===")
                    print(f"Par: {symbol}")
                    print(f"Direção: {sinal}")
                    print(f"Stake: ${current_stake:.2f}")
                    print(f"Duração: {duracao}{duration_unit}")

                    # Processa ordem
                    if hedge_active and symbol.startswith("stpRNG"):
                        success, contract_info = await process_hedge_entry(
                            api, symbol, current_stake, sinal, duracao
                        )
                    else:
                        success, contract_info = api.buy(
                            par=symbol,
                            entrada=round(current_stake, 2),
                            dir=sinal,
                            timeframe=duracao,
                            duration_unit=duration_unit
                        )

                    # Verifica sucesso da ordem
                    if not success:
                        update_order_in_table(
                            row_id,
                            datetime.now().strftime("%H:%M:%S"),
                            0,
                            "Erro",
                            f"Falha ao enviar ordem: {contract_info}"
                        )
                        last_symbol = None
                        last_signal = None
                        continue

                    # Processa resultado
                    resultado, status = await process_order_result(
                        api, contract_info, row_id, duracao, symbol, sinal
                    )

                    if resultado:
                        if status == "Win":
                            await process_win(row_id)
                            ultimo_par_negociado = symbol
                            last_symbol = None
                            last_signal = None
                        else:
                            should_continue_gale = await process_loss(row_id)
                            if not should_continue_gale:
                                gales = 0
                                ultimo_par_negociado = symbol
                                last_symbol = None
                                last_signal = None
                            else:
                                last_symbol = symbol
                                last_signal = sinal

                    update_status()

                except Exception as e:
                    print(f"❌ Erro ao processar ordem: {e}")
                    traceback.print_exc()
                    last_symbol = None
                    last_signal = None
                    continue

            except Exception as e:
                print(f"Erro no loop principal: {e}")
                traceback.print_exc()
                await asyncio.sleep(1)

    except Exception as e:
        print(f"Erro crítico em sample_calls: {e}")
        traceback.print_exc()
    finally:
        print("Sample calls finalizado")
        if api:
            await atualizar_saldo(api)
        update_status()
        save_transactions()


async def process_hedge_entry(api, symbol, stake, sinal, duracao):
    """Processa entrada hedge para pares STEP"""
    try:
        sinal_original = sinal
        sinal_hedge = "PUT" if sinal_original == "CALL" else "CALL"

        # Primeira ordem
        success1, contract_info1 = api.buy(
            par=symbol,
            entrada=round(stake, 2),
            dir=sinal_original,
            timeframe=duracao
        )

        # Segunda ordem (hedge)
        success2, contract_info2 = api.buy(
            par=symbol,
            entrada=round(stake, 2),
            dir=sinal_hedge,
            timeframe=duracao
        )

        if success1 and success2:
            print(f"✅ Entrada hedge processada: {symbol}")
            print(f"Contract 1: {contract_info1}")
            print(f"Contract 2: {contract_info2}")
            return True, [contract_info1, contract_info2]
        else:
            print(f"❌ Falha na entrada hedge: {symbol}")
            return False, None

    except Exception as e:
        print(f"❌ Erro ao processar hedge: {e}")
        return False, None


def show_welcome_popup():
    if dpg.does_item_exist("welcome_popup"):
        dpg.delete_item("welcome_popup")

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    window_width = 400
    window_height = 250
    pos_x = (viewport_width - window_width) // 2
    pos_y = (viewport_height - window_height) // 2

    with dpg.window(label=language_manager.get_text("ANUNCIO_GRUPO"), tag="welcome_popup", modal=True,
                    width=window_width, height=window_height, pos=[pos_x, pos_y], no_resize=True, no_close=True):
        dpg.add_spacer(height=10)
        dpg.add_text(language_manager.get_text("BEM_VINDO_BINARY_BOT"), tag="welcome_text", color=(255, 215, 0))
        dpg.add_separator()
        dpg.add_spacer(height=10)

        dpg.add_text(language_manager.get_text("ENTRE_GRUPO_TELEGRAM"),
                     color=(255, 255, 255), wrap=380)

        dpg.add_spacer(height=10)
        dpg.add_text(language_manager.get_text("LOGANDO_FECHAR_SEGUNDOS"), tag="timer_text")

        dpg.add_spacer(height=20)
        button_width = 200
        button_x = (window_width - button_width) // 2

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=button_x)
            dpg.add_button(label=language_manager.get_text("ACESSAR_GRUPO"), width=button_width, callback=lambda: open_telegram_group())

    def rgb_effect():
        hue = 0
        start_time = time.time()
        while dpg.does_item_exist("welcome_popup"):
            try:
                # Calcula cores RGB
                r = int(127 * (math.sin(hue) + 1))
                g = int(127 * (math.sin(hue + 2 * math.pi / 3) + 1))
                b = int(127 * (math.sin(hue + 4 * math.pi / 3) + 1))

                # Atualiza cor do texto do timer
                if dpg.does_item_exist("timer_text"):
                    elapsed = int(time.time() - start_time)
                    remaining = max(0, 6 - elapsed)
                    dpg.configure_item("timer_text", color=(r, g, b))
                    dpg.set_value("timer_text", f"{language_manager.get_text('LOGANDO_FECHAR')} {remaining} {language_manager.get_text('SEGUNDOS')}!")

                    # Fecha a janela após 8 segundos
                    if remaining == 0:
                        dpg.delete_item("welcome_popup")
                        break

                hue += 0.05
                time.sleep(0.05)

            except Exception as e:
                print(f"Erro no efeito RGB: {e}")
                break

    # Inicia o efeito RGB em uma thread separada
    threading.Thread(target=rgb_effect, daemon=True).start()

    # Timer separado para garantir que a janela feche
    def close_window():
        time.sleep(8)
        if dpg.does_item_exist("welcome_popup"):
            dpg.delete_item("welcome_popup")

    threading.Thread(target=close_window, daemon=True).start()


def open_telegram_group():
    import webbrowser
    webbrowser.open("https://t.me/Binaryelitevip")


def get_last_candles(symbol, lookback=20):
    """Gets the last N candles for a symbol with validation"""
    global velas

    try:
        if symbol not in velas:
            print(f"❌ No candles available for {symbol}")
            return []

        # Get last N candles
        candles = list(velas[symbol][-lookback:])

        if len(candles) < lookback:
            print(f"⚠️ Not enough candles for {symbol}: {len(candles)}/{lookback}")
            return candles

        print(f"✅ Got {len(candles)} candles for {symbol}")
        return candles

    except Exception as e:
        print(f"❌ Error getting candles for {symbol}: {e}")
        traceback.print_exc()
        return []


async def process_win(row_id):
    """Processa vitória com feedback detalhado para ML"""
    global total_wins, gales, cached_stake, lucro_total, last_symbol, last_signal
    global VerificaSeAntlossEstavaAtivo, antiloss_ativado, type_order, alvoresete
    global mt4_receiver, velas

    try:
        # Validação inicial
        if row_id is None:
            print("❌ row_id inválido")
            return

        if hasattr(process_win, 'last_processed_row') and process_win.last_processed_row == row_id:
            print("⚠️ Operação já processada para este row_id")
            return

        process_win.last_processed_row = row_id
        total_wins += 1

        if abr_strategy_active and tipo_sinal_original == "ABR":
            abr_strategy.record_result(symbol, True)  # Para win
            print(f"✅ Resultado ABR registrado: Win para {symbol}")

        if ml_strategy_active and last_symbol in trading_strategies:
            strategy = trading_strategies[last_symbol]

            if hasattr(velas[last_symbol], "__getitem__") and not isinstance(velas[last_symbol], (str, bytes)):
                # It's likely already a sequence, but let's make sure it supports slicing
                velas_sequence = list(velas[last_symbol])
                velas_data = velas_sequence[-20:] if len(velas_sequence) >= 20 else velas_sequence
            else:
                # It doesn't support slicing, so handle appropriately
                print(f"⚠️ velas[{last_symbol}] is not sliceable, type: {type(velas[last_symbol])}")
                velas_data = []

            if velas_data:  # Processa apenas se tiver dados
                # Determina se foi recuperação via gale
                gale_recovery = gales > 0

                # Pass all required parameters to process_trade_feedback
                strategy.process_trade_feedback(
                    win=True,
                    velas_data=velas_data,
                    action_type=last_signal,  # Pass the signal direction (CALL/PUT)
                    gale_level=gales,  # 0 if direct win, 1+ if win in gale
                    gale_recovery=gale_recovery  # True if recovered through gale
                )
                print(f"✅ ML feedback enviado para {last_symbol} - WIN (Gale: {gales}, Recovery: {gale_recovery})")
            else:
                print(f"❌ Unable to process ML feedback due to missing candles")

        # Libera o processamento de novos sinais
        shared_state.set_order_in_progress(False)

        # Processa Masaniello
        if gerenciamento_ativo == "Masaniello":
            cycle_reset, reset_message, remaining_trades = masaniello.win()
            mark_cycle_reset(row_id, reset_message, cycle_reset,
                             remaining_trades['wins'], remaining_trades['losses'])

            if cycle_reset:
                play_cash_sound()
                if VerificaSeAntlossEstavaAtivo:
                    antiloss_ativado = True
                    print("✅ Antiloss reativado após ciclo win")
            cached_stake = masaniello.getStake()
        else:
            config = configuracoes_gerenciamentos["Ciclos"]
            matriz = config["matriz_ciclos"]
            modo_ataque_defesa = config.get("modo_ataque_defesa", False)

            print("\n=== Processando Win em Ciclos ===")
            print(f"Modo Ataque/Defesa: {'Sim' if modo_ataque_defesa else 'Não'}")
            print(f"Nível de Gale: {gales}")

            if modo_ataque_defesa:
                alvo_atingido = verificar_alvo_ciclo(lucro_total)

                print(f"Lucro atual: ${lucro_total:.2f}")
                print(f"Alvo: ${config.get('alvo_lucro', 0.0):.2f}")
                print(f"Alvo atingido: {'Sim' if alvo_atingido else 'Não'}")

                if alvo_atingido:
                    config["linha_atual"] = 0
                    config["coluna_atual"] = 0
                    config["linha_atual_repetindo"] = False
                    cached_stake = float(matriz[0][0])

                    play_cash_sound()
                    alvoresete = True
                    if VerificaSeAntlossEstavaAtivo:
                        antiloss_ativado = True
                        print("✅ Antiloss reativado após ciclo win")
                    mark_cycle_reset(row_id, "", True)
                else:
                    config["linha_atual_repetindo"] = True
                    config["coluna_atual"] = 0
                    linha_atual = config["linha_atual"]
                    cached_stake = float(matriz[linha_atual][0])
                    mark_cycle_reset(row_id, "", False)
            else:
                config["linha_atual"] = 0
                config["coluna_atual"] = 0
                cached_stake = float(matriz[0][0])

                mark_cycle_reset(row_id, "", True)
                play_cash_sound()
                if VerificaSeAntlossEstavaAtivo:
                    antiloss_ativado = True
                    print("✅ Antiloss reativado após ciclo win")

        # Reset de valores mantendo estado do antiloss
        gales = 0

        if mt4_receiver and mt4_receiver.is_processing_order:
            mt4_receiver.mark_order_complete()
            print("✅ Ordem MT4 completada")

        # Atualiza interface
        dpg.split_frame()
        update_status()

        print("\n=== Status Final da Operação ===")
        print(f"Total wins: {total_wins}")
        print(f"Gales: {gales}")
        print(f"Stake atual: ${cached_stake:.2f}")
        print(f"Lucro total: ${lucro_total:.2f}")
        if gerenciamento_ativo == "Ciclos":
            print(f"Linha atual: {config['linha_atual'] + 1}")
            print(f"Coluna atual: {config['coluna_atual']}")
        print("===================================")

        await asyncio.sleep(0.1)
        # Envia mensagem Telegram antes de resetar o símbolo
        await enviar_resultados_telegram("Win")

        # Reset do last_symbol e last_signal após enviar mensagem
        last_symbol = None
        last_signal = None

    except Exception as e:
        print(f"❌ Erro ao processar win: {e}")
        traceback.print_exc()


async def process_loss(row_id):
    """Processa loss com feedback detalhado para ML"""
    global total_losses, gales, cached_stake, NumeroDeGales, api, lucro_total, gerenciamento_ativo
    global VerificaSeAntlossEstavaAtivo, antiloss_ativado, last_symbol, last_signal
    global mt4_receiver, velas

    try:
        await atualizar_saldo(api)

        if ml_strategy_active and last_symbol in trading_strategies:
            strategy = trading_strategies[last_symbol]

            if hasattr(velas[last_symbol], "__getitem__") and not isinstance(velas[last_symbol], (str, bytes)):
                # It's likely already a sequence, but let's make sure it supports slicing
                velas_sequence = list(velas[last_symbol])
                velas_data = velas_sequence[-20:] if len(velas_sequence) >= 20 else velas_sequence
            else:
                # It doesn't support slicing, so handle appropriately
                print(f"⚠️ velas[{last_symbol}] is not sliceable, type: {type(velas[last_symbol])}")
                velas_data = []

            if velas_data:  # Only process if we have candles
                # Pass all required parameters to process_trade_feedback
                strategy.process_trade_feedback(
                    win=False,  # Loss
                    velas_data=velas_data,
                    action_type=last_signal,  # Pass the last signal (CALL/PUT)
                    gale_level=gales,  # Current gale level
                    gale_recovery=False  # Loss is never recovery
                )
                print(f"✅ ML feedback enviado para {last_symbol} - LOSS (Gale: {gales})")
            else:
                print(f"❌ Unable to process ML feedback due to missing candles")

        shared_state.set_order_in_progress(False)

        if gerenciamento_ativo == "Masaniello":
            cycle_reset, reset_message, remaining_trades = masaniello.loss()
            mark_cycle_reset(row_id, reset_message, cycle_reset,
                             remaining_trades['wins'], remaining_trades['losses'])

            if cycle_reset:
                total_losses += 1
                gales = 0
                row_id = None
                cached_stake = masaniello.getStake()
                await enviar_resultados_telegram("Loss")
                if mt4_receiver and mt4_receiver.is_processing_order:
                    mt4_receiver.mark_order_complete()
                last_symbol = None
                last_signal = None
                return False
            else:
                # Verifica se pode tentar gale
                if gales < NumeroDeGales:
                    gales += 1
                    cached_stake = masaniello.getStake()
                    print(f"\n=== Preparando Gale {gales} ===")
                    print(f"Novo stake: ${cached_stake:.2f}")
                    return True
                else:
                    # Atingiu limite de gales
                    total_losses += 1
                    gales = 0
                    row_id = None
                    cached_stake = masaniello.getStake()
                    await enviar_resultados_telegram("Loss")
                    if mt4_receiver and mt4_receiver.is_processing_order:
                        mt4_receiver.mark_order_complete()
                    last_symbol = None
                    last_signal = None
                    return False

        else:  # Ciclos
            config = configuracoes_gerenciamentos["Ciclos"]
            matriz = config["matriz_ciclos"]
            linha_atual = config["linha_atual"]
            coluna_atual = config["coluna_atual"]
            max_gales = get_line_max_gales(linha_atual)
            proxima_coluna = coluna_atual + 1

            print(f"\n=== Processando Loss em Ciclos ===")
            print(f"Linha atual: {linha_atual + 1}")
            print(f"Coluna atual: {coluna_atual + 1}")
            print(f"Gales disponíveis: {max_gales}")
            print(f"Gales usados: {gales}")

            # Verifica se pode tentar gale na linha atual
            if gales < max_gales and proxima_coluna < len(matriz[linha_atual]) and matriz[linha_atual][
                proxima_coluna] > 0:
                gales += 1
                config["coluna_atual"] = proxima_coluna
                cached_stake = float(matriz[linha_atual][proxima_coluna])
                print(f"✅ Avançando para Gale {gales}")
                mark_cycle_reset(row_id, "", False)
                return True
            else:
                # Verifica se pode avançar para próxima linha
                proxima_linha = (linha_atual + 1) % len(matriz)
                tem_proxima_linha = matriz[proxima_linha][0] > 0

                print(f"Próxima linha: {proxima_linha + 1}")
                print(f"Valor na próxima linha: {matriz[proxima_linha][0]}")

                if tem_proxima_linha:
                    total_losses += 1
                    gales = 0
                    config["linha_atual"] = proxima_linha
                    config["coluna_atual"] = 0
                    cached_stake = float(matriz[proxima_linha][0])
                    print(f"✅ Avançando para próximo ciclo (Linha {proxima_linha + 1})")
                    mark_cycle_reset(row_id, "", False)
                else:
                    total_losses += 1
                    gales = 0
                    config["linha_atual"] = 0
                    config["coluna_atual"] = 0
                    cached_stake = float(matriz[0][0])
                    print("❌ Sem mais linhas disponíveis - Ciclo com perda")
                    mark_cycle_reset(row_id, "Perda", False)

                if mt4_receiver and mt4_receiver.is_processing_order:
                    mt4_receiver.mark_order_complete()

                if abr_strategy_active and tipo_sinal_original == "ABR":
                    abr_strategy.record_result(symbol, False)  # Para loss
                    print(f"❌ Resultado ABR registrado: Loss para {symbol}")

                await enviar_resultados_telegram("Loss")
                last_symbol = None
                last_signal = None
                return False

        update_status()
        return gales > 0

    except Exception as e:
        print(f"Erro ao processar loss: {e}")
        traceback.print_exc()
        return False



def mark_cycle_reset(row_id, message, is_reset, remaining_wins=0, remaining_losses=0):
    """Marca reset de ciclo na interface com melhor gerenciamento de status."""
    global VerificaSeAntlossEstavaAtivo, antiloss_ativado, gales, lucro_total, alvoresete

    try:
        if dpg.does_item_exist(row_id):
            children = dpg.get_item_children(row_id, slot=1)
            if children and len(children) > 9:
                # Verifica o gerenciamento atual de forma mais robusta
                atual_gerenciamento = dpg.get_value("gerenciamento_selector") if dpg.does_item_exist("gerenciamento_selector") else gerenciamento_ativo

                if atual_gerenciamento == language_manager.get_text("CICLOS"):  # Compara com a tradução
                    config = configuracoes_gerenciamentos["Ciclos"]
                    linha_atual = config["linha_atual"]
                    alvo = config.get("alvo_lucro", 0.0)

                    if config.get("modo_ataque_defesa", False):
                        if "Perda" in message:
                            dpg.set_value(children[9], language_manager.get_text("CICLO_PERDA"))
                            dpg.configure_item(children[9], color=(255, 0, 0))
                        elif config.get("linha_atual_repetindo", False):
                            dpg.set_value(children[9], language_manager.get_text("ALVO_NAO_ATINGIDO").format(alvo))
                            dpg.configure_item(children[9], color=(186, 85, 211))
                        else:
                            if lucro_total >= config.get("lucro_ultimo_ciclo_sucesso", 0.0) + alvo and alvoresete == True:
                                dpg.set_value(children[9], language_manager.get_text("ALVO_ATINGIDO_REINICIANDO").format(alvo))
                                dpg.configure_item(children[9], color=(0, 255, 0))
                                alvoresete = False
                            else:
                                if linha_atual == 0:
                                    dpg.set_value(children[9], language_manager.get_text("ALVO_NAO_ALCANCADO"))
                                    dpg.configure_item(children[9], color=(255, 215, 0))
                                else:
                                    dpg.set_value(children[9], language_manager.get_text("AVANCANDO_CICLO").format(linha_atual + 1))
                                    dpg.configure_item(children[9], color=(255, 215, 0))
                    else:
                        if "Perda" in message:
                            dpg.set_value(children[9], language_manager.get_text("CICLO_REINICIADO_LOSS"))
                            dpg.configure_item(children[9], color=(255, 0, 0))
                        elif is_reset:
                            dpg.set_value(children[9], language_manager.get_text("CICLO_REINICIADO_WIN"))
                            dpg.configure_item(children[9], color=(0, 255, 0))
                        else:
                            dpg.set_value(children[9], language_manager.get_text("AVANCANDO_CICLO").format(linha_atual + 1))
                            dpg.configure_item(children[9], color=(255, 215, 0))

                elif atual_gerenciamento == language_manager.get_text("MASANIELLO"):  # Compara com a tradução
                    if is_reset:
                        if VerificaSeAntlossEstavaAtivo and "Ciclo Reiniciado" in message:
                            antiloss_ativado = True
                            print("✅ Antiloss reativado após ciclo win")
                        dpg.set_value(children[9], message)
                        dpg.configure_item(children[9], color=(255, 165, 0))
                    else:
                        status_message = language_manager.get_text("LOSS_RESTANTE").format(remaining_losses, remaining_wins)
                        dpg.set_value(children[9], status_message)
                        dpg.configure_item(children[9], color=(186, 85, 211))

    except Exception as e:
        print(f"Erro ao atualizar status na tabela para {row_id}: {e}")
        traceback.print_exc()





ultimas_velas = {symbol: None for symbol in symbols}

async def start_bot():
    global api_token, symbols, velas, ultimas_velas, first_initialization
    global stop_event, is_running, is_shutting_down, ws_manager, should_send_orders
    global api, cached_stake, masaniello, saldo_atual, initial_balance

    if not api_token:
        print("Por favor, insira o token antes de iniciar o bot.")
        abrir_popup_token()
        return

    try:
        print("\n=== Iniciando Bot ===")



        # Inicialização da API
        api = await inicializar_api()
        if not api:
            print("❌ Falha ao inicializar API")
            return

        # Atualização inicial do saldo
        await atualizar_saldo(api)
        initial_balance = saldo_atual

        # Inicialização do Masaniello se necessário
        if not masaniello:
            masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)

        # Configuração inicial do stake
        if cached_stake is None:
            cached_stake = masaniello.getStake()

        print(f"✅ Saldo inicial: ${initial_balance:.2f}")
        print(f"✅ Stake inicial: ${cached_stake:.2f}")

        # Iniciar conexões e verificações
        is_running = True
        should_send_orders = True
        stop_event.clear()

        # Iniciar tasks de monitoramento
        tasks = [
            asyncio.create_task(check_connection_health()),
            asyncio.create_task(start_rgb_effect_during_sample()),
            asyncio.create_task(periodic_stop_check()),

        ]

        print("🔄 Iniciando loop principal do bot...")
        await sample_calls()

    except Exception as e:
        print(f"❌ Erro durante a execução do bot: {e}")
        import traceback
        traceback.print_exc()
        is_running = False
        stop_event.set()
    finally:
        update_gui_state(is_running)
        # Cancela todas as tasks pendentes
        for task in asyncio.all_tasks():
            if task is not asyncio.current_task():
                task.cancel()


async def unified_reconnect(reconnect_type="all", force=False):
    """More robust unified reconnection system"""
    global api, websocket_client, is_running, saldo_atual

    base_delay = 5
    max_delay = 30
    current_delay = base_delay
    max_retries = 3

    async def verify_api_connection():
        try:
            if api:
                balance = await atualizar_saldo(api)
                return balance is not None
            return False
        except Exception:
            return False

    # Verify need for reconnection
    if not force:
        if reconnect_type in ["api", "all"] and await verify_api_connection():
            return True

        if reconnect_type in ["websocket",
                              "all"] and websocket_client and websocket_client.sock and websocket_client.sock.connected:
            return True

    # Main reconnection loop
    for attempt in range(max_retries):
        try:
            # API reconnection
            if reconnect_type in ["api", "all"]:
                if api:
                    await api.logout()
                    await asyncio.sleep(1)
                    api = None

                api = BinaryAPI(api_token)
                status, message = api.start()

                if not status:
                    raise Exception(f"API initialization failed: {message}")

                balance = api.get_balance()
                if balance is None:
                    raise Exception("Could not get balance")

                    # WebSocket reconnection
            if reconnect_type in ["websocket", "all"]:
                if websocket_client:
                    websocket_client.close()
                    await asyncio.sleep(1)

                websocket.enableTrace(False)
                ws = websocket.WebSocketApp(
                    URL,
                    on_open=on_open,
                    on_message=on_message,
                    on_error=on_error,
                    on_close=on_close
                )

                ws_thread = threading.Thread(
                    target=lambda: ws.run_forever(
                        ping_interval=60,
                        ping_timeout=10,
                        sslopt={"cert_reqs": ssl.CERT_NONE}
                    ),
                    daemon=True
                )
                ws_thread.start()

                # Wait for connection
                for _ in range(10):
                    if ws.sock and ws.sock.connected:
                        websocket_client = ws
                        await subscribe_to_all_symbols(ws)
                        break
                    await asyncio.sleep(0.5)

            return True

        except Exception as e:
            print(f"\nError on attempt {attempt + 1}:")
            print(f"Error: {str(e)}")

            if attempt < max_retries - 1:
                await asyncio.sleep(current_delay)
                current_delay = min(current_delay * 2, max_delay)

    return False


# Função auxiliar para atualizar saldo sem recursão
async def update_balance_safe():
    """Atualiza o saldo de forma segura sem recursão"""
    global saldo_atual, api

    try:
        if not api or not api.check_connect:
            return None

        balance = api.get_balance()
        if balance is not None:
            saldo_atual = float(balance)
            print(f"✅ Saldo atualizado: ${saldo_atual:.2f}")
            return saldo_atual

    except Exception as e:
        print(f"Erro ao atualizar saldo: {e}")
        return None


def login_wrapper():
    """Wrapper to run the async login function in a thread"""

    def run_login():
        asyncio.run(logar_e_verificar_atualizacoes())
        show_welcome_popup()

    # Start in a new thread
    threading.Thread(target=run_login, daemon=True).start()


# Modify the logar_e_verificar_atualizacoes function to properly initialize MT4 receiver
async def logar_e_verificar_atualizacoes():
    """Synchronous wrapper for async login function"""
    global masaniello, is_maintenance, mt4_receiver, stop_event

    try:
        if is_maintenance:
            if dpg.does_item_exist("maintenance_login_popup"):
                dpg.delete_item("maintenance_login_popup")

            with dpg.window(label=language_manager.get_text("SISTEMA_EM_MANUTENCAO"),
                            modal=True,
                            no_close=True,
                            tag="maintenance_login_popup",
                            width=400,
                            height=150):
                dpg.add_text(language_manager.get_text("SISTEMA_EM_MANUTENCAO"), color=(255, 0, 0))
                dpg.add_separator()
                dpg.add_text(language_manager.get_text("SISTEMA_INDISPONIVEL"))
                dpg.add_text(language_manager.get_text("AGUARDE_MANUTENCAO"), color=(255, 165, 0))
                dpg.add_button(label="OK",
                               callback=lambda: dpg.delete_item("maintenance_login_popup"),
                               width=100,
                               pos=[150, 100])
            return

        demo_token, real_token = carregar_tokens()

        if not demo_token or not real_token:
            print("Por favor, insira ambos os tokens.")
            abrir_popup_token()
            return

        # Initialize Masaniello
        masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)
        print("Tokens carregados com sucesso.")
        print(f"Demo Token: {demo_token[:5]}...")
        print(f"Real Token: {real_token[:5]}...")

        # Initialize MT4 receiver
        try:
            print("\n=== Inicializando MT4 Signal Receiver ===")
            print("Criando nova instância do MT4SignalReceiver...")

            # Create receiver instance
            mt4_receiver = MT4SignalReceiver(
                host='127.0.0.1',
                port=5000,
                stop_event=stop_event,
                simbolos_ativos=simbolos_ativos
            )

            def mt4_worker():
                try:
                    import traceback
                    print("Iniciando servidor MT4 na porta 5000...")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(mt4_receiver.start())
                except Exception as e:
                    print(f"❌ Erro no worker MT4: {e}")
                    traceback.print_exc()

            # Start MT4 thread
            mt4_thread = threading.Thread(
                target=mt4_worker,
                daemon=True,
                name="MT4Receiver"
            )
            mt4_thread.start()

            print("✅ MT4SignalReceiver iniciado com sucesso")
            print(f"✅ Porta: 5000")
            print(f"✅ Host: 127.0.0.1")
            print(f"✅ Aguardando sinais do MetaTrader...")

        except Exception as e:
            print("\n❌ Erro ao inicializar MT4SignalReceiver:")
            print(f"Erro: {str(e)}")
            print("Stack trace:")
            traceback.print_exc()
            mt4_receiver = None

        # Start async login process in a new thread
        threading.Thread(
            target=lambda: asyncio.run(run_login_in_thread()),
            daemon=True,
            name="LoginThread"
        ).start()

    except Exception as e:
        print(f"Erro durante o login: {e}")
        import traceback
        traceback.print_exc()


def toggle_modo_gale(sender, app_data):
    """Alterna entre modo de gale normal e zigzag"""
    global modo_gale

    try:
        modo_gale = "normal" if app_data == "Normal" else "zigzag"
        print(f"\n=== Modo de Gale alterado para: {modo_gale} ===")

        # Salva configuração automaticamente
        save_configurations()

    except Exception as e:
        print(f"Erro ao alternar modo de gale: {e}")
        traceback.print_exc()

def toggle_modo_entrada(sender, app_data):
    """Alterna entre modo Tempo Fixo e Fim da Vela"""
    global modo_entrada, default_expiration, fim_da_vela_time

    # Atualiza o modo baseado na seleção do radio button
    modo_entrada = "fim_da_vela" if app_data == "Fim da Vela" else "tempo_fixo"

    # Atualiza o combo de expiração
    if dpg.does_item_exist("expiration_selector"):
        if modo_entrada == "fim_da_vela":
            # Extrai apenas o número do timeframe (ex: "M1" -> "1")
            timeframe_value = fim_da_vela_time.replace("M", "") if fim_da_vela_time.startswith("M") else fim_da_vela_time
            dpg.configure_item(
                "expiration_selector",
                items=["1", "5", "15", "30"],
                default_value=timeframe_value
            )
            dpg.set_value("expiration_selector", timeframe_value)
        else:
            dpg.configure_item(
                "expiration_selector",
                items=["1", "2", "3", "4", "5", "10", "15", "30"],
                default_value=str(default_expiration)
            )
            dpg.set_value("expiration_selector", str(default_expiration))

    print(f"\n=== Modo de Entrada Alterado ===")
    print(f"Novo modo: {modo_entrada}")
    if modo_entrada == "fim_da_vela":
        print(f"Timeframe: {fim_da_vela_time}")
    else:
        print(f"Expiração: {default_expiration} minutos")

    # Salva configurações imediatamente
    save_configurations()


def toggle_bot():
    global is_running, stop_event, should_send_orders, websocket_client, stop_message_sent
    global first_initialization, api_token, gales, tipo_ordem_anterior, ultimas_velas
    global total_wins, total_losses, is_maintenance, lucro_total, initial_balance
    global saldo_atual, cached_stake, masaniello, row_id, lucro_monitor

    # Inicialização de variáveis globais caso não existam
    if 'stop_message_sent' not in globals():
        global stop_message_sent
        stop_message_sent = False

    if is_maintenance:
        if dpg.does_item_exist("maintenance_toggle_popup"):
            dpg.delete_item("maintenance_toggle_popup")

        with dpg.window(label="Sistema em Manutenção", modal=True, no_close=True,
                        tag="maintenance_toggle_popup", width=400, height=150):
            dpg.add_text("SISTEMA EM MANUTENCAO", color=(255, 0, 0))
            dpg.add_separator()
            dpg.add_text("Sistema temporariamente indisponível.")
            dpg.add_text("Por favor, Aguarde a Conclusa Da Manutencao.", color=(255, 165, 0))
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item("maintenance_toggle_popup"),
                           width=100, pos=[150, 100])

        # Força o estado de parado
        is_running = False
        should_send_orders = False
        dpg.configure_item("toggle_button", label="INICIAR")
        update_button_image("toggle_button", "play.png")
        dpg.set_value("bot_status_text", "SISTEMA EM MANUTENCAO")
        dpg.configure_item("bot_status_text", color=(255, 0, 0))
        dpg.disable_item("toggle_button")
        dpg.disable_item("token_mode")
        return

    try:
        print("\n=== Alterando estado do bot ===")
        print(f"Estado atual - is_running: {is_running}, should_send_orders: {should_send_orders}")

        # Verificação de token
        if not api_token:
            print("Por favor, faça login antes de iniciar.")
            criar_login_required_popup()
            return

        # Pausando o bot
        if is_running and should_send_orders:
            print("Pausando bot...")
            should_send_orders = False

            stop_message_sent = False  # Reset do flag ao pausar

            # Reseta variáveis de controle
            gales = 0
            tipo_ordem_anterior = None
            row_id = None
            ultimas_velas = {symbol: None for symbol in symbols}

            # Atualiza interface
            dpg.configure_item("toggle_button", label="INICIAR")
            update_button_image("toggle_button", "play.png")
            dpg.set_value("bot_status_text", "Bot Pausado")
            dpg.configure_item("bot_status_text", color=(255, 255, 255))
            controlar_seletor_ativo(True)

            print("Bot pausado com sucesso")
            return

        # Iniciando o bot
        if not is_running or not should_send_orders:
            if first_initialization:
                print("Primeira inicialização, resetando valores...")
                reset_bot_state()
                first_initialization = False
            elif stop_message_sent:
                print("Continuando após TP/SL, resetando lucro...")
                resetarlucro()
                stop_message_sent = False

            print("Iniciando bot...")
            is_running = True
            should_send_orders = True
            stop_event.clear()
            lucro_monitor = LucroMonitor()

            # Verifica saldo inicial
            if initial_balance is None or initial_balance == 0:
                initial_balance = saldo_atual
                print(f"Saldo inicial definido: ${initial_balance:.2f}")

            # Inicializa ou reseta Masaniello se necessário
            if not masaniello:
                masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)

            # Reseta stake se necessário
            if cached_stake is None:
                cached_stake = masaniello.getStake()
                print(f"Stake inicial: ${cached_stake:.2f}")

            # Atualiza interface
            dpg.configure_item("toggle_button", label="PARAR")
            update_button_image("toggle_button", "parar.png")
            dpg.set_value("bot_status_text", "Bot Em Execução")
            controlar_seletor_ativo(False)

            # Inicia conexões necessárias
            if not websocket_client:
                threading.Thread(target=lambda: asyncio.run(start_websocket()), daemon=True).start()

            # Verifica se já existe uma thread do bot rodando
            if not any(t.name == "bot_thread" for t in threading.enumerate()):
                threading.Thread(target=lambda: asyncio.run(start_bot()), daemon=True, name="bot_thread").start()

            print("\n=== Bot Iniciado com Sucesso ===")
            print(f"Saldo Inicial: ${initial_balance:.2f}")
            print(f"Stake Inicial: ${cached_stake:.2f}")
            print(f"Masaniello configurado: {style}")
            print("================================")

        print(f"Novo estado - is_running: {is_running}, should_send_orders: {should_send_orders}")
        update_gui_state(is_running)

    except Exception as e:
        print(f"Erro ao alternar estado do bot: {e}")
        import traceback
        traceback.print_exc()

        # Em caso de erro, tenta parar o bot de forma segura
        should_send_orders = False
        stop_message_sent = False
        is_running = False

        # Reseta variáveis críticas
        gales = 0
        tipo_ordem_anterior = None
        row_id = None

        # Atualiza interface para estado seguro
        dpg.configure_item("toggle_button", label="INICIAR")
        update_button_image("toggle_button", "play.png")
        dpg.set_value("bot_status_text", "Bot Pausado (Erro)")
        dpg.configure_item("bot_status_text", color=(255, 255, 255))
        controlar_seletor_ativo(True)

        # Tenta salvar estado atual
        save_transactions()
        save_configurations()


def update_button_image(button_tag, image_name):
    """Atualiza apenas a textura do botão mantendo sua posição"""
    try:
        image_path = resource_path(image_name)
        if os.path.exists(image_path):
            width, height, channels, data = dpg.load_image(image_path)

            # Cria nova textura
            with dpg.texture_registry():
                texture_id = dpg.add_static_texture(width, height, data)

            # Atualiza a textura do botão existente
            dpg.configure_item(button_tag, texture_tag=texture_id)

            print(f"✅ Textura do botão {button_tag} atualizada com sucesso")
        else:
            print(f"❌ Arquivo de imagem não encontrado: {image_path}")

    except Exception as e:
        print(f"❌ Erro ao atualizar imagem do botão: {e}")
        import traceback
        traceback.print_exc()

# Função para desativar/ativar o seletor Demo/Real
def controlar_seletor_ativo(ativo):
    if ativo:
        dpg.enable_item("token_mode")  # Ativa o seletor Demo/Real
    else:
        dpg.disable_item("token_mode")  # Desativa o seletor Demo/Real



async def connect_to_api():
    global api_token, api, saldo_atual, initial_balance

    mode = dpg.get_value("token_mode")
    api_token = demo_token if mode == "Demo" else real_token

    if not api_token or api_token.strip() == "":
        print(f"Por favor, insira o token para o modo {mode} antes de logar o bot.")
        return

    try:
        print(f"Conectando ao servidor na conta {mode}...")
        api = await inicializar_api()

        if api and await verificar_api_autorizada():
            print(f"Bot conectado com sucesso na conta {mode}!")


            # Atualiza interface
            dpg.set_value("success_message", f"Conectado com sucesso na conta {mode}!")
            dpg.show_item("success_message")
            dpg.enable_item("toggle_button")

            await update_gui_after_login(mode)
        else:
            print("Falha na conexão com a API")
            dpg.set_value("success_message", "Erro ao conectar com a API")
            dpg.show_item("success_message")

    except Exception as e:
        print(f"Erro ao conectar o bot na conta {mode}: {e}")
        dpg.set_value("success_message", f"Erro ao conectar: {str(e)}")
        dpg.show_item("success_message")


async def run_login_in_thread():
    """Processa login sem inicializar Telegram automaticamente"""
    try:
        print("\n=== Iniciando Login ===")

        # Conecta apenas à API Deriv
        await connect_to_api()

        # Atualiza interface
        if dpg.does_item_exist("success_message"):
            dpg.configure_item("success_message", show=True)
            dpg.set_value("success_message", "Conectado com sucesso!")

            # Esconde mensagem após delay
            await asyncio.sleep(3)
            dpg.configure_item("success_message", show=False)

    except Exception as e:
        print(f"❌ Erro no processo de login: {e}")
        if dpg.does_item_exist("success_message"):
            dpg.set_value("success_message", f"Erro ao conectar: {str(e)}")
            dpg.configure_item("success_message", show=True)





# Popup para mostrar se o token não foi inserido
def criar_login_required_popup():
    try:
        # Verifique se o popup já existe e, se existir, delete
        if dpg.does_item_exist("login_required_popup"):
            dpg.delete_item("login_required_popup")

        # Crie o popup
        with dpg.window(label="Aviso", modal=True, no_close=True, tag="login_required_popup", width=300, height=100):
            dpg.add_text("Acesso negado: Faca Login Antes", tag="login_required_popup_text")
            dpg.add_spacer(height=10)  # Adiciona espaçamento
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item("login_required_popup"))

        # Mostra o popup
        dpg.show_item("login_required_popup")
    except Exception as e:
        print(f"Erro ao criar o popup: {e}")



async def verificar_velas_antiloss(api, symbol, sinal, hora_sinal, row_id, NumeroDeGales):
    global antiloss_ativado, required_losses, pares_verificados_antiloss, modo_antiloss, VerificaSeAntlossEstavaAtivo
    global modo_entrada, default_expiration

    VerificaSeAntlossEstavaAtivo = True

    if not hasattr(verificar_velas_antiloss, 'loss_sequences'):
        verificar_velas_antiloss.loss_sequences = {}

    try:
        print(f"\n=== Verificando Antiloss para {symbol} ===")
        print(f"Modo: {modo_antiloss}")
        print(f"Modo de entrada: {modo_entrada}")
        print(f"Pares verificados: {pares_verificados_antiloss}")

        if symbol not in verificar_velas_antiloss.loss_sequences:
            verificar_velas_antiloss.loss_sequences[symbol] = 0

        # Define duração baseada no modo de entrada
        if modo_entrada == "fim_da_vela":
            DURACAO_FIXA = calculate_candle_expiration(default_expiration)
            if DURACAO_FIXA is None:
                print("❌ Tempo insuficiente para verificação antiloss")
                return False
            print(f"✅ Verificação antiloss com {DURACAO_FIXA}s até o fim da vela")
        else:
            DURACAO_FIXA = 15 if symbol.startswith("stpRNG") else default_expiration * 60

        # Determina número máximo de gales baseado no gerenciamento atual
        if gerenciamento_ativo == "Masaniello":
            max_gales = NumeroDeGales
        else:  # Ciclos
            config = configuracoes_gerenciamentos["Ciclos"]
            linha_atual = config["linha_atual"]
            max_gales = get_line_max_gales(linha_atual)

        print(f"Gales máximos para operação: {max_gales}")

        async def atualizar_countdown(tag_suffix=""):
            for tempo in range(DURACAO_FIXA, -1, -1):
                if dpg.does_item_exist(f"fechamento_{row_id}"):
                    cor = (255, 0, 0) if tempo <= 3 else (255, 165, 0) if tempo <= 10 else (0, 255, 0)
                    status_text = f"AntLoss{tag_suffix} {tempo}s"
                    dpg.configure_item(f"fechamento_{row_id}", color=cor)
                    dpg.set_value(f"fechamento_{row_id}", status_text)
                await asyncio.sleep(1)

        async def capturar_preco_entrada(is_gale=False, tentativa=0, max_tentativas=3):
            delay = 1 if is_gale else 1
            timeframe = default_expiration * 60
            await asyncio.sleep(delay)
            try:

                candle_data = await api.ticks_history({
                    "ticks_history": symbol,
                    "end": "latest",
                    "start": 1,
                    "count": 1,
                    "style": "candles",
                    "granularity": timeframe
                })

                if 'candles' in candle_data and len(candle_data['candles']) > 0:
                    ultima_vela = candle_data['candles'][0]
                    preco = float(ultima_vela['close'])
                    print(f"✅ Preço entrada capturado após delay de {delay}s: {preco}")
                    return preco
                else:
                    if tentativa < max_tentativas:
                        print(f"⚠️ Tentativa {tentativa + 1} falhou, tentando novamente...")
                        return await capturar_preco_entrada(is_gale, tentativa + 1)
                    print("❌ Não foi possível obter dados da vela")
                    return None
            except Exception as e:
                if tentativa < max_tentativas:
                    print(f"⚠️ Erro na tentativa {tentativa + 1}: {e}, tentando novamente...")
                    return await capturar_preco_entrada(is_gale, tentativa + 1)
                print(f"❌ Erro ao capturar preço: {e}")
                return None

        print("\n=== Processando Entrada Inicial ===")
        print("⏳ Aguardando 1s para captura do preço inicial...")
        preco_entrada = await capturar_preco_entrada(is_gale=False)
        if preco_entrada is None:
            if mt4_receiver and mt4_receiver.is_processing_order:
                mt4_receiver.mark_order_complete()
            return False

        # Aguarda duração fixa para verificar resultado
        await atualizar_countdown()
        timeframe = default_expiration * 60
        candle_data = await api.ticks_history({
            "ticks_history": symbol,
            "end": "latest",
            "start": 1,
            "count": 1,
            "style": "candles",
            "granularity": timeframe
        })

        if 'candles' in candle_data and len(candle_data['candles']) > 0:
            preco_saida = float(candle_data['candles'][0]['close'])
        else:
            if mt4_receiver and mt4_receiver.is_processing_order:
                mt4_receiver.mark_order_complete()
            return False

        is_loss = verificar_loss_por_preco(preco_entrada, preco_saida, sinal)
        gales_executados = 0

        if is_loss and max_gales > 0:
            print(f"\n❌ Loss na entrada inicial em {symbol} - Iniciando gales")
            while gales_executados < max_gales:
                gales_executados += 1
                print(f"\n=== Verificando Gale {gales_executados}/{max_gales} ===")
                print("⏳ Aguardando 2s para captura do preço do gale...")

                preco_entrada_gale = await capturar_preco_entrada(is_gale=True)
                if preco_entrada_gale is None:
                    if mt4_receiver and mt4_receiver.is_processing_order:
                        mt4_receiver.mark_order_complete()
                    return False

                await atualizar_countdown(f" G{gales_executados}")
                timeframe = default_expiration * 60
                candle_data = await api.ticks_history({
                    "ticks_history": symbol,
                    "end": "latest",
                    "start": 1,
                    "count": 1,
                    "style": "candles",
                    "granularity": timeframe
                })

                if 'candles' in candle_data and len(candle_data['candles']) > 0:
                    preco_saida_gale = float(candle_data['candles'][0]['close'])
                else:
                    if mt4_receiver and mt4_receiver.is_processing_order:
                        mt4_receiver.mark_order_complete()
                    return False

                is_loss = verificar_loss_por_preco(preco_entrada_gale, preco_saida_gale, sinal)
                if not is_loss:
                    print(f"✅ Win no gale {gales_executados} para {symbol}")
                    verificar_velas_antiloss.loss_sequences[symbol] = 0
                    update_antiloss_status(row_id, 0, required_losses)
                    if mt4_receiver and mt4_receiver.is_processing_order:
                        mt4_receiver.mark_order_complete()
                    return False

        if is_loss:
            if modo_antiloss == "restrito":
                if symbol not in pares_verificados_antiloss:
                    pares_verificados_antiloss[symbol] = 1
                else:
                    pares_verificados_antiloss[symbol] += 1
                print(
                    f"Antiloss restrito: {symbol} registrou {pares_verificados_antiloss[symbol]}/{required_losses} losses")

            verificar_velas_antiloss.loss_sequences[symbol] += 1
            current_losses = verificar_velas_antiloss.loss_sequences[symbol]

            print(f"❌ Loss após {gales_executados} gales em {symbol}")
            print(f"Sequência de losses: {current_losses}/{required_losses}")
            update_antiloss_status(row_id, current_losses, required_losses)

            if current_losses >= required_losses:
                print(f"✅ Antiloss completado para {symbol}")
                verificar_velas_antiloss.loss_sequences[symbol] = 0
                if modo_antiloss == "global":
                    antiloss_ativado = False
                    pares_verificados_antiloss.clear()
                if mt4_receiver and mt4_receiver.is_processing_order:
                    mt4_receiver.mark_order_complete()
                    print("✅ MT4 ordem virtual completada após antiloss")
                return True

            if mt4_receiver and mt4_receiver.is_processing_order:
                mt4_receiver.mark_order_complete()
                print("✅ MT4 ordem virtual completada após antiloss")
            return True

        else:
            print(f"✅ Win na entrada inicial em {symbol}")
            verificar_velas_antiloss.loss_sequences[symbol] = 0
            update_antiloss_status(row_id, 0, required_losses)
            update_order_in_table(row_id, datetime.now().strftime("%H:%M:%S"), DURACAO_FIXA, "Win", "AntLoss Win")
            if mt4_receiver and mt4_receiver.is_processing_order:
                mt4_receiver.mark_order_complete()
                print("✅ MT4 ordem virtual completada após antiloss")
            return False

    except Exception as e:
        if mt4_receiver and mt4_receiver.is_processing_order:
            mt4_receiver.mark_order_complete()
        print(f"❌ Erro no verificar_velas_antiloss para {symbol}: {e}")
        traceback.print_exc()
        return False


def toggle_antiloss(sender, app_data):
    global antiloss_ativado
    antiloss_ativado = app_data
    print(f"Antiloss {'ativado' if antiloss_ativado else 'desativado'}")
    save_configurations()
    print(f"💾 Estado Antiloss salvo: {'Ativado' if antiloss_ativado else 'Desativado'}")


def toggle_language(sender, app_data):
    """Alterna entre os idiomas de forma mais robusta"""
    try:
        # Obtém idioma atual
        current_lang = dpg.get_item_user_data("language_toggle")

        # Define sequência de idiomas e imagens
        lang_sequence = {
            'PT': ('EN', 'us.png', 'en'),
            'EN': ('ES', 'es.png', 'es'),
            'ES': ('PT', 'br.png', 'pt')
        }

        if current_lang not in lang_sequence:
            print(f"Idioma atual inválido: {current_lang}")
            current_lang = 'PT'  # Fallback para português

        # Obtém próximo idioma e imagem
        next_lang, next_image, next_code = lang_sequence[current_lang]
        image_path = resource_path(next_image)

        if os.path.exists(image_path):
            # Carrega nova imagem
            width, height, channels, data = dpg.load_image(image_path)
            with dpg.texture_registry():
                texture_id = dpg.add_static_texture(width, height, data)

            # Atualiza textura do botão
            dpg.configure_item("language_toggle", texture_tag=texture_id)

            # Atualiza estado do idioma
            dpg.set_item_user_data("language_toggle", next_lang)

            # Atualiza idioma no sistema
            language_manager.set_language(next_code)

            # Salva configurações incluindo o idioma
            save_configurations()

            # Após salvar, recarrega as configurações preservando o novo idioma
            load_configurations()

            # Atualiza interface com novo idioma
            update_gui_language(dpg, language_manager)
            update_header_elements(dpg, language_manager)

            print(f"\n=== Idioma Alterado ===")
            print(f"Anterior: {current_lang}")
            print(f"Novo: {next_lang}")
            print(f"Código: {next_code}")
            print("======================\n")

        else:
            print(f"❌ Arquivo de imagem não encontrado: {image_path}")

    except Exception as e:
        print(f"❌ Erro ao alternar idioma: {e}")
        traceback.print_exc()


# Na criação do botão:
def create_language_button():
    """Cria o botão de idioma com a imagem inicial e tooltip"""
    try:
        image_path = resource_path("br.png")
        if os.path.exists(image_path):
            width, height, channels, data = dpg.load_image(image_path)
            with dpg.texture_registry():
                texture_id = dpg.add_static_texture(width, height, data)

            language_button = dpg.add_image_button(
                texture_id,
                width=23,
                height=23,
                callback=toggle_language,
                tag="language_toggle"
            )

            # Define o idioma inicial como PT
            dpg.set_item_user_data(language_button, "PT")

            # Adiciona tooltip multilíngue
            with dpg.tooltip(language_button):
                dpg.add_text("Mudar Idioma / Change Language / Cambiar Idioma")

            print("✅ Botão de idioma criado com sucesso")
            return language_button

    except Exception as e:
        print(f"❌ Erro ao criar botão de idioma: {e}")
        traceback.print_exc()
        return None


def toggle_modo_antiloss(sender, app_data):
    global modo_antiloss
    modo_antiloss = app_data.lower()
    print(f"Modo Antiloss alterado para: {modo_antiloss}")

    if modo_antiloss == "global":
        global pares_verificados_antiloss
        pares_verificados_antiloss.clear()

    save_configurations()
    print(f"💾 Modo Antiloss salvo: {modo_antiloss}")



def update_antiloss_status(row_id, current_losses, required_losses):
    """Atualiza o status do antiloss na interface"""
    try:
        if dpg.does_item_exist(row_id):
            children = dpg.get_item_children(row_id, slot=1)
            if children and len(children) > 9:
                antloss_text = f"AntLoss {current_losses}/{required_losses}"

                # Define cores baseadas no estado
                if current_losses >= required_losses:
                    cor = (0, 255, 255)  # Cyan para completo
                else:
                    cor = (255, 0, 255)  # Magenta para em andamento

                dpg.set_value(children[9], antloss_text)
                dpg.configure_item(children[9], color=cor)
                print(f"Status antloss atualizado: {antloss_text}")

    except Exception as e:
        print(f"Erro ao atualizar status antloss: {e}")



def verificar_loss_por_preco(preco_entrada, preco_saida, direcao):
    if direcao == "CALL":
        resultado = preco_saida <= preco_entrada
        print(f"CALL - Entrada: {preco_entrada}, Saída: {preco_saida}, Resultado: {'LOSS' if resultado else 'WIN'}")
        return resultado
    elif direcao == "PUT":
        resultado = preco_saida >= preco_entrada
        print(f"PUT - Entrada: {preco_entrada}, Saída: {preco_saida}, Resultado: {'LOSS' if resultado else 'WIN'}")
        return resultado
    return False



def validar_volume_profile(symbol, sinal, velas_symbol, preco_atual):
    """
    Valida um sinal usando Volume Profile com verificações abrangentes.
    """
    try:
        # Calcula o Volume Profile
        volume_profile_data = calcular_volume_profile(velas_symbol)
        if not volume_profile_data:
            print(f"❌ {symbol}: Dados Volume Profile insuficientes")
            return False

        # Logs iniciais
        print(f"\n=== Análise Volume Profile para {symbol} ===")
        print(f"Sinal Original: {sinal}")
        print(f"Tendência: {volume_profile_data['tendencia']}")
        print(f"Força: {volume_profile_data['forca_tendencia']:.2f}")
        print(f"Pressão Compradora: {volume_profile_data['pressao_compradora']:.2f}")
        print(f"Pressão Vendedora: {volume_profile_data['pressao_vendedora']:.2f}")

        # Verificação de Value Area
        dentro_value_area = (
            volume_profile_data['value_area_low'] <= preco_atual <= volume_profile_data['value_area_high']
        )
        print(f"Dentro da Value Area: {dentro_value_area}")

        if sinal == "CALL":
            # 1. Verificação de Pressão Compradora
            pressao_suficiente = (
                volume_profile_data['pressao_compradora'] >= 0.6 and
                volume_profile_data['distribuicao']['acima_poc'] >
                volume_profile_data['distribuicao']['abaixo_poc']
            )
            if not pressao_suficiente:
                print(f"❌ {symbol}: Pressão compradora insuficiente")
                print(f"Pressão atual: {volume_profile_data['pressao_compradora']:.2f}")
                print(f"Distribuição acima/abaixo: {volume_profile_data['distribuicao']['acima_poc']:.2f} / "
                      f"{volume_profile_data['distribuicao']['abaixo_poc']:.2f}")
                return False

            # 2. Verificação de Tendência
            tendencia_valida = (
                volume_profile_data['tendencia'] == 'up' and
                volume_profile_data['forca_tendencia'] > 0.6
            )
            if not tendencia_valida:
                print(f"❌ {symbol}: Tendência ou força insuficiente para CALL")
                print(f"Tendência: {volume_profile_data['tendencia']}")
                print(f"Força: {volume_profile_data['forca_tendencia']:.2f}")
                return False

            # 3. Verificação de Value Area
            if not dentro_value_area:
                volume_anormal = volume_profile_data.get('volume_anormal', False)
                if not volume_anormal:
                    print(f"❌ {symbol}: Fora da Value Area sem volume anormal")
                    return False
                print(f"⚠️ {symbol}: Fora da Value Area mas com volume anormal")

        elif sinal == "PUT":
            # 1. Verificação de Pressão Vendedora
            pressao_suficiente = (
                volume_profile_data['pressao_vendedora'] >= 0.6 and
                volume_profile_data['distribuicao']['abaixo_poc'] >
                volume_profile_data['distribuicao']['acima_poc']
            )
            if not pressao_suficiente:
                print(f"❌ {symbol}: Pressão vendedora insuficiente")
                print(f"Pressão atual: {volume_profile_data['pressao_vendedora']:.2f}")
                print(f"Distribuição acima/abaixo: {volume_profile_data['distribuicao']['acima_poc']:.2f} / "
                      f"{volume_profile_data['distribuicao']['abaixo_poc']:.2f}")
                return False

            # 2. Verificação de Tendência
            tendencia_valida = (
                volume_profile_data['tendencia'] == 'down' and
                volume_profile_data['forca_tendencia'] > 0.6
            )
            if not tendencia_valida:
                print(f"❌ {symbol}: Tendência ou força insuficiente para PUT")
                print(f"Tendência: {volume_profile_data['tendencia']}")
                print(f"Força: {volume_profile_data['forca_tendencia']:.2f}")
                return False

            # 3. Verificação de Value Area
            if not dentro_value_area:
                volume_anormal = volume_profile_data.get('volume_anormal', False)
                if not volume_anormal:
                    print(f"❌ {symbol}: Fora da Value Area sem volume anormal")
                    return False
                print(f"⚠️ {symbol}: Fora da Value Area mas com volume anormal")

        # Se chegou até aqui, todas as validações passaram
        print(f"✅ {symbol}: Volume Profile confirmou sinal de {sinal}")
        print("Detalhes da confirmação:")
        print(f"- Força da tendência: {volume_profile_data['forca_tendencia']:.2f}")
        print(f"- Pressão compradora: {volume_profile_data['pressao_compradora']:.2f}")
        print(f"- Pressão vendedora: {volume_profile_data['pressao_vendedora']:.2f}")
        print("=====================")
        return True

    except Exception as e:
        print(f"❌ Erro na validação do Volume Profile para {symbol}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False




async def processar_antiloss_imediato(symbol, sinal, tipo_sinal):
    """
    Processa antiloss imediato para um par específico

    Args:
        symbol (str): Símbolo para verificação
        sinal (str): Direção do sinal ('CALL' ou 'PUT')
        tipo_sinal (str): Tipo do sinal para registro
    """
    global antiloss_em_andamento, ultimo_par_negociado, antiloss_ativado, NumeroDeGales

    try:
        if antiloss_em_andamento:
            print("⚠️ Antiloss já em andamento - aguardando conclusão")
            return None, False, 0, False, None

        print(f"\n=== Processando Antiloss Imediato ===")
        print(f"Par: {symbol}")
        print(f"Sinal: {sinal}")
        print(f"Tipo: {tipo_sinal}")

        # Aguarda intervalo entre operações no mesmo par
        if ultimo_par_negociado == symbol:
            await asyncio.sleep(3)

        # Registra operação na tabela
        current_row_id = add_open_order_to_table(
            datetime.now().strftime("%H:%M:%S"),
            1.0,
            symbol,
            sinal,
            default_expiration * 60 - 2 if not symbol.startswith("stpRNG") else 15,
            0,
            False,
            True
        )

        # Marca início do antiloss
        antiloss_em_andamento = True

        try:
            # Verifica antiloss com timeout
            antiloss_result = await verificar_velas_antiloss(
                api,
                symbol,
                sinal,
                datetime.now(),
                current_row_id,
                NumeroDeGales
            )

            # Se não houver loss, registra win
            if not antiloss_result:
                update_order_in_table(
                    current_row_id,
                    datetime.now().strftime("%H:%M:%S"),
                    0,
                    "WIN",
                    f"Reset AntLoss ({tipo_sinal})"
                )

            # Atualiza último par negociado
            ultimo_par_negociado = symbol
            return None, False, 0, False, None

        finally:
            # Garante que antiloss_em_andamento seja resetado
            antiloss_em_andamento = False
            await asyncio.sleep(10)  # Intervalo entre operações

    except Exception as e:
        print(f"❌ Erro no antiloss imediato: {e}")
        antiloss_em_andamento = False
        traceback.print_exc()
        return None, False, 0, False, None


def initialize_telegram():
    global telegram_interface, telegram_pending_signals

    # Certifique-se de que a lista está inicializada
    if 'telegram_pending_signals' not in globals():
        global telegram_pending_signals
        telegram_pending_signals = []

    # Inicializa a interface do Telegram se necessário
    if not telegram_interface:
        from telegram_interface import TelegramInterface
        telegram_interface = TelegramInterface()

    # Verifica se o Telegram Manager existe
    telegram_manager = telegram_interface.get_telegram_manager()

    print("🔄 Interface Telegram inicializada")
    print(f"📨 Sinais pendentes: {len(telegram_pending_signals)}")

    return telegram_interface, telegram_manager





async def verificar_e_enviar_sinais(api, symbols):
    """
    Verifica e envia sinais para todas as estratégias suportando fim da vela.
    """
    global tick_data, volume_atual, estrategias_combinadas, stop_event
    global antiloss_ativado, antiloss_em_andamento, tipo_ordem_anterior
    global row_id, ultimo_par_negociado, default_expiration, should_send_orders
    global required_losses, pares_verificados_antiloss, modo_antiloss, VerificaSeAntlossEstavaAtivo
    global last_symbol, last_signal, last_sample_run, NumeroDeGales, em_espera
    global fluxo_active, mt4_receiver, hedge_active, type_order, last_trade_time
    global modo_entrada, fim_da_vela_time, velas
    global telegram_interface, telegram_manager
    global telegram_pending_signals  # Ensure telegram_pending_signals is global

    try:
        # Define janelas de tempo baseadas no timeframe
        now = datetime.now()
        minuto_atual = now.minute
        segundo_atual = now.second

        # Define janelas de tempo para reversão
        if default_expiration == 1:
            is_reversao_window = 57 <= segundo_atual <= 59 or 0 <= segundo_atual <= 1
            is_retracao_window = 37 <= segundo_atual <= 44
        else:
            proxima_vela = (minuto_atual // default_expiration + 1) * default_expiration
            eh_ultimo_minuto = minuto_atual == proxima_vela - 1
            is_reversao_window = eh_ultimo_minuto and segundo_atual >= 57
            dentro_timeframe = minuto_atual % default_expiration < default_expiration - 1
            is_retracao_window = dentro_timeframe and 37 <= segundo_atual <= 44

        is_execution_time = segundo_atual == 58

        # Inicializa sinal_pendente se não existir
        if not hasattr(verificar_e_enviar_sinais, 'sinal_pendente'):
            verificar_e_enviar_sinais.sinal_pendente = None

        # Verifica se passou tempo suficiente desde a última operação (1 minuto)
        current_time = time.time()
        if hasattr(verificar_e_enviar_sinais, 'last_trade_times'):
            for symbol, last_time in verificar_e_enviar_sinais.last_trade_times.items():
                if current_time - last_time < 60:  # 60 segundos
                    print(f"⏳ Aguardando tempo mínimo para operar {symbol} novamente")
                    print(f"Tempo restante: {60 - int(current_time - last_time)}s")
                    return None, False, 0, False, None
        else:
            verificar_e_enviar_sinais.last_trade_times = {}

        # Verificações iniciais do bot
        if stop_event.is_set() or not should_send_orders:
            return None, False, 0, False, None

        if antiloss_em_andamento:
            print("⚠️ Antiloss em andamento - aguardando resultado...")
            return None, False, 0, False, None

        # Processa gales se necessário
        if gales > 0 and last_symbol and last_signal:
            symbol = last_symbol
            sinal = last_signal
            sinal_info = (symbol, sinal)

            if modo_entrada == "fim_da_vela":
                print("\n=== Processando Gale no Modo Fim da Vela ===")
                duracao = calculate_candle_expiration(default_expiration)
                if duracao is None:
                    print("❌ Tempo insuficiente para gale. Aguardando próxima vela...")
                    await asyncio.sleep(0.5)
                    return None, False, 0, False, None
                print(f"✅ Gale com {duracao}s até o fim da vela")
            else:
                duracao = 15 if symbol.startswith("stpRNG") else default_expiration * 60 - 2
                print(f"✅ Gale com duração fixa de {duracao}s")

            antiloss_ativado_local = False
            return sinal_info, False, duracao, antiloss_ativado_local, row_id

        try:
            # Importa o módulo de estado compartilhado
            import shared_state

            # Se uma ordem estiver em andamento, não processa novos sinais
            if shared_state.is_order_in_progress():
                print("⚠️ Ordem em andamento, aguardando conclusão antes de processar novos sinais")
                return None, False, 0, False, None

            # Verifica se há sinais Telegram pendentes
            telegram_pending_signals = shared_state.get_pending_signals()

            if telegram_pending_signals:
                print("\n=== Verificando sinais Telegram ===")
                print(f"Sinais pendentes: {len(telegram_pending_signals)}")

                # Processa o primeiro sinal na fila
                signal_data = telegram_pending_signals[0]

                # Extrai informações do sinal
                symbol = signal_data['symbol']
                action = signal_data['action']
                timeframe = signal_data['timeframe']

                print(f"Processando sinal Telegram: {symbol} {action} {timeframe}M")

                # Verifica se o símbolo está nos ativos
                if not symbol in symbols or not simbolos_ativos.get(symbol, False):
                    print(f"❌ {symbol} não está ativo ou não disponível")
                    shared_state.remove_signal(0)  # Remove o sinal
                    return None, False, 0, False, None

                # Verifica validação de símbolos para antiloss restrito
                if modo_antiloss == "restrito" and symbol in pares_verificados_antiloss:
                    print(f"✅ {symbol} já completou antiloss no modo restrito")
                    pares_verificados_antiloss.pop(symbol)
                    shared_state.remove_signal(0)  # Remove o sinal
                    return None, False, 0, False, None


                symbol_candles = velas.get(symbol, [])


                # Aplicar validações adicionais
                sinal_validado = True

                if price_action_active:
                    price_action_result = await validar_price_action(symbol, action, symbol_candles)
                    if not price_action_result:
                        print(f"❌ Sinal rejeitado por Price Action para {symbol}")
                        sinal_validado = False

                if volume_profile_active and sinal_validado:
                    try:
                        current_price = float(symbol_candles[-1]['close'])
                        volume_result = validar_volume_profile(symbol, action, symbol_candles, current_price)
                        if not volume_result:
                            print(f"❌ Sinal rejeitado por Volume Profile para {symbol}")
                            sinal_validado = False
                    except Exception as e:
                        print(f"Erro na validação de Volume Profile: {e}")
                        sinal_validado = False

                # Marca o início do processamento de ordem
                shared_state.set_order_in_progress(True)

                # Se todas as validações passarem, processa o sinal
                if sinal_validado:
                    # Limpa todos os sinais da fila para evitar processamento duplicado
                    shared_state.clear_all_signals()

                    print(f"✅ Sinal Telegram validado para {symbol}: {action}")

                    # Processar antiloss se ativado
                    if antiloss_ativado:
                        return await processar_antiloss_imediato(symbol, action, "Telegram")

                    # Calcula duração baseada no modo de entrada
                    if modo_entrada == "fim_da_vela":
                        duracao = calculate_candle_expiration(timeframe)  # Usa o timeframe do sinal!
                        if duracao is None:
                            print(f"❌ Tempo insuficiente para sinal Telegram em {symbol}")
                            shared_state.set_order_in_progress(False)  # Reseta o status de ordem
                            return None, False, 0, False, None
                        print(f"✅ Sinal Telegram com {duracao}s até o fim da vela")
                    else:
                        duracao = 15 if symbol.startswith("stpRNG") else timeframe * 60 - 2

                    # Registra o último tempo de operação para este símbolo
                    if not hasattr(verificar_e_enviar_sinais, 'last_trade_times'):
                        verificar_e_enviar_sinais.last_trade_times = {}
                    verificar_e_enviar_sinais.last_trade_times[symbol] = time.time()

                    # MODIFICAÇÃO: Preserva a duração do sinal Telegram para uso nos gales
                    verificar_e_enviar_sinais.last_signal_info = signal_data

                    # Retorna as informações do sinal para execução
                    return (symbol, action), False, duracao, False, None
                else:
                    # Se o sinal não foi validado, remova-o e desative o flag de ordem em andamento
                    shared_state.remove_signal(0)
                    shared_state.set_order_in_progress(False)
                    print(f"❌ Sinal Telegram não validado para {symbol}. Removendo da fila.")

        except ImportError:
            print("Módulo shared_state não encontrado. Sinais Telegram não serão processados.")

        if reversao_value or retracao_value or ml_strategy_active or fluxo_active :
            resultados = await analisar_estrategias_e_filtros(
                api, symbols, tick_data, volume_atual, estrategias_combinadas
            )

        if abr_strategy_active:
            all_abr_signals = {}
            best_symbol = None
            best_confidence = 0

            # Primeiro, atualizamos as sequências atuais para todos os símbolos ativos
            for symbol in symbols:
                if not simbolos_ativos.get(symbol, False):
                    continue

                if symbol in velas and len(velas[symbol]) > 0:
                    last_candle = velas[symbol][-1]
                    abr_strategy.update_current_sequences(symbol, last_candle)

            # Depois, busca por sinais em todos os símbolos ativos
            for symbol in symbols:
                # Pula se o símbolo não está ativo
                if not simbolos_ativos.get(symbol, False):
                    print(f"❌ {symbol}: Par desativado - ignorando análise ABR")
                    continue

                # Skip último par negociado para evitar overtrading
                if symbol == ultimo_par_negociado:
                    print(f"⏩ {symbol}: Pulando - último par negociado")
                    continue

                if symbol in velas and isinstance(velas[symbol], (list, deque)) and len(velas[symbol]) >= 400:
                    # Forçar análise histórica para este símbolo específico
                    # Isso garante que tenhamos as sequências ótimas antes de buscar sinais
                    abr_strategy.analyze_historical_data(symbol, velas[symbol])

                    # Obtém sinal da estratégia ABR
                    signal, confidence, info = abr_strategy.get_signal(symbol, velas[symbol])

                    if signal:
                        print(f"\n=== Sinal ABR para {symbol} ===")
                        print(f"Sinal: {signal} com {confidence:.2f}% de confiança")
                        print(f"Sequência: {info}")

                        # Validar se o sinal segue a lógica correta de sequências
                        sequences = abr_strategy.get_pair_sequences(symbol)
                        current_red = sequences['red']
                        current_green = sequences['green']

                        # Verificação crítica para validar a lógica da estratégia ABR:
                        # - CALL só deve ser gerado após sequência de velas VERMELHAS
                        # - PUT só deve ser gerado após sequência de velas VERDES
                        valid_signal = True

                        if signal == "CALL" and current_red == 0:
                            print(f"❌ Sinal ABR inválido: CALL sem sequência de velas vermelhas")
                            valid_signal = False
                        elif signal == "PUT" and current_green == 0:
                            print(f"❌ Sinal ABR inválido: PUT sem sequência de velas verdes")
                            valid_signal = False

                        # Se o sinal não for válido, pula para o próximo símbolo
                        if not valid_signal:
                            continue

                        # Adiciona validações adicionais aqui se necessário
                        # Por exemplo, verificar volatilidade, filtros extras, etc.
                        volatility_ok = True
                        price_action_ok = True

                        if price_action_active:
                            price_action_ok = await validar_price_action(symbol, signal, velas[symbol])
                            if not price_action_ok:
                                print(f"❌ Sinal ABR rejeitado por Price Action para {symbol}")
                                continue

                        if volume_profile_active:
                            try:
                                current_price = float(velas[symbol][-1]['close'])
                                volume_profile_ok = validar_volume_profile(symbol, signal, velas[symbol], current_price)
                                if not volume_profile_ok:
                                    print(f"❌ Sinal ABR rejeitado por Volume Profile para {symbol}")
                                    continue
                            except Exception as e:
                                print(f"Erro na validação de Volume Profile: {e}")
                                continue

                        # Se passou por todas as validações, armazena o sinal
                        all_abr_signals[symbol] = {
                            "signal": signal,
                            "confidence": confidence,
                            "info": info
                        }

                        # Guarda o melhor sinal baseado na confiança
                        if confidence > best_confidence:
                            best_confidence = confidence
                            best_symbol = symbol
                else:
                    print(f"❌ {symbol}: Velas insuficientes para análise ABR")
                    continue

            # Se encontramos sinais, escolhemos o de maior confiança
            if all_abr_signals:
                best_symbol = best_symbol or max(all_abr_signals.keys(), key=lambda s: all_abr_signals[s]["confidence"])
                best_signal = all_abr_signals[best_symbol]["signal"]
                best_confidence = all_abr_signals[best_symbol]["confidence"]
                best_info = all_abr_signals[best_symbol]["info"]

                print(f"\n=== Melhor Sinal ABR: {best_symbol} ===")
                print(f"Sinal: {best_signal} com {best_confidence:.2f}% de confiança")
                print(f"Sequência: {best_info}")

                # Reseta outros tipos de entrada para evitar conflitos
                tipo_sinal_original = "ABR"

                # Processa antiloss se ativado
                if antiloss_ativado:
                    return await processar_antiloss_imediato(best_symbol, best_signal, "ABR")

                # Calcula duração baseada no modo de entrada
                if modo_entrada == "fim_da_vela":
                    duracao = calculate_candle_expiration(default_expiration)
                    if duracao is None:
                        print(f"❌ Tempo insuficiente para sinal ABR em {best_symbol}")
                        return None, False, 0, False, None
                    print(f"✅ Sinal ABR com {duracao}s até o fim da vela")
                else:
                    duracao = 15 if best_symbol.startswith("stpRNG") else default_expiration * 60 - 2

                # Registra o último tempo de operação para este símbolo
                if not hasattr(verificar_e_enviar_sinais, 'last_trade_times'):
                    verificar_e_enviar_sinais.last_trade_times = {}
                verificar_e_enviar_sinais.last_trade_times[best_symbol] = time.time()

                # Retorna o sinal no formato esperado pelo sistema principal
                return (best_symbol, best_signal), False, duracao, False, None


        if mt4_receiver and mt4_receiver.get_pending_signals():
            print("\n=== Verificando sinais MT4 ===")
            pending_signals = mt4_receiver.get_pending_signals()
            print(f"Sinais pendentes: {pending_signals}")

            for symbol, signal_data in pending_signals.items():
                if modo_antiloss == "restrito" and symbol in pares_verificados_antiloss:
                    print(f"✅ {symbol} já completou antiloss no modo restrito")
                    pares_verificados_antiloss.pop(symbol)
                    if modo_entrada == "fim_da_vela":
                        duracao = calculate_candle_expiration(default_expiration)
                        if duracao is None:
                            print("❌ Tempo insuficiente para sinal MT4")
                            mt4_receiver.mark_order_complete()
                            continue
                        print(f"✅ Sinal MT4 com {duracao}s até o fim da vela")
                    else:
                        duracao = 15 if symbol.startswith("stpRNG") else default_expiration * 60 - 2
                    return signal_data['sinal_info'], False, duracao, False, None

                symbol_candles = velas.get(symbol, [])
                if len(symbol_candles) < 3:
                    continue

                sinal_validado = True
                if price_action_active:
                    sinal_validado = await validar_price_action(symbol, signal_data['sinal_info'][1], symbol_candles)

                if volume_profile_active and sinal_validado:
                    current_price = float(symbol_candles[-1]['close'])
                    sinal_validado = validar_volume_profile(symbol, signal_data['sinal_info'][1], symbol_candles, current_price)

                if sinal_validado:
                    if antiloss_ativado:
                        return await processar_antiloss_imediato(symbol, signal_data['sinal_info'][1], "MT4")

                    if modo_entrada == "fim_da_vela":
                        duracao = calculate_candle_expiration(default_expiration)
                        if duracao is None:
                            print("❌ Tempo insuficiente para sinal MT4")
                            mt4_receiver.mark_order_complete()
                            continue
                        print(f"✅ Sinal MT4 com {duracao}s até o fim da vela")
                    else:
                        duracao = 15 if symbol.startswith("stpRNG") else default_expiration * 60 - 2
                    return signal_data['sinal_info'], False, duracao, False, None

                mt4_receiver.mark_order_complete()

        if ml_strategy_active:
            print("\n=== Verificando Sinais ML ===")
            all_ml_signals = {}  # Armazena todos os sinais ML encontrados
            best_ml_confidence = 0
            best_ml_symbol = None
            
            for symbol in symbols:
                try:
                    # Skip if this is the last traded pair
                    if symbol == ultimo_par_negociado:
                        print(f"⏩ {symbol}: Pulando - último par negociado")
                        continue

                    # Skip if this symbol is not active
                    if not simbolos_ativos.get(symbol, False):
                        print(f"❌ {symbol}: Par desativado - ignorando análise ML")
                        continue

                    # Skip if we don't have enough candle data
                    if symbol not in velas or len(velas[symbol]) < 100:
                        print(f"❌ {symbol}: Dados insuficientes para análise ML ({len(velas.get(symbol, []))}/100)")
                        continue

                    # Get ML signal for this symbol
                    ml_signal = get_ml_signal(symbol, velas[symbol])

                    if ml_signal:
                        print(f"\n=== Sinal ML Detectado para {symbol} ===")
                        print(f"Direção: {ml_signal}")

                        # Obter confiança do sinal (se disponível)
                        try:
                            ml_strategy_obj = trading_strategies.get(symbol)
                            if ml_strategy_obj and hasattr(ml_strategy_obj, 'last_confidence'):
                                confidence = ml_strategy_obj.last_confidence
                            else:
                                confidence = 0.7  # Confiança padrão
                        except:
                            confidence = 0.7

                        # Apply validation filters just like other strategies
                        sinal_validado = True
                        # Price Action validation
                        if price_action_active:
                            sinal_validado = await validar_price_action(symbol, ml_signal, velas[symbol])
                            if not sinal_validado:
                                print(f"❌ Sinal ML rejeitado por Price Action para {symbol}")
                                continue

                        # Volume Profile validation
                        if volume_profile_active and sinal_validado:
                            try:
                                current_price = float(velas[symbol][-1]['close'])
                                volume_result = validar_volume_profile(symbol, ml_signal, velas[symbol], current_price)
                                if not volume_result:
                                    print(f"❌ Sinal ML rejeitado por Volume Profile para {symbol}")
                                    continue
                            except Exception as e:
                                print(f"Erro na validação de Volume Profile para ML: {e}")
                                continue

                        # Se passou por todas as validações, armazena o sinal
                        all_ml_signals[symbol] = {
                            "signal": ml_signal,
                            "confidence": confidence
                        }

                        # Guarda o melhor sinal baseado na confiança
                        if confidence > best_ml_confidence:
                            best_ml_confidence = confidence
                            best_ml_symbol = symbol

                        print(f"✅ Sinal ML validado para {symbol}: {ml_signal} (confiança: {confidence:.3f})")

                except Exception as e:
                    print(f"❌ Erro ao processar ML para {symbol}: {e}")
                    continue

            # Se encontramos sinais ML, escolhemos o de maior confiança
            if all_ml_signals:
                # Escolhe o melhor sinal
                best_symbol = best_ml_symbol or max(all_ml_signals.keys(), key=lambda s: all_ml_signals[s]["confidence"])
                best_signal = all_ml_signals[best_symbol]["signal"]
                best_confidence = all_ml_signals[best_symbol]["confidence"]

                print(f"\n=== Melhor Sinal ML: {best_symbol} ===")
                print(f"Sinal: {best_signal} com confiança {best_confidence:.3f}")
                print(f"Total de sinais ML encontrados: {len(all_ml_signals)}")

                # Check if we should process antiloss first
                if antiloss_ativado:
                    print(f"✅ Processando antiloss para melhor sinal ML: {best_symbol}")
                    return await processar_antiloss_imediato(best_symbol, best_signal, "ML")

                # Calculate duration based on entry mode
                if modo_entrada == "fim_da_vela":
                    duracao = calculate_candle_expiration(default_expiration)
                    if duracao is None:
                        print(f"❌ Tempo insuficiente para sinal ML em {best_symbol}")
                    else:
                        print(f"✅ Sinal ML com {duracao}s até o fim da vela")
                else:
                    duracao = 15 if best_symbol.startswith("stpRNG") else default_expiration * 60 - 2

                if duracao is not None:
                    # Register the last trading time for this symbol
                    if not hasattr(verificar_e_enviar_sinais, 'last_trade_times'):
                        verificar_e_enviar_sinais.last_trade_times = {}
                    verificar_e_enviar_sinais.last_trade_times[best_symbol] = time.time()

                    return (best_symbol, best_signal), False, duracao, False, None

        if fluxo_active:
            current_time = time.time()
            # Verificar STP pairs
            for symbol in symbols:
                if symbol.startswith("stpRNG") and simbolos_ativos.get(symbol, False):
                    try:
                        # Skip se for último par negociado
                        if symbol == ultimo_par_negociado:
                            await asyncio.sleep(0.5)
                            continue

                        # Verificar se tem velas suficientes
                        if not velas.get(symbol) or len(velas[symbol]) < 3:
                            print(f"❌ {symbol}: Dados insuficientes")
                            continue

                        sinal = random.choice(["CALL", "PUT"])

                        # Se antiloss estiver ativo, verifica condições
                        if antiloss_ativado:
                            await verificar_velas_antiloss(api, symbol, sinal, datetime.now(), None, NumeroDeGales)

                        print(f"\n=== Entrada Aleatória STP ===")
                        print(f"Par: {symbol}")
                        print(f"Direção: {sinal}")

                        return (symbol, sinal), False, 2, False, None

                    except Exception as e:
                        print(f"❌ Erro ao processar {symbol}: {e}")
                        continue

                if symbol in velas and len(velas[symbol]) >= 20:
                    try:
                        flow_signal = await analyze_fluxo(velas[symbol])
                        if not flow_signal:
                            continue

                        sinal_validado = True

                        if price_action_active:
                            sinal_validado = await validar_price_action(symbol, flow_signal, velas[symbol])
                            if not sinal_validado:
                                continue

                        if volume_profile_active and sinal_validado:
                            try:
                                current_price = float(velas[symbol][-1]['close'])
                                sinal_validado = await usar_volume_profile_na_analise(velas[symbol], current_price)
                                if not sinal_validado:
                                    continue
                            except Exception as e:
                                print(f"Erro na validação de Volume Profile para {symbol}: {e}")
                                continue

                        if sinal_validado:
                            if antiloss_ativado:
                                return await processar_antiloss_imediato(symbol, flow_signal, "Fluxo")

                            if modo_entrada == "fim_da_vela":
                                duracao = calculate_candle_expiration(default_expiration)
                                if duracao is None:
                                    print(f"❌ Tempo insuficiente para sinal de fluxo em {symbol}")
                                    continue
                                print(f"✅ Sinal de fluxo com {duracao}s até o fim da vela")
                            else:
                                duracao = 15 if symbol.startswith("stpRNG") else default_expiration * 60 - 2

                            print(f"✅ Sinal de fluxo validado para {symbol}: {flow_signal}")
                            return (symbol, flow_signal), False, duracao, False, None

                    except Exception as e:
                        print(f"Erro ao processar fluxo para {symbol}: {e}")
                        continue

        if reversao_value or retracao_value:
            for symbol, sinal in resultados.items():
                if symbol == ultimo_par_negociado:
                    continue

                if not simbolos_ativos.get(symbol, False):
                    continue

                # Verifica se está na janela correta
                if reversao_value and is_reversao_window:
                    sr_levels = calculate_sr_levels(velas.get(symbol, []))
                    preco_atual = float(velas[symbol][-1]['open'])
                    sinal_valido, razao = validate_sr_signal(preco_atual, velas[symbol], sinal, sr_levels)

                    if not sinal_valido or \
                            (volume_profile_active and not validar_volume_profile(symbol, sinal, velas[symbol],
                                                                                  preco_atual)) or \
                            (price_action_active and not await validar_price_action(symbol, sinal, velas[symbol])):
                        continue

                    if antiloss_ativado:
                        if is_execution_time:
                            verificar_e_enviar_sinais.sinal_pendente = {
                                'type': 'antiloss',
                                'symbol': symbol,
                                'sinal': sinal,
                                'hora_validacao': now
                            }
                        return None, False, 0, False, None

                    if modo_entrada == "fim_da_vela":
                        duracao = calculate_candle_expiration(default_expiration)
                        if duracao is None:
                            print(f"❌ Tempo insuficiente para sinal de reversão em {symbol}")
                            continue
                        print(f"✅ Sinal de reversão com {duracao}s até o fim da vela")
                    else:
                        duracao = 15 if symbol.startswith("stpRNG") else default_expiration * 60 - 2

                    if is_execution_time:
                        verificar_e_enviar_sinais.sinal_pendente = {
                            'type': 'reversao',
                            'symbol': symbol,
                            'sinal': sinal,
                            'hora_validacao': now
                        }
                        return None, False, 0, False, None

                    return (symbol, sinal), False, duracao, False, None

                elif retracao_value and is_retracao_window:
                    # NOVA LÓGICA CORRETA DE RETRAÇÃO
                    print(f"\n🔍 Analisando RETRAÇÃO para {symbol}...")
                    
                    resultado_retracao = analisar_retracao_correta(velas[symbol])
                    
                    if resultado_retracao and resultado_retracao['sinal']:
                        sinal_retracao = resultado_retracao['sinal']
                        confianca = resultado_retracao['confianca']
                        motivo = resultado_retracao['motivo']
                        
                        print(f"✅ RETRAÇÃO DETECTADA: {sinal_retracao}")
                        print(f"   Confiança: {confianca:.2f}")
                        print(f"   Motivo: {motivo}")
                        
                        # Só prossegue se a confiança for suficiente
                        if confianca >= 0.5:
                            # Validações adicionais (se ativadas)
                            sinal_validado = True
                            
                            if price_action_active:
                                sinal_validado = await validar_price_action(symbol, sinal_retracao, velas[symbol])
                                if not sinal_validado:
                                    print("❌ Retração rejeitada por Price Action")
                                    continue
                                    
                            if volume_profile_active:
                                preco_atual = float(velas[symbol][-1]['close'])
                                sinal_validado = validar_volume_profile(symbol, sinal_retracao, velas[symbol], preco_atual)
                                if not sinal_validado:
                                    print("❌ Retração rejeitada por Volume Profile")
                                    continue
                            
                            if sinal_validado:
                                if antiloss_ativado:
                                    return await processar_antiloss_imediato(symbol, sinal_retracao, "Retracao")

                                if modo_entrada == "fim_da_vela":
                                    duracao = calculate_candle_expiration(default_expiration)
                                    if duracao is None:
                                        print(f"❌ Tempo insuficiente para retração em {symbol}")
                                        continue
                                    print(f"✅ Retração com {duracao}s até o fim da vela")
                                else:
                                    duracao = 15 if symbol.startswith("stpRNG") else default_expiration * 60 - 2

                                print(f"🎯 EXECUTANDO RETRAÇÃO: {symbol} {sinal_retracao}")
                                return (symbol, sinal_retracao), True, duracao, False, None
                        else:
                            print(f"❌ Confiança insuficiente para retração: {confianca:.2f} < 0.5")
                    else:
                        print("❌ Nenhuma condição de retração válida encontrada")
                        
                    continue  # Vai para o próximo símbolo

                else:
                    print(f"Sinal detectado para {symbol}, aguardando janela de tempo adequada")



        # Processa sinais pendentes
        if is_execution_time and verificar_e_enviar_sinais.sinal_pendente:
            sinal_dados = verificar_e_enviar_sinais.sinal_pendente

            if sinal_dados['type'] == 'antiloss':
                print(f"⏱️ Executando antiloss validado para {sinal_dados['symbol']} (Reversao)")
                antiloss_em_andamento = True

                if modo_entrada == "fim_da_vela":
                    duracao = calculate_candle_expiration(default_expiration)
                else:
                    duracao = 15 if sinal_dados['symbol'].startswith("stpRNG") else default_expiration * 60 - 2

                row_id = add_open_order_to_table(
                    now.strftime("%H:%M:%S"),
                    1.0,
                    sinal_dados['symbol'],
                    sinal_dados['sinal'],
                    duracao,
                    0,
                    False,
                    True
                )

                try:
                    antiloss_result = await verificar_velas_antiloss(
                        api,
                        sinal_dados['symbol'],
                        sinal_dados['sinal'],
                        now,
                        row_id,
                        NumeroDeGales
                    )

                    if not antiloss_result:
                        update_order_in_table(
                            row_id,
                            now.strftime("%H:%M:%S"),
                            0,
                            "WIN",
                            "Reset AntLoss (Reversao)"
                        )
                finally:
                    antiloss_em_andamento = False
                    verificar_e_enviar_sinais.sinal_pendente = None
                    await asyncio.sleep(10)

                return None, False, 0, False, None

            elif sinal_dados['type'] == 'reversao':
                print(f"⏱️ Executando reversão para {sinal_dados['symbol']}")
                verificar_e_enviar_sinais.sinal_pendente = None

                if modo_entrada == "fim_da_vela":
                    duracao = calculate_candle_expiration(default_expiration)
                else:
                    duracao = 15 if sinal_dados['symbol'].startswith("stpRNG") else default_expiration * 60 - 2

                return (sinal_dados['symbol'], sinal_dados['sinal']), False, duracao, False, None

        return None, False, 0, False, None

    except Exception as e:
        print(f"❌ Erro ao verificar sinais: {e}")
        traceback.print_exc()
        return None, False, 0, False, None



async def update_clock():
    while True:
        try:
            now = datetime.now().strftime("%H:%M:%S")
            dpg.set_value("clock_tex", now)
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Erro ao atualizar relógio: {e}")
            await asyncio.sleep(5)

def run_async_function(async_func):
    def wrapper():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(async_func())
        finally:
            loop.close()

    return threading.Thread(target=wrapper).start()

# Função para iniciar a atualização do relógio em uma thread separada
def start_clock_update():
    run_async_function(update_clock)


def resetarlucro():
    """Reseta o lucro com validações e proteções"""
    global lucro_total, initial_balance, saldo_atual, total_wins, total_losses
    global should_send_orders, masaniello, cached_stake, stop_message_sent

    try:
        # Verifica se o bot está pausado
        if stop_event.is_set():
            print("\n⚠️ Não é possível resetar o lucro com o bot em execução!")
            with dpg.window(label="Aviso", modal=True, no_close=True, tag="reset_warning", width=300, height=100):
                dpg.add_text("Pause o bot antes de resetar o lucro!")
                dpg.add_button(label="OK", callback=lambda: dpg.delete_item("reset_warning"))
            return False

        print("\n=== Iniciando Reset de Lucro ===")

        # Backup dos valores anteriores
        old_initial = initial_balance
        old_saldo = saldo_atual

        try:
            # Atualiza saldo inicial para o saldo atual
            initial_balance = saldo_atual
            lucro_total = 0
            cached_stake = None

            # Reinicializa o Masaniello
            masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)
            masaniello.atualizarSaldo(saldo_atual, "base")

            # Força a reinicialização do stake
            cached_stake = masaniello.getStake()

            # Atualiza interface
            if dpg.does_item_exist("saldo_text"):
                dpg.set_value("saldo_text", f"$ {saldo_atual:.2f}")
            if dpg.does_item_exist("pnl_text"):
                dpg.set_value("pnl_text", f"$ {lucro_total:.2f}")
                dpg.configure_item("pnl_text", color=(0, 255, 0) if lucro_total >= 0 else (255, 0, 0))

            # Atualiza outras estatísticas
            update_status()

            print(f"=== Reset de Lucro Concluído ===")
            print(f"Novo saldo inicial: ${initial_balance:.2f}")
            print(f"Lucro zerado: ${lucro_total:.2f}")
            print(f"Novo stake inicial: ${cached_stake:.2f}")
            print(f"Bot continua pausado e pronto para iniciar")
            print("================================")

            return True

        except Exception as e:
            # Restaura valores em caso de erro
            initial_balance = old_initial
            saldo_atual = old_saldo
            raise e

    except Exception as e:
        print(f"Erro ao resetar lucro: {e}")
        import traceback
        traceback.print_exc()
        return False


def reset_bot_state():
    """Reseta o estado do bot para primeira inicialização"""
    global total_wins, total_losses, lucro_total, saldo_atual, transactions
    global previous_num_transactions, cached_stake, initial_balance
    global is_running, em_espera, should_send_orders, stop_message_sent
    global velas, tick_data, row_id, gales, tipo_ordem_anterior, VerificaSeAntlossEstavaAtivo
    global configuracoes_gerenciamentos  # Adicionando para resetar ciclos

    reset_stop_message()
    total_wins = 0
    total_losses = 0
    lucro_total = 0
    last_symbol = None
    last_signal = None
    VerificaSeAntlossEstavaAtivo = False
    saldo_atual = initial_balance
    cached_stake = None
    transactions = []
    previous_num_transactions = 0
    velas = {}
    tick_data = []
    em_espera = False
    stop_message_sent = False
    row_id = None
    gales = 0
    tipo_ordem_anterior = None

    # Reset específico para os ciclos
    if "Ciclos" in configuracoes_gerenciamentos:
        configuracoes_gerenciamentos["Ciclos"].update({
            "linha_atual": 0,  # Volta para primeira linha
            "coluna_atual": 0,  # Volta para primeira coluna
            "linha_atual_repetindo": False,  # Reset do estado de repetição
            "lucro_inicial_ciclo": 0.0  # Reset do lucro inicial do ciclo
        })

    # Limpar tabela de transações
    if dpg.does_item_exist("transactions_table"):
        children = dpg.get_item_children("transactions_table", slot=1)
        if children:
            for child in children:
                dpg.delete_item(child)

    # Salva o estado resetado
    salvar_configuracoes_gerenciamento()

    print("\n=== Estado do Bot Resetado ===")
    print("✅ Contadores zerados")
    print("✅ Ciclos reiniciados na primeira linha")
    print("✅ Tabela de transações limpa")
    print("============================")

    update_status()


def inicializar_estado_bot():
    """Inicializa/reinicia o estado do bot garantindo estado inicial correto"""
    global configuracoes_gerenciamentos, cached_stake

    try:
        print("\n=== Inicializando Estado do Bot ===")

        # Garante que os ciclos começam do início
        if "Ciclos" in configuracoes_gerenciamentos:
            config = configuracoes_gerenciamentos["Ciclos"]

            # Reset da posição do ciclo
            config["linha_atual"] = 0
            config["coluna_atual"] = 0
            config["linha_atual_repetindo"] = False

            # Pega valor inicial do ciclo
            matriz = config["matriz_ciclos"]
            if matriz and matriz[0] and matriz[0][0] > 0:
                cached_stake = float(matriz[0][0])
                print(f"✅ Stake inicial definido: ${cached_stake:.2f}")

            print(f"✅ Ciclos resetados para primeira posição")

            # Salva configuração
            salvar_configuracoes_gerenciamento()

        print("=== Inicialização Concluída ===\n")
        return True

    except Exception as e:
        print(f"❌ Erro ao inicializar estado do bot: {e}")
        import traceback
        traceback.print_exc()
        return False


def reset_bot():
    """Reseta todas as configurações do bot para os valores iniciais"""
    global total_wins, total_losses, lucro_total, saldo_atual, transactions
    global previous_num_transactions, cached_stake, masaniello, is_running
    global initial_balance, em_espera, should_send_orders, stop_message_sent
    global row_id, gales, tipo_ordem_anterior, ultimo_par_negociado
    global configuracoes_gerenciamentos , VerificaSeAntlossEstavaAtivo # Adicionado para acessar as configs dos ciclos

    try:
        # Verifica se o bot está em execução
        if stop_event.is_set():
            with dpg.window(label="Aviso", modal=True, no_close=True, tag="reset_warning", width=300, height=100):
                dpg.add_text("O bot precisa estar parado para fazer o reset!")
                dpg.add_button(label="OK", callback=lambda: dpg.delete_item("reset_warning"))
            return

        print("\n=== Iniciando Reset Completo do Bot ===")

        # Reset das variáveis de controle
        stop_message_sent = False
        em_espera = False
        row_id = None
        gales = 0
        tipo_ordem_anterior = None
        ultimo_par_negociado = None

        # Reset de estatísticas
        total_wins = 0
        total_losses = 0
        lucro_total = 0
        previous_num_transactions = 0
        transactions.clear()

        reset_stop_message()
        total_wins = 0
        total_losses = 0
        lucro_total = 0
        last_symbol = None
        last_signal = None
        VerificaSeAntlossEstavaAtivo = False
        saldo_atual = initial_balance
        cached_stake = None
        transactions = []
        previous_num_transactions = 0
        velas = {}
        tick_data = []
        em_espera = False
        stop_message_sent = False
        row_id = None
        gales = 0
        tipo_ordem_anterior = None


        # Reset dos ciclos - Modificado para garantir reset em ambos os modos
        config = configuracoes_gerenciamentos["Ciclos"]
        config["linha_atual"] = 0
        config["coluna_atual"] = 0
        config["linha_atual_repetindo"] = False  # Reseta flag de repetição
        config["lucro_inicial_ciclo"] = 0.0  # Reseta lucro inicial do ciclo

        # Reset do Masaniello
        cached_stake = None
        masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)

        # Limpa a tabela de transações
        if dpg.does_item_exist("transactions_table"):
            children = dpg.get_item_children("transactions_table", slot=1)
            if children:
                for child in children:
                    dpg.delete_item(child)


        print("=== Reset Completo ===")
        print("✅ Todas as variáveis resetadas")
        print("✅ Interface atualizada")
        print("✅ Ciclos reiniciados (linha 0, coluna 0)")
        print("=====================\n")

        return True

    except Exception as e:
        print(f"Erro ao resetar bot: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_config_directory():
    """Retorna o diretorio apropriado para salvar as configuracoes"""
    try:
        # Tenta usar o diretorio do usuario primeiro
        user_home = os.path.expanduser("~")
        config_dir = os.path.join(user_home, ".fenixbot")

        # Tenta criar o diretorio se nao existir
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        # Testa se tem permissao de escrita
        test_file = os.path.join(config_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)

        return config_dir
    except:
        # Se falhar, usa o diretorio atual do programa
        try:
            if getattr(sys, 'frozen', False):
                # Se for executavel
                program_dir = os.path.dirname(sys.executable)
            else:
                # Se for script Python
                program_dir = os.path.dirname(os.path.abspath(__file__))

            config_dir = os.path.join(program_dir, "config")
            if not os.path.exists(config_dir):
                os.makedirs(config_dir)
            return config_dir
        except:
            # Se tudo falhar, usa diretorio temporario
            import tempfile
            temp_dir = os.path.join(tempfile.gettempdir(), "fenixbot")
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)
            return temp_dir


def salvar_tokens():
    """Salva os tokens de forma segura"""
    config_dir = get_config_directory()
    token_file = os.path.join(config_dir, "token.json")

    try:
        demo_token = dpg.get_value("demo_token_input")
        real_token = dpg.get_value("real_token_input")

        if demo_token and real_token:
            # Salva em arquivo temporario primeiro
            temp_file = os.path.join(config_dir, "temp_token.json")
            with open(temp_file, 'w') as f:
                json.dump({
                    "demo_token": demo_token,
                    "real_token": real_token,
                }, f, indent=2)

            # Move para arquivo final
            if os.path.exists(token_file):
                os.replace(token_file, token_file + ".bak")
            os.replace(temp_file, token_file)

            print("Tokens salvos com sucesso")
            dpg.delete_item("token_popup")
        else:
            print("Erro: ambos os tokens devem ser preenchidos")

    except Exception as e:
        print(f"Erro ao salvar tokens: {e}")

        if dpg.does_item_exist("token_error_popup"):
            dpg.delete_item("token_error_popup")

        with dpg.window(label="Erro ao Salvar Tokens", modal=True, tag="token_error_popup", width=400, height=200):
            dpg.add_text(f"Erro ao salvar tokens: {str(e)}")
            dpg.add_text("\nSugestoes:")
            dpg.add_text("1. Execute o programa como administrador")
            dpg.add_text("2. Verifique as permissoes da pasta")
            dpg.add_text(f"3. Pasta atual: {config_dir}")
            dpg.add_button(label="OK", callback=lambda: dpg.delete_item("token_error_popup"))


def carregar_tokens():
    """Carrega os tokens salvos"""
    global demo_token, real_token

    config_dir = get_config_directory()
    token_file = os.path.join(config_dir, "token.json")

    try:
        if os.path.exists(token_file):
            with open(token_file, "r") as f:
                tokens = json.load(f)
                demo_token = tokens.get("demo_token", "")
                real_token = tokens.get("real_token", "")

            print("Tokens carregados com sucesso")
            return demo_token, real_token

    except Exception as e:
        print(f"Erro ao carregar tokens: {e}")

    return "", ""


def carregar_tokens_ao_iniciar():
    """Carrega os tokens ao iniciar a GUI e define ambos os tokens, Demo, Real e o Chat ID."""

    demo_token, real_token = carregar_tokens()  # Carrega os tokens salvos

    # Define os tokens carregados nos campos de entrada, se eles existirem
    if demo_token:
        print(f"Token Demo carregado automaticamente: {demo_token}")
        if dpg.does_item_exist("demo_token_input"):
            dpg.set_value("demo_token_input", demo_token)

    if real_token:
        print(f"Token Real carregado automaticamente: {real_token}")
        if dpg.does_item_exist("real_token_input"):
            dpg.set_value("real_token_input", real_token)



async def logout():
    global api
    if api:
        try:
            await api.logout()  # Logout da API
            print("Logout realizado com sucesso.")
        except APIError as e:
            print(f"Erro ao tentar deslogar: {e}")
    else:
        print("API não está logada.")



def aplicar_tema_moderno():
    with dpg.theme() as dark_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255))  # Cor do texto (branco)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))  # Fundo da janela
            dpg.add_theme_color(dpg.mvThemeCol_Border, (50, 50, 50))  # Cor das bordas
            dpg.add_theme_color(dpg.mvThemeCol_Button, (44, 62, 80))  # Cor dos botões
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (52, 73, 94))  # Cor do botão quando hover
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (41, 128, 185))  # Cor do botão ao clicar
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (40, 40, 40))  # Fundo dos campos de entrada
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (41, 128, 185))  # Fundo ao passar o mouse
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (41, 128, 185))  # Fundo ao clicar
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (40, 40, 40))  # Fundo da barra de rolagem
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (70, 70, 70))  # Cor do controle da barra de rolagem
            dpg.add_theme_color(dpg.mvThemeCol_Header, (52, 152, 219))  # Cabeçalhos
            dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (41, 128, 185))  # Cabeçalhos ao passar o mouse
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (31, 97, 141))  # Cabeçalhos ao clicar

            # Modificações de estilos
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 5)  # Padding das janelas
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 7)  # Bordas arredondadas dos frames
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 5, 5)  # Espaçamento entre itens
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 5)  # Bordas arredondadas da barra de rolagem
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 5)  # Bordas arredondadas dos controles de deslizamento

    dpg.bind_theme(dark_theme)  # Aplica o tema globalmente



def create_transactions_table():
    """Cria uma tabela moderna e funcional para as transações"""
    try:
        # Tema personalizado para a tabela
        with dpg.theme() as table_theme:
            with dpg.theme_component(dpg.mvAll):
                # Cores de fundo
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (35, 35, 35))
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (45, 45, 45))

                # Cores do cabeçalho
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (55, 55, 55))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (45, 45, 50))

                # Cores da borda
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, (60, 60, 60))
                dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (40, 40, 40))

                # Estilo geral
                dpg.add_theme_style(dpg.mvStyleVar_CellPadding, 4, 2)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 4, 2)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 10)

        # Grupo principal que contém a tabela
        with dpg.group(horizontal=False , height=-35):
            # Cria a tabela
            with dpg.table(header_row=True,
                           resizable=True,
                           policy=dpg.mvTable_SizingStretchProp,
                           borders_innerH=True,
                           borders_outerH=True,
                           borders_innerV=True,
                           borders_outerV=True,
                           tag="transactions_table"):


                dpg.add_table_column(label=language_manager.get_text("HORA_ABERTURA"), tag="col_hora_abertura" , init_width_or_weight=0.10)
                dpg.add_table_column(label=language_manager.get_text("HORA_FECHAMENTO"), tag="col_hora_fechamento", init_width_or_weight=0.11)
                dpg.add_table_column(label=language_manager.get_text("TIPO_SINAL"), tag="col_tipo_sinal", init_width_or_weight=0.08)
                dpg.add_table_column(label=language_manager.get_text("ENTRADA"), tag="col_entrada", init_width_or_weight=0.08)
                dpg.add_table_column(label=language_manager.get_text("PARIDADES"), tag="col_paridades", init_width_or_weight=0.12)
                dpg.add_table_column(label=language_manager.get_text("GALES"), tag="col_gales", init_width_or_weight=0.08)
                dpg.add_table_column(label=language_manager.get_text("DIRECAO"), tag="col_direcao", init_width_or_weight=0.08)
                dpg.add_table_column(label=language_manager.get_text("DURACAO"), tag="col_duracao", init_width_or_weight=0.08)
                dpg.add_table_column(label=language_manager.get_text("W_L"), tag="col_wl", init_width_or_weight=0.05)
                dpg.add_table_column(label=language_manager.get_text("COMENTARIOS"), tag="col_comentarios", init_width_or_weight=0.23)

                # Aplica o tema
                dpg.bind_item_theme("transactions_table", table_theme)

        print("Tabela de transações criada com sucesso!")
        return True

    except Exception as e:
        print(f"Erro ao criar tabela de transações: {e}")
        import traceback
        traceback.print_exc()
        return False



def setup_fonts():
    with dpg.font_registry():
        # Pega o caminho da fonte usando a função get_font_path
        default_font_path = get_font_path("HappySelfie-ov9m0.ttf")

        # Verifica se a fonte existe
        if os.path.exists(default_font_path):
            default_font = dpg.add_font(default_font_path, 14)
            print(f"Fonte HappySelfie carregada com sucesso.")
        else:
            print(f"Erro: Fonte HappySelfie não encontrada.")
            default_font = None
    return default_font


def get_font_path(font_name):
    if getattr(sys, 'frozen', False):  # Se estiver rodando no executável
        base_path = sys._MEIPASS  # Caminho para os arquivos empacotados
    else:
        base_path = os.path.abspath(".")  # Caminho normal durante o desenvolvimento
    return os.path.join(base_path, font_name)

def open_statistics_window():
    if dpg.does_item_exist("statistics_window"):
        dpg.delete_item("statistics_window")

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    window_width = 800
    window_height = 600
    pos_x = (viewport_width - window_width) // 2
    pos_y = (viewport_height - window_height) // 2

    with dpg.window(label="Estatisticas Detalhadas", tag="statistics_window", width=window_width, height=window_height,
                    no_resize=True, no_collapse=True, pos=[pos_x, pos_y]):
        create_statistics_content()

    # Apply custom theme to the statistics window
    with dpg.theme() as statistics_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 70, 70))
            dpg.add_theme_color(dpg.mvThemeCol_Tab, (50, 50, 50))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (70, 70, 70))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, (90, 90, 90))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 120, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)

    dpg.bind_item_theme("statistics_window", statistics_theme)



def resource_path(relative_path):
    """Função para obter o caminho absoluto do arquivo, seja rodando como .py ou como .exe."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# Acessando o ícone e outros arquivos
icon_path = resource_path("fnx.ico")
mp3_file = resource_path("cash_sound.mp3")
qrcode_path = resource_path("qrcode_pix.png")


def safe_play_sound(sound_file):
    """Toca o som de forma segura, com tratamento de erros."""
    try:
        # Inicializa o mixer com diferentes configurações
        try:
            pygame.mixer.init(44100, -16, 2, 2048)
        except:
            try:
                pygame.mixer.init(44100, 16, 2, 2048)
            except:
                try:
                    pygame.mixer.init()
                except:
                    print("Sistema de áudio não disponível - Som não será reproduzido")
                    return

        try:
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
            # Aguarda o som terminar de tocar
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Aviso: Não foi possível tocar o som - {str(e)}")
            return

    except Exception as e:
        print(f"Aviso: Sistema de áudio não inicializado - {str(e)}")
    finally:
        try:
            pygame.mixer.quit()
        except:
            pass

def play_cash_sound():
    """Função wrapper para tocar o som."""
    try:
        if os.path.exists(mp3_file):
            safe_play_sound(mp3_file)
        else:
            print(f"Arquivo de som não encontrado: {mp3_file}")
    except Exception as e:
        print(f"Erro ao tocar som: {e}")

# Exemplo de uso no seu código para carregar uma imagem
img = Image.open(qrcode_path)


def create_statistics_content():
    """
    Cria e exibe estatísticas completas do bot incluindo análise de sinais externos.
    Usa apenas os contadores globais sem recalculá-los.
    """
    global statistics_transactions, symbols, total_wins, total_losses, saldo_atual, initial_balance, NumeroDeGales

    try:
        if not statistics_transactions:
            dpg.add_text("Nenhuma operacao realizada ainda.")
            return

        # Cores para interface
        GOLD = (255, 215, 0)  # Títulos
        CYAN = (0, 255, 255)  # Subtítulos
        GREEN = (0, 255, 0)  # Resultados positivos
        RED = (255, 0, 0)  # Resultados negativos
        BLUE = (0, 191, 255)  # Destaques
        WHITE = (255, 255, 255)  # Texto normal
        ORANGE = (255, 165, 0)  # Avisos

        # Encontra nível máximo de Gale
        max_gale = max([int(t.get("Gales", 0)) for t in statistics_transactions] + [NumeroDeGales])

        # Inicializa estruturas de dados para análise sem modificar contadores globais
        stats_por_par = {symbol: {
            "wins": 0,
            "losses": 0,
            "lucro": 0,
            "gales": {f"G{i}": {"wins": 0, "losses": 0, "lucro": 0}
                      for i in range(max_gale + 1)}
        } for symbol in symbols}

        # Atualiza tipos de sinais para incluir sinais externos
        stats_por_tipo = {
            tipo: {
                "wins": 0,
                "losses": 0,
                "lucro": 0,
                "gales": {f"G{i}": {"wins": 0, "losses": 0, "lucro": 0}
                          for i in range(max_gale + 1)}
            } for tipo in ["Retracao", "Reversao", "Fluxo", "Externo" , "PPONetwork" , "ABR" ]
        }

        stats_por_gale = {
            f"G{i}": {"wins": 0, "losses": 0, "lucro": 0, "operacoes": 0}
            for i in range(max_gale + 1)
        }

        lucro_total = saldo_atual - initial_balance if initial_balance is not None else 0
        total_operacoes = len(statistics_transactions)

        # Processa transações para estatísticas detalhadas sem afetar contadores globais
        for operacao in statistics_transactions:
            try:
                symbol = operacao["Par"]
                resultado = operacao["W/L"]
                tipo_sinal = operacao["Tipo Sinal"]
                lucro = float(operacao["Profit"])
                gales = int(operacao.get("Gales", 0))
                gale_key = f"G{gales}"

                # Determina o tipo base do sinal
                if tipo_sinal == "Externo" or "MT" in tipo_sinal:
                    tipo_base = "Externo"
                elif "PPONetwork" :
                    tipo_base = "PPONetwork"
                elif "ABR" :
                    tipo_base = "ABR"
                elif tipo_sinal == "Fluxo":
                    tipo_base = "Fluxo"
                else:
                    tipo_base = "Retracao" if "Retracao" in tipo_sinal else "Reversao"

                # Atualiza estatísticas por par
                if symbol in stats_por_par:
                    par_stats = stats_por_par[symbol]
                    par_stats["lucro"] += lucro
                    # Apenas conta para estatísticas específicas, não afeta contadores globais
                    if resultado == "Win":
                        par_stats["wins"] += 1
                    else:
                        par_stats["losses"] += 1

                    if gale_key in par_stats["gales"]:
                        gale_stats = par_stats["gales"][gale_key]
                        if resultado == "Win":
                            gale_stats["wins"] += 1
                        else:
                            gale_stats["losses"] += 1
                        gale_stats["lucro"] += lucro

                # Atualiza estatísticas por tipo
                tipo_stats = stats_por_tipo[tipo_base]
                tipo_stats["lucro"] += lucro
                if resultado == "Win":
                    tipo_stats["wins"] += 1
                else:
                    tipo_stats["losses"] += 1

                if gale_key in tipo_stats["gales"]:
                    gale_stats = tipo_stats["gales"][gale_key]
                    if resultado == "Win":
                        gale_stats["wins"] += 1
                    else:
                        gale_stats["losses"] += 1
                    gale_stats["lucro"] += lucro

                # Atualiza estatísticas de Gale
                if gale_key in stats_por_gale:
                    gale_stats = stats_por_gale[gale_key]
                    if resultado == "Win":
                        gale_stats["wins"] += 1
                    else:
                        gale_stats["losses"] += 1
                    gale_stats["lucro"] += lucro
                    gale_stats["operacoes"] += 1

            except Exception as e:
                print(f"Erro ao processar operação: {e}")
                continue

        if abr_strategy_active:
            # Adiciona uma nova aba para estatísticas da ABR
            with dpg.tab(label="Estratégia ABR"):
                abr_status = abr_strategy.get_status()

                with dpg.group():
                    dpg.add_text("Análise de Sequências", color=GOLD)
                    dpg.add_separator()

                    # Informações sobre sequências ótimas
                    call_length = abr_status["optimal_call_length"]
                    put_length = abr_status["optimal_put_length"]
                    call_rate = abr_status["call_success_rate"]
                    put_rate = abr_status["put_success_rate"]

                    if call_length:
                        dpg.add_text(f"CALL: {call_length} velas vermelhas - {call_rate:.2f}% de sucesso", color=GREEN)
                    else:
                        dpg.add_text("CALL: Sequência ótima não encontrada", color=RED)

                    if put_length:
                        dpg.add_text(f"PUT: {put_length} velas verdes - {put_rate:.2f}% de sucesso", color=GREEN)
                    else:
                        dpg.add_text("PUT: Sequência ótima não encontrada", color=RED)

                    # Informações sobre sequências atuais
                    dpg.add_text("\nSequências Atuais", color=CYAN)
                    dpg.add_text(f"Velas verdes consecutivas: {abr_status['current_green_sequence']}")
                    dpg.add_text(f"Velas vermelhas consecutivas: {abr_status['current_red_sequence']}")

                    # Estatísticas gerais
                    win_rate = abr_status["win_rate"]
                    dpg.add_text("\nDesempenho Geral", color=CYAN)
                    dpg.add_text(f"Total de sinais: {abr_status['total_signals']}")
                    dpg.add_text(f"Sinais bem-sucedidos: {abr_status['successful_signals']}")
                    dpg.add_text(f"Taxa de acerto: {win_rate:.2f}%",
                                 color=GREEN if win_rate >= 70 else ORANGE if win_rate >= 50 else RED)

        with dpg.tab_bar():
            # Tab 1: Overview - Usa contadores globais
            with dpg.tab(label="Visao Geral"):
                with dpg.group(horizontal=True):
                    # General Statistics
                    with dpg.group():
                        dpg.add_text("Estatisticas Gerais", color=GOLD)
                        dpg.add_separator()
                        dpg.add_text(f"Total de Operacoes: {total_operacoes}")
                        dpg.add_text(f"Total de Wins: {total_wins}", color=GREEN)
                        dpg.add_text(f"Total de Losses: {total_losses}", color=RED)
                        taxa_win = (total_wins / total_operacoes * 100) if total_operacoes > 0 else 0
                        dpg.add_text(f"Taxa de Acerto: {taxa_win:.2f}%", color=BLUE)

                    create_vertical_divider()

                    # Financial Results
                    with dpg.group():
                        dpg.add_text("Resultados Financeiros", color=GOLD)
                        dpg.add_separator()
                        cor_lucro = GREEN if lucro_total >= 0 else RED
                        dpg.add_text(f"Lucro Total: ${lucro_total:.2f}", color=cor_lucro)
                        media_lucro = lucro_total / total_operacoes if total_operacoes > 0 else 0
                        dpg.add_text(f"Media por Operacao: ${media_lucro:.2f}",
                                   color=GREEN if media_lucro >= 0 else RED)

                    create_vertical_divider()

                    # Gale Analysis
                    with dpg.group():
                        dpg.add_text("Analise de Gale", color=GOLD)
                        dpg.add_separator()
                        for gale_key, stats in stats_por_gale.items():
                            total_gale = stats["wins"] + stats["losses"]
                            if total_gale > 0:
                                taxa_gale = (stats["wins"] / total_gale * 100)
                                lucro_gale = stats["lucro"]
                                dpg.add_text(f"{gale_key}:", color=CYAN)
                                dpg.add_text(f"Taxa: {taxa_gale:.2f}%", color=BLUE)
                                dpg.add_text(f"Lucro: ${lucro_gale:.2f}",
                                           color=GREEN if lucro_gale >= 0 else RED)

            # Tab 2: Pair Analysis
            with dpg.tab(label="Analise por Par"):
                with dpg.group():
                    row = dpg.add_group(horizontal=True)
                    contagem_coluna = 0
                    for symbol in symbols:
                        if contagem_coluna > 0 and contagem_coluna % 4 == 0:
                            row = dpg.add_group(horizontal=True)

                        with dpg.group(parent=row):
                            stats = stats_por_par[symbol]
                            wins = stats["wins"]
                            losses = stats["losses"]
                            total = wins + losses
                            taxa = (wins / total * 100) if total > 0 else 0
                            lucro = stats["lucro"]

                            dpg.add_text(f"{symbol}", color=CYAN)
                            dpg.add_separator()
                            dpg.add_text(f"Operacoes: {total}")
                            dpg.add_text(f"W: {wins} | L: {losses}")
                            dpg.add_text(f"Taxa: {taxa:.2f}%", color=BLUE)
                            dpg.add_text(f"Lucro: ${lucro:.2f}",
                                       color=GREEN if lucro >= 0 else RED)

                            if total > 0:
                                dpg.add_text("Detalhes de Gale:", color=ORANGE)
                                for gale_key in stats["gales"]:
                                    gale_stats = stats["gales"][gale_key]
                                    gale_wins = gale_stats["wins"]
                                    gale_losses = gale_stats["losses"]
                                    gale_total = gale_wins + gale_losses
                                    if gale_total > 0:
                                        gale_taxa = (gale_wins / gale_total * 100)
                                        dpg.add_text(f"{gale_key}: {gale_taxa:.1f}%")

                        contagem_coluna += 1
                        if contagem_coluna % 4 != 0 and contagem_coluna < len(symbols):
                            create_vertical_divider()

            # Tab 3: Strategy Analysis
            with dpg.tab(label="Estrategias"):
                with dpg.group(horizontal=True):
                    for i, tipo_sinal in enumerate(["Retracao", "Reversao", "Fluxo", "Externo" , "PPONetwork" , "ABR" ]):
                        if i > 0:
                            create_vertical_divider()
                        with dpg.group():
                            stats = stats_por_tipo[tipo_sinal]
                            wins = stats["wins"]
                            losses = stats["losses"]
                            total = wins + losses
                            taxa = (wins / total * 100) if total > 0 else 0
                            lucro = stats["lucro"]

                            dpg.add_text(f"Analise de {tipo_sinal}", color=GOLD)
                            dpg.add_separator()
                            dpg.add_text(f"Total de Operacoes: {total}")
                            dpg.add_text(f"Wins: {wins} | Losses: {losses}")
                            dpg.add_text(f"Taxa de Acerto: {taxa:.2f}%", color=BLUE)
                            dpg.add_text(f"Lucro: ${lucro:.2f}",
                                       color=GREEN if lucro >= 0 else RED)

                            if total > 0:
                                dpg.add_text("\nDesempenho por Gale:", color=ORANGE)
                                for gale_key, gale_stats in stats["gales"].items():
                                    gale_wins = gale_stats["wins"]
                                    gale_losses = gale_stats["losses"]
                                    gale_total = gale_wins + gale_losses
                                    if gale_total > 0:
                                        gale_taxa = (gale_wins / gale_total * 100)
                                        gale_lucro = gale_stats["lucro"]
                                        dpg.add_text(f"{gale_key}:")
                                        dpg.add_text(f"Taxa: {gale_taxa:.1f}% Lucro: ${gale_lucro:.2f}")

            # Tab 4: Hourly Analysis
            with dpg.tab(label="Analise Horarios"):
                with dpg.group(horizontal=True):
                    stats_horario = calculate_hourly_stats()
                    for coluna, hora in enumerate(range(0, 24, 6)):
                        if coluna > 0:
                            create_vertical_divider()
                        with dpg.group():
                            for h in range(hora, min(hora + 6, 24)):
                                stats = stats_horario.get(h, {
                                    "total": 0, "wins": 0, "losses": 0,
                                    "taxa": 0, "lucro": 0
                                })

                                dpg.add_text(f"{h:02d}:00 - {(h + 1) % 24:02d}:00", color=ORANGE)
                                dpg.add_text(f"Ops: {stats['total']}")
                                dpg.add_text(f"W: {stats['wins']} L: {stats['losses']}")
                                dpg.add_text(f"Taxa: {stats['taxa']:.1f}%", color=BLUE)
                                dpg.add_text(f"Lucro: ${stats['lucro']:.2f}",
                                           color=GREEN if stats['lucro'] >= 0 else RED)
                                dpg.add_separator()

            # Aba 5: Metricas Avancadas
            with dpg.tab(label="Metricas Avancadas"):
                with dpg.group(horizontal=True):
                    # Metricas de Desempenho
                    with dpg.group():
                        dpg.add_text("Metricas de Desempenho", color=GOLD)
                        dpg.add_separator()

                        fator_lucro = calculate_profit_factor()
                        dpg.add_text(f"Fator de Lucro: {fator_lucro:.2f}", color=BLUE)

                        risco_retorno = calculate_risk_reward_ratio()
                        dpg.add_text(f"Risco/Retorno: {risco_retorno:.2f}", color=BLUE)

                        sharpe = calculate_sharpe_ratio()
                        dpg.add_text(f"Indice Sharpe: {sharpe:.2f}", color=BLUE)

                        drawdown_max = calculate_max_drawdown()
                        dpg.add_text(f"Drawdown Maximo: {drawdown_max:.2f}%", color=RED)

                    create_vertical_divider()

                    # Analise de Sequencias
                    with dpg.group():
                        dpg.add_text("Analise de Sequencias", color=GOLD)
                        dpg.add_separator()

                        for estrategia in ["Retracao", "Reversao", "Fluxo", "Externo" , "PPONetwork" , "ABR"]:
                            max_win, max_loss, atual = calculate_streaks(estrategia)
                            if max_win > 0 or max_loss > 0:  # Só mostra se tiver operações
                                dpg.add_text(f"{estrategia}:", color=CYAN)
                                dpg.add_text(f"Maior Seq. Wins: {max_win}", color=GREEN)
                                dpg.add_text(f"Maior Seq. Losses: {max_loss}", color=RED)
                                cor_atual = GREEN if atual > 0 else RED if atual < 0 else WHITE
                                dpg.add_text(f"Sequencia Atual: {abs(atual)}", color=cor_atual)
                                dpg.add_separator()

        with dpg.group(horizontal=True):
            dpg.add_button(label="Reset Statistics", callback=clear_transactions_history)
            dpg.add_button(label="Export to CSV", callback=lambda: export_statistics_to_csv(
                stats_by_pair, stats_by_signal_type, stats_by_gale
            ))

    except Exception as e:
        print(f"Error creating statistics: {e}")
        import traceback
        traceback.print_exc()
        dpg.add_text("Error generating statistics. Check console for details.", color=RED)

def create_vertical_divider():
    with dpg.group():
        for _ in range(1):  # Adjust this number to change the height of the divider
            dpg.add_text("|")


def calculate_streaks(signal_type=None):
    """
    Calcula as maiores sequências de wins e losses, opcionalmente filtrando por tipo de sinal.

    Args:
        signal_type (str, optional): Tipo de sinal para filtrar ("Retracao", "Reversao", etc)

    Returns:
        tuple: (max_win_streak, max_loss_streak, current_streak)
    """
    try:
        # Inicializa variáveis
        current_streak = 0
        max_win_streak = 0
        max_loss_streak = 0
        last_result = None

        # Filtra transações pelo tipo de sinal se especificado
        transactions = statistics_transactions
        if signal_type:
            transactions = [t for t in transactions if t.get("Tipo Sinal", "").startswith(signal_type)]

        # Ordena transações por hora
        sorted_transactions = sorted(transactions,
                                     key=lambda x: x.get("Hora de Abertura", datetime.min))

        for transaction in sorted_transactions:
            result = transaction.get("W/L")

            if result == "Win":
                if last_result == "Win":
                    current_streak += 1
                else:
                    current_streak = 1
                max_win_streak = max(max_win_streak, current_streak)
            elif result == "Loss":
                if last_result == "Loss":
                    current_streak -= 1
                else:
                    current_streak = -1
                max_loss_streak = max(max_loss_streak, abs(current_streak))

            last_result = result

        print(f"\n=== Análise de Sequências ===")
        print(f"Tipo de sinal: {signal_type if signal_type else 'Todos'}")
        print(f"Maior sequência de wins: {max_win_streak}")
        print(f"Maior sequência de losses: {max_loss_streak}")
        print(f"Sequência atual: {current_streak}")

        return max_win_streak, max_loss_streak, current_streak

    except Exception as e:
        print(f"Erro ao calcular sequências: {e}")
        import traceback
        traceback.print_exc()
        return 0, 0, 0


def calculate_hourly_stats():
    """
    Calcula estatísticas por hora com taxa de acerto corrigida.
    """
    hourly_stats = {i: {
        "wins": 0,
        "losses": 0,
        "profit": 0,
        "total": 0,
        "taxa": 0,
        "lucro": 0
    } for i in range(24)}

    for transaction in statistics_transactions:
        try:
            # Verifica se "Hora de Abertura" é um objeto datetime ou uma string
            if isinstance(transaction["Hora de Abertura"], datetime):
                hour = transaction["Hora de Abertura"].hour
            else:
                try:
                    hora_str = str(transaction["Hora de Abertura"])
                    if ":" in hora_str:
                        hour = int(hora_str.split(":")[0])
                    else:
                        continue  # Pula transação com formato inválido
                except (ValueError, AttributeError):
                    print(f"Erro ao processar horário da transação: {transaction}")
                    continue

            result = transaction["W/L"]
            profit = float(transaction.get("Profit", 0))

            # Atualiza estatísticas
            hourly_stats[hour]["total"] += 1
            hourly_stats[hour]["lucro"] += profit

            if result == "Win":
                hourly_stats[hour]["wins"] += 1
            else:
                hourly_stats[hour]["losses"] += 1

        except Exception as e:
            print(f"Erro ao processar transação: {e}")
            continue

    # Calcula taxa de acerto para cada hora
    for hour, stats in hourly_stats.items():
        total = stats["wins"] + stats["losses"]
        if total > 0:
            stats["taxa"] = (stats["wins"] / total) * 100
        else:
            stats["taxa"] = 0.0

        # Garante que todos os campos necessários existem
        stats.setdefault("winrate", stats["taxa"])
        stats.setdefault("profit", stats["lucro"])

    return hourly_stats


def calculate_profit_factor():
    total_gains = sum(t["Profit"] for t in statistics_transactions if t["Profit"] > 0)
    total_losses = abs(sum(t["Profit"] for t in statistics_transactions if t["Profit"] < 0))
    return total_gains / total_losses if total_losses != 0 else float('inf')


def calculate_risk_reward_ratio():
    avg_win = sum(t["Profit"] for t in statistics_transactions if t["W/L"] == "Win") / total_wins if total_wins > 0 else 0
    avg_loss = abs(
        sum(t["Profit"] for t in statistics_transactions if t["W/L"] == "Loss") / total_losses) if total_losses > 0 else 0
    return avg_win / avg_loss if avg_loss != 0 else float('inf')


def calculate_sharpe_ratio():
    returns = [t["Profit"] for t in statistics_transactions]
    avg_return = sum(returns) / len(returns) if returns else 0
    std_dev = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5 if returns else 0
    return (avg_return / std_dev) * (252 ** 0.5) if std_dev != 0 else 0  # Anualizado assumindo 252 dias de trading


def calculate_max_drawdown():
    peak = 0
    max_dd = 0
    for t in statistics_transactions:
        if t["Profit"] > peak:
            peak = t["Profit"]
        dd = (peak - t["Profit"]) / peak if peak > 0 else 0
        if dd > max_dd:
            max_dd = dd
    return max_dd * 100  # Convert to percentage


def clear_transactions_history():
    """Limpa completamente o histórico de estatísticas e seus arquivos"""
    global statistics_transactions, total_wins, total_losses, lucro_total

    try:
        print("\n=== Limpando Histórico de Estatísticas ===")

        # Reseta variáveis
        statistics_transactions = []
        total_wins = 0
        total_losses = 0
        lucro_total = 0

        # Obtém o diretório onde os arquivos estão salvos
        user_dir = os.path.expanduser("~")
        json_file = os.path.join(user_dir, "transactions_history.json")
        bak_file = os.path.join(user_dir, "transactions_history.json.bak")

        # Remove os arquivos físicos
        try:
            if os.path.exists(json_file):
                os.remove(json_file)
                print(f"✅ Arquivo principal removido: {json_file}")

            if os.path.exists(bak_file):
                os.remove(bak_file)
                print(f"✅ Arquivo backup removido: {bak_file}")

        except PermissionError:
            print("❌ Erro de permissão ao remover arquivos")
            print("Tente executar o bot como administrador")
            return False

        # Cria novo arquivo vazio
        with open(json_file, 'w') as f:
            json.dump([], f, indent=2)

        # Atualiza interface
        update_status()

        print("✅ Arquivos de histórico removidos com sucesso")
        print("✅ Interface atualizada")
        return True

    except Exception as e:
        print(f"❌ Erro ao limpar histórico: {e}")
        traceback.print_exc()
        return False


def show_pix_popup():
    if dpg.does_item_exist("pix_popup"):
        dpg.delete_item("pix_popup")

    with dpg.window(label="Contribua via PIX", tag="pix_popup", width=265, height=395 ,no_resize=True, no_collapse=True):
        dpg.add_text("Contribua Para Melhorias No Projeto!")
        dpg.add_spacer(height=10)

        # Carregar a imagem do QR code
        img_path = resource_path("qrcode_pix.png")
        img = Image.open(img_path).convert("RGBA")
        img_data = np.array(img).flatten() / 255.0  # Converter para formato compatível com DearPyGui

        width, height = img.size

        # Registrar a textura no DearPyGui
        with dpg.texture_registry():
            texture_id = dpg.add_static_texture(width, height, img_data)

        # Adicionar a imagem na interface
        dpg.add_image(texture_id, width=250, height=250)

        dpg.add_spacer(height=10)
        dpg.add_text("Obrigado pelo seu apoio!")
        dpg.add_button(label="Fechar", callback=lambda: dpg.delete_item("pix_popup"))



volatilidade_opcoes = {
    # Português
    "Baixa": 0.0007,
    "Media": 0.0017,
    "Alta": 0.0025,
    # Inglês
    "Low": 0.0007,
    "Medium": 0.0017,
    "High": 0.0025,
    # Espanhol
    "Baja": 0.0007,
    "Media": 0.0017,
    "Alta": 0.0025
}

# Ajuste o dicionário para incluir as chaves em todos os idiomas
volatilidade_opcoes1 = {
    # Português
    "5 Velas": 5,
    "10 Velas": 10,
    "20 Velas": 20,
    # Inglês
    "5 Candles": 5,
    "10 Candles": 10,
    "20 Candles": 20,
    # Espanhol
    "5 Velas": 5,
    "10 Velas": 10,
    "20 Velas": 20
}


def on_volatilidade_selecionada1(sender, app_data):
    global velas_selecionadas
    velas_selecionadas = app_data

    # Mapeamento de tradução para o valor da chave
    traducao_velas = {
        # Inglês para chave em português
        "5 Candles": "5 Velas",
        "10 Candles": "10 Velas",
        "20 Candles": "20 Velas",
        # Espanhol igual português
        "5 Velas": "5 Velas",
        "10 Velas": "10 Velas",
        "20 Velas": "20 Velas"
    }

    # Pega a chave traduzida
    chave_traduzida = traducao_velas.get(app_data, app_data)
    valor_selecionado1 = volatilidade_opcoes1[chave_traduzida]
    print(f"Número de velas selecionado: {app_data} com valor: {valor_selecionado1}")


def on_volatilidade_selecionada(sender, app_data):
    global volatilidade_selecionada
    volatilidade_selecionada = app_data

    # Mapeamento de tradução para o valor da chave
    traducao_volatilidade = {
        # Inglês para chave em português
        "Low": "Baixa",
        "Medium": "Media",
        "High": "Alta",
        # Espanhol para chave em português
        "Baja": "Baixa",
        "Media": "Media",
        "Alta": "Alta",
        # Português mantém igual
        "Baixa": "Baixa",
        "Media": "Media",
        "Alta": "Alta"
    }

    # Pega a chave traduzida
    chave_traduzida = traducao_volatilidade.get(app_data, app_data)
    valor_selecionado = volatilidade_opcoes[chave_traduzida]

    print(f"Volatilidade selecionada: {app_data} com valor: {valor_selecionado}")


def toggle_telegram(sender, app_data):
    global telegram_ativado
    telegram_ativado = bool(app_data)
    print(f"Telegram {'ativado' if telegram_ativado else 'desativado'}")

def toggle_price_action(sender, app_data):
    global price_action_active
    price_action_active = app_data
    print(f"Price Action como confluência obrigatória: {'ativado' if price_action_active else 'desativado'}")
    save_configurations()

def toggle_volume_profile(sender, app_data):
    global volume_profile_active
    volume_profile_active = app_data
    print(f"Volume Profile como confluência obrigatória: {'ativado' if volume_profile_active else 'desativado'}")
    save_configurations()

def toggle_fluxo(sender, app_data):
    global fluxo_active, retracao_value, reversao_value
    fluxo_active = app_data
    if fluxo_active:
        retracao_value = False
        reversao_value = False
        dpg.set_value("retracao_value", False)
        dpg.set_value("reversao_value", False)
        dpg.disable_item("retracao_value")
        dpg.disable_item("reversao_value")
    else:
        dpg.enable_item("retracao_value")
        dpg.enable_item("reversao_value")
    save_configurations()

def toggle_retracao(sender, app_data):
    global retracao_value, antiloss_ativado
    retracao_value = app_data
    print(f"Retração {'ativada' if retracao_value else 'desativada'}")

    if retracao_value:
        antiloss_ativado = False
        dpg.set_value("antiloss_value", False)
        dpg.disable_item("antiloss_value")
        print("Antiloss desativado automaticamente")
    else:
        dpg.enable_item("antiloss_value")

    save_configurations()
    print(f"💾 Estado Retração salvo: {'Ativada' if retracao_value else 'Desativada'}")



def toggle_reversao(sender, app_data):
    global reversao_value
    reversao_value = app_data
    print(f"Reversão {'ativada' if reversao_value else 'desativada'}")
    save_configurations()
    print(f"💾 Estado Reversão salvo: {'Ativada' if reversao_value else 'Desativada'}")



simbolos_ativos = {symbol: True for symbol in symbols}


async def analyze_fluxo(velas_symbol):
    if len(velas_symbol) < 26:
        print("❌ Dados insuficientes para análise")
        return None

    print("\n=== Iniciando Análise de Fluxo ===")

    # Extração de dados existente...
    closes = np.array([float(vela['close']) for vela in velas_symbol])
    opens = np.array([float(vela['open']) for vela in velas_symbol])
    highs = np.array([float(vela['high']) for vela in velas_symbol])
    lows = np.array([float(vela['low']) for vela in velas_symbol])

    # Calcula níveis de Suporte e Resistência
    sr_levels = calculate_sr_levels(velas_symbol)
    current_price = float(velas_symbol[-1]['close'])
    signal_valid, reason = validate_sr_signal(current_price, velas_symbol, None, sr_levels)

    # Se estiver muito próximo a um nível de S/R, não gera sinal
    if not signal_valid:
        print(f"❌ Análise de Fluxo: {reason}")
        return None

    # Usando VWAP em vez de preço típico
    volumes = np.ones_like(closes)  # Se não tiver volume real, usa 1
    vwap = np.cumsum(closes * volumes) / np.cumsum(volumes)

    # Médias móveis com EMA em vez de SMA (mais responsiva)
    ema_5 = talib.EMA(closes, timeperiod=5)
    ema_20 = talib.EMA(closes, timeperiod=20)

    # Momentum atual
    momentum = (closes[-1] - closes[-5]) / closes[-5] * 100

    # Função para detectar Kicker Pattern
    def detect_kicker():
        # Verifica as duas últimas velas
        prev_candle = {
            'open': opens[-2],
            'close': closes[-2],
            'high': highs[-2],
            'low': lows[-2]
        }
        current_candle = {
            'open': opens[-1],
            'close': closes[-1],
            'high': highs[-1],
            'low': lows[-1]
        }

        # Kicker de alta
        bullish_kicker = (
            prev_candle['close'] < prev_candle['open'] and  # Vela anterior é vermelha
            current_candle['open'] > prev_candle['open'] and  # Gap de abertura acima
            current_candle['close'] > current_candle['open']  # Vela atual é verde
        )

        # Kicker de baixa
        bearish_kicker = (
            prev_candle['close'] > prev_candle['open'] and  # Vela anterior é verde
            current_candle['open'] < prev_candle['open'] and  # Gap de abertura abaixo
            current_candle['close'] < current_candle['open']  # Vela atual é vermelha
        )

        return {
            'bullish': bullish_kicker,
            'bearish': bearish_kicker
        }

    # Cálculos de RSI
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains[-14:])
    avg_loss = np.mean(losses[-14:])
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))

    # Volume Profile Analysis
    vp_data = calcular_volume_profile(velas_symbol)
    if not vp_data:
        print("❌ Erro ao calcular Volume Profile")
        return None

    preco_atual = closes[-1]
    poc_price = vp_data['poc']

    # Adiciona análise de força da tendência
    tendencia_force = abs(ema_5[-1] - ema_20[-1]) / ema_20[-1] * 100

    # Detecta padrão Kicker se estiver ativo
    kicker_pattern = detect_kicker() if kicker_active else {'bullish': False, 'bearish': False}

    print("\n=== Análise Detalhada ===")
    print(f"Momentum: {momentum:.2f}%")
    print(f"Força da Tendência: {tendencia_force:.2f}%")
    print(f"RSI: {rsi:.2f}")
    print(f"Distância do POC: {abs(preco_atual - poc_price) / poc_price * 100:.2f}%")
    print(f"Suportes/Resistências: {reason}")  # Mostra a razão da validação S/R

    # CALL conditions
    if ema_5[-1] > ema_20[-1]:
        confirmacoes_call = 0
        print("\n🔍 Verificando condições CALL:")

        # Primeiro verifica S/R para CALL
        call_signal_valid, call_reason = validate_sr_signal(preco_atual, velas_symbol, "CALL", sr_levels)
        if not call_signal_valid:
            print(f"❌ CALL bloqueado: {call_reason}")
            return None

        # Verifica Kicker como confluência
        if kicker_pattern['bullish']:
            confirmacoes_call += 2  # Dá peso maior ao Kicker
            print("✅✅ Kicker de alta detectado")

        # Tendência
        if tendencia_force > 0.15:  # Tendência significativa
            confirmacoes_call += 1
            print("✅ Força da tendência confirmada")

        # Momentum
        if momentum > 0:
            confirmacoes_call += 1
            print("✅ Momentum positivo")

        # RSI
        if 35 < rsi < 65:
            confirmacoes_call += 1
            print("✅ RSI em zona neutra")

        if vp_data['distribuicao']['acima_poc'] > vp_data['distribuicao']['abaixo_poc'] * 1.1:
            confirmacoes_call += 1
            print("✅ Volume bem distribuído acima")

        # Adiciona verificação de distância do POC
        poc_dist = (preco_atual - poc_price) / poc_price
        if 0.001 < poc_dist < 0.005:  # Entre 0.1% e 0.5% acima do POC
            confirmacoes_call += 1
            print("✅ Distância ideal do POC")

        if kicker_active:
            print("\n🔍 Verificando padrão Kicker prioritário:")
            if confirmacoes_call >= 3 and kicker_pattern['bullish'] and vp_data['pressao_compradora'] > pressao_compradora_min:
                print("✅✅ Kicker de alta validado com pressão compradora suficiente")
                print("\n🎯 Sinal CALL gerado por Kicker!")
                return "CALL"
        else:
            if confirmacoes_call >= 4 and vp_data['pressao_compradora'] > pressao_compradora_min:
                print(f"\n🎯 Sinal CALL gerado com {confirmacoes_call} confirmações!")
                return "CALL"

    # PUT conditions
    if ema_5[-1] < ema_20[-1]:
        confirmacoes_put = 0
        print("\n🔍 Verificando condições PUT:")

        # Primeiro verifica S/R para PUT
        put_signal_valid, put_reason = validate_sr_signal(preco_atual, velas_symbol, "PUT", sr_levels)
        if not put_signal_valid:
            print(f"❌ PUT bloqueado: {put_reason}")
            return None

        # Verifica Kicker como confluência
        if kicker_pattern['bearish']:
            confirmacoes_put += 2  # Dá peso maior ao Kicker
            print("✅✅ Kicker de baixa detectado")

        # Tendência
        if tendencia_force > 0.15:
            confirmacoes_put += 1
            print("✅ Força da tendência confirmada")

        # Momentum
        if momentum < 0:
            confirmacoes_put += 1
            print("✅ Momentum negativo")

        # RSI
        if 35 < rsi < 65:
            confirmacoes_put += 1
            print("✅ RSI em zona neutra")

        if vp_data['distribuicao']['abaixo_poc'] > vp_data['distribuicao']['acima_poc'] * 1.1:
            confirmacoes_put += 1
            print("✅ Volume bem distribuído abaixo")

        # Verifica distância do POC
        poc_dist = (poc_price - preco_atual) / poc_price
        if 0.001 < poc_dist < 0.005:
            confirmacoes_put += 1
            print("✅ Distância ideal do POC")

        if kicker_active:
            print("\n🔍 Verificando padrão Kicker prioritário:")
            if confirmacoes_put >= 3 and kicker_pattern['bearish'] and vp_data['pressao_vendedora'] > pressao_vendedora_min:
                print("✅✅ Kicker de baixa validado com pressão vendedora suficiente")
                print("\n🎯 Sinal PUT gerado por Kicker!")
                return "PUT"
        else:
            if confirmacoes_put >= 4 and vp_data['pressao_vendedora'] > pressao_vendedora_min:
                print(f"\n🎯 Sinal PUT gerado com {confirmacoes_put} confirmações!")
                return "PUT"

    print("\n❌ Nenhum sinal gerado - Confirmações insuficientes ou bloqueado por S/R")
    return None


def toggle_symbol(sender, app_data):
    """Toggle symbol selection without disabling other types of pairs"""
    # Extract the symbol from the sender tag
    if sender.startswith("checkbox_R_"):
        symbol = "R_" + sender.split("_")[-1]
    else:
        symbol = sender.split("_")[-1]

    is_active = app_data
    global simbolos_ativos

    try:
        # Simplesmente atualiza o status do símbolo clicado
        simbolos_ativos[symbol] = is_active
        print(f"Symbol {symbol} {'activated' if is_active else 'deactivated'}")

        # Save the configuration
        save_configurations()

        # Lista os símbolos ativos para debug
        active_symbols = [
            sym for sym, active in simbolos_ativos.items()
            if active and dpg.get_value(f"checkbox_{sym}")
        ]

        print("\n=== Pares Atualmente Ativos ===")
        print(f"Total ativos: {len(active_symbols)}")
        print(f"Pares ativos: {active_symbols}")

    except Exception as e:
        print(f"Erro em toggle_symbol: {e}")
        import traceback
        traceback.print_exc()



def update_masaniello_type(sender, app_data):
    global tipo
    tipo = 1 if app_data == "Normal" else 0  # 1 para Normal, 0 para Progressivo
    print(f"Tipo Masaniello atualizado para: {app_data} (tipo={tipo})")

def update_masaniello_style(sender, app_data):
    global style
    style = app_data  # "Normal", "Composto" ou "Conservador"
    print(f"Estilo Masaniello atualizado para: {style}")


def toggle_gerenciamento(sender, app_data):
    """Alterna entre as configurações de Masaniello e Ciclos"""
    global gerenciamento_ativo
    gerenciamento_ativo = app_data

    try:
        if app_data == "Masaniello":
            dpg.show_item("masaniello_container")
            dpg.hide_item("ciclos_container")
            print("Alternado para gerenciamento Masaniello")
        else:  # Ciclos
            dpg.hide_item("masaniello_container")
            dpg.show_item("ciclos_container")
            print("Alternado para gerenciamento Ciclos")

        # Salva a seleção do gerenciamento
        save_gerenciamento_selection()

    except Exception as e:
        print(f"Erro ao alternar gerenciamento: {e}")
        import traceback
        traceback.print_exc()




def criar_ciclos_presets_step():
    """Cria os presets de ciclos STEP otimizados para payout de 130%"""
    ciclos_presets = {
        "G1": {
            "CICLO 1": [  # MODERADO
                [0.35, 0.65],                 # Ataque - Proteção (1.86x)
                [0.75, 1.40],                 # Defesa - Ataque (1.87x)
                [1.40, 2.60],                 # Ataque - Defesa (1.86x)
                [2.60, 4.85],                 # Defesa - Ataque (1.87x)
                [4.85, 9.05]                  # Ataque final (1.87x)
            ],
            "CICLO 2": [  # CONSERVADOR
                [0.35, 0.60],                 # Ataque suave - Defesa (1.71x)
                [0.70, 1.20],                 # Proteção - Ataque (1.71x)
                [1.20, 2.05],                 # Ataque - Defesa (1.71x)
                [2.05, 3.50],                 # Defesa - Ataque (1.71x)
                [3.50, 6.00]                  # Recuperação máxima (1.71x)
            ],
            "CICLO 3": [  # AGRESSIVO
                [0.35, 0.70],                 # Ataque forte - Defesa (2.00x)
                [0.80, 1.60],                 # Ataque - Proteção (2.00x)
                [1.60, 3.20],                 # Defesa - Ataque (2.00x)
                [3.20, 6.40],                 # Ataque - Defesa (2.00x)
                [6.40, 12.80]                 # Recuperação agressiva (2.00x)
            ],
            "CICLO 4": [  # MODERADO PLUS
                [0.35, 0.68],                 # Ataque moderado - Defesa (1.94x)
                [0.78, 1.50],                 # Proteção - Ataque (1.92x)
                [1.50, 2.90],                 # Ataque - Defesa (1.93x)
                [2.90, 5.60],                 # Defesa - Ataque (1.93x)
                [5.60, 10.80]                 # Recuperação balanceada (1.93x)
            ]
        },
        "G2": {
            "CICLO 1": [  # MODERADO
                [0.35, 0.65, 1.20],           # A-D-A (1.86x - 1.85x)
                [0.95, 1.75, 3.25],           # D-A-D (1.84x - 1.86x)
                [2.60, 4.80, 8.90],           # A-D-A (1.85x - 1.85x)
                [7.15, 13.20, 24.50],         # D-A-D (1.85x - 1.86x)
                [0.0, 0.0, 0.0]               # Reserva
            ],
            "CICLO 2": [  # CONSERVADOR
                [0.35, 0.60, 1.05],           # A-D-A (1.71x - 1.75x)
                [0.85, 1.45, 2.50],           # D-A-D (1.71x - 1.72x)
                [2.00, 3.40, 5.80],           # A-D-A (1.70x - 1.71x)
                [4.65, 7.95, 13.60],          # D-A-D (1.71x - 1.71x)
                [0.0, 0.0, 0.0]               # Reserva
            ],
            "CICLO 3": [  # AGRESSIVO
                [0.35, 0.70, 1.40],           # A-D-A (2.00x - 2.00x)
                [1.10, 2.20, 4.40],           # D-A-D (2.00x - 2.00x)
                [3.50, 7.00, 14.00],          # A-D-A (2.00x - 2.00x)
                [11.20, 22.40, 44.80],        # D-A-D (2.00x - 2.00x)
                [0.0, 0.0, 0.0]               # Reserva
            ],
            "CICLO 4": [  # MODERADO PLUS
                [0.35, 0.68, 1.30],           # A-D-A (1.94x - 1.91x)
                [1.05, 2.00, 3.80],           # D-A-D (1.90x - 1.90x)
                [3.00, 5.70, 10.80],          # A-D-A (1.90x - 1.89x)
                [8.65, 16.40, 31.20],         # D-A-D (1.90x - 1.90x)
                [0.0, 0.0, 0.0]               # Reserva
            ]
        }
    }
    return ciclos_presets

def criar_ciclos_presets_normal():
    """Cria os presets de ciclos NORMAL otimizados para payout de 88%"""
    ciclos_presets = {
        "G1": {
            "CICLO 1": [  # MODERADO
                [0.35, 0.85],                 # Ataque - Defesa (2.43x)
                [1.00, 2.40],                 # Defesa - Ataque (2.40x)
                [2.40, 5.75],                 # Ataque - Defesa (2.40x)
                [5.75, 13.80],                # Defesa - Ataque (2.40x)
                [0.0, 0.0]                    # Reserva
            ],
            "CICLO 2": [  # CONSERVADOR
                [0.35, 0.80],                 # Ataque - Defesa (2.29x)
                [0.95, 2.15],                 # Defesa - Ataque (2.26x)
                [2.15, 4.85],                 # Ataque - Defesa (2.26x)
                [4.85, 11.00],                # Defesa - Ataque (2.27x)
                [0.0, 0.0]                    # Reserva
            ],
            "CICLO 3": [  # AGRESSIVO
                [0.35, 0.95],                 # Ataque forte - Defesa (2.71x)
                [1.15, 3.10],                 # Ataque - Proteção (2.70x)
                [3.10, 8.35],                 # Defesa - Ataque (2.69x)
                [8.35, 22.50],                # Ataque - Defesa (2.69x)
                [0.0, 0.0]                    # Reserva
            ],
            "CICLO 4": [  # MODERADO PLUS
                [0.35, 0.90],                 # Ataque moderado - Defesa (2.57x)
                [1.10, 2.80],                 # Proteção - Ataque (2.55x)
                [2.80, 7.15],                 # Ataque - Defesa (2.55x)
                [7.15, 18.25],                # Defesa - Ataque (2.55x)
                [0.0, 0.0]                    # Reserva
            ]
        },
        "G2": {
            "CICLO 1": [  # MODERADO
                [0.35, 0.85, 2.05],           # A-D-A (2.43x - 2.41x)
                [1.65, 4.00, 9.60],           # D-A-D (2.42x - 2.40x)
                [7.70, 18.50, 44.40],         # A-D-A (2.40x - 2.40x)
                [0.0, 0.0, 0.0],              # Reserva
                [0.0, 0.0, 0.0]               # Reserva
            ],
            "CICLO 2": [  # CONSERVADOR
                [0.35, 0.80, 1.85],           # A-D-A (2.29x - 2.31x)
                [1.50, 3.40, 7.70],           # D-A-D (2.27x - 2.26x)
                [6.20, 14.00, 31.70],         # A-D-A (2.26x - 2.26x)
                [0.0, 0.0, 0.0],              # Reserva
                [0.0, 0.0, 0.0]               # Reserva
            ],
            "CICLO 3": [  # AGRESSIVO
                [0.35, 0.95, 2.55],           # A-D-A (2.71x - 2.68x)
                [2.05, 5.50, 14.80],          # D-A-D (2.68x - 2.69x)
                [11.90, 32.00, 86.00],        # A-D-A (2.69x - 2.69x)
                [0.0, 0.0, 0.0],              # Reserva
                [0.0, 0.0, 0.0]               # Reserva
            ],
            "CICLO 4": [  # MODERADO PLUS
                [0.35, 0.90, 2.30],           # A-D-A (2.57x - 2.56x)
                [1.85, 4.70, 12.00],          # D-A-D (2.54x - 2.55x)
                [9.60, 24.50, 62.50],         # A-D-A (2.55x - 2.55x)
                [0.0, 0.0, 0.0],              # Reserva
                [0.0, 0.0, 0.0]               # Reserva
            ]
        }
    }
    return ciclos_presets


def criar_interface_preset_ciclos_step():
    """Cria interface profissional para seleção de presets de ciclos STEP"""
    ciclos_presets = criar_ciclos_presets_step()

    def get_classificacao_detalhada(grupo, ciclo):
        """Retorna classificação detalhada do ciclo"""
        classificacoes = {
            "G1": {
                "CICLO 1": {
                    "perfil": "MODERADO",
                    "cor": (255, 165, 0),
                    "desc": language_manager.get_text("BALANCEADO"),
                    "recomendado": language_manager.get_text("OPERACOES_PADRAO"),
                    "estrategia": language_manager.get_text("BALANCEADO")
                },
                "CICLO 2": {
                    "perfil": "CONSERVADOR",
                    "cor": (0, 255, 100),
                    "desc": language_manager.get_text("PROTECAO_MAXIMA"),
                    "recomendado": language_manager.get_text("INICIANTES"),
                    "estrategia": language_manager.get_text("PROTECAO_MAXIMA")
                },
                "CICLO 3": {
                    "perfil": "AGRESSIVO",
                    "cor": (255, 50, 50),
                    "desc": language_manager.get_text("RECUPERACAO_RAPIDA"),
                    "recomendado": language_manager.get_text("EXPERIENTES"),
                    "estrategia": language_manager.get_text("RECUPERACAO_RAPIDA")
                },
                "CICLO 4": {
                    "perfil": "MODERADO_PLUS",
                    "cor": (255, 140, 0),
                    "desc": language_manager.get_text("BALANCEADO"),
                    "recomendado": language_manager.get_text("INTERMEDIARIOS"),
                    "estrategia": language_manager.get_text("BALANCEADO")
                }
            },
            "G2": {
                "CICLO 1": {
                    "perfil": "MODERADO",
                    "cor": (255, 165, 0),
                    "desc": language_manager.get_text("BALANCEADO"),
                    "recomendado": language_manager.get_text("MEDIO_RISCO"),
                    "estrategia": language_manager.get_text("BALANCEADO")
                },
                "CICLO 2": {
                    "perfil": "CONSERVADOR",
                    "cor": (0, 255, 100),
                    "desc": language_manager.get_text("PROTECAO_MAXIMA"),
                    "recomendado": language_manager.get_text("LONGO_PRAZO"),
                    "estrategia": language_manager.get_text("PROTECAO_MAXIMA")
                },
                "CICLO 3": {
                    "perfil": "AGRESSIVO",
                    "cor": (255, 50, 50),
                    "desc": language_manager.get_text("RECUPERACAO_RAPIDA"),
                    "recomendado": language_manager.get_text("EXPERT"),
                    "estrategia": language_manager.get_text("RECUPERACAO_RAPIDA")
                },
                "CICLO 4": {
                    "perfil": "MODERADO_PLUS",
                    "cor": (255, 140, 0),
                    "desc": language_manager.get_text("BALANCEADO"),
                    "recomendado": language_manager.get_text("CONSISTENCIA"),
                    "estrategia": language_manager.get_text("BALANCEADO")
                }
            }

        }
        return classificacoes[grupo][ciclo]

    def calcular_metricas_ciclo(matriz):
        """Calcula métricas importantes do ciclo"""
        risco_total = sum(sum(valor for valor in linha if valor > 0) for linha in matriz)
        entrada_inicial = matriz[0][0]
        maior_entrada = max(max(valor for valor in linha if valor > 0) for linha in matriz if any(linha))
        num_entradas = sum(1 for linha in matriz for valor in linha if valor > 0)
        num_gales = sum(1 for linha in matriz if any(valor > 0 for valor in linha))
        num_ciclos = sum(1 for valor in matriz[0] if valor > 0)
        return {
            "risco_total": risco_total,
            "entrada_inicial": entrada_inicial,
            "maior_entrada": maior_entrada,
            "num_entradas": num_entradas,
            "num_gales": num_gales - 1,
            "num_ciclos": num_ciclos
        }

    if dpg.does_item_exist("preset_ciclos_step_window"):
        dpg.delete_item("preset_ciclos_step_window")

    with dpg.window(label=language_manager.get_text("CICLOS_STEP"), width=500, height=600, modal=True,
                   tag="preset_ciclos_step_window"):
        dpg.add_text(language_manager.get_text("SELECIONE_CICLO_STEP"), tag="selecione_ciclo_step_text")
        dpg.add_separator()

        for grupo in ["G1", "G2"]:
            num_entradas = {"G1": 2, "G2": 3}[grupo]
            grupo_text = f"{language_manager.get_text('CICLOS_DE')} {grupo}"
            dpg.add_text(grupo_text, color=(255, 255, 0), tag=f"step_ciclos_grupo_{grupo}_text")
            dpg.add_separator()

            for ciclo in ["CICLO 1", "CICLO 2", "CICLO 3", "CICLO 4"]:
                metricas = calcular_metricas_ciclo(ciclos_presets[grupo][ciclo])
                info = get_classificacao_detalhada(grupo, ciclo)
                base_tag = f"step_{grupo}_{ciclo}"

                with dpg.group(horizontal=False):
                    button_text = f"{ciclo} - {language_manager.get_text(info['perfil'])} ($ {metricas['risco_total']:.2f})"
                    dpg.add_button(
                        label=button_text,
                        callback=aplicar_preset_ciclo_step,
                        user_data=(grupo, ciclo),
                        tag=f"{base_tag}_button",
                        width=400
                    )

                    with dpg.group(indent=20):
                        dpg.add_text(
                            f"{language_manager.get_text('PERFIL')}: {language_manager.get_text(info['perfil'])}",
                            color=info['cor'],
                            tag=f"step_perfil_{base_tag}"
                        )
                        dpg.add_text(
                            f"{language_manager.get_text('ESTRATEGIA')}: {info['estrategia']}",
                            color=(180, 180, 180),
                            tag=f"step_estrategia_{base_tag}"
                        )
                        dpg.add_text(
                            f"{language_manager.get_text('ENTRADA')}: $ {metricas['entrada_inicial']:.2f} | {language_manager.get_text('MAIOR')}: $ {metricas['maior_entrada']:.2f}",
                            color=(150, 150, 150),
                            tag=f"step_entrada_{base_tag}"
                        )
                        dpg.add_text(
                            f"{language_manager.get_text('RECOMENDADO')}: {info['recomendado']}",
                            color=(150, 150, 150),
                            tag=f"step_recomendado_{base_tag}"
                        )

                dpg.add_separator()

        dpg.add_text("", tag="step_risco_total_text")

        # Aplica tema personalizado
        with dpg.theme() as theme_ciclos:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 70, 70))
                dpg.add_theme_color(dpg.mvThemeCol_Tab, (50, 50, 50))
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (70, 70, 70))
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, (90, 90, 90))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 120, 120))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)

        dpg.bind_item_theme("preset_ciclos_step_window", theme_ciclos)


def criar_interface_preset_ciclos_normal():
    """Cria interface profissional para seleção de presets de ciclos NORMAL"""
    ciclos_presets = criar_ciclos_presets_normal()

    def calcular_metricas_ciclo(matriz):
        """Calcula métricas importantes do ciclo"""
        risco_total = sum(sum(valor for valor in linha if valor > 0) for linha in matriz)
        entrada_inicial = matriz[0][0]
        maior_entrada = max(max(valor for valor in linha if valor > 0) for linha in matriz if any(linha))
        num_entradas = sum(1 for linha in matriz for valor in linha if valor > 0)
        num_gales = sum(1 for linha in matriz if any(valor > 0 for valor in linha))
        num_ciclos = sum(1 for valor in matriz[0] if valor > 0)
        return {
            "risco_total": risco_total,
            "entrada_inicial": entrada_inicial,
            "maior_entrada": maior_entrada,
            "num_entradas": num_entradas,
            "num_gales": num_gales - 1,  # -1 pois primeira linha não é gale
            "num_ciclos": num_ciclos
        }

    def get_classificacao_detalhada(grupo, ciclo):
        """Retorna classificação detalhada do ciclo"""
        classificacoes = {
            "G1": {
                "CICLO 1": {
                    "perfil": "MODERADO",
                    "cor": (255, 165, 0),
                    "desc": language_manager.get_text("BALANCEADO"),
                    "recomendado": language_manager.get_text("OPERACOES_PADRAO"),
                    "estrategia": language_manager.get_text("BALANCEADO")
                },
                "CICLO 2": {
                    "perfil": "CONSERVADOR",
                    "cor": (0, 255, 100),
                    "desc": language_manager.get_text("PROTECAO_MAXIMA"),
                    "recomendado": language_manager.get_text("INICIANTES"),
                    "estrategia": language_manager.get_text("PROTECAO_MAXIMA")
                },
                "CICLO 3": {
                    "perfil": "AGRESSIVO",
                    "cor": (255, 50, 50),
                    "desc": language_manager.get_text("RECUPERACAO_RAPIDA"),
                    "recomendado": language_manager.get_text("EXPERIENTES"),
                    "estrategia": language_manager.get_text("RECUPERACAO_RAPIDA")
                },
                "CICLO 4": {
                    "perfil": "MODERADO_PLUS",
                    "cor": (255, 140, 0),
                    "desc": language_manager.get_text("BALANCEADO"),
                    "recomendado": language_manager.get_text("INTERMEDIARIOS"),
                    "estrategia": language_manager.get_text("BALANCEADO")
                }
            },
            "G2": {
                "CICLO 1": {
                    "perfil": "MODERADO",
                    "cor": (255, 165, 0),
                    "desc": language_manager.get_text("BALANCEADO"),
                    "recomendado": language_manager.get_text("MEDIO_RISCO"),
                    "estrategia": language_manager.get_text("BALANCEADO")
                },
                "CICLO 2": {
                    "perfil": "CONSERVADOR",
                    "cor": (0, 255, 100),
                    "desc": language_manager.get_text("PROTECAO_MAXIMA"),
                    "recomendado": language_manager.get_text("LONGO_PRAZO"),
                    "estrategia": language_manager.get_text("PROTECAO_MAXIMA")
                },
                "CICLO 3": {
                    "perfil": "AGRESSIVO",
                    "cor": (255, 50, 50),
                    "desc": language_manager.get_text("RECUPERACAO_RAPIDA"),
                    "recomendado": language_manager.get_text("EXPERT"),
                    "estrategia": language_manager.get_text("RECUPERACAO_RAPIDA")
                },
                "CICLO 4": {
                    "perfil": "MODERADO_PLUS",
                    "cor": (255, 140, 0),
                    "desc": language_manager.get_text("BALANCEADO"),
                    "recomendado": language_manager.get_text("CONSISTENCIA"),
                    "estrategia": language_manager.get_text("BALANCEADO")
                }
            }
        }
        return classificacoes[grupo][ciclo]

    if dpg.does_item_exist("preset_ciclos_normal_window"):
        dpg.delete_item("preset_ciclos_normal_window")

    with dpg.window(label=language_manager.get_text("CICLOS_NORMAL"), width=500, height=600, modal=True,
                    tag="preset_ciclos_normal_window"):
        dpg.add_text(language_manager.get_text("SELECIONE_CICLO_NORMAL"), tag="selecione_ciclo_normal_text")
        dpg.add_separator()

        for grupo in ["G1", "G2"]:
            num_entradas = {"G1": 2, "G2": 3}[grupo]
            grupo_text = f"{language_manager.get_text('CICLOS_DE')} {grupo}"
            dpg.add_text(grupo_text, color=(255, 255, 0), tag=f"ciclos_grupo_{grupo}_text")
            dpg.add_separator()

            for ciclo in ["CICLO 1", "CICLO 2", "CICLO 3", "CICLO 4"]:
                metricas = calcular_metricas_ciclo(ciclos_presets[grupo][ciclo])
                info = get_classificacao_detalhada(grupo, ciclo)
                base_tag = f"ciclo_{grupo}_{ciclo}"

                with dpg.group(horizontal=False):
                    button_text = f"{ciclo} - {language_manager.get_text(info['perfil'])} ($ {metricas['risco_total']:.2f})"
                    dpg.add_button(
                        label=button_text,
                        callback=aplicar_preset_ciclo_normal,
                        user_data=(grupo, ciclo),
                        tag=f"{base_tag}_button",
                        width=400
                    )

                    with dpg.group(indent=20):
                        dpg.add_text(
                            f"{language_manager.get_text('PERFIL')}: {language_manager.get_text(info['perfil'])}",
                            color=info['cor'],
                            tag=f"perfil_{base_tag}"
                        )
                        dpg.add_text(
                            f"{language_manager.get_text('ESTRATEGIA')}: {info['estrategia']}",
                            color=(180, 180, 180),
                            tag=f"estrategia_{base_tag}"
                        )
                        dpg.add_text(
                            f"{language_manager.get_text('ENTRADA')}: $ {metricas['entrada_inicial']:.2f} | {language_manager.get_text('MAIOR')}: $ {metricas['maior_entrada']:.2f}",
                            color=(150, 150, 150),
                            tag=f"entrada_{base_tag}"
                        )
                        dpg.add_text(
                            f"{language_manager.get_text('RECOMENDADO')}: {info['recomendado']}",
                            color=(150, 150, 150),
                            tag=f"recomendado_{base_tag}"
                        )

                dpg.add_separator()

        dpg.add_text("", tag="risco_total_text_normal")

        # Aplica tema personalizado
        with dpg.theme() as theme_ciclos:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 70, 70))
                dpg.add_theme_color(dpg.mvThemeCol_Tab, (50, 50, 50))
                dpg.add_theme_color(dpg.mvThemeCol_TabHovered, (70, 70, 70))
                dpg.add_theme_color(dpg.mvThemeCol_TabActive, (90, 90, 90))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 120, 120))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)

        dpg.bind_item_theme("preset_ciclos_normal_window", theme_ciclos)


def atualizar_interface_ciclos(nova_matriz_ciclos):
    """
    Atualiza a interface dos ciclos garantindo que a matriz tem o tamanho correto.

    Args:
        nova_matriz_ciclos (list): Matriz com os novos valores a serem aplicados

    Returns:
        bool: True se a atualização foi bem sucedida, False caso contrário
    """
    try:
        print("\n=== Atualizando Interface dos Ciclos ===")

        # Cria uma cópia da matriz para não modificar a original
        matriz_validada = []

        # Garante que a matriz tem 10 linhas
        for indice_linha in range(10):
            if indice_linha < len(nova_matriz_ciclos):
                # Copia a linha existente
                linha_atual = list(nova_matriz_ciclos[indice_linha])

                # Garante que a linha tem 10 colunas
                while len(linha_atual) < 10:
                    linha_atual.append(0.0)

                matriz_validada.append(linha_atual)
            else:
                # Adiciona uma nova linha com zeros
                matriz_validada.append([0.0] * 10)

        # Atualiza cada elemento na interface
        for indice_linha in range(10):
            for indice_coluna in range(10):
                # Tag para a matriz na tela principal
                identificador_matriz_principal = f"ciclos_matriz_{indice_linha}_{indice_coluna}"

                # Tag para a matriz nas configurações
                identificador_matriz_configuracoes = f"ciclos_matriz_settings_{indice_linha}_{indice_coluna}"

                # Valor a ser aplicado
                valor_atual = matriz_validada[indice_linha][indice_coluna]

                # Atualiza o elemento na interface principal se existir
                if dpg.does_item_exist(identificador_matriz_principal):
                    dpg.set_value(identificador_matriz_principal, valor_atual)

                # Atualiza o elemento nas configurações se existir
                if dpg.does_item_exist(identificador_matriz_configuracoes):
                    dpg.set_value(identificador_matriz_configuracoes, valor_atual)

        print("✅ Interface atualizada com sucesso")
        print(f"• Dimensões finais da matriz: 10x10")
        print(f"• Total de elementos atualizados: {10 * 10}")
        return True

    except Exception as erro:
        print(f"❌ Erro ao atualizar interface dos ciclos: {str(erro)}")
        import traceback
        traceback.print_exc()
        return False


def aplicar_preset_ciclo_normal(sender, app_data, user_data):
    """
    Aplica o preset selecionado para ciclos NORMAL e mostra info window,
    garantindo que a matriz seja expandida para 10x10.
    """
    try:
        # Remove existing info window if it exists
        if dpg.does_item_exist("info_ciclo_window"):
            dpg.delete_item("info_ciclo_window")

        # Extrai informações do preset selecionado
        gerenciamento, ciclo = user_data
        ciclos_presets = criar_ciclos_presets_normal()
        matriz_preset = ciclos_presets[gerenciamento][ciclo]

        # Atualiza configurações com expansão para 10x10
        config = configuracoes_gerenciamentos["Ciclos"]
        nova_matriz = []

        # Copia as linhas do preset
        for linha in matriz_preset:
            # Expande a linha para 10 colunas
            nova_linha = list(linha)
            while len(nova_linha) < 10:
                nova_linha.append(0.0)
            nova_matriz.append(nova_linha)

        # Expande para 10 linhas
        while len(nova_matriz) < 10:
            nova_matriz.append([0.0] * 10)

        config["matriz_ciclos"] = nova_matriz

        # Calcula risco total considerando apenas valores não zero
        risco_total = sum(sum(valor for valor in linha if valor > 0)
                          for linha in matriz_preset)

        # Calcula Take Profits sugeridos (ajustados para payout de 88%)
        tp_conservador = round(risco_total * 0.12, 2)  # Ajustado para payout menor
        tp_moderado = round(risco_total * 0.18, 2)
        tp_agressivo = round(risco_total * 0.25, 2)

        # Atualiza interface usando a função aprimorada
        atualizar_interface_ciclos(nova_matriz)

        # Calcular posição central para a janela de informações
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        window_width = 300
        window_height = 250
        pos_x = (viewport_width - window_width) // 2
        pos_y = (viewport_height - window_height) // 2

        # Criar janela de informações
        with dpg.window(label=language_manager.get_text("DICAS_CICLO"),
                        tag="info_ciclo_window",
                        width=window_width,
                        height=window_height,
                        no_resize=True,
                        no_collapse=True,
                        pos=[pos_x, pos_y]):

            with dpg.group(tag="texto_ciclo_info"):
                dpg.add_text(
                    f"{language_manager.get_text('GALES_DO_CICLO')}: {gerenciamento}",
                    color=(255, 255, 0),
                    tag="gales_ciclo_text"
                )
                dpg.add_separator()

                dpg.add_text(
                    f"{language_manager.get_text('RISCO_TOTAL')}:",
                    color=(255, 50, 50),
                    tag="risco_total_ciclo_text"
                )
                dpg.add_text(
                    f"$ {risco_total:.2f}",
                    color=(255, 255, 255),
                    tag="valor_risco_text"
                )
                dpg.add_separator()

                dpg.add_text(
                    f"{language_manager.get_text('TAKE_PROFIT_SUGERIDO')}:",
                    color=(50, 255, 50),
                    tag="take_profit_text"
                )
                dpg.add_text(
                    f"{language_manager.get_text('CONSERVADOR')}: $ {tp_conservador:.2f}",
                    color=(0, 255, 255),
                    tag="tp_conservador_text"
                )
                dpg.add_text(
                    f"{language_manager.get_text('MODERADO')}: $ {tp_moderado:.2f}",
                    color=(255, 165, 0),
                    tag="tp_moderado_text"
                )
                dpg.add_text(
                    f"{language_manager.get_text('AGRESSIVO')}: $ {tp_agressivo:.2f}",
                    color=(255, 100, 100),
                    tag="tp_agressivo_text"
                )

        # Aplica tema personalizado à janela de informações
        with dpg.theme() as theme_settings:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 70, 70))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 120, 120))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)

        dpg.bind_item_theme("info_ciclo_window", theme_settings)

        # Salva configurações
        salvar_configuracoes_gerenciamento()

    except Exception as e:
        print(f"Erro ao aplicar preset NORMAL: {e}")
        import traceback
        traceback.print_exc()


def aplicar_preset_ciclo_step(sender, app_data, user_data):
    """
    Aplica o preset selecionado para ciclos STEP e mostra info window,
    garantindo que a matriz seja expandida para 10x10.
    """
    try:
        # Remove existing info window if it exists
        if dpg.does_item_exist("info_ciclo_window"):
            dpg.delete_item("info_ciclo_window")

        # Extrai informações do preset selecionado
        gerenciamento, ciclo = user_data
        ciclos_presets = criar_ciclos_presets_step()
        matriz_preset = ciclos_presets[gerenciamento][ciclo]

        # Atualiza configurações com expansão para 10x10
        config = configuracoes_gerenciamentos["Ciclos"]
        nova_matriz = []

        # Copia as linhas do preset
        for linha in matriz_preset:
            # Expande a linha para 10 colunas
            nova_linha = list(linha)
            while len(nova_linha) < 10:
                nova_linha.append(0.0)
            nova_matriz.append(nova_linha)

        # Expande para 10 linhas
        while len(nova_matriz) < 10:
            nova_matriz.append([0.0] * 10)

        config["matriz_ciclos"] = nova_matriz

        # Calcula risco total considerando apenas valores não zero
        risco_total = sum(sum(valor for valor in linha if valor > 0)
                          for linha in matriz_preset)

        # Calcula Take Profits sugeridos
        tp_conservador = round(risco_total * 0.15, 2)
        tp_moderado = round(risco_total * 0.25, 2)
        tp_agressivo = round(risco_total * 0.35, 2)

        # Atualiza interface usando a função aprimorada
        atualizar_interface_ciclos(nova_matriz)

        # Calcular posição central para a janela de informações
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        window_width = 300
        window_height = 250
        pos_x = (viewport_width - window_width) // 2
        pos_y = (viewport_height - window_height) // 2

        # Criar janela de informações
        with dpg.window(label=language_manager.get_text("DICAS_CICLO"),
                        tag="info_ciclo_window",
                        width=window_width,
                        height=window_height,
                        no_resize=True,
                        no_collapse=True,
                        pos=[pos_x, pos_y]):

            with dpg.group(tag="texto_ciclo_info"):
                dpg.add_text(
                    f"{language_manager.get_text('GALES_DO_CICLO')}: {gerenciamento}",
                    color=(255, 255, 0),
                    tag="gales_ciclo_text"
                )
                dpg.add_separator()

                dpg.add_text(
                    f"{language_manager.get_text('RISCO_TOTAL')}:",
                    color=(255, 50, 50),
                    tag="risco_total_ciclo_text"
                )
                dpg.add_text(
                    f"$ {risco_total:.2f}",
                    color=(255, 255, 255),
                    tag="valor_risco_text"
                )
                dpg.add_separator()

                dpg.add_text(
                    f"{language_manager.get_text('TAKE_PROFIT_SUGERIDO')}:",
                    color=(50, 255, 50),
                    tag="take_profit_text"
                )
                dpg.add_text(
                    f"{language_manager.get_text('CONSERVADOR')}: $ {tp_conservador:.2f}",
                    color=(0, 255, 255),
                    tag="tp_conservador_text"
                )
                dpg.add_text(
                    f"{language_manager.get_text('MODERADO')}: $ {tp_moderado:.2f}",
                    color=(255, 165, 0),
                    tag="tp_moderado_text"
                )
                dpg.add_text(
                    f"{language_manager.get_text('AGRESSIVO')}: $ {tp_agressivo:.2f}",
                    color=(255, 100, 100),
                    tag="tp_agressivo_text"
                )

        # Aplica tema personalizado à janela de informações
        with dpg.theme() as theme_settings:
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 70, 70))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 120, 120))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)

        dpg.bind_item_theme("info_ciclo_window", theme_settings)

        # Salva configurações
        salvar_configuracoes_gerenciamento()

    except Exception as e:
        print(f"Erro ao aplicar preset STEP: {e}")
        import traceback
        traceback.print_exc()

def update_required_losses(sender, app_data):
    global required_losses

    try:
        new_value = int(app_data)
        if new_value > 0:
            required_losses = new_value
            print(f"Número de losses para antiloss atualizado: {required_losses}")
            save_configurations()
        else:
            print("Valor inválido para número de losses")
    except ValueError:
        print("Erro: valor deve ser um número inteiro positivo")


def toggle_abr_strategy(sender, app_data):
    """Alterna entre ativar/desativar a estratégia ABR"""
    global abr_strategy_active
    abr_strategy_active = app_data
    print(f"Estratégia ABR {'ativada' if abr_strategy_active else 'desativada'}")
    update_abr_status_display()
    save_configurations()  # Salva a configuração


def update_sequencia_minima(sender, app_data):
    """Atualiza o valor da sequência mínima"""
    global SequenciaMinima , SequenciaMaxima

    # Garante que a sequência mínima seja menor que a máxima
    if app_data >= SequenciaMaxima:
        app_data = SequenciaMaxima - 1
        if app_data < 1:
            app_data = 1
            # Também atualiza a sequência máxima se necessário
            SequenciaMaxima = 2
            dpg.set_value("sequencia_maxima_input", SequenciaMaxima)

    SequenciaMinima = app_data
    print(f"Sequência mínima atualizada para: {SequenciaMinima}")
    dpg.set_value("sequencia_minima_input", SequenciaMinima)  # Atualiza o input
    save_configurations()


def update_sequencia_maxima(sender, app_data):
    """Atualiza o valor da sequência máxima"""
    global SequenciaMaxima, SequenciaMinima

    # Garante que a sequência máxima seja maior que a mínima
    if app_data <= SequenciaMinima:
        app_data = SequenciaMinima + 1

    SequenciaMaxima = app_data
    print(f"Sequência máxima atualizada para: {SequenciaMaxima}")
    dpg.set_value("sequencia_maxima_input", SequenciaMaxima)  # Atualiza o input
    save_configurations()


def update_winrate(sender, app_data):
    """Atualiza o win rate mínimo"""
    global Winrate
    Winrate = app_data
    print(f"Win rate mínimo atualizado para: {Winrate}%")
    save_configurations()


def reiniciar_abr_strategy():
    """Reinicia a estratégia ABR com os novos parâmetros"""
    global abr_strategy, SequenciaMinima, SequenciaMaxima, Winrate

    try:
        # Cria uma nova instância da estratégia com os parâmetros atualizados
        abr_strategy = ABRStrategy(
            min_sequence=SequenciaMinima,
            max_sequence=SequenciaMaxima,
            analysis_candles=400,
            min_success_rate=Winrate
        )

        print(f"Estratégia ABR reiniciada com sucesso.")
        print(f"Parâmetros: min={SequenciaMinima}, max={SequenciaMaxima}, winrate={Winrate}%")

        # Atualiza o display de status
        update_abr_status_display()

        # Mostra uma mensagem de sucesso
        if dpg.does_item_exist("abr_status_text"):
            dpg.set_value("abr_status_text", "Estratégia reiniciada com sucesso!")
            dpg.configure_item("abr_status_text", color=(0, 255, 0))

    except Exception as e:
        print(f"Erro ao reiniciar estratégia ABR: {e}")
        if dpg.does_item_exist("abr_status_text"):
            dpg.set_value("abr_status_text", f"Erro: {str(e)}")
            dpg.configure_item("abr_status_text", color=(255, 0, 0))


def update_abr_status_display():
    """Atualiza o texto de status da estratégia ABR na janela de configurações"""
    if not dpg.does_item_exist("abr_status_text"):
        return

    if not abr_strategy_active:
        dpg.set_value("abr_status_text", "Estratégia ABR desativada")
        dpg.configure_item("abr_status_text", color=(255, 100, 100))
        return

    # Obtém status atual da estratégia
    status = abr_strategy.get_status()
    call_length = status.get("optimal_call_length", "N/A")
    put_length = status.get("optimal_put_length", "N/A")
    call_rate = status.get("call_success_rate", 0)
    put_rate = status.get("put_success_rate", 0)

    status_text = (
        f"Ativa: Sim\n"
        f"Sequência CALL: {call_length} velas vermelhas ({call_rate:.2f}%)\n"
        f"Sequência PUT: {put_length} velas verdes ({put_rate:.2f}%)\n"
        f"Configuração: Min={SequenciaMinima}, Max={SequenciaMaxima}, WR={Winrate}%"
    )

    dpg.set_value("abr_status_text", status_text)
    dpg.configure_item("abr_status_text", color=(100, 255, 100))

def open_settings_window():
    global numero_confluencias, simbolos_ativos, volatilidade_selecionada, velas_selecionadas
    global retracao_value, reversao_value, antiloss_ativado, required_losses , fluxo_active
    global risco, total_operations, wins, payout, min_entry, STOP_WIN, STOP_LOSS, NumeroDeGales, tipo, style

    if dpg.does_item_exist("settings_window"):
        dpg.delete_item("settings_window")

    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()

    window_width = 750
    window_height = 500
    pos_x = (viewport_width - window_width) // 2
    pos_y = (viewport_height - window_height) // 2

    with dpg.window(label=language_manager.get_text("CONFIGURACOES"), tag="settings_window", width=window_width, height=window_height,
                    no_resize=True, no_collapse=True, pos=[pos_x, pos_y]):
        with dpg.tab_bar():
            with dpg.tab(label=language_manager.get_text("ESTRATEGIAS")):
                dpg.add_text(language_manager.get_text("CONFLUENCIAS"), color=(255, 215, 0))

                dpg.add_input_int(label=language_manager.get_text("NUMERO_CONFLUENCIAS"), default_value=numero_confluencias,
                                  tag="numero_confluencias", width=200, callback=update_numero_confluencias)

                dpg.add_spacer(height=10)
                dpg.add_separator()

                dpg.add_text(language_manager.get_text("FILTROS_BOT"), color=(255, 215, 0),tag="filtrostext")
                # Adiciona checkboxes para Price Action e Volume Profile
                dpg.add_checkbox(
                    label=language_manager.get_text("PRICE_ACTION"),
                    tag="price_action_checkbox",
                    default_value=price_action_active,
                    callback=toggle_price_action
                )

                dpg.add_checkbox(
                    label=language_manager.get_text("VOLUME_PROFILE"),
                    tag="volume_profile_checkbox",
                    default_value=volume_profile_active,
                    callback=toggle_volume_profile
                )

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_text("TIFRAMEMODE/GALEMODE", color=(255, 215, 0))
                with dpg.group():
                    # Radio buttons para selecionar o modo
                    dpg.add_radio_button(
                        items=["Tempo Fixo", "Fim da Vela"],
                        default_value="Tempo Fixo" if modo_entrada == "tempo_fixo" else "Fim da Vela",
                        horizontal=True,
                        callback=toggle_modo_entrada,
                        tag="modo_entrada_radio"
                    )

                    dpg.add_spacer(height=10)

                    # Combo único para expiração
                    dpg.add_combo(
                        label="Timeframe",
                        items=["1", "2", "3", "4", "5", "10", "15", "30"] if modo_entrada == "tempo_fixo" else ["1",
                                                                                                                "5",
                                                                                                                "15",
                                                                                                                "30"],
                        default_value=str(default_expiration),
                        callback=update_expiration,
                        tag="expiration_selector",
                        width=100
                    )

                    # Adicionar seletor de modo de gale
                    dpg.add_spacer(height=10)
                    dpg.add_separator()
                    dpg.add_text("GALE MODE", color=(255, 215, 0))
                    dpg.add_radio_button(
                        items=["Normal", "ZigZag"],
                        default_value="Normal" if modo_gale == "normal" else "ZigZag",
                        horizontal=True,
                        callback=toggle_modo_gale,
                        tag="modo_gale_radio"
                    )

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_text(language_manager.get_text("FLUXO_BOT"), color=(255, 215, 0), tag="fluxotext")

                # FLUXO checkbox first since it disables other options
                dpg.add_checkbox(label=language_manager.get_text("ATIVA_FLUXO"), tag="fluxo_value",
                                 default_value=fluxo_active, callback=toggle_fluxo)

                dpg.add_spacer(height=10)
                dpg.add_separator()

                dpg.add_text(("I.A GENARATION ML"), color=(255, 215, 0))

                dpg.add_checkbox(
                    label="ML Strategy (DQN/PPO)",
                    tag="ml_strategy_checkbox",
                    default_value=ml_strategy_active,
                    callback=toggle_ml_strategy
                )

                dpg.add_spacer(height=10)
                dpg.add_separator()

                dpg.add_text(("CANDLES SEQUENCE ABR"), color=(255, 215, 0))

                dpg.add_checkbox(
                    label="ABR I.A",
                    tag="abr_strategy_checkbox",
                    default_value=abr_strategy_active,
                    callback=toggle_abr_strategy
                )




                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_text(language_manager.get_text("ESTRATEGIAS_PADROES"), color=(255, 215, 0))
                dpg.add_checkbox(label=language_manager.get_text("ATIVAR_RETRACAO"), tag="retracao_value",
                                 default_value=retracao_value, callback=toggle_retracao)

                dpg.add_checkbox(label=language_manager.get_text("ATIVAR_REVERSAO"), tag="reversao_value",
                                 default_value=reversao_value, callback=toggle_reversao)

                dpg.add_spacer(height=10)
                dpg.add_separator()


                dpg.add_checkbox(label=language_manager.get_text("ATIVAR_ANTILOSS"), tag="antiloss_value",
                                 default_value=antiloss_ativado, callback=toggle_antiloss)
                dpg.add_combo(
                    label=language_manager.get_text("MODO_ANTILOSS"),
                    items=[language_manager.get_text("GLOBAL"), language_manager.get_text("RESTRITO")],
                    default_value=language_manager.get_text("GLOBAL") if modo_antiloss == "global" else language_manager.get_text("RESTRITO"),
                    tag="modo_antiloss_combo",
                    callback=toggle_modo_antiloss,
                )

                dpg.add_input_int(
                    label=language_manager.get_text("QTD_ANTLOSS"),
                    default_value=required_losses,
                    tag="required_losses_input",
                    min_value=1,
                    max_value=10,
                    callback=update_required_losses
                )

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_text(language_manager.get_text("VOLATILIDADE"), color=(255, 215, 0))


                with dpg.group(horizontal=True):
                    dpg.add_combo(items=[language_manager.get_text("BAIXA"), language_manager.get_text("MEDIA"), language_manager.get_text("ALTA")], default_value=volatilidade_selecionada,
                                  tag="volatilidade_opcoes", width=100, callback=on_volatilidade_selecionada)
                    dpg.add_combo(items=[language_manager.get_text("5_VELAS"), language_manager.get_text("10_VELAS"), language_manager.get_text("20_VELAS")], default_value=velas_selecionadas,
                                  tag="volatilidade_opcoes1", width=100, callback=on_volatilidade_selecionada1)

                dpg.add_spacer(height=10)
                dpg.add_separator()
                dpg.add_text(language_manager.get_text("SELECIONE_PARES"), color=(255, 215, 0))

                primeira_fileira = symbols[:5]
                segunda_fileira = symbols[5:10]
                quarta_fileira = symbols[10:15]
                quinta_fileira = symbols[15:20]
                sexta_fileira = symbols[20:]

                with dpg.group(horizontal=True):
                    for fileira in [primeira_fileira, segunda_fileira, quarta_fileira , quinta_fileira , sexta_fileira]:
                        with dpg.group():
                            for symbol in fileira:
                                friendly_name = get_display_name(symbol)
                                dpg.add_checkbox(
                                    label=friendly_name,  # Usa o nome amigável aqui
                                    tag=f"checkbox_{symbol}",  # Mantém a tag original para processamento interno
                                    default_value=simbolos_ativos.get(symbol, True),
                                    callback=toggle_symbol
                                )
                        if fileira != sexta_fileira:
                            dpg.add_spacer(width=20)



            # Aba de Gerenciamento
            with dpg.tab(label=language_manager.get_text("GERENCIAMENTO"),tag="gerenciamentotext"):
                dpg.add_text(language_manager.get_text("TIPO_GERENCIAMENTO"), color=(255, 215, 0))
                dpg.add_combo(
                    label=language_manager.get_text("SELECIONE_GERENCIAMENTO"),
                    items=[language_manager.get_text("MASANIELLO"), language_manager.get_text("CICLOS")],
                    default_value=gerenciamento_ativo,
                    callback=toggle_gerenciamento,
                    tag="gerenciamento_selector",
                    width=200
                )

                # Container Masaniello
                with dpg.group(tag="masaniello_container", show=(gerenciamento_ativo == language_manager.get_text("MASANIELLO"))):
                    dpg.add_input_float(label=language_manager.get_text("RISCO"), default_value=risco, tag="risco_input", format="%.2f")
                    dpg.add_input_int(label=language_manager.get_text("TOTAL_OPERACOES"), default_value=total_operations, tag="total_operations_input")
                    dpg.add_input_int(label=language_manager.get_text("NUMERO_WINS"), default_value=wins, tag="wins_input")
                    dpg.add_input_float(label=language_manager.get_text("PAYOUT"), default_value=payout, tag="payout_input", format="%.2f")
                    dpg.add_input_float(label=language_manager.get_text("MIN_ENTRADA"), default_value=min_entry, tag="min_entry_input", format="%.2f")
                    dpg.add_input_int(label=language_manager.get_text("QTD_GALES"), default_value=NumeroDeGales, tag="quant_gales", min_value=0, max_value=5)
                    dpg.add_combo(
                        label=language_manager.get_text("TIPO_MASANIELLO"),
                        items=[language_manager.get_text("NORMAL"), language_manager.get_text("PROGRESSIVO")],
                        default_value=language_manager.get_text("NORMAL") if tipo == 1 else language_manager.get_text("PROGRESSIVO"),
                        tag="masaniello_type_selector",
                        callback=update_masaniello_type
                    )
                    dpg.add_combo(
                        label=language_manager.get_text("ESTILO_MASANIELLO"),
                        items=[language_manager.get_text("NORMAL"), language_manager.get_text("COMPOSTO"), language_manager.get_text("CONSERVADOR")],
                        default_value=style,
                        tag="masaniello_style_selector",
                        callback=update_masaniello_style
                    )

                # Container Ciclos
                with dpg.group(tag="ciclos_container", show=(gerenciamento_ativo == language_manager.get_text("CICLOS"))):
                    criar_interface_ciclos()




            with dpg.tab(label=language_manager.get_text("STOP_WIN_STOP_LOSS")):
                dpg.add_input_float(label=language_manager.get_text("STOP_WIN"), default_value=STOP_WIN, tag="stop_win_input", format="%.2f")
                dpg.add_input_float(label=language_manager.get_text("STOP_LOSS"), default_value=STOP_LOSS, tag="stop_loss_input",
                                    format="%.2f")

        with dpg.group(horizontal=True):
            dpg.add_button(label=language_manager.get_text("SALVAR"), width=135, height=20, callback=submit_masaniello_settings)
            dpg.add_button(label=language_manager.get_text("CANCELAR"), width=135, height=20, callback=close_settings_window)

    # Aplica tema personalizado
    with dpg.theme() as theme_settings:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 70, 70))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 120, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)

    dpg.bind_item_theme("settings_window", theme_settings)


def toggle_ml_strategy(sender, app_data):
    """Ativa/desativa estratégia ML com inicialização segura"""
    global ml_strategy_active
    ml_strategy_active = app_data

    try:
        if ml_strategy_active:
            # Limpa estratégias existentes
            trading_strategies.clear()

            # Inicializa novas estratégias
            print("\n=== Iniciando Estratégias ML ===")
            initialize_strategies(symbols)
            print("✅ Estratégias ML ativadas e inicializadas")

            # Inicia o auto-save em uma thread separada
            def run_auto_save():
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    while ml_strategy_active and is_running and not stop_event.is_set():
                        try:
                            # Salva os modelos
                            save_count = 0
                            for symbol, strategy in trading_strategies.items():
                                if strategy.save_models():
                                    save_count += 1
                            if save_count > 0:
                                print(f"✅ {save_count} modelos ML salvos automaticamente")
                        except Exception as e:
                            print(f"Erro ao salvar modelos ML: {e}")

                        # Aguarda 5 minutos de forma interruptível
                        for _ in range(300):  # 5 minutos em segundos
                            if not ml_strategy_active or not is_running or stop_event.is_set():
                                break
                            time.sleep(1)  # Verifica a cada segundo

                except Exception as e:
                    print(f"Erro na thread de auto-save ML: {e}")
                    import traceback
                    traceback.print_exc()
                finally:
                    print("Thread de auto-save ML finalizada")

            # Inicia a thread se não existir ou se não estiver ativa
            if not hasattr(toggle_ml_strategy, 'save_thread') or not toggle_ml_strategy.save_thread.is_alive():
                toggle_ml_strategy.save_thread = threading.Thread(
                    target=run_auto_save,
                    daemon=True,
                    name="MLAutoSave"
                )
                toggle_ml_strategy.save_thread.start()
                print("✅ Thread de auto-save ML iniciada")
        else:
            # Desativa e salva estratégias
            for strategy in trading_strategies.values():
                strategy.save_models()
            trading_strategies.clear()
            print("✅ Estratégias ML desativadas e salvas")

        # Salva o estado da configuração
        save_configurations()
        print(f"💾 Estado ML Strategy salvo: {'Ativada' if ml_strategy_active else 'Desativada'}")

    except Exception as e:
        print(f"❌ Erro ao alternar estratégia ML: {e}")
        ml_strategy_active = False
        trading_strategies.clear()
        save_configurations()  # Salva mesmo em caso de erro


async def force_initial_training():
    """Força treinamento inicial de todos os modelos ML ativos"""
    print("\n=== Iniciando Treinamento Inicial dos Modelos ML ===")

    trained_count = 0
    for symbol in symbols:
        if symbol not in trading_strategies:
            print(f"⚠️ No strategy object for {symbol}")
            continue

        symbol_dir = f"models/{symbol}"
        if not os.path.exists(symbol_dir):
            try:
                os.makedirs(symbol_dir)
                # Test write permissions
                test_file = os.path.join(symbol_dir, "test.txt")
                with open(test_file, "w") as f:
                    f.write("test")
                os.remove(test_file)
                print(f"✅ Directory for {symbol} created and writable")
            except Exception as e:
                print(f"❌ Cannot create/write to {symbol_dir}: {e}")
                continue

    for symbol, strategy in trading_strategies.items():
        if not simbolos_ativos.get(symbol, False):
            print(f"⏩ Pulando {symbol} - Par desativado")
            continue

        print(f"\n>> Verificando dados para {symbol}...")
        if symbol in velas and len(velas[symbol]) >= 150:
            try:
                print(f"📊 Dados disponíveis: {len(velas[symbol])} velas")
                print(f"Iniciando treinamento para {symbol}...")
                # Treina usando dados históricos com gale
                result = await strategy.train_on_historical(velas[symbol], include_gale=True)
                if result:
                    # Salva o modelo treinado
                    saved = strategy.save_models()
                    trained_count += 1
                    print(f"✅ Treinamento inicial concluído para {symbol} (Salvo: {'Sim' if saved else 'Não'})")
                else:
                    print(f"⚠️ Treinamento falhou para {symbol}")
            except Exception as e:
                print(f"❌ Erro no treinamento de {symbol}: {e}")
                traceback.print_exc()
        else:
            velas_count = len(velas.get(symbol, []))
            print(f"❌ Dados insuficientes para {symbol}: {velas_count}/150 velas")

    print(f"\n=== Treinamento Inicial Concluído ===")
    print(f"✅ {trained_count}/{len(trading_strategies)} modelos treinados com sucesso")
    return trained_count > 0


# Primeiro inicializamos o dicionário principal
configuracoes_gerenciamentos = {}

configuracoes_gerenciamentos["Ciclos"] = {
    "matriz_ciclos": [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 1
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 2
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 3
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 4
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 5
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 6
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 7
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 8
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 9
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Linha 10
    ],
    "linha_atual": 0,
    "coluna_atual": 0,
    "modo_ataque_defesa": False,
    "alvo_lucro": 0.01,
    "lucro_inicial_ciclo": 0.0,
    "lucro_melhor_resultado": 0.0,  # Armazena o melhor resultado já obtido
    "linha_atual_repetindo": False
}

# Agora você pode fazer atualizações seguras
configuracoes_gerenciamentos["Ciclos"].update({
    "modo_ataque_defesa": False,  # Flag para ativar/desativar modo
    "alvo_lucro": 0.5,  # Valor alvo de lucro por ciclo
    "lucro_inicial_ciclo": 0.0,  # Lucro no início do ciclo
    "linha_atual_repetindo": False  # Flag para controlar repetição de linha
})

def update_expiration(sender, app_data):
    """Updates expiration/timeframe"""
    global default_expiration, fim_da_vela_time, modo_entrada

    try:
        print(f"\n🔧 DEBUG update_expiration:")
        print(f"   sender: {sender}")
        print(f"   app_data: {app_data}")
        print(f"   modo_entrada: {modo_entrada}")
        print(f"   ANTES - fim_da_vela_time: {fim_da_vela_time}")
        print(f"   ANTES - default_expiration: {default_expiration}")

        if modo_entrada == "fim_da_vela":
            novo_timeframe = f"M{app_data}"
            if novo_timeframe != fim_da_vela_time:
                print(f"   🔄 MUDANÇA DETECTADA: {fim_da_vela_time} → {novo_timeframe}")
                fim_da_vela_time = novo_timeframe
            else:
                print(f"   ℹ️ SEM MUDANÇA: Mantendo {fim_da_vela_time}")
            print(f"   DEPOIS - fim_da_vela_time: {fim_da_vela_time}")
            print(f"Timeframe Fim da Vela updated to: M{app_data}")
        else:
            if int(app_data) != default_expiration:
                print(f"   🔄 MUDANÇA DETECTADA: {default_expiration} → {app_data}")
                default_expiration = int(app_data)
            else:
                print(f"   ℹ️ SEM MUDANÇA: Mantendo {default_expiration}")
            print(f"   DEPOIS - default_expiration: {default_expiration}")
            print(f"Expiration updated to: {app_data}")

        # Salva as configurações imediatamente
        save_configurations()
        print(f"💾 Configuração de expiração/timeframe salva: {fim_da_vela_time if modo_entrada == 'fim_da_vela' else f'{default_expiration} min'}")

    except Exception as e:
        print(f"Error updating expiration: {e}")
        traceback.print_exc()


def toggle_modo_ataque_defesa(sender, app_data):
    """Função callback para ativar/desativar modo Ataque/Defesa"""
    try:
        config = configuracoes_gerenciamentos["Ciclos"]
        config["modo_ataque_defesa"] = app_data

        # Mostra/esconde configurações específicas do modo
        if dpg.does_item_exist("grupo_alvo_lucro"):
            dpg.configure_item("grupo_alvo_lucro", show=app_data)
        if dpg.does_item_exist("instrucoes_ataque_defesa"):
            dpg.configure_item("instrucoes_ataque_defesa", show=app_data)

        print(f"Modo Ataque/Defesa {'ativado' if app_data else 'desativado'}")
        salvar_configuracoes_gerenciamento()

    except Exception as e:
        print(f"Erro ao alternar modo Ataque/Defesa: {e}")


def atualizar_alvo_lucro(sender, app_data):
    """Função callback para atualizar o valor alvo de lucro"""
    try:
        config = configuracoes_gerenciamentos["Ciclos"]
        config["alvo_lucro"] = float(app_data)
        print(f"Alvo de lucro atualizado para: ${app_data:.2f}")
        salvar_configuracoes_gerenciamento()

    except Exception as e:
        print(f"Erro ao atualizar alvo de lucro: {e}")


# Adicionar nas configurações iniciais
configuracoes_gerenciamentos["Ciclos"].update({
    "lucro_inicial_ciclo": 0.0,  # Lucro base do ciclo atual
    "lucro_ultimo_ciclo_sucesso": 0.0,  # Lucro do último ciclo bem sucedido
})


def verificar_alvo_ciclo(lucro_total):
    """
    Verifica se o alvo foi atingido considerando o melhor resultado anterior
    """
    try:
        config = configuracoes_gerenciamentos["Ciclos"]

        if not config["modo_ataque_defesa"]:
            return False

        lucro_base = config.get("lucro_inicial_ciclo", 0.0)
        melhor_resultado = config.get("lucro_melhor_resultado", 0.0)
        alvo_lucro = config.get("alvo_lucro", 0.01)

        # Validação adicional para garantir que lucro_total é válido
        if lucro_total is None or not isinstance(lucro_total, (float, int)):
            print("❌ Lucro total inválido para verificação")
            return False

        # Calcula ganho em relação ao lucro base
        ganho_ciclo = lucro_total - lucro_base

        # Log detalhado para melhor debug
        print(f"\n=== Verificação de Alvo do Ciclo ===")
        print(f"Lucro total atual: ${lucro_total:.2f}")
        print(f"Lucro base do ciclo: ${lucro_base:.2f}")
        print(f"Melhor resultado: ${melhor_resultado:.2f}")
        print(f"Ganho neste ciclo: ${ganho_ciclo:.2f}")
        print(f"Alvo necessário: ${alvo_lucro:.2f}")

        # Verifica se o ganho é significativo o suficiente (evita flutuações mínimas)
        if abs(ganho_ciclo) < 0.001:
            print("⚠️ Ganho muito pequeno para considerar")
            return False

        # Considera alvo atingido apenas se:
        # 1. O ganho for maior que o alvo E
        # 2. O lucro total for maior que o melhor resultado anterior
        resultado = ganho_ciclo >= alvo_lucro and lucro_total >= melhor_resultado

        if resultado:
            print(f"✅ Alvo atingido!")
            print(f"Ganho confirmado: ${ganho_ciclo:.2f}")
            # Atualiza melhor resultado
            config["lucro_melhor_resultado"] = lucro_total
            return True
        else:
            if ganho_ciclo < 0:
                print(f"❌ Loss detectado: ${ganho_ciclo:.2f}")
            else:
                print(f"❌ Alvo não atingido. Faltam: ${(alvo_lucro - ganho_ciclo):.2f}")
            return False

    except Exception as e:
        print(f"Erro ao verificar alvo do ciclo: {e}")
        traceback.print_exc()
        return False


def criar_interface_ciclos():
    """Cria a interface do gerenciamento de Ciclos com suporte completo a matriz 10x10"""
    try:
        config = configuracoes_gerenciamentos["Ciclos"]

        # Garante que a matriz tem o tamanho correto (10x10)
        matriz = config["matriz_ciclos"]
        while len(matriz) < 10:
            matriz.append([0.0] * 10)
        for i in range(len(matriz)):
            while len(matriz[i]) < 10:
                matriz[i].append(0.0)

        # Atualiza a matriz no configuracoes_gerenciamentos
        config["matriz_ciclos"] = matriz

        dpg.add_text(language_manager.get_text("PRESETS_CICLOS_AD"), color=(255, 215, 0), tag="presets_ciclos_ad_text")

        with dpg.group(horizontal=True):
            dpg.add_button(
                label=language_manager.get_text("PRESETS_STEP_SEGURO"),
                callback=criar_interface_preset_ciclos_step,
                width=200,
                tag="presets_step_seguro_button"
            )
            dpg.add_spacer(width=10)
            dpg.add_button(
                label=language_manager.get_text("PRESETS_NORMAL_MODERADO"),
                callback=criar_interface_preset_ciclos_normal,
                width=200,
                tag="presets_normal_moderado_button"
            )

        dpg.add_separator()
        dpg.add_text("", tag="risco_total_text_main")
        dpg.add_text(language_manager.get_text("MODO_CICLOS"), color=(255, 215, 0), tag="modo_ciclos_text")

        with dpg.group():
            dpg.add_checkbox(
                label=language_manager.get_text("MODO_AD"),
                default_value=config.get("modo_ataque_defesa", False),
                callback=toggle_modo_ataque_defesa,
                tag="checkbox_ataque_defesa"
            )

            # Grupo para configurações do modo Ataque/Defesa
            with dpg.group(tag="grupo_alvo_lucro", show=config.get("modo_ataque_defesa", False)):
                dpg.add_input_float(
                    label=language_manager.get_text("ALVO_LUCRO"),
                    default_value=config.get("alvo_lucro", 0.5),
                    format="%.2f",
                    callback=atualizar_alvo_lucro,
                    tag="input_alvo_lucro",
                    width=150
                )

        dpg.add_separator()

        def matriz_callback(sender, app_data, user_data):
            try:
                linha, coluna = user_data
                valor = dpg.get_value(sender)
                configuracoes_gerenciamentos["Ciclos"]["matriz_ciclos"][linha][coluna] = float(valor)
                salvar_configuracoes_gerenciamento()
            except Exception as e:
                print(f"Erro no callback da matriz: {e}")

        # Cria a matriz 10x10 (número de linhas e colunas fixo)
        total_linhas = 10
        total_colunas = 10

        for linha in range(total_linhas):
            with dpg.group(horizontal=True):
                dpg.add_text(f"{language_manager.get_text('LINHA')} {linha + 1}", color=(0, 255, 255),
                             tag=f"linha_{linha}_text")
                for coluna in range(total_colunas):
                    # Garante que existe um valor para esta posição da matriz
                    valor = 0.0
                    if linha < len(matriz) and coluna < len(matriz[linha]):
                        valor = float(matriz[linha][coluna])

                    dpg.add_input_float(
                        label="",
                        width=60,
                        format="%.2f",
                        default_value=valor,
                        callback=matriz_callback,
                        user_data=(linha, coluna),
                        step=0.0,
                        tag=f"ciclos_matriz_{linha}_{coluna}"
                    )

        dpg.add_separator()

        with dpg.group(horizontal=True):
            dpg.add_button(label=language_manager.get_text("LIMPAR_MATRIZ"), callback=limpar_matriz, width=120,
                           tag="limpar_matriz_button")
            dpg.add_button(label=language_manager.get_text("SALVAR_MATRIZ"), callback=salvar_matriz, width=120,
                           tag="salvar_matriz_button")

        # Instruções específicas para modo Ataque/Defesa
        with dpg.group(tag="instrucoes_ataque_defesa", show=config.get("modo_ataque_defesa", False)):
            dpg.add_separator()
            dpg.add_text(language_manager.get_text("MODO_AD") + ":", color=(255, 215, 0), tag="instrucoes_ad_title")
            dpg.add_text("- " + language_manager.get_text("INSTRUCAO_AD_1"), tag="instrucao_ad_1")
            dpg.add_text("- " + language_manager.get_text("INSTRUCAO_AD_2"), tag="instrucao_ad_2")
            dpg.add_text("- " + language_manager.get_text("INSTRUCAO_AD_3"), tag="instrucao_ad_3")
            dpg.add_text("- " + language_manager.get_text("INSTRUCAO_AD_4"), tag="instrucao_ad_4")

    except Exception as e:
        print(f"Erro ao criar interface dos ciclos: {e}")
        import traceback
        traceback.print_exc()



def save_gerenciamento_selection():
    """Salva a seleção do tipo de gerenciamento"""
    config_dir = get_config_directory()
    config_file = os.path.join(config_dir, "gerenciamento_tipo.json")

    try:
        # Converte o texto traduzido para o valor base antes de salvar
        tipo_base = "Masaniello" if gerenciamento_ativo == language_manager.get_text("MASANIELLO") else "Ciclos"

        # Salva também os dados completos do ciclo junto com o tipo
        dados = {
            "tipo": tipo_base,
            "ciclos_config": configuracoes_gerenciamentos["Ciclos"]
        }

        with open(config_file, 'w') as f:
            json.dump(dados, f, indent=2)
        print(f"Tipo de gerenciamento e configurações dos ciclos salvos: {tipo_base}")

        # Salva separadamente os dados completos do ciclo também no arquivo de gerenciamento
        salvar_configuracoes_gerenciamento()
    except Exception as e:
        print(f"Erro ao salvar tipo de gerenciamento: {e}")


def load_gerenciamento_tipo():
    """Carrega o tipo de gerenciamento salvo e suas configurações"""
    global gerenciamento_ativo, configuracoes_gerenciamentos

    try:
        config_dir = get_config_directory()
        tipo_file = os.path.join(config_dir, "gerenciamento_tipo.json")
        gerenciamento_file = os.path.join(config_dir, "gerenciamento_config.json")

        print("\n=== Carregando Configurações de Gerenciamento ===")

        # Carrega tipo de gerenciamento
        if os.path.exists(tipo_file):
            with open(tipo_file, 'r') as f:
                data = json.load(f)
                saved_tipo = data.get("tipo", "Masaniello")
                ciclos_config = data.get("ciclos_config", None)

                print(f"Tipo carregado: {saved_tipo}")
                print(f"Configurações de ciclos encontradas: {'Sim' if ciclos_config else 'Não'}")

                # Converte o tipo salvo para o texto traduzido atual
                gerenciamento_ativo = language_manager.get_text(
                    "MASANIELLO") if saved_tipo == "Masaniello" else language_manager.get_text("CICLOS")

        # Carrega configurações completas dos ciclos
        if os.path.exists(gerenciamento_file):
            with open(gerenciamento_file, 'r') as f:
                config = json.load(f)
                if "Ciclos" in config:
                    configuracoes_gerenciamentos["Ciclos"].update({
                        "matriz_ciclos": config["Ciclos"]["matriz_ciclos"],
                        "linha_atual": config["Ciclos"].get("linha_atual", 0),
                        "coluna_atual": config["Ciclos"].get("coluna_atual", 0),
                        "modo_ataque_defesa": config["Ciclos"].get("modo_ataque_defesa", False),
                        "alvo_lucro": config["Ciclos"].get("alvo_lucro", 0.5),
                        "lucro_inicial_ciclo": config["Ciclos"].get("lucro_inicial_ciclo", 0.0),
                        "linha_atual_repetindo": config["Ciclos"].get("linha_atual_repetindo", False)
                    })
                    print(f"Configurações dos ciclos carregadas:")
                    print(f"Modo Ataque/Defesa: {configuracoes_gerenciamentos['Ciclos']['modo_ataque_defesa']}")
                    print(f"Alvo Lucro: {configuracoes_gerenciamentos['Ciclos']['alvo_lucro']}")
                    print(f"Linha Atual: {configuracoes_gerenciamentos['Ciclos']['linha_atual']}")

        # Atualiza interface se existir
        update_interface_after_load()

        print("=== Carregamento de Gerenciamento Concluído ===")
        return True

    except Exception as e:
        print(f"Erro ao carregar tipo de gerenciamento: {e}")
        traceback.print_exc()
        return False


def salvar_configuracoes_gerenciamento():
    config_dir = get_config_directory()
    config_file = os.path.join(config_dir, "gerenciamento_config.json")

    try:
        print("\n=== Salvando Configurações de Gerenciamento ===")

        matriz = configuracoes_gerenciamentos["Ciclos"]["matriz_ciclos"]
        if not all(isinstance(linha, list) and len(linha) == 10 for linha in matriz):  # Atualizado
            raise ValueError("Formato inválido da matriz")

        dados = {
            "Ciclos": {
                "matriz_ciclos": [
                    [float(col) for col in linha]
                    for linha in matriz
                ],
                "linha_atual": configuracoes_gerenciamentos["Ciclos"]["linha_atual"],
                "coluna_atual": configuracoes_gerenciamentos["Ciclos"]["coluna_atual"],
                "modo_ataque_defesa": configuracoes_gerenciamentos["Ciclos"]["modo_ataque_defesa"],
                "alvo_lucro": configuracoes_gerenciamentos["Ciclos"]["alvo_lucro"],
                "lucro_inicial_ciclo": configuracoes_gerenciamentos["Ciclos"]["lucro_inicial_ciclo"],
                "linha_atual_repetindo": configuracoes_gerenciamentos["Ciclos"]["linha_atual_repetindo"]
            }
        }

        # Salva em arquivo temporário primeiro
        temp_file = os.path.join(config_dir, "temp_gerenciamento.json")
        with open(temp_file, 'w') as f:
            json.dump(dados, f, indent=2)

        # Move para arquivo final
        if os.path.exists(config_file):
            os.replace(config_file, config_file + ".bak")
        os.replace(temp_file, config_file)

        print("Configurações salvas:")
        print(f"Modo Ataque/Defesa: {dados['Ciclos']['modo_ataque_defesa']}")
        print(f"Alvo lucro: {dados['Ciclos']['alvo_lucro']}")
        print(f"Linha atual: {dados['Ciclos']['linha_atual']}")
        print("===============================")

    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
        traceback.print_exc()


def limpar_matriz():
    """Limpa a matriz garantindo uma matriz 10x10 com zeros"""
    try:
        config = configuracoes_gerenciamentos["Ciclos"]
        config["matriz_ciclos"] = [
            [0.0] * 10 for _ in range(10)  # Sempre cria matriz 10x10
        ]

        # Atualiza interface
        for linha in range(10):
            for coluna in range(10):
                if dpg.does_item_exist(f"ciclos_matriz_{linha}_{coluna}"):
                    dpg.set_value(f"ciclos_matriz_{linha}_{coluna}", 0.0)

        # Reset dos controles de posição
        config["linha_atual"] = 0
        config["coluna_atual"] = 0

        print("Matriz limpa")
        salvar_configuracoes_gerenciamento()

    except Exception as e:
        print(f"Erro ao limpar matriz: {e}")



def save_configurations():
    """Salva todas as configurações do bot incluindo traduções e visibilidade do antiloss"""
    global risco, total_operations, wins, payout, min_entry, STOP_WIN, STOP_LOSS
    global NumeroDeGales, tipo, style, numero_confluencias, simbolos_ativos
    global volatilidade_selecionada, velas_selecionadas, retracao_value, reversao_value
    global antiloss_ativado, required_losses, language_manager
    global modo_entrada, default_expiration, fim_da_vela_time, modo_gale
    global hedge_active, alvoresete, kicker_active, kicker_priority
    global pressao_compradora_min, pressao_vendedora_min, fluxo_active
    global price_action_active, volume_profile_active, modo_antiloss
    global abr_strategy_active, SequenciaMinima, SequenciaMaxima, Winrate
    global ml_strategy_active

    config_dir = get_config_directory()
    config_file = os.path.join(config_dir, "bot_config.json")

    try:
        # Converte valores traduzidos para valores base antes de salvar
        base_volatilidade = "Baixa" if volatilidade_selecionada == language_manager.get_text("BAIXA") else \
            "Media" if volatilidade_selecionada == language_manager.get_text("MEDIA") else "Alta"

        base_velas = "5 Velas" if velas_selecionadas == language_manager.get_text("5_VELAS") else \
            "10 Velas" if velas_selecionadas == language_manager.get_text("10_VELAS") else "20 Velas"

        # Obtém estado atual do toggle antiloss
        show_antiloss = False
        if dpg.does_item_exist("toggle_antiloss_visibility"):
            show_antiloss = dpg.get_item_user_data("toggle_antiloss_visibility")

        config = {
            "masaniello": {
                "risco": float(risco),
                "total_operations": int(total_operations),
                "wins": int(wins),
                "payout": float(payout),
                "min_entry": float(min_entry),
                "NumeroDeGales": int(NumeroDeGales),
                "tipo": int(tipo),
                "style": str(style)
            },

            "interface": {
                "language": language_manager.current_language,
                "show_antiloss_rows": show_antiloss
            },

            "stops": {
                "stop_win": float(STOP_WIN),
                "stop_loss": float(STOP_LOSS)
            },

            "estrategias": {
                "required_losses": int(required_losses),
                "numero_confluencias": int(numero_confluencias),
                "simbolos_ativos": simbolos_ativos,
                "volatilidade_selecionada": base_volatilidade,
                "velas_selecionadas": base_velas,
                "retracao_value": bool(retracao_value),
                "reversao_value": bool(reversao_value),
                "antiloss_ativado": bool(antiloss_ativado),
                "required_losses": int(required_losses),
                "abr_strategy": {
                    "active": bool(abr_strategy_active),
                    "sequencia_minima": int(SequenciaMinima),
                    "sequencia_maxima": int(SequenciaMaxima),
                    "winrate": int(Winrate)
                }
            },

            # Outras estratégias e configurações
            "outras_estrategias": {
                "hedge_active": bool(hedge_active),
                "alvoresete": bool(alvoresete),
                "kicker_active": bool(kicker_active),
                "kicker_priority": bool(kicker_priority),
                "pressao_compradora_min": float(pressao_compradora_min),
                "pressao_vendedora_min": float(pressao_vendedora_min),
                "fluxo_active": bool(fluxo_active),
                "price_action_active": bool(price_action_active),
                "volume_profile_active": bool(volume_profile_active),
                "modo_antiloss": str(modo_antiloss),
                "ml_strategy_active": bool(ml_strategy_active)
            },

            # Nova seção de modo de entrada
            "modo_entrada": {
                "tipo": modo_entrada,
                "expiracao": {
                    "tempo_fixo": default_expiration,
                    "fim_da_vela": fim_da_vela_time
                },
                "modo_gale": modo_gale
            }
        }

        print(f"\n💾 DEBUG save_configurations:")
        print(f"   Salvando modo_entrada: '{modo_entrada}'")
        print(f"   Salvando default_expiration: {default_expiration}")
        print(f"   Salvando fim_da_vela_time: '{fim_da_vela_time}'")
        print(f"   Salvando modo_gale: '{modo_gale}'")
        print(f"   Seção completa modo_entrada: {config['modo_entrada']}")
        print(f"💾 FIM DEBUG save\n")

        # Salva em arquivo temporário primeiro
        temp_file = os.path.join(config_dir, "temp_config.json")
        with open(temp_file, 'w') as arquivo:
            json.dump(config, arquivo, indent=2)

        # Move para arquivo final
        if os.path.exists(config_file):
            os.replace(config_file, config_file + ".bak")
        os.replace(temp_file, config_file)

        print("\n=== Configurações Salvas Com Sucesso ===")
        print(f"Idioma: {config['interface']['language']}")
        print(f"Mostrar linhas antiloss: {config['interface']['show_antiloss_rows']}")
        print(f"Modo de entrada: {modo_entrada}")
        
        if modo_entrada == "fim_da_vela":
            print(f"Timeframe (Fim da Vela): {fim_da_vela_time}")
        else:
            print(f"Expiração (Tempo Fixo): {default_expiration} minutos")
            
        print(f"Modo Gale: {modo_gale}")
        print("====================================")
        return True

    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
        traceback.print_exc()
        return False


def load_configurations():
    """Carrega todas as configurações do bot incluindo traduções e visibilidade do antiloss"""
    global risco, total_operations, wins, payout, min_entry, STOP_WIN, STOP_LOSS
    global NumeroDeGales, tipo, style, masaniello, numero_confluencias, simbolos_ativos
    global volatilidade_selecionada, velas_selecionadas, retracao_value, reversao_value
    global antiloss_ativado, required_losses, language_manager
    global modo_entrada, default_expiration, fim_da_vela_time, modo_gale
    global abr_strategy_active, SequenciaMinima, SequenciaMaxima, Winrate, abr_strategy
    global ml_strategy_active

    config_dir = get_config_directory()
    config_file = os.path.join(config_dir, "bot_config.json")

    try:
        if os.path.exists(config_file):
            with open(config_file, 'r') as arquivo:
                config = json.load(arquivo)

            # Carrega configurações do Masaniello
            m_config = config.get('masaniello', {})
            risco = float(m_config.get('risco', 35.0))
            total_operations = int(m_config.get('total_operations', 12))
            wins = int(m_config.get('wins', 3))
            payout = float(m_config.get('payout', 1.94))
            min_entry = float(m_config.get('min_entry', 0.35))
            NumeroDeGales = int(m_config.get('NumeroDeGales', 1))
            tipo = int(m_config.get('tipo', 1))
            style = str(m_config.get('style', "Normal"))

            # Carrega configurações de estratégias
            e_config = config.get('estrategias', {})
            required_losses = int(e_config.get('required_losses', 2))
            numero_confluencias = int(e_config.get('numero_confluencias', 1))
            simbolos_ativos.update(e_config.get('simbolos_ativos', {symbol: True for symbol in symbols}))

            # Carrega configurações ABR Strategy
            abr_config = e_config.get('abr_strategy', {})
            abr_strategy_active = bool(abr_config.get('active', False))
            SequenciaMinima = int(abr_config.get('sequencia_minima', 7))
            SequenciaMaxima = int(abr_config.get('sequencia_maxima', 13))
            Winrate = int(abr_config.get('winrate', 60))

            abr_strategy = ABRStrategy(
                min_sequence=SequenciaMinima,
                max_sequence=SequenciaMaxima,
                analysis_candles=400,
                min_success_rate=Winrate
            )

            if dpg.does_item_exist("abr_strategy_checkbox"):
                dpg.set_value("abr_strategy_checkbox", abr_strategy_active)
            if dpg.does_item_exist("sequencia_minima_input"):
                dpg.set_value("sequencia_minima_input", SequenciaMinima)
            if dpg.does_item_exist("sequencia_maxima_input"):
                dpg.set_value("sequencia_maxima_input", SequenciaMaxima)
            if dpg.does_item_exist("winrate_input"):
                dpg.set_value("winrate_input", Winrate)

            # Carrega configurações de interface
            i_config = config.get('interface', {})
            saved_language = i_config.get('language', 'pt')
            language_manager.set_language(saved_language)

            # Carrega configurações do modo de entrada
            entrada_config = config.get('modo_entrada', {})
            modo_entrada = entrada_config.get('tipo', 'tempo_fixo')
            modo_gale = entrada_config.get('modo_gale', 'normal')

            expiracoes = entrada_config.get('expiracao', {})
            default_expiration = expiracoes.get('tempo_fixo', 1)
            fim_da_vela_time = expiracoes.get('fim_da_vela', 'M1')

            # Carrega configurações de Stop Win/Loss
            stops_config = config.get('stops', {})
            STOP_WIN = float(stops_config.get('stop_win', 500.0))
            STOP_LOSS = float(stops_config.get('stop_loss', 300.0))

            # Carrega configurações de visibilidade do antiloss
            show_antiloss = i_config.get('show_antiloss_rows', False)

            # Aplica traduções aos valores
            base_volatilidade = str(e_config.get('volatilidade_selecionada', "Media"))
            volatilidade_selecionada = language_manager.get_text("BAIXA") if base_volatilidade == "Baixa" else \
                language_manager.get_text("MEDIA") if base_volatilidade == "Media" else \
                    language_manager.get_text("ALTA")

            base_velas = str(e_config.get('velas_selecionadas', "20 Velas"))
            velas_selecionadas = language_manager.get_text("5_VELAS") if base_velas == "5 Velas" else \
                language_manager.get_text("10_VELAS") if base_velas == "10 Velas" else \
                    language_manager.get_text("20_VELAS")

            retracao_value = bool(e_config.get('retracao_value', False))
            reversao_value = bool(e_config.get('reversao_value', False))
            antiloss_ativado = bool(e_config.get('antiloss_ativado', False))

            # Carrega outras configurações de estratégias
            outras_config = config.get('outras_estrategias', {})
            ml_strategy_active = bool(outras_config.get('ml_strategy_active', False))
            print(f"DEBUG load_configurations: ml_strategy_active carregado = {ml_strategy_active}")

            # Atualiza interface após carregar configurações
            update_interface_after_load()
            update_gui_language(dpg, language_manager)

            print("\n=== Configurações Carregadas ===")
            print(f"Idioma: {saved_language}")
            print(f"Mostrar linhas antiloss: {show_antiloss}")
            print(f"Modo de entrada: {modo_entrada}")
            print(f"Expiração Tempo Fixo: {default_expiration}")
            print(f"Timeframe Fim da Vela: {fim_da_vela_time}")
            print(f"Modo Gale: {modo_gale}")
            print("============================")

        else:
            print("Arquivo de configurações não encontrado. Usando valores padrão.")

    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        traceback.print_exc()


def restore_configs_after_language_change():
    """Restaura configurações após mudança de idioma"""
    try:
        # Recarrega configurações preservando valores
        load_configurations()

        # Atualiza interface com valores carregados
        update_interface_after_load()

        print("Configurações restauradas após mudança de idioma")

    except Exception as e:
        print(f"Erro ao restaurar configurações: {e}")
        traceback.print_exc()

def update_interface_after_load():
    """Atualiza todos os elementos da interface com as configurações carregadas"""
    try:
        # Atualiza interfaces do Masaniello
        if dpg.does_item_exist("risco_input"):
            dpg.set_value("risco_input", risco)
        if dpg.does_item_exist("total_operations_input"):
            dpg.set_value("total_operations_input", total_operations)
        if dpg.does_item_exist("wins_input"):
            dpg.set_value("wins_input", wins)
        if dpg.does_item_exist("payout_input"):
            dpg.set_value("payout_input", payout)
        if dpg.does_item_exist("min_entry_input"):
            dpg.set_value("min_entry_input", min_entry)
        if dpg.does_item_exist("stop_win_input"):
            dpg.set_value("stop_win_input", STOP_WIN)
        if dpg.does_item_exist("stop_loss_input"):
            dpg.set_value("stop_loss_input", STOP_LOSS)
        if dpg.does_item_exist("quant_gales"):
            dpg.set_value("quant_gales", NumeroDeGales)
        if dpg.does_item_exist("masaniello_type_selector"):
            dpg.set_value("masaniello_type_selector", "Normal" if tipo == 1 else "Progressivo")
        if dpg.does_item_exist("masaniello_style_selector"):
            dpg.set_value("masaniello_style_selector", style)

        # Atualiza interfaces da Estratégia
        if dpg.does_item_exist("numero_confluencias"):
            dpg.set_value("numero_confluencias", numero_confluencias)
        if dpg.does_item_exist("volatilidade_opcoes"):
            dpg.set_value("volatilidade_opcoes", volatilidade_selecionada)
        if dpg.does_item_exist("volatilidade_opcoes1"):
            dpg.set_value("volatilidade_opcoes1", velas_selecionadas)
        if dpg.does_item_exist("retracao_value"):
            dpg.set_value("retracao_value", retracao_value)
        if dpg.does_item_exist("reversao_value"):
            dpg.set_value("reversao_value", reversao_value)
        if dpg.does_item_exist("antiloss_value"):
            dpg.set_value("antiloss_value", antiloss_ativado)
        if dpg.does_item_exist("required_losses_input"):
            dpg.set_value("required_losses_input", required_losses)

        if dpg.does_item_exist("expiration_selector"):
            print(f"\n🖥️ DEBUG update_interface_after_load:")
            print(f"   modo_entrada: '{modo_entrada}'")
            print(f"   default_expiration: {default_expiration}")
            print(f"   fim_da_vela_time: '{fim_da_vela_time}'")
            
            if modo_entrada == "fim_da_vela":
                # Configura para timeframes e define o valor atual
                timeframe_value = fim_da_vela_time.replace("M", "") if fim_da_vela_time.startswith("M") else fim_da_vela_time
                print(f"   timeframe_value extraído: '{timeframe_value}'")
                dpg.configure_item("expiration_selector", items=["1", "5", "15", "30"])
                dpg.set_value("expiration_selector", timeframe_value)
                print(f"   ✅ Interface configurada para Fim da Vela com valor: {timeframe_value}")
            else:
                # Configura para expirações e define o valor atual
                dpg.configure_item("expiration_selector", items=["1", "2", "3", "4", "5", "10", "15", "30"])
                dpg.set_value("expiration_selector", str(default_expiration))
                print(f"   ✅ Interface configurada para Tempo Fixo com valor: {default_expiration}")
            print(f"🖥️ FIM DEBUG interface\n")

        # Atualiza controles de modo de entrada
        if dpg.does_item_exist("modo_entrada_radio"):
            entrada_texto = "Fim da Vela" if modo_entrada == "fim_da_vela" else "Tempo Fixo"
            dpg.set_value("modo_entrada_radio", entrada_texto)

        # Atualiza combo de timeframe para Fim da Vela
        if dpg.does_item_exist("timeframe_combo"):
            if modo_entrada == "fim_da_vela":
                dpg.set_value("timeframe_combo", fim_da_vela_time)

        # Atualiza modo de gale se existir
        if dpg.does_item_exist("modo_gale_radio"):
            gale_texto = "Agressivo" if modo_gale == "agressivo" else "Normal"
            dpg.set_value("modo_gale_radio", gale_texto)

        # Atualiza outras estratégias se existirem
        if dpg.does_item_exist("hedge_checkbox"):
            dpg.set_value("hedge_checkbox", hedge_active)
        if dpg.does_item_exist("alvoresete_checkbox"):
            dpg.set_value("alvoresete_checkbox", alvoresete)
        if dpg.does_item_exist("kicker_checkbox"):
            dpg.set_value("kicker_checkbox", kicker_active)
        if dpg.does_item_exist("fluxo_checkbox"):
            dpg.set_value("fluxo_checkbox", fluxo_active)
        if dpg.does_item_exist("price_action_checkbox"):
            dpg.set_value("price_action_checkbox", price_action_active)
        if dpg.does_item_exist("volume_profile_checkbox"):
            dpg.set_value("volume_profile_checkbox", volume_profile_active)

        # Atualiza configurações ABR Strategy
        if dpg.does_item_exist("abr_strategy_checkbox"):
            dpg.set_value("abr_strategy_checkbox", abr_strategy_active)
        if dpg.does_item_exist("sequencia_minima_input"):
            dpg.set_value("sequencia_minima_input", SequenciaMinima)
        if dpg.does_item_exist("sequencia_maxima_input"):
            dpg.set_value("sequencia_maxima_input", SequenciaMaxima)
        if dpg.does_item_exist("winrate_input"):
            dpg.set_value("winrate_input", Winrate)

        # Atualiza configurações ML Strategy
        if dpg.does_item_exist("ml_strategy_checkbox"):
            print(f"DEBUG update_interface_after_load: Atualizando ml_strategy_checkbox para {ml_strategy_active}")
            dpg.set_value("ml_strategy_checkbox", ml_strategy_active)
            # Confirma se o valor foi aplicado
            current_value = dpg.get_value("ml_strategy_checkbox")
            print(f"DEBUG update_interface_after_load: Valor atual do checkbox após set_value: {current_value}")

        # Atualiza checkboxes dos símbolos
        for symbol in symbols:
            if dpg.does_item_exist(f"checkbox_{symbol}"):
                dpg.set_value(f"checkbox_{symbol}", simbolos_ativos.get(symbol, True))

        print("Interface atualizada com as configuracoes carregadas")
        print(f"Modo de entrada atualizado: {modo_entrada}")
        print(f"Timeframe atualizado: {fim_da_vela_time}")
        print(f"Expiração atualizada: {default_expiration}")
        print(f"Modo gale atualizado: {modo_gale}")

    except Exception as e:
        print(f"Erro ao atualizar interface: {e}")
        import traceback
        traceback.print_exc()


def submit_masaniello_settings():
    """Função para salvar configurações do Masaniello e Stop Win/Loss"""
    global risco, total_operations, wins, payout, min_entry, STOP_WIN, STOP_LOSS, masaniello, NumeroDeGales, tipo, style

    try:
        # Verifica se o bot está em execução
        if is_running or should_send_orders:
            if dpg.does_item_exist("masaniello_warning"):
                dpg.delete_item("masaniello_warning")

            with dpg.window(label=language_manager.get_text("AVISO"), modal=True, no_close=True,
                            tag="masaniello_warning", width=450, height=200):
                dpg.add_text(language_manager.get_text("DICA_CONFIGURACOES"))
                dpg.add_text("1. " + language_manager.get_text("PARAR_BOT"))
                dpg.add_text("2. " + language_manager.get_text("RESETAR_BOT"))
                dpg.add_text("3. " + language_manager.get_text("FAZER_ALTERACOES"))
                dpg.add_separator()
                dpg.add_button(label="OK", callback=lambda: dpg.delete_item("masaniello_warning"), width=100)


        # Captura o tipo de gerenciamento selecionado
        gerenciamento_ativo = dpg.get_value("gerenciamento_selector")

        # Captura os valores de Stop Win/Loss da nova aba com validação
        try:
            novo_stop_win = float(dpg.get_value("stop_win_input"))
            novo_stop_loss = float(dpg.get_value("stop_loss_input"))

            # Validação dos valores de stop
            if novo_stop_win <= 0:
                raise ValueError("Stop Win deve ser maior que zero")
            if novo_stop_loss <= 0:
                raise ValueError("Stop Loss deve ser maior que zero")

        except ValueError as error:
            print(f"Erro nos valores de Stop: {error}")
            return

        if gerenciamento_ativo == "Masaniello":
            # Captura os valores do Masaniello com validação
            try:
                novo_risco = float(dpg.get_value("risco_input"))
                novo_total_operations = int(dpg.get_value("total_operations_input"))
                novo_wins = int(dpg.get_value("wins_input"))
                novo_payout = float(dpg.get_value("payout_input"))
                novo_min_entry = float(dpg.get_value("min_entry_input"))
                novo_gales = int(dpg.get_value("quant_gales"))
                novo_tipo = 1 if dpg.get_value("masaniello_type_selector") == "Normal" else 0
                novo_style = dpg.get_value("masaniello_style_selector")

                # Validações específicas do Masaniello
                if novo_total_operations < 1:
                    raise ValueError("Total de operações deve ser maior que zero")
                if novo_wins < 1:
                    raise ValueError("Número de wins deve ser maior que zero")
                if novo_min_entry <= 0:
                    raise ValueError("Entrada mínima deve ser maior que zero")
                if novo_risco <= 0:
                    raise ValueError("Risco deve ser maior que zero")
                if novo_payout <= 1:
                    raise ValueError("Payout deve ser maior que 1")
                if novo_gales < 0:
                    raise ValueError("Número de gales não pode ser negativo")

                # Atualiza variáveis globais do Masaniello
                risco = novo_risco
                total_operations = novo_total_operations
                wins = novo_wins
                payout = novo_payout
                min_entry = novo_min_entry
                NumeroDeGales = novo_gales
                tipo = novo_tipo
                style = novo_style

                # Atualiza objeto Masaniello
                masaniello = MasanielloAPI(risco, total_operations, wins, payout, min_entry, tipo, style)

                print("\n=== Configurações Masaniello Atualizadas ===")
                print(f"Risco: ${risco:.2f}")
                print(f"Total Operações: {total_operations}")
                print(f"Wins: {wins}")
                print(f"Payout: {payout:.2f}")
                print(f"Min Entry: ${min_entry:.2f}")
                print(f"Gales: {NumeroDeGales}")
                print(f"Tipo: {'Normal' if tipo == 1 else 'Progressivo'}")
                print(f"Style: {style}")

            except ValueError as error:
                print(f"Erro nas configurações do Masaniello: {error}")
                return

        else:
            # Se não for Masaniello, salva configurações dos Ciclos
            salvar_configuracoes_gerenciamento()

        # Atualiza Stop Win/Loss globais
        STOP_WIN = novo_stop_win
        STOP_LOSS = novo_stop_loss

        print("\n=== Configurações de Stop Atualizadas ===")
        print(f"Stop Win: ${STOP_WIN:.2f}")
        print(f"Stop Loss: ${STOP_LOSS:.2f}")

        # Salva todas as configurações
        save_configurations()

        # Fecha a janela de configurações
        close_settings_window()

        print("Todas as configurações foram salvas com sucesso!")

    except Exception as error:
        print(f"Erro ao atualizar configurações: {error}")
        import traceback
        traceback.print_exc()


def close_settings_window():
    if dpg.does_item_exist("settings_window"):
        dpg.delete_item("settings_window")
    else:
        print("Settings window not found. It may have been already closed.")


def salvar_matriz():
    """Salva os valores atuais da matriz"""
    try:
        # Atualiza a matriz com os valores atuais da interface
        for linha in range(10):
            for coluna in range(10):
                tag = f"ciclos_matriz_{linha}_{coluna}"
                if dpg.does_item_exist(tag):
                    valor = dpg.get_value(tag)
                    configuracoes_gerenciamentos["Ciclos"]["matriz_ciclos"][linha][coluna] = float(valor)

        # Salva as configurações
        salvar_configuracoes_gerenciamento()

        print("Matriz salva com sucesso!")

    except Exception as e:
        print(f"Erro ao salvar matriz: {e}")
        import traceback
        traceback.print_exc()


def save_telegram_settings():
    """Salva as configurações do Telegram"""
    global telegram_ativado, chat_id_value, bot_token, required_losses

    config_dir = get_config_directory()
    telegram_file = os.path.join(config_dir, "telegram_config.json")

    try:
        # Pega os valores atuais da interface
        current_chat_id = dpg.get_value("chat_id_input")
        current_telegram_status = dpg.get_value("telegram_ativado_checkbox")

        config = {
            "chat_id": current_chat_id,
            "telegram_ativado": current_telegram_status,
            "bot_token": bot_token,
            "required_losses": required_losses
        }

        # Atualiza as variáveis globais
        chat_id_value = current_chat_id
        telegram_ativado = current_telegram_status

        # Salva em arquivo temporário primeiro
        temp_file = os.path.join(config_dir, "temp_telegram.json")
        with open(temp_file, 'w') as f:
            json.dump(config, f, indent=2)

        # Faz backup e move arquivo final
        if os.path.exists(telegram_file):
            os.replace(telegram_file, telegram_file + ".bak")
        os.replace(temp_file, telegram_file)

        print("\n=== Configurações do Telegram salvas ===")
        print(f"Chat ID: {chat_id_value}")
        print(f"Telegram ativado: {telegram_ativado}")
        print(f"Required losses: {required_losses}")
        if dpg.does_item_exist("telegram_settings"):
            dpg.delete_item("telegram_settings")
        return True
    except Exception as e:
        print(f"Erro ao salvar configurações do Telegram: {e}")
        import traceback
        traceback.print_exc()
        return False


def load_telegram_settings():
    """Carrega as configuracoes do Telegram"""
    global chat_id_value, telegram_ativado, bot_token
    config_dir = get_config_directory()
    telegram_file = os.path.join(config_dir, "telegram_config.json")
    try:
        # Tenta ler arquivo principal
        if os.path.exists(telegram_file):
            with open(telegram_file, 'r') as f:
                config = json.load(f)
        # Se falhar, tenta backup
        elif os.path.exists(telegram_file + ".bak"):
            with open(telegram_file + ".bak", 'r') as f:
                config = json.load(f)
        else:
            print("Arquivo de configuracoes do Telegram nao encontrado. Usando valores padrao.")
            chat_id_value = ""
            telegram_ativado = False
            return

        chat_id_value = config.get("chat_id", "")
        telegram_ativado = config.get("telegram_ativado", False)
        bot_token = config.get("bot_token", "")

        print("Configuracoes do Telegram carregadas com sucesso.")
        print(f"Chat ID carregado: {chat_id_value}")
        print(f"Telegram ativado: {telegram_ativado}")

        # Atualiza interface grafica
        if dpg.does_item_exist("chat_id_input"):
            dpg.set_value("chat_id_input", chat_id_value)
        if dpg.does_item_exist("telegram_ativado_checkbox"):
            dpg.set_value("telegram_ativado_checkbox", telegram_ativado)

    except Exception as e:
        print(f"Erro ao carregar configuracoes do Telegram: {e}")
        chat_id_value = ""
        telegram_ativado = False


def open_telegram_settings():
    """Opens Telegram settings window with language support and bot link"""
    global telegram_ativado, chat_id_value

    telegram_ativado = bool(telegram_ativado)

    # Remove existing window if present
    if dpg.does_item_exist("telegram_settings"):
        dpg.delete_item("telegram_settings")

    # Calculate window position
    viewport_width = dpg.get_viewport_client_width()
    viewport_height = dpg.get_viewport_client_height()
    window_width = 380
    window_height = 400
    pos_x = (viewport_width - window_width) // 2
    pos_y = (viewport_height - window_height) // 2

    with dpg.window(label=language_manager.get_text("CONFIG_TELEGRAM_TITULO"),
                    tag="telegram_settings",
                    width=window_width,
                    height=window_height,
                    no_resize=True,
                    no_collapse=True,
                    pos=[pos_x, pos_y]):

        # Instructions Header
        dpg.add_spacer(height=10)
        dpg.add_text(language_manager.get_text("INSTRUCOES_TELEGRAM"),
                     color=(255, 255, 0),
                     tag="instrucoes_telegram_text")

        # Instructions
        dpg.add_text(language_manager.get_text("INSTRUCAO_1"),
                     tag="instrucao_1_text",
                     wrap=360)
        dpg.add_text(language_manager.get_text("INSTRUCAO_2"),
                     tag="instrucao_2_text",
                     wrap=360)
        dpg.add_text(language_manager.get_text("INSTRUCAO_3"),
                     tag="instrucao_3_text",
                     wrap=360)
        dpg.add_text(language_manager.get_text("INSTRUCAO_4"),
                     tag="instrucao_4_text",
                     wrap=360)

        dpg.add_spacer(height=10)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        # Telegram Bot Button with icon
        image_path = resource_path("tele.png")
        with dpg.group(horizontal=True):
            if os.path.exists(image_path):
                width, height, channels, data = dpg.load_image(image_path)
                with dpg.texture_registry():
                    texture_id = dpg.add_static_texture(width, height, data)
                dpg.add_image(texture_id, width=23, height=23)

            dpg.add_button(
                label=language_manager.get_text("IR_PARA_BOT"),
                callback=lambda: webbrowser.open("https://t.me/FenixTradingg_Bot"),
                tag="ir_para_bot_button",
                width=-1
            )

        dpg.add_spacer(height=20)

        # Chat ID Input
        dpg.add_text(language_manager.get_text("CHAT_ID"),
                     tag="chat_id_label")
        dpg.add_input_text(tag="chat_id_input",
                           default_value=chat_id_value,
                           width=-1)

        dpg.add_spacer(height=10)

        # Enable Telegram Checkbox
        dpg.add_checkbox(
            label=language_manager.get_text("ATIVAR_TELEGRAM"),
            tag="telegram_ativado_checkbox",
            default_value=telegram_ativado,
            callback=toggle_telegram
        )

        dpg.add_spacer(height=20)

        # Save/Cancel Buttons
        with dpg.group(horizontal=True):
            # Calculate button widths to fill the space
            button_width = (window_width - 50) // 2

            dpg.add_button(
                label=language_manager.get_text("SALVAR"),
                width=button_width,
                height=30,
                callback=save_telegram_settings,
                tag="telegram_save_button"
            )

            dpg.add_spacer(width=10)

            dpg.add_button(
                label=language_manager.get_text("CANCELAR"),
                width=button_width,
                height=30,
                callback=lambda: dpg.delete_item("telegram_settings"),
                tag="telegram_cancel_button"
            )

    # Apply custom theme
    with dpg.theme() as theme_telegram:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (30, 30, 30))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (70, 70, 70))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 100, 100))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (120, 120, 120))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (140, 140, 140))
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 15, 15)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 4)
            dpg.add_theme_style(dpg.mvStyleVar_ButtonTextAlign, 0.5)

    dpg.bind_item_theme("telegram_settings", theme_telegram)


def toggle_antiloss_rows(sender, app_data):
    """Alterna a visibilidade das linhas de antiloss na tabela e o ícone do botão"""
    try:
        # Obtém estado atual do toggle (inicia como False)
        current_state = dpg.get_item_user_data(sender)
        if current_state is None:  # Se é a primeira vez, define como False
            current_state = False

        # Inverte o estado
        new_state = not current_state

        print(f"\n=== Alternando visibilidade ===")
        print(f"Estado anterior: {current_state}")
        print(f"Novo estado: {new_state}")

        # Define qual ícone usar
        image_path = resource_path("visivel.png" if new_state else "invisivel.png")

        # Carrega e aplica a nova imagem
        if os.path.exists(image_path):
            width, height, channels, data = dpg.load_image(image_path)
            with dpg.texture_registry():
                texture_id = dpg.add_static_texture(width, height, data)

            # Obtém o parent do botão atual
            parent = dpg.get_item_parent(sender)

            # Remove o botão antigo
            dpg.delete_item(sender)

            # Cria o novo botão
            new_button = dpg.add_image_button(
                texture_id,
                width=23,
                height=23,
                callback=toggle_antiloss_rows,
                tag="toggle_antiloss_visibility",
                parent=parent
            )

            # Define o novo estado
            dpg.set_item_user_data(new_button, new_state)

            # Recria a tooltip
            with dpg.tooltip(new_button):
                dpg.add_text("Mostrar/Ocultar Linhas Antiloss")

            # Atualiza visibilidade das linhas
            rows = dpg.get_item_children("transactions_table", 1)
            if rows:
                for row in rows:
                    if dpg.get_item_user_data(row) == "antiloss_row":
                        if new_state:
                            dpg.show_item(row)
                        else:
                            dpg.hide_item(row)

            print(f"✅ Visibilidade alterada com sucesso")
            print(f"📌 Linhas de antiloss: {'visíveis' if new_state else 'ocultas'}")
            print(f"📌 Ícone atualizado para: {'visível' if new_state else 'invisível'}")

    except Exception as e:
        print(f"❌ Erro ao alternar visibilidade: {e}")
        import traceback
        traceback.print_exc()


def update_gui_language(dpg, language_manager):
    """Atualiza todos os elementos da interface com o novo idioma"""
    try:

        if dpg.does_item_exist("volatilidade_opcoes"):
            current_lang = language_manager.current_language
            if current_lang == "en":
                items = ["Low", "Medium", "High"]
            elif current_lang == "es":
                items = ["Baja", "Media", "Alta"]
            else:  # pt
                items = ["Baixa", "Media", "Alta"]
            dpg.configure_item("volatilidade_opcoes", items=items)

        # Atualiza headers da tabela
        if dpg.does_item_exist("transactions_table"):
            headers = [
                ("col_hora_abertura", "HORA_ABERTURA"),
                ("col_hora_fechamento", "HORA_FECHAMENTO"),
                ("col_tipo_sinal", "TIPO_SINAL"),
                ("col_entrada", "ENTRADA"),
                ("col_paridades", "PARIDADES"),
                ("col_gales", "GALES"),
                ("col_direcao", "DIRECAO"),
                ("col_duracao", "DURACAO"),
                ("col_wl", "W_L"),
                ("col_comentarios", "COMENTARIOS")
            ]

            for tag, key in headers:
                if dpg.does_item_exist(tag):
                    dpg.configure_item(tag, label=language_manager.get_text(key))

        # Atualiza textos principais
        text_items = [
            ("saldo_label", "SALDO_ATUAL"),
            ("lucro_label", "LUCRO_ATUAL"),
            ("wins_label", "WINS"),
            ("losses_label", "LOSSES"),
            ("winrate_label", "WINRATE"),
            ("hora_atual_label", "HORA_ATUAL"),
            ("bot_status_text", "BOT_PRONTO")
        ]

        for tag, key in text_items:
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, language_manager.get_text(key))

        # Atualiza tooltips dos botões
        tooltips = [
            ("login_tooltip", "INSERIR_TOKENS"),
            ("config_tooltip", "CONFIGURACOES_BOT"),
            ("stats_tooltip", "ESTATISTICAS"),
            ("telegram_tooltip", "CONFIG_TELEGRAM"),
            ("reset_tooltip", "RESET_COMPLETO")
        ]

        for tag, key in tooltips:
            if dpg.does_item_exist(tag):
                dpg.set_value(tag, language_manager.get_text(key))

        print(f"Interface atualizada para o idioma: {language_manager.current_language}")

    except Exception as e:
        print(f"Erro ao atualizar interface: {e}")
        import traceback
        traceback.print_exc()



def update_header_elements(dpg, language_manager):
    try:

        if dpg.does_item_exist("preset_ciclos_normal_window"):
            dpg.configure_item("preset_ciclos_normal_window",
                               label=language_manager.get_text("CICLOS_NORMAL"))

        if dpg.does_item_exist("selecione_ciclo_normal_text"):
            dpg.set_value("selecione_ciclo_normal_text",
                          language_manager.get_text("SELECIONE_CICLO_NORMAL"))

            # Atualiza para grupos G1 e G2 dos ciclos NORMAL
        for grupo in ["G1", "G2"]:
            grupo_tag = f"ciclos_grupo_{grupo}_text"
            if dpg.does_item_exist(grupo_tag):
                dpg.set_value(grupo_tag,
                              f"{language_manager.get_text('CICLOS_DE')} {grupo}")

            # Atualiza cada ciclo do grupo NORMAL
            for ciclo in ["CICLO 1", "CICLO 2", "CICLO 3", "CICLO 4"]:
                base_tag = f"ciclo_{grupo}_{ciclo}"

                # Atualiza botão
                button_tag = f"{base_tag}_button"
                if dpg.does_item_exist(button_tag):
                    current_label = dpg.get_item_label(button_tag)
                    perfil = current_label.split(" - ")[1].split(" (")[0]
                    risco = current_label.split("$ ")[1].rstrip(")")
                    new_label = f"{ciclo} - {language_manager.get_text(perfil)} ($ {risco})"
                    dpg.configure_item(button_tag, label=new_label)

                # Atualiza textos do grupo NORMAL
                perfil_tag = f"perfil_{base_tag}"
                if dpg.does_item_exist(perfil_tag):
                    dpg.set_value(perfil_tag,
                                  f"{language_manager.get_text('PERFIL')}: {language_manager.get_text(perfil)}")

                estrategia_tag = f"estrategia_{base_tag}"
                if dpg.does_item_exist(estrategia_tag):
                    dpg.set_value(estrategia_tag,
                                  f"{language_manager.get_text('ESTRATEGIA')}: {language_manager.get_text('BALANCEADO')}")

                entrada_tag = f"entrada_{base_tag}"
                if dpg.does_item_exist(entrada_tag):
                    current_text = dpg.get_value(entrada_tag)
                    valores = current_text.split("$ ")[1:]
                    dpg.set_value(entrada_tag,
                                  f"{language_manager.get_text('ENTRADA')}: $ {valores[0]} | {language_manager.get_text('MAIOR')}: $ {valores[1]}")

                recomendado_tag = f"recomendado_{base_tag}"
                if dpg.does_item_exist(recomendado_tag):
                    current_text = dpg.get_value(recomendado_tag)
                    recomendacao = current_text.split(": ")[1]
                    dpg.set_value(recomendado_tag,
                                  f"{language_manager.get_text('RECOMENDADO')}: {language_manager.get_text(recomendacao)}")

            # Atualiza textos de dicas do ciclo NORMAL
        if dpg.does_item_exist("info_ciclo_window"):
            dpg.configure_item("info_ciclo_window",
                               label=language_manager.get_text("DICAS_CICLO"))

            if dpg.does_item_exist("gales_ciclo_text"):
                dpg.set_value("gales_ciclo_text",
                              f"{language_manager.get_text('GALES_DO_CICLO')}: {gerenciamento}")

            if dpg.does_item_exist("risco_total_ciclo_text"):
                dpg.set_value("risco_total_ciclo_text",
                              f"{language_manager.get_text('RISCO_TOTAL')}:")

            if dpg.does_item_exist("take_profit_text"):
                dpg.set_value("take_profit_text",
                              f"{language_manager.get_text('TAKE_PROFIT_SUGERIDO')}:")

            if dpg.does_item_exist("tp_conservador_text"):
                current_value = dpg.get_value("tp_conservador_text").split("$ ")[1]
                dpg.set_value("tp_conservador_text",
                              f"{language_manager.get_text('CONSERVADOR')}: $ {current_value}")

            if dpg.does_item_exist("tp_moderado_text"):
                current_value = dpg.get_value("tp_moderado_text").split("$ ")[1]
                dpg.set_value("tp_moderado_text",
                              f"{language_manager.get_text('MODERADO')}: $ {current_value}")

            if dpg.does_item_exist("tp_agressivo_text"):
                current_value = dpg.get_value("tp_agressivo_text").split("$ ")[1]
                dpg.set_value("tp_agressivo_text",
                              f"{language_manager.get_text('AGRESSIVO')}: $ {current_value}")

        if dpg.does_item_exist("telegram_settings"):
            dpg.configure_item("telegram_settings", label=language_manager.get_text("CONFIG_TELEGRAM_TITULO"))

            # Atualiza textos das instruções
            if dpg.does_item_exist("instrucoes_telegram_text"):
                dpg.set_value("instrucoes_telegram_text", language_manager.get_text("INSTRUCOES_TELEGRAM"))

            # Atualiza os textos das instruções individuais
            for i in range(1, 5):
                if dpg.does_item_exist(f"instrucao_{i}_text"):
                    dpg.set_value(f"instrucao_{i}_text", language_manager.get_text(f"INSTRUCAO_{i}"))

            # Atualiza texto do chat ID
            if dpg.does_item_exist("chat_id_label"):
                dpg.set_value("chat_id_label", language_manager.get_text("CHAT_ID"))

            # Atualiza checkbox do Telegram
            if dpg.does_item_exist("telegram_ativado_checkbox"):
                dpg.configure_item("telegram_ativado_checkbox", label=language_manager.get_text("ATIVAR_TELEGRAM"))

            # Atualiza botão ir para bot
            if dpg.does_item_exist("ir_para_bot_button"):
                dpg.configure_item("ir_para_bot_button", label=language_manager.get_text("IR_PARA_BOT"))

            # Atualiza botões salvar e cancelar
            if dpg.does_item_exist("telegram_save_button"):
                dpg.configure_item("telegram_save_button", label=language_manager.get_text("SALVAR"))
            if dpg.does_item_exist("telegram_cancel_button"):
                dpg.configure_item("telegram_cancel_button", label=language_manager.get_text("CANCELAR"))

        if dpg.does_item_exist("preset_ciclos_step_window"):
            dpg.configure_item("preset_ciclos_step_window",
                               label=language_manager.get_text("CICLOS_STEP"))

        if dpg.does_item_exist("selecione_ciclo_step_text"):
            dpg.set_value("selecione_ciclo_step_text",
                          language_manager.get_text("SELECIONE_CICLO_STEP"))

            # Atualiza textos dos grupos
        for grupo in ["G1", "G2", "G3"]:
            grupo_tag = f"ciclos_grupo_{grupo}_text"
            if dpg.does_item_exist(grupo_tag):
                dpg.set_value(grupo_tag,
                              f"{language_manager.get_text('CICLOS_DE')} {grupo}")

            # Atualiza cada ciclo do grupo
            for ciclo in ["CICLO 1", "CICLO 2", "CICLO 3", "CICLO 4"]:
                base_tag = f"ciclo_{grupo}_{ciclo}"

                # Atualiza botão
                button_tag = f"{base_tag}_button"
                if dpg.does_item_exist(button_tag):
                    current_label = dpg.get_item_label(button_tag)
                    perfil = current_label.split(" - ")[1].split(" (")[0]
                    risco = current_label.split("$ ")[1].rstrip(")")
                    new_label = f"{ciclo} - {language_manager.get_text(perfil)} ($ {risco})"
                    dpg.configure_item(button_tag, label=new_label)

                # Atualiza textos do grupo
                perfil_tag = f"perfil_{base_tag}"
                if dpg.does_item_exist(perfil_tag):
                    dpg.set_value(perfil_tag,
                                  f"{language_manager.get_text('PERFIL')}: {language_manager.get_text(perfil)}")

                estrategia_tag = f"estrategia_{base_tag}"
                if dpg.does_item_exist(estrategia_tag):
                    dpg.set_value(estrategia_tag,
                                  f"{language_manager.get_text('ESTRATEGIA')}: {language_manager.get_text('BALANCEADO')}")

                entrada_tag = f"entrada_{base_tag}"
                if dpg.does_item_exist(entrada_tag):
                    current_text = dpg.get_value(entrada_tag)
                    valores = current_text.split("$ ")[1:]
                    dpg.set_value(entrada_tag,
                                  f"{language_manager.get_text('ENTRADA')}: $ {valores[0]} | {language_manager.get_text('MAIOR')}: $ {valores[1]}")

                recomendado_tag = f"recomendado_{base_tag}"
                if dpg.does_item_exist(recomendado_tag):
                    current_text = dpg.get_value(recomendado_tag)
                    recomendacao = current_text.split(": ")[1]
                    dpg.set_value(recomendado_tag,
                                  f"{language_manager.get_text('RECOMENDADO')}: {language_manager.get_text(recomendacao)}")


        if dpg.does_item_exist("volatilidade_opcoes"):
            current_lang = language_manager.current_language
            if current_lang == "en":
                items = ["Low", "Medium", "High"]
                # Mapeia valor atual para novo idioma
                current_value = dpg.get_value("volatilidade_opcoes")
                value_map = {"Baixa": "Low", "Media": "Medium", "Alta": "High"}
                new_value = value_map.get(current_value, "Medium")
                dpg.configure_item("volatilidade_opcoes", items=items)
                dpg.set_value("volatilidade_opcoes", new_value)
            elif current_lang == "es":
                items = ["Baja", "Media", "Alta"]
                current_value = dpg.get_value("volatilidade_opcoes")
                value_map = {"Baixa": "Baja", "Media": "Media", "Alta": "Alta"}
                new_value = value_map.get(current_value, "Media")
                dpg.configure_item("volatilidade_opcoes", items=items)
                dpg.set_value("volatilidade_opcoes", new_value)
            else:  # pt
                items = ["Baixa", "Media", "Alta"]
                current_value = dpg.get_value("volatilidade_opcoes")
                value_map = {"Low": "Baixa", "Medium": "Media", "High": "Alta",
                             "Baja": "Baixa", "Media": "Media", "Alta": "Alta"}
                new_value = value_map.get(current_value, "Media")
                dpg.configure_item("volatilidade_opcoes", items=items)
                dpg.set_value("volatilidade_opcoes", new_value)

            # Atualiza combo de número de velas
        if dpg.does_item_exist("volatilidade_opcoes1"):
            current_lang = language_manager.current_language
            if current_lang == "en":
                items = ["5 Candles", "10 Candles", "20 Candles"]
                current_value = dpg.get_value("volatilidade_opcoes1")
                value_map = {"5 Velas": "5 Candles", "10 Velas": "10 Candles", "20 Velas": "20 Candles"}
                new_value = value_map.get(current_value, "20 Candles")
                dpg.configure_item("volatilidade_opcoes1", items=items)
                dpg.set_value("volatilidade_opcoes1", new_value)
            else:  # pt e es
                items = ["5 Velas", "10 Velas", "20 Velas"]
                current_value = dpg.get_value("volatilidade_opcoes1")
                value_map = {"5 Candles": "5 Velas", "10 Candles": "10 Velas", "20 Candles": "20 Velas"}
                new_value = value_map.get(current_value, "20 Velas")
                dpg.configure_item("volatilidade_opcoes1", items=items)
                dpg.set_value("volatilidade_opcoes1", new_value)



        if dpg.does_item_exist("antiloss_tooltip_static"):
            dpg.set_value("antiloss_tooltip_static", language_manager.get_text("TOGGLE_ANTILOSS"))


        if dpg.does_item_exist("idiomatext"):
            dpg.set_value("idiomatext", language_manager.get_text("IDIOMA_TEXT"))

        if dpg.does_item_exist("verificando_atualizacoes_text"):
            dpg.set_value("verificando_atualizacoes_text", language_manager.get_text("VERIFICANDO_ATUALIZACOES"))

        if dpg.does_item_exist("sem_resposta_servidor_text"):
            dpg.set_value("sem_resposta_servidor_text", language_manager.get_text("SEM_RESPOSTA_SERVIDOR"))

        if dpg.does_item_exist("atualizacoes_software_text"):
            dpg.set_value("atualizacoes_software_text", language_manager.get_text("ATUALIZACOES_SOFTWARE"))

        if dpg.does_item_exist("maintenance_text"):
            dpg.set_value("maintenance_text", language_manager.get_text("SISTEMA_EM_MANUTENCAO"))

        if dpg.does_item_exist("welcome_text"):
            dpg.set_value("welcome_text", language_manager.get_text("BEM_VINDO_BINARY_BOT"))

        if dpg.does_item_exist("timer_text"):
            dpg.set_value("timer_text", language_manager.get_text("LOGANDO_FECHAR_SEGUNDOS"))

        if dpg.does_item_exist("presets_ciclos_ad_text"):
            dpg.set_value("presets_ciclos_ad_text", language_manager.get_text("PRESETS_CICLOS_AD"))

        if dpg.does_item_exist("presets_step_seguro_button"):
            dpg.configure_item("presets_step_seguro_button", label=language_manager.get_text("PRESETS_STEP_SEGURO"))

        if dpg.does_item_exist("presets_normal_moderado_button"):
            dpg.configure_item("presets_normal_moderado_button",
                               label=language_manager.get_text("PRESETS_NORMAL_MODERADO"))

        if dpg.does_item_exist("modo_ciclos_text"):
            dpg.set_value("modo_ciclos_text", language_manager.get_text("MODO_CICLOS"))

        if dpg.does_item_exist("checkbox_ataque_defesa"):
            dpg.configure_item("checkbox_ataque_defesa", label=language_manager.get_text("MODO_AD"))

        if dpg.does_item_exist("input_alvo_lucro"):
            dpg.configure_item("input_alvo_lucro", label=language_manager.get_text("ALVO_LUCRO"))

        for linha in range(10):
            if dpg.does_item_exist(f"linha_{linha}_text"):
                dpg.set_value(f"linha_{linha}_text", f"{language_manager.get_text('LINHA')} {linha + 1}")

        if dpg.does_item_exist("limpar_matriz_button"):
            dpg.configure_item("limpar_matriz_button", label=language_manager.get_text("LIMPAR_MATRIZ"))

        if dpg.does_item_exist("salvar_matriz_button"):
            dpg.configure_item("salvar_matriz_button", label=language_manager.get_text("SALVAR_MATRIZ"))

        if dpg.does_item_exist("instrucoes_ad_title"):
            dpg.set_value("instrucoes_ad_title", language_manager.get_text("MODO_AD") + ":")

        if dpg.does_item_exist("instrucao_ad_1"):
            dpg.set_value("instrucao_ad_1", "- " + language_manager.get_text("INSTRUCAO_AD_1"))

        if dpg.does_item_exist("instrucao_ad_2"):
            dpg.set_value("instrucao_ad_2", "- " + language_manager.get_text("INSTRUCAO_AD_2"))

        if dpg.does_item_exist("instrucao_ad_3"):
            dpg.set_value("instrucao_ad_3", "- " + language_manager.get_text("INSTRUCAO_AD_3"))

        if dpg.does_item_exist("instrucao_ad_4"):
            dpg.set_value("instrucao_ad_4", "- " + language_manager.get_text("INSTRUCAO_AD_4"))

        if dpg.does_item_exist("preset_ciclos_step_window"):
            dpg.configure_item("preset_ciclos_step_window", label=language_manager.get_text("CICLOS_STEP"))

        if dpg.does_item_exist("selecione_ciclo_step_text"):
            dpg.set_value("selecione_ciclo_step_text", language_manager.get_text("SELECIONE_CICLO_STEP"))

        if dpg.does_item_exist("5_ciclos_g1_43_16_button"):
            dpg.configure_item("5_ciclos_g1_43_16_button", label=language_manager.get_text("5_CICLOS_G1_43_16"))

        if dpg.does_item_exist("5_ciclos_g1_26_97_button"):
            dpg.configure_item("5_ciclos_g1_26_97_button", label=language_manager.get_text("5_CICLOS_G1_26_97"))

        if dpg.does_item_exist("5_ciclos_g1_54_12_button"):
            dpg.configure_item("5_ciclos_g1_54_12_button", label=language_manager.get_text("5_CICLOS_G1_54_12"))

        if dpg.does_item_exist("5_ciclos_g1_38_60_button"):
            dpg.configure_item("5_ciclos_g1_38_60_button", label=language_manager.get_text("5_CICLOS_G1_38_60"))

        if dpg.does_item_exist("4_ciclos_g2_49_97_button"):
            dpg.configure_item("4_ciclos_g2_49_97_button", label=language_manager.get_text("4_CICLOS_G2_49_97"))

        if dpg.does_item_exist("4_ciclos_g2_31_53_button"):
            dpg.configure_item("4_ciclos_g2_31_53_button", label=language_manager.get_text("4_CICLOS_G2_31_53"))

        if dpg.does_item_exist("4_ciclos_g2_62_00_button"):
            dpg.configure_item("4_ciclos_g2_62_00_button", label=language_manager.get_text("4_CICLOS_G2_62_00"))

        if dpg.does_item_exist("4_ciclos_g2_44_38_button"):
            dpg.configure_item("4_ciclos_g2_44_38_button", label=language_manager.get_text("4_CICLOS_G2_44_38"))

        if dpg.does_item_exist("4_ciclos_g3_123_85_button"):
            dpg.configure_item("4_ciclos_g3_123_85_button", label=language_manager.get_text("4_CICLOS_G3_123_85"))

        if dpg.does_item_exist("4_ciclos_g3_70_30_button"):
            dpg.configure_item("4_ciclos_g3_70_30_button", label=language_manager.get_text("4_CICLOS_G3_70_30"))

        if dpg.does_item_exist("4_ciclos_g3_161_23_button"):
            dpg.configure_item("4_ciclos_g3_161_23_button", label=language_manager.get_text("4_CICLOS_G3_161_23"))

        if dpg.does_item_exist("4_ciclos_g3_107_16_button"):
            dpg.configure_item("4_ciclos_g3_107_16_button", label=language_manager.get_text("4_CICLOS_G3_107_16"))

        if dpg.does_item_exist("risco_total_text_step"):
            dpg.set_value("risco_total_text_step", language_manager.get_text("RISCO_TOTAL_STEP"))

        if dpg.does_item_exist("logar_button"):
            dpg.configure_item("logar_button", label=language_manager.get_text("LOGAR"))

        if dpg.does_item_exist("saldo_atual_text"):
            dpg.set_value("saldo_atual_text", language_manager.get_text("SALDO_ATUAL"))

        if dpg.does_item_exist("lucro_atual_text"):
            dpg.set_value("lucro_atual_text", language_manager.get_text("LUCRO_ATUAL"))

        if dpg.does_item_exist("clock_text"):
            dpg.set_value("clock_text", language_manager.get_text("HORA_ATUAL"))

        if dpg.does_item_exist("inserirtokens"):
            dpg.set_value("inserirtokens", language_manager.get_text("INSERIR_TOKENS"))

        if dpg.does_item_exist("configtext"):
            dpg.set_value("configtext", language_manager.get_text("CONFIGURACOES_BOT"))

        if dpg.does_item_exist("estatisiticatext"):
            dpg.set_value("estatisiticatext", language_manager.get_text("ESTATISTICAS"))



        if dpg.does_item_exist("telegramtext"):
            dpg.set_value("telegramtext", language_manager.get_text("CONFIG_TELEGRAM"))

        if dpg.does_item_exist("tutorialtext"):
            dpg.set_value("tutorialtext", language_manager.get_text("VIDEO_TUTORIAL"))

        if dpg.does_item_exist("sitetext"):
            dpg.set_value("sitetext", language_manager.get_text("ACESSAR_SITE"))

        if dpg.does_item_exist("atualizacaotext"):
            dpg.set_value("atualizacaotext", language_manager.get_text("VERIFICAR_ATUALIZACOES"))

        if dpg.does_item_exist("connectortext"):
            dpg.set_value("connectortext", language_manager.get_text("BAIXAR_CONECTORES"))

        if dpg.does_item_exist("resettext"):
            dpg.set_value("resettext", language_manager.get_text("RESET_COMPLETO"))

        if dpg.does_item_exist("antlosstext"):
            dpg.set_value("antlosstext", language_manager.get_text("TOGGLE_ANTILOSS"))

        if dpg.does_item_exist("lucrotext"):
            dpg.set_value("lucrotext", language_manager.get_text("RESETAR_LUCRO"))

        if dpg.does_item_exist("settings_window"):
            dpg.configure_item("settings_window", label=language_manager.get_text("CONFIGURACOES"))

        if dpg.does_item_exist("estrategias_tab"):
            dpg.configure_item("estrategias_tab", label=language_manager.get_text("ESTRATEGIAS"))

        if dpg.does_item_exist("confluencias_text"):
            dpg.set_value("confluencias_text", language_manager.get_text("CONFLUENCIAS"))

        if dpg.does_item_exist("numero_confluencias"):
            dpg.configure_item("numero_confluencias", label=language_manager.get_text("NUMERO_CONFLUENCIAS"))

        if dpg.does_item_exist("filtrostext"):
            dpg.set_value("filtrostext", language_manager.get_text("FILTROS_BOT"))

        if dpg.does_item_exist("price_action_checkbox"):
            dpg.configure_item("price_action_checkbox", label=language_manager.get_text("PRICE_ACTION"))

        if dpg.does_item_exist("volume_profile_checkbox"):
            dpg.configure_item("volume_profile_checkbox", label=language_manager.get_text("VOLUME_PROFILE"))

        if dpg.does_item_exist("fluxotext"):
            dpg.set_value("fluxotext", language_manager.get_text("FLUXO_BOT"))

        if dpg.does_item_exist("fluxo_value"):
            dpg.configure_item("fluxo_value", label=language_manager.get_text("ATIVA_FLUXO"))

        if dpg.does_item_exist("kicker_active"):
            dpg.configure_item("kicker_active", label=language_manager.get_text("ATIVA_GAP"))

        if dpg.does_item_exist("pressao_compradora_slider"):
            dpg.configure_item("pressao_compradora_slider", label=language_manager.get_text("PRESSAO_COMPRADORA"))

        if dpg.does_item_exist("pressao_vendedora_slider"):
            dpg.configure_item("pressao_vendedora_slider", label=language_manager.get_text("PRESSAO_VENDEDORA"))

        if dpg.does_item_exist("valores_recomendados_text"):
            dpg.set_value("valores_recomendados_text", language_manager.get_text("VALORES_RECOMENDADOS"))

        if dpg.does_item_exist("estrategias_padroes_text"):
            dpg.set_value("estrategias_padroes_text", language_manager.get_text("ESTRATEGIAS_PADROES"))

        if dpg.does_item_exist("retracao_value"):
            dpg.configure_item("retracao_value", label=language_manager.get_text("ATIVAR_RETRACAO"))

        if dpg.does_item_exist("reversao_value"):
            dpg.configure_item("reversao_value", label=language_manager.get_text("ATIVAR_REVERSAO"))

        if dpg.does_item_exist("antiloss_value"):
            dpg.configure_item("antiloss_value", label=language_manager.get_text("ATIVAR_ANTILOSS"))

        if dpg.does_item_exist("modo_antiloss_combo"):
            dpg.configure_item("modo_antiloss_combo", label=language_manager.get_text("MODO_ANTILOSS"))
            dpg.configure_item("modo_antiloss_combo",
                               items=[language_manager.get_text("GLOBAL"), language_manager.get_text("RESTRITO")])

        if dpg.does_item_exist("required_losses_input"):
            dpg.configure_item("required_losses_input", label=language_manager.get_text("QTD_ANTLOSS"))

        if dpg.does_item_exist("volatilidade_text"):
            dpg.set_value("volatilidade_text", language_manager.get_text("VOLATILIDADE"))

        if dpg.does_item_exist("volatilidade_opcoes"):
            dpg.configure_item("volatilidade_opcoes",
                               items=[language_manager.get_text("BAIXA"), language_manager.get_text("MEDIA"),
                                      language_manager.get_text("ALTA")])

        if dpg.does_item_exist("volatilidade_opcoes1"):
            dpg.configure_item("volatilidade_opcoes1",
                               items=[language_manager.get_text("5_VELAS"), language_manager.get_text("10_VELAS"),
                                      language_manager.get_text("20_VELAS")])

        if dpg.does_item_exist("selecione_pares_text"):
            dpg.set_value("selecione_pares_text", language_manager.get_text("SELECIONE_PARES"))

        if dpg.does_item_exist("gerenciamento_tab"):
            dpg.configure_item("gerenciamento_tab", label=language_manager.get_text("GENCIAMENTO"))

        if dpg.does_item_exist("tipo_gerenciamento_text"):
            dpg.set_value("tipo_gerenciamento_text", language_manager.get_text("TIPO_GERENCIAMENTO"))

        if dpg.does_item_exist("gerenciamento_selector"):
            dpg.configure_item("gerenciamento_selector", label=language_manager.get_text("SELECIONE_GERENCIAMENTO"))
            dpg.configure_item("gerenciamento_selector",
                               items=[language_manager.get_text("MASANIELLO"), language_manager.get_text("CICLOS")])

        if dpg.does_item_exist("risco_input"):
            dpg.configure_item("risco_input", label=language_manager.get_text("RISCO"))

        if dpg.does_item_exist("total_operations_input"):
            dpg.configure_item("total_operations_input", label=language_manager.get_text("TOTAL_OPERACOES"))

        if dpg.does_item_exist("wins_input"):
            dpg.configure_item("wins_input", label=language_manager.get_text("NUMERO_WINS"))

        if dpg.does_item_exist("payout_input"):
            dpg.configure_item("payout_input", label=language_manager.get_text("PAYOUT"))

        if dpg.does_item_exist("min_entry_input"):
            dpg.configure_item("min_entry_input", label=language_manager.get_text("MIN_ENTRADA"))

        if dpg.does_item_exist("quant_gales"):
            dpg.configure_item("quant_gales", label=language_manager.get_text("QTD_GALES"))

        if dpg.does_item_exist("masaniello_type_selector"):
            dpg.configure_item("masaniello_type_selector", label=language_manager.get_text("TIPO_MASANIELLO"))
            dpg.configure_item("masaniello_type_selector",
                               items=[language_manager.get_text("NORMAL"), language_manager.get_text("PROGRESSIVO")])

        if dpg.does_item_exist("masaniello_style_selector"):
            dpg.configure_item("masaniello_style_selector", label=language_manager.get_text("ESTILO_MASANIELLO"))

        if dpg.does_item_exist("stop_win_stop_loss_tab"):
            dpg.configure_item("stop_win_stop_loss_tab", label=language_manager.get_text("STOP_WIN_STOP_LOSS"))

        if dpg.does_item_exist("stop_win_input"):
            dpg.configure_item("stop_win_input", label=language_manager.get_text("STOP_WIN"))

        if dpg.does_item_exist("stop_loss_input"):
            dpg.configure_item("stop_loss_input", label=language_manager.get_text("STOP_LOSS"))

        if dpg.does_item_exist("salvar_button"):
            dpg.configure_item("salvar_button", label=language_manager.get_text("SALVAR"))

        if dpg.does_item_exist("cancelar_button"):
            dpg.configure_item("cancelar_button", label=language_manager.get_text("CANCELAR"))

        if dpg.does_item_exist("gerenciamentotext"):
            dpg.configure_item("gerenciamentotext", label=language_manager.get_text("GERENCIAMENTO"))

        if dpg.does_item_exist("togggleiniciartext"):
            dpg.configure_item("togggleiniciartext", label=language_manager.get_text("INICIAR"))

        if dpg.does_item_exist("botpausadotext"):
            dpg.set_value("botpausadotext", language_manager.get_text("BOT_PAUSADO"))

        if dpg.does_item_exist("stopwinatingidotext"):
            dpg.set_value("stopwinatingidotext", language_manager.get_text("STOP_WIN_ATINGIDO"))

        if dpg.does_item_exist("stoplossatingidotext"):
            dpg.set_value("stoplossatingidotext", language_manager.get_text("STOP_LOSS_ATINGIDO"))

        if dpg.does_item_exist("horaatualtext"):
            dpg.set_value("horaatualtext", language_manager.get_text("HORA_ATUAL"))

        if dpg.does_item_exist("lucroatualtext"):
            dpg.set_value("lucroatualtext", language_manager.get_text("LUCRO_ATUAL"))

        if dpg.does_item_exist("estatisticastext"):
            dpg.set_value("estatisticastext", language_manager.get_text("ESTATISTICAS"))

        if dpg.does_item_exist("winstext"):
            dpg.set_value("winstext", language_manager.get_text("WINS"))

        if dpg.does_item_exist("lossestext"):
            dpg.set_value("lossestext", language_manager.get_text("LOSSES"))

        if dpg.does_item_exist("winratetext"):
            dpg.set_value("winratetext", language_manager.get_text("WINRATE"))

        if dpg.does_item_exist("saldoatualtext"):
            dpg.set_value("saldoatualtext", language_manager.get_text("SALDO_ATUAL"))

        if dpg.does_item_exist("saldoatual2text"):
            dpg.set_value("saldoatual2text", language_manager.get_text("SALDO_ATUAL"))

        if dpg.does_item_exist("metalucroatingidatext"):
            dpg.set_value("metalucroatingidatext", language_manager.get_text("META_LUCRO_ATINGIDA"))

        if dpg.does_item_exist("horaatual2text"):
            dpg.set_value("horaatual2text", language_manager.get_text("HORA_ATUAL"))

        if dpg.does_item_exist("perdatotaltext"):
            dpg.set_value("perdatotaltext", language_manager.get_text("PERDA_TOTAL"))

        if dpg.does_item_exist("estatisticas2text"):
            dpg.set_value("estatisticas2text", language_manager.get_text("ESTATISTICAS"))



        if dpg.does_item_exist("saldoatual3text"):
            dpg.set_value("saldoatual3text", language_manager.get_text("SALDO_ATUAL"))

        if dpg.does_item_exist("saldoatual4text"):
            dpg.set_value("saldoatual4text", language_manager.get_text("SALDO_ATUAL"))

        if dpg.does_item_exist("limiteperdaatingidotext"):
            dpg.set_value("limiteperdaatingidotext", language_manager.get_text("LIMITE_PERDA_ATINGIDO"))

        if dpg.does_item_exist("operacoesencarradastext"):
            dpg.set_value("operacoesencarradastext", language_manager.get_text("OPERACOES_ENCERRADAS"))

        if dpg.does_item_exist("stopwinoulosstabletext"):
            dpg.set_value("stopwinoulosstabletext", language_manager.get_text("STOP_WIN_ATINGIDO"))

    except Exception as e:
        print(f"Erro ao atualizar elementos do cabeçalho: {e}")

def create_gui():
    print("Iniciando GUI...")
    global language_manager
    language_manager = LanguageManager()
    load_all_configurations()
    load_transactions()
    load_gerenciamento_tipo()
    telegram_interface = TelegramInterface()
    telegram_manager = telegram_interface.get_telegram_manager()

    start_clock_update()

    def on_exit(sender, app_data, user_data):
        cleanup()
        dpg.stop_dearpygui()

    try:
        dpg.create_context()
        carregar_tokens_ao_iniciar()
        default_font = setup_fonts()
        aplicar_tema_moderno()
        criar_login_required_popup()
        dpg.hide_item("login_required_popup")


        with dpg.theme() as custom_green_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (76, 175, 80))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (56, 142, 60))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (46, 125, 50))

        with dpg.theme() as custom_martingale_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (30, 144, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (24, 116, 205))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (16, 78, 139))

        while dpg.is_dearpygui_running():
            # Process any pending group refreshes
            check_telegram_refresh()

            # Render frame
            dpg.render_dearpygui_frame()

        # Janela principal
        with dpg.window(label=language_manager.get_text("BINARY_BOT"), width=980, height=700, tag="main_window",
                        no_resize=True, no_close=True, no_title_bar=True):

            # Grupo superior com todos os botões
            with dpg.group(horizontal=True):


                # Botão Login
                image_path = resource_path("login.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    login_button = dpg.add_image_button(texture_id, width=23, height=23, callback=abrir_popup_token)
                    with dpg.tooltip(login_button):
                        dpg.add_text(language_manager.get_text("INSERIR_TOKENS"),tag="inserirtokens")



                image_path = resource_path("play.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    login_button = dpg.add_image_button(texture_id, width=23, height=23, callback=toggle_bot, tag="toggle_button")
                    with dpg.tooltip(login_button):
                        dpg.add_text(language_manager.get_text("START"))

                # Botão Configurações
                image_path = resource_path("eng.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    settings_button = dpg.add_image_button(texture_id, width=23, height=23,
                                                           callback=open_settings_window)
                    with dpg.tooltip(settings_button):
                        dpg.add_text(language_manager.get_text("CONFIGURACOES_BOT"),tag="configtext")

                # Botão Estatísticas
                image_path = resource_path("esta.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    stats_button = dpg.add_image_button(texture_id, width=23, height=23,
                                                        callback=open_statistics_window)
                    with dpg.tooltip(stats_button):
                        dpg.add_text(language_manager.get_text("ESTATISTICAS"),tag="estatisiticatext")


                # Botão Telegram
                image_path = resource_path("tele.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    telegram_button = dpg.add_image_button(texture_id, width=23, height=23,
                                                           callback=open_telegram_settings)
                    with dpg.tooltip(telegram_button):
                        dpg.add_text(language_manager.get_text("CONFIG_TELEGRAM"),tag="telegramtext")

                # Botão Tutorial
                image_path = resource_path("video.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    tutorial_button = dpg.add_image_button(texture_id, width=23, height=23, callback=open_youtube_video)
                    with dpg.tooltip(tutorial_button):
                        dpg.add_text(language_manager.get_text("VIDEO_TUTORIAL"),tag="tutorialtext")


                # Botão Atualização
                image_path = resource_path("att.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    update_button = dpg.add_image_button(
                        texture_id,
                        width=25,
                        height=25,
                        callback=lambda: threading.Thread(target=update_manager.verificar_atualizacoes_manual()).start()
                    )
                    with dpg.tooltip(update_button):
                        dpg.add_text(language_manager.get_text("VERIFICAR_ATUALIZACOES"),tag="atualizacaotext")

                # Botão Conectores
                image_path = resource_path("dd.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    connector_button = dpg.add_image_button(texture_id, width=23, height=23,
                                                            callback=download_connector)
                    with dpg.tooltip(connector_button):
                        dpg.add_text(language_manager.get_text("BAIXAR_CONECTORES"),tag="connectortext")

                # Botão Reset
                image_path = resource_path("res.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    reset_button = dpg.add_image_button(texture_id, width=23, height=23, callback=reset_bot)
                    with dpg.tooltip(reset_button):
                        dpg.add_text(language_manager.get_text("RESET_COMPLETO"),tag="resettext")

                language_button = create_language_button()
                if language_button is not None:
                    with dpg.theme() as button_theme:
                        with dpg.theme_component(dpg.mvAll):
                            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)
                    dpg.bind_item_theme(language_button, button_theme)

                image_path = resource_path("telesinais.png")  # Adicione um ícone apropriado
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    telegram_signals_button = dpg.add_image_button(
                        texture_id,
                        width=23,
                        height=23,
                        callback=telegram_interface.open_telegram_signal_settings
                        # Aqui mudou para usar o método da classe
                    )
                    with dpg.tooltip(telegram_signals_button):
                        dpg.add_text("Configurar Sinais Telegram")


                # Visibility toggle button
                image_path = resource_path("invisivel.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)
                    antiloss_button = dpg.add_image_button(
                        texture_id,
                        width=23,
                        height=23,
                        callback=toggle_antiloss_rows,
                        tag="toggle_antiloss_visibility"
                    )
                    dpg.set_item_user_data(antiloss_button, False)
                    with dpg.tooltip(antiloss_button, tag="antiloss_tooltip_parent"):
                        dpg.add_text(language_manager.get_text("TOGGLE_ANTILOSS"),tag="antiloss_tooltip_static")





            # Informações principais
            dpg.add_spacer(width=80)
            dpg.add_text(language_manager.get_text("CONEXAO_SUCESSO"), tag="success_message", show=False,
                         color=(0, 255, 0))

            with dpg.group(horizontal=True):
                # Seletor Demo/Real
                dpg.add_combo(
                    items=["Demo", "Real"],
                    default_value="Demo",
                    tag="token_mode",
                    width=100,
                    callback=on_account_change
                )
                dpg.disable_item("token_mode")

                # Botão Logar
                dpg.add_button(
                    label=language_manager.get_text("LOGAR"),
                    callback=login_wrapper,
                    tag="logar_button"
                )
                dpg.bind_item_theme(dpg.last_item(), custom_green_theme)

                # Informações de Saldo e Lucro
                dpg.add_spacer(width=1)
                dpg.add_text(
                    language_manager.get_text("SALDO_ATUAL"),
                    color=(0, 255, 255),
                    wrap=100,
                    tag="saldo_atual_text"
                )




                dpg.add_text("$ 0.00", tag="saldo_text", color=(255, 255, 255))
                dpg.add_spacer(width=455)

                image_path = resource_path("resetlucro.png")
                if os.path.exists(image_path):
                    width, height, channels, data = dpg.load_image(image_path)
                    with dpg.texture_registry():
                        texture_id = dpg.add_static_texture(width, height, data)

                    # Criar tema transparente para o botão
                    with dpg.theme() as transparent_button_theme:
                        with dpg.theme_component(dpg.mvImageButton):
                            dpg.add_theme_color(dpg.mvThemeCol_Button,
                                                (30, 30, 30, 0))  # Cor do fundo do bot com alpha 0
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (30, 30, 30, 0))  # Mesmo para hover
                            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (30, 30, 30, 0))  # Mesmo para click
                            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0)
                            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 0, 0)
                            dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 0)

                    button = dpg.add_image_button(
                        texture_id,
                        width=18,
                        height=18,
                        callback=resetarlucro,
                        tag="resetlucro_button"
                    )

                    # Aplicar o tema transparente ao botão
                    dpg.bind_item_theme(button, transparent_button_theme)

                    with dpg.tooltip(button):
                        dpg.add_text("Reset Lucro/Profit", tag="resetlucro_tooltip_text")


                dpg.add_text(
                    language_manager.get_text("LUCRO_ATUAL"),
                    color=(0, 255, 255),
                    wrap=100,
                    tag="lucro_atual_text"
                )
                dpg.add_text("$ 0.00", tag="pnl_text", color=(255, 255, 255))

            # Tabela de transações
            if default_font:
                dpg.bind_font(default_font)
            create_transactions_table()

            # Rodapé
            with dpg.group(horizontal=True, height=20, tag="footer_group"):
                dpg.add_spacer(width=10)
                dpg.add_text(language_manager.get_text("HORA_ATUAL"), tag="clock_text", color=(255, 255, 255))
                dpg.add_text("00:00:00", tag="clock_tex", color=(255, 255, 255))
                dpg.add_spacer(width=80)
                dpg.add_text(language_manager.get_text("WINS"), color=(0, 255, 0), wrap=100)
                dpg.add_text("0", tag="wins_text", color=(0, 255, 0))
                dpg.add_spacer(width=100)
                dpg.add_text(language_manager.get_text("LOSSES"), color=(255, 0, 0), wrap=100)
                dpg.add_text("0", tag="losses_text", color=(255, 0, 0))
                dpg.add_spacer(width=100)
                dpg.add_text(language_manager.get_text("WINRATE"), color=(0, 191, 255), wrap=100)
                dpg.add_text("0%", tag="winrate_text", color=(0, 191, 255))
                dpg.add_spacer(width=130)
                dpg.add_text(language_manager.get_text("CARREGANDO"), tag="bot_status_text")

        # Configuração da viewport
        dpg.create_viewport(title='BINARY ELITE', width=980, height=700, decorated=True)
        dpg.set_viewport_max_width(980)
        dpg.set_viewport_min_width(980)
        dpg.set_viewport_max_height(700)
        dpg.set_viewport_min_height(700)
        dpg.set_viewport_resizable(False)

        # Configurar ícone
        icon_path = resource_path("fnx.ico")
        if os.path.exists(icon_path):
            dpg.set_viewport_small_icon(icon_path)
            dpg.set_viewport_large_icon(icon_path)
            print("Ícone configurado com sucesso!")
        else:
            print(f"Ícone não encontrado no caminho: {icon_path}")

        dpg.show_viewport()
        dpg.bind_item_theme("main_window", custom_martingale_theme)
        dpg.setup_dearpygui()
        dpg.set_viewport_resize_callback(on_resize)
        dpg.set_primary_window("main_window", True)
        dpg.set_exit_callback(on_exit)

        # Iniciar threads e loops assíncronos
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Iniciar thread para o loop assíncrono
        threading.Thread(target=lambda: asyncio.run(start_bot()), daemon=True).start()

        # Iniciar DearPyGui
        dpg.start_dearpygui()
        update_interface_after_load()
        start_update_check_thread()
        print("GUI iniciada com sucesso.")

    except Exception as e:
        print(f"Erro na execução da GUI: {e}")
        import traceback
        traceback.print_exc()
    finally:
        dpg.destroy_context()



def on_resize(sender, app_data):
    # Get the current viewport width and height
    viewport_width, viewport_height = dpg.get_viewport_client_width(), dpg.get_viewport_client_height()

    # Set the main window size to always match the viewport
    dpg.set_item_width("main_window", viewport_width)
    dpg.set_item_height("main_window", viewport_height)

    # Ensure the footer stays fixed at the bottom
    margin_from_bottom = 20
    footer_height = 10  # Ajuste conforme o tamanho real do rodapé
    footer_y = viewport_height - footer_height - margin_from_bottom

    # Set the footer to stay at the bottom of the window
    dpg.set_item_pos("footer_group", [10, footer_y])

    # Adjust the height of the transactions table to fit above the footer
    table_max_height = footer_y - 100  # Ajuste conforme o espaço disponível acima do rodapé
    dpg.set_item_height("transactions_table", table_max_height)

    # Ative a barra de rolagem na tabela quando exceder a altura máxima
    dpg.configure_item("transactions_table", scrollY=True)


def update_gui_state(is_running):
    """Atualiza o estado da interface gráfica"""
    global should_send_orders
    try:
        if is_running:
            should_send_orders = True
            dpg.configure_item("toggle_button", label="PARAR")
            update_button_image("toggle_button", "parar.png")
            dpg.set_value("bot_status_text", f"BINARY ELITE BOT V{CURRENT_VERSION}")
            controlar_seletor_ativo(False)
            print("Interface atualizada - Bot em execução")
        else:
            should_send_orders = False
            dpg.configure_item("toggle_button", label="INICIAR")
            update_button_image("toggle_button", "play.png")
            dpg.set_value("bot_status_text", "Bot Pausado")
            controlar_seletor_ativo(True)
            print("Interface atualizada - Bot pausado")

    except Exception as e:
        print(f"Erro ao atualizar interface: {e}")
        import traceback
        traceback.print_exc()
    update_status()

def is_connected(self):
    """Verifica se o cliente está conectado"""
    return self.client is not None and self.client.is_connected()

def cleanup():
    global is_shutting_down, websocket_client, is_running, stop_event, api
    global row_id, gales, total_wins, total_losses

    for process in multiprocessing.active_children():
        process.terminate()
        process.join(timeout=2.0)

    print("Iniciando limpeza...")
    is_shutting_down = True
    is_running = False
    stop_event.set()
    if mt4_receiver:
        mt4_receiver.stop()
    # Fechar o WebSocket
    if websocket_client:
        try:
            websocket_client.close()
        except Exception as e:
            print(f"Aviso ao fechar WebSocket durante limpeza: {e}")
        websocket_client = None

    if telegram_client:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
            loop.run_until_complete(telegram_client.disconnect())
            telegram_client = None
            print("Cliente Telegram desconectado")
        except Exception as e:
            print(f"Erro ao desconectar Telegram: {e}")

        # Fechar Telegram Manager
    if telegram_manager:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
            loop.run_until_complete(telegram_manager.stop())
            telegram_manager = None
            print("Gerenciador Telegram parado")
        except Exception as e:
            print(f"Erro ao parar gerenciador Telegram: {e}")

    # Cancelar todas as tarefas pendentes
    loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(loop):
        task.cancel()

    # Reiniciar os valores globais
    row_id = None
    gales = 0
    total_wins = 0
    total_losses = 0

    # Encerrar todas as threads em execução
    for thread in threading.enumerate():
        if thread != threading.main_thread():
            try:
                thread.join(timeout=2.0)
            except Exception as e:
                print(f"Erro ao encerrar thread: {e}")

    # Realizar logout da API
    if 'api' in globals() and api is not None:
        try:
            loop.run_until_complete(api.logout())
        except Exception as e:
            print(f"Erro ao fazer logout da API: {e}")

    # Salvar transações e outras informações importantes
    save_transactions()

    print("Limpeza concluída. Encerrando o programa.")
    dpg.destroy_context()
    sys.exit(0)

if __name__ == "__main__":
    def signal_handler(signum, frame):
        cleanup()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    load_transactions()

    create_gui()
