import subprocess
from pathlib import Path
import sys
import os
from bot_lib.common.colorama_print import print_with_color_tags
from .portainer import *
from bot_lib.settings import botConfig
from bot_lib.libs import Task,show_config,show_tasks
from .common import get_git_remote_url,get_current_git_ref
import re
from sys import argv

def botlib_commands():
    print_with_color_tags(f"<black><bg_white>{'-'*50} COMMANDS </bg_white></black>")
    
    print("gitup",'\t\t','<comment>','\t','ATUALIZA O REPOSITORIO DO GIT') 
    print("upreq",'\t\t','','\t\t','ATUALIZA O REQUIREMENTS DA VENV ATUAL')
    print("setupy",'\t\t','','\t\t','CRIA A VENV, ATUALIZA O PIP, INSTALA OS REQUIREMENTS')
    print("createstack",'\t\t','','\t','CRIA A STACK NO PORTAINER')
    print("redeploy",'\t\t','','\t','DA UM REDEPLOY NA STACK DO PORTAINER')
    print("runprd",'\t\t','','\t\t','RODA O ROBO EM PRODUCAO')
    print("runprdstream",'\t','<task>','\t','RODA O ROBO EM PRODUCAO E MOSTRA OS LOGS EM TEMPO REAL')
    pass

def existe_venv():
    for d in os.listdir():
        if os.path.isdir(d) and os.path.exists(os.path.join(d, "bin" if os.name != "nt" else "Scripts", "activate")):
            return d
    return None

def get_python_exe_path_in_venv(project_path=None):
    # Se o projeto não for especificado, use o diretório atual
    if project_path is None:
        project_path = os.path.join(os.getcwd(),existe_venv())

 
    # Verifica se a pasta "Scripts" (Windows) ou "bin" (Linux/Mac) existe dentro do diretório do projeto
    if os.name == 'nt':  # Para Windows
        venv_path = os.path.join(project_path, 'Scripts', 'python.exe')
    else:  # Para Linux/Mac
        venv_path = os.path.join(project_path, 'bin', 'python')

    # Verifica se o arquivo python.exe ou python existe no caminho
    if os.path.exists(venv_path):
        return venv_path
    else:
        return None  # Caso não encontre

def venv_ativa():
    return bool(os.environ.get("VIRTUAL_ENV"))

def setupy():
    if venv_ativa():
        return print_with_color_tags(f"<bg_red>{'*'*20} SAIA DA VENV ATUAL PARA CRIAR UMA NOVA {'*'*20}</bg_red>")
    if existe_venv() and 0:
        print_with_color_tags(f"<bg_red>{'*'*50} VENV JA EXISTE {'*'*50}</bg_red>")
    else:
        print_with_color_tags(f"<bg_green>{'-'*50} CRIANDO VENV </bg_green>")
        os.system(r"python -m venv venv")
        print()
        print_with_color_tags(f"<bg_blue>{'-'*50} ATUALIZANDO PIP </bg_blue>")
        upgrade_pip()
        print_with_color_tags(f"<bg_cyan>{'-'*50} INSTALANDO REQUIREMENTS </bg_cyan>")
        upreq()

def gitup():
    print_with_color_tags(f"<black><bg_white>{'-'*50} ATUALIZANDO GIT </bg_white></black>")
    comment = sys.argv[1] if len(sys.argv) >1 else 'Update'
    subprocess.run(['git', 'add', '.'],             cwd=os.getcwd(), check=True)
    # Verifica se há algo para commitar
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=os.getcwd())
    if result.returncode == 0:
        return print_with_color_tags(f"<black><bg_green>NENHUMA MUDANCA PARA COMITAR</bg_green></black>")
    subprocess.run(['git', 'commit', '-m',comment], cwd=os.getcwd(), check=True)
    subprocess.run(['git', 'push'],                 cwd=os.getcwd(), check=True)

def upreq():
    if not os.path.isfile(os.path.join(os.getcwd(), 'requirements.txt')):
        return print_with_color_tags(f"<bg_red>{'*'*20} ARQUIVO REQUIREMENTS.TXT NAO ENCONTRADO {'*'*20}</bg_red>")

    venv = existe_venv()
    exe = get_python_exe_path_in_venv() if venv else 'python'
    subprocess.run([exe,"-m",'pip', 'install', '-r','requirements.txt'], cwd=os.getcwd(), check=True)

