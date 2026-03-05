import subprocess
from pathlib import Path
import sys
import os
from bot_lib.common.colorama_print import print_with_color_tags
from .portainer import *
from bot_lib.settings import botConfig
from bot_lib.libs import Task, show_config
from .common import get_git_remote_url, get_current_git_ref
import re
from sys import argv
import shutil
import base64
import tempfile
import io
import zipfile

def print_item_terminal(text, title=False, total_size=80,
                        color="black", bg_color="white"):
    fill_left = f" {text} ".center(
        total_size, '=') if title else f"{'-' * ((total_size - len(text)) // 2)} {text}"
    fill_left = fill_left.ljust(
        total_size,
        '=') if title else fill_left.ljust(
        60,
        ' ')
    print_with_color_tags(
        f"<{color}><bg_{bg_color}>{fill_left}</bg_{bg_color}></{color}>")


def botlib_commands():
    print_item_terminal("COMMANDS", title=True)

    print_item_terminal("UTILS", color="black", bg_color="cyan")
    print("gitup", '\t\t', '<comment>', '\t', 'ATUALIZA O REPOSITORIO DO GIT')
    print("upreq", '\t\t', '', '\t\t', 'ATUALIZA O REQUIREMENTS DA VENV ATUAL')
    print( "setupy", '\t\t', '', '\t\t', 'CRIA A VENV, ATUALIZA O PIP, INSTALA OS REQUIREMENTS')

    print_item_terminal("BOT UTILS", color="black", bg_color="cyan")
    print("bot-new", '\t\t', '', '\t', 'CRIA UMA ESTRUTURA BASICA DE PASTAS E ARQUIVOS PARA UM NOVO ROBO')
    print("bot-tasks", '\t\t', '', '\t', 'LISTA TODAS AS TASKS DO ROBO')
    print( "bot-run", '\t', '<task>', '\t', 'RODA UMA TASK (CASO NAO INFORMADA RODA A PRIMEIRA ENCONTRADA)')
    print("bot-run-all", '\t\t', '', '\t', 'RODA TODAS AS TASKS INDEPENDENTE DO CRON')
    print("bot-loop", '\t\t', '', '\t', 'INICIA O LOOP DO PROCESSO')

    print_item_terminal("PORTAINER", color="black", bg_color="cyan")
    print("bot-stack", '\t\t', '', '\t', 'CRIA A STACK NO PORTAINER')
    print("bot-deploy", '\t\t', '', '\t', 'DA UM REDEPLOY NA STACK DO PORTAINER')
    print("bot-run-prd", '\t\t', '', '\t', 'RODA O ROBO EM PRODUCAO')
    print( "bot-stream", '\t', '<task>', '\t', 'RODA O ROBO EM PRODUCAO E MOSTRA OS LOGS EM TEMPO REAL')

    print()
    print_item_terminal("ENVARS", title=True, color="black", bg_color="white")
    print_item_terminal("REQUIRED", color="black", bg_color="cyan")
    print("BOT_NAME", '\t', '<BOT_NAME>', '\t', '')
    print("BOT_ID", '\t\t', '<BOT_ID>', '\t', '')
    print("MODE", '\t\t', '<DEV|PRD>', '\t', '')
    print_item_terminal("PORTAINER", color="black", bg_color="cyan")
    print("PORTAINER_HOST", '\t\t', '', '\t', '<http://localhost:9000>')
    print("PORTAINER_USER", '\t\t', '', '\t', '<USERNAME>')
    print("PORTAINER_PASSWORD", '\t', '', '\t', '<PASSWORD>')
    print_item_terminal("OTHERS", color="black", bg_color="cyan")
    print("DATABASE_URL", '\t\t', '', '\t', '<sqlite:///path_to.db> or <postgresql://user:password@host/db>')
    print("LOG_DB", '\t\t', '', '\t', '<Y|N>')
    print("MOON_HOST", '\t\t', '', '\t', '<http://localhost:444/wd/hub>')
    print("MSI_HOST", '\t\t', '', '\t', '<http://localhost:5000>')
    print("MSI_TOKEN", '\t\t', '', '\t', '<TOKEN>')


def existe_venv():
    for d in os.listdir():
        if os.path.isdir(d) and os.path.exists(os.path.join(
                d, "bin" if os.name != "nt" else "Scripts", "activate")):
            return d
    return None


