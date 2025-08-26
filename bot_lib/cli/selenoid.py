import requests
from bot_lib.common.colorama_print import print_with_color_tags
import sys
import os 

def listar_sessoes():
    moon_host     = os.getenv("MOON_HOST")
    try:
        response = requests.get(f"{moon_host}/status")
        response.raise_for_status()
        status_data = response.json()
        return list(status_data.get("sessions", []).keys())
    except Exception as e:
        print_with_color_tags(f"<bg_red>Erro ao listar sessões</bg_red>")
        sys.exit(1)

def deletar_sessao(session_id):
    moon_host     = os.getenv("MOON_HOST")
    try:
        resp = requests.delete(f"{moon_host}/wd/hub/session/{session_id}")
        print_with_color_tags(f"<bg_green>Removendo sessão {session_id}: {resp.status_code}</bg_green>")
    except Exception as e:
        print_with_color_tags(f"<bg_red>Erro ao remover sessão {session_id}: {e}</bg_red>")

def deletar_todas():
    sessao_ids = listar_sessoes()
    if not sessao_ids:
        return print_with_color_tags(f"<black><bg_white>Nenhuma sessão ativa encontrada</bg_white></black>")

    print_with_color_tags(f"<bg_blue>{len(sessao_ids)} sessões encontradas. Iniciando remoção...</bg_blue>")
    for session_id in sessao_ids:
        deletar_sessao(session_id)