def upgrade_pip():
    venv = existe_venv()
    exe = get_python_exe_path_in_venv() if venv else 'python'

    subprocess.run([exe,"-m",'pip', 'install', '--upgrade','pip'], cwd=os.getcwd(), check=True)

def pull_redeploy():
    print_with_color_tags(f"<black><bg_cyan>{'-'*50} REDEPLOY </bg_cyan></black>")
    status,token = validade_portainer_credentials()
    if not status:return

    stack = get_stack(token,botConfig.BOT_NAME)
    if not stack:
        print_with_color_tags(f"<bg_red> ERRO AO CAPTURAR A STACK </bg_red>")
        return print_with_color_tags(f"<bg_red> STACK '{botConfig.BOT_NAME}' NAO ENCONTRADA </bg_red>")
    
    redeploy_stack(stack,token)
    print_with_color_tags(f"<bg_green> RE-DEPLOY FEITO COM SUCESSO </bg_green>")

def create_stack():
    print_with_color_tags(f"<black><bg_cyan>{'-'*50} CREATE BOT STACK </bg_cyan></black>")

    status,token = validade_portainer_credentials()
    if not status:return

    botname   =  botConfig.BOT_NAME
    giturl    =  get_git_remote_url() #"https://github.com/SymplaAutomate/AdiantamentoPro_Deliberacao"
    reference = get_current_git_ref()
    print("BOTNAME:\t",botname)
    print("GITURL:\t\t",giturl)
    print("REFERENCE:\t",reference)
    print()

    status,message = create_git_stack(token,botname,giturl,reference)
    if not status:
        print_with_color_tags(f"<bg_red> ERRO AO CRIAR A STACK </bg_red>")
        print_with_color_tags(f"<bg_red> ERRO: {message} </bg_red>")
        return

    print_with_color_tags(f"<bg_green> STACK CRIADA COM SUCESSO </bg_green>")

def run_prd():
    print_with_color_tags(f"<black><bg_cyan>{'-'*50} START PRD BOT </bg_cyan></black>")
    host = os.getenv("MSI_HOST")
    token = os.getenv("MSI_TOKEN")
    if not token or not host:
        return print_with_color_tags(f"<bg_red> PARA USAR O MSI CONFIGURE AS VARIAVEIS DE AMBIENTE CORRETAMENTE </bg_red>")
    
    url = host + "/rpa/run_bot"
    data = { "botnames": [botConfig.BOT_NAME], "params": [] }

    response = requests.post(url,json=data)
    if response.status_code != 200:
        return print_with_color_tags(f"<bg_red> ERRO AO INICIAR O BOT: {response.text} </bg_red>")
    
    print_with_color_tags(f"<bg_green> CONCLUIDO </bg_green>")

    pass

def run_prd_stream():  
    print_with_color_tags(f"<black><bg_cyan>{'-'*50} START PRD BOT STREAM </bg_cyan></black>")
    host = os.getenv("MSI_HOST")
    token = os.getenv("MSI_TOKEN")
    if not token or not host:
        return print_with_color_tags(f"<bg_red> PARA USAR O MSI CONFIGURE AS VARIAVEIS DE AMBIENTE CORRETAMENTE </bg_red>")
    
    task = argv[1] if len(argv) >1 else ""
    url = host + "/rpa/stream"
    params = { "botname": botConfig.BOT_NAME, "task": task }

    try:
        with requests.get(url, stream=True,params=params) as response:
            clear_cmd_pattern = re.compile(r'(\x1bc|\x1b\[2J|\x1b\[H|\x1b\[2J\x1b\[H|\x1b\[3J|\x1b\[H\x1b\[J)')
            
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    print(clear_cmd_pattern.sub('', line))
    except Exception as e:
        pass

def bot_tasks():
    sys.path.append(str(Path(os.getcwd())))
    sys.path.append(str(Path(os.getcwd()).joinpath("app")))
    import app.__main__ #CARREGA AS TASKS
    show_tasks()


def task_loop():
    sys.path.append(str(Path(os.getcwd())))
    sys.path.append(str(Path(os.getcwd()).joinpath("app")))
    import app.__main__ #CARREGA AS TASKS
    show_config()
    Task.loop()