def get_python_exe_path_in_venv(project_path=None):
    # Se o projeto não for especificado, use o diretório atual
    if project_path is None:
        project_path = os.path.join(os.getcwd(), existe_venv())

    # Verifica se a pasta "Scripts" (Windows) ou "bin" (Linux/Mac) existe
    # dentro do diretório do projeto
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
        return print_with_color_tags( f"<bg_red>{'*' * 20} SAIA DA VENV ATUAL PARA CRIAR UMA NOVA {'*' * 20}</bg_red>")
    if existe_venv() and 0:
        print_with_color_tags( f"<bg_red>{ '*' * 50} VENV JA EXISTE { '*' * 50}</bg_red>")
    else:
        print_with_color_tags(f"<bg_green>{'-' * 50} CRIANDO VENV </bg_green>")
        os.system(r"python -m venv venv")
        print()
        print_with_color_tags( f"<bg_blue>{ '-' * 50} ATUALIZANDO PIP </bg_blue>")
        upgrade_pip()
        print_with_color_tags( f"<bg_cyan>{ '-' * 50} INSTALANDO REQUIREMENTS </bg_cyan>")
        upreq()


def gitup():
    print_with_color_tags( f"<black><bg_white>{ '-' * 50} ATUALIZANDO GIT </bg_white></black>")
    comment = sys.argv[1] if len(sys.argv) > 1 else 'Update'
    subprocess.run(['git', 'add', '.'], cwd=os.getcwd(), check=True)
    # Verifica se há algo para commitar
    result = subprocess.run(
        ['git', 'diff', '--cached', '--quiet'], cwd=os.getcwd())
    if result.returncode == 0:
        return print_with_color_tags(f"<black><bg_green>NENHUMA MUDANCA PARA COMITAR</bg_green></black>")
    subprocess.run(['git', 'commit', '-m', comment], cwd=os.getcwd(), check=True)
    subprocess.run(['git', 'push'], cwd=os.getcwd(), check=True)


def upreq():
    if not os.path.isfile(os.path.join(os.getcwd(), 'requirements.txt')):
        return print_with_color_tags(
            f"<bg_red>{'*' * 20} ARQUIVO REQUIREMENTS.TXT NAO ENCONTRADO {'*' * 20}</bg_red>")

    venv = existe_venv()
    exe = get_python_exe_path_in_venv() if venv else 'python'
    subprocess.run([exe, "-m", 'pip', 'install', '-r',
                   'requirements.txt'], cwd=os.getcwd(), check=True)


def upgrade_pip():
    venv = existe_venv()
    exe = get_python_exe_path_in_venv() if venv else 'python'

    subprocess.run([exe, "-m", 'pip', 'install', '--upgrade',
                   'pip'], cwd=os.getcwd(), check=True)


def pull_redeploy():
    print_with_color_tags( f"<black><bg_cyan>{ '-' * 50} REDEPLOY </bg_cyan></black>")
    status, token = validade_portainer_credentials()
    if not status:
        return

    stack = get_stack(token, botConfig.BOT_NAME)
    if not stack:
        print_with_color_tags(f"<bg_red> ERRO AO CAPTURAR A STACK </bg_red>")
        return print_with_color_tags(
            f"<bg_red> STACK '{botConfig.BOT_NAME}' NAO ENCONTRADA </bg_red>")

    redeploy_stack(stack, token)
    print_with_color_tags( f"<bg_green> RE-DEPLOY FEITO COM SUCESSO </bg_green>")


def create_stack():
    print_with_color_tags( f"<black><bg_cyan>{ '-' * 50} CREATE BOT STACK </bg_cyan></black>")

    status, token = validade_portainer_credentials()
    if not status:
        return

    botname = botConfig.BOT_NAME
    # "https://github.com/SymplaAutomate/AdiantamentoPro_Deliberacao"
    giturl = get_git_remote_url()
    reference = get_current_git_ref()
    print("BOTNAME:\t", botname)
    print("GITURL:\t\t", giturl)
    print("REFERENCE:\t", reference)
    print()

    status, message = create_git_stack(token, botname, giturl, reference)
    if not status:
        print_with_color_tags(f"<bg_red> ERRO AO CRIAR A STACK </bg_red>")
        print_with_color_tags(f"<bg_red> ERRO: {message} </bg_red>")
        return

    print_with_color_tags(f"<bg_green> STACK CRIADA COM SUCESSO </bg_green>")


def run_prd():
    print_with_color_tags( f"<black><bg_cyan>{ '-' * 50} START PRD BOT </bg_cyan></black>")
    host = os.getenv("MSI_HOST")
    token = os.getenv("MSI_TOKEN")
    if not token or not host:
        return print_with_color_tags(
            f"<bg_red> PARA USAR O MSI CONFIGURE AS VARIAVEIS DE AMBIENTE CORRETAMENTE </bg_red>")

    url = host + "/rpa/run_bot"
    data = {"botnames": [botConfig.BOT_NAME], "params": []}

    response = requests.post(url, json=data)
    if response.status_code != 200:
        return print_with_color_tags(
            f"<bg_red> ERRO AO INICIAR O BOT: {response.text} </bg_red>")

    print_with_color_tags(f"<bg_green> CONCLUIDO </bg_green>")

    pass


def run_prd_stream():
    print_with_color_tags( f"<black><bg_cyan>{ '-' * 50} START PRD BOT STREAM </bg_cyan></black>")
    host = os.getenv("MSI_HOST")
    token = os.getenv("MSI_TOKEN")
    if not token or not host:
        return print_with_color_tags( f"<bg_red> PARA USAR O MSI CONFIGURE AS VARIAVEIS DE AMBIENTE CORRETAMENTE </bg_red>")

    task = argv[1] if len(argv) > 1 else ""
    url = host + "/rpa/stream"
    params = {"botname": botConfig.BOT_NAME, "task": task}

    try:
        with requests.get(url, stream=True, params=params) as response:
            clear_cmd_pattern = re.compile( r'(\x1bc|\x1b\[2J|\x1b\[H|\x1b\[2J\x1b\[H|\x1b\[3J|\x1b\[H\x1b\[J)')

            for line in response.iter_lines(decode_unicode=True):
                if line:
                    print(clear_cmd_pattern.sub('', line))
    except Exception as e:
        pass


def bot_tasks():
    sys.path.append(str(Path(os.getcwd())))
    sys.path.append(str(Path(os.getcwd()).joinpath("app")))
    import app.__main__  # CARREGA AS TASKS
    Task.show_tasks()


def task_loop():
    sys.path.append(str(Path(os.getcwd())))
    sys.path.append(str(Path(os.getcwd()).joinpath("app")))
    import app.__main__  # CARREGA AS TASKS
    show_config()
    Task.loop()


def run_task():
    sys.path.append(str(Path(os.getcwd())))
    sys.path.append(str(Path(os.getcwd()).joinpath("app")))
    import app.__main__  # CARREGA AS TASKS
    task_name = argv[1] if len(argv) > 1 else ""
    if not task_name:
        tasks = Task.TASKS
        if not tasks.keys():
            return print_with_color_tags(
                f"<bg_red> NENHUMA TASK ENCONTRADA </bg_red>")
        task_name = tasks.keys()[0]

    Task.run_task(task_name)


def run_all_tasks():
    sys.path.append(str(Path(os.getcwd())))
    sys.path.append(str(Path(os.getcwd()).joinpath("app")))
    import app.__main__  # CARREGA AS TASKS
    Task.run_all_tasks()


def b64_template_path():
    template_path = Path("./template")

    if not template_path.exists():
        raise Exception(f"Template path does not exist.")
    
    template_path = template_path.resolve()

    with tempfile.TemporaryDirectory() as temp_dir:
        arq = shutil.make_archive(temp_dir, 'zip', template_path)
        #CONVERTE PARA BASE64
        with open(arq, "rb") as arquivo:
            # Codifica os bytes do arquivo
            string_base64 = base64.b64encode(arquivo.read()).decode('utf-8')
        os.remove(arq)

    return string_base64

def new_bot():
    print_with_color_tags( f"<black><bg_cyan>{ '-' * 50} NEW BOT </bg_cyan></black>")
    botname = input("Enter the new bot name:")
    if not botname:
        return print_with_color_tags(f"<bg_red> BOT NAME CANNOT BE EMPTY </bg_red>")
    
    bot_id = input("Enter the new bot id: ")
    if not bot_id:
        return print_with_color_tags(f"<bg_red> BOT ID CANNOT BE EMPTY </bg_red>")

    string_base64 = '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'

    zip_data = base64.b64decode(string_base64)
    zip_buffer = io.BytesIO(zip_data)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
        zip_ref.extractall(f'./{botname}')

        #REPLACES
        with open(f'./{botname}/.env', 'w') as env_file:
            env_file.write(f"BOT_NAME\t= {botname}\n")
            env_file.write(f"BOT_ID\t\t= {bot_id}\n")
        
        compose_text = open(f'./{botname}/docker-compose.yml', 'r',encoding="utf-8").read()
        compose_text = compose_text.format(bot_name=botname)
        with open(f'./{botname}/docker-compose.yml', 'w') as compose_file:
            compose_file.write(compose_text)

    print_with_color_tags(f"<bg_green> NEW BOT '{botname}' CREATED SUCCESSFULLY </bg_green>")
