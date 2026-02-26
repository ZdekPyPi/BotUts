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
    print(
        "setupy",
        '\t\t',
        '',
        '\t\t',
        'CRIA A VENV, ATUALIZA O PIP, INSTALA OS REQUIREMENTS')

    print_item_terminal("BOT UTILS", color="black", bg_color="cyan")
    print("bot-tasks", '\t\t', '', '\t', 'LISTA TODAS AS TASKS DO ROBO')
    print(
        "bot-run",
        '\t',
        '<task>',
        '\t',
        'RODA UMA TASK (CASO NAO INFORMADA RODA A PRIMEIRA ENCONTRADA)')
    print("bot-run-all", '\t\t', '', '\t',
          'RODA TODAS AS TASKS INDEPENDENTE DO CRON')
    print("bot-loop", '\t\t', '', '\t', 'INICIA O LOOP DO PROCESSO')

    print_item_terminal("PORTAINER", color="black", bg_color="cyan")
    print("bot-stack", '\t\t', '', '\t', 'CRIA A STACK NO PORTAINER')
    print("bot-deploy", '\t\t', '', '\t',
          'DA UM REDEPLOY NA STACK DO PORTAINER')
    print("bot-run-prd", '\t\t', '', '\t', 'RODA O ROBO EM PRODUCAO')
    print(
        "bot-stream",
        '\t',
        '<task>',
        '\t',
        'RODA O ROBO EM PRODUCAO E MOSTRA OS LOGS EM TEMPO REAL')

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
        return print_with_color_tags(
            f"<bg_red>{'*' * 20} SAIA DA VENV ATUAL PARA CRIAR UMA NOVA {'*' * 20}</bg_red>")
    if existe_venv() and 0:
        print_with_color_tags(
            f"<bg_red>{
                '*' *
                50} VENV JA EXISTE {
                '*' *
                50}</bg_red>")
    else:
        print_with_color_tags(f"<bg_green>{'-' * 50} CRIANDO VENV </bg_green>")
        os.system(r"python -m venv venv")
        print()
        print_with_color_tags(
            f"<bg_blue>{
                '-' *
                50} ATUALIZANDO PIP </bg_blue>")
        upgrade_pip()
        print_with_color_tags(
            f"<bg_cyan>{
                '-' *
                50} INSTALANDO REQUIREMENTS </bg_cyan>")
        upreq()


def gitup():
    print_with_color_tags(
        f"<black><bg_white>{
            '-' *
            50} ATUALIZANDO GIT </bg_white></black>")
    comment = sys.argv[1] if len(sys.argv) > 1 else 'Update'
    subprocess.run(['git', 'add', '.'], cwd=os.getcwd(), check=True)
    # Verifica se há algo para commitar
    result = subprocess.run(
        ['git', 'diff', '--cached', '--quiet'], cwd=os.getcwd())
    if result.returncode == 0:
        return print_with_color_tags(
            f"<black><bg_green>NENHUMA MUDANCA PARA COMITAR</bg_green></black>")
    subprocess.run(['git', 'commit', '-m', comment],
                   cwd=os.getcwd(), check=True)
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
    print_with_color_tags(
        f"<black><bg_cyan>{
            '-' * 50} REDEPLOY </bg_cyan></black>")
    status, token = validade_portainer_credentials()
    if not status:
        return

    stack = get_stack(token, botConfig.BOT_NAME)
    if not stack:
        print_with_color_tags(f"<bg_red> ERRO AO CAPTURAR A STACK </bg_red>")
        return print_with_color_tags(
            f"<bg_red> STACK '{botConfig.BOT_NAME}' NAO ENCONTRADA </bg_red>")

    redeploy_stack(stack, token)
    print_with_color_tags(
        f"<bg_green> RE-DEPLOY FEITO COM SUCESSO </bg_green>")


def create_stack():
    print_with_color_tags(
        f"<black><bg_cyan>{
            '-' *
            50} CREATE BOT STACK </bg_cyan></black>")

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
    print_with_color_tags(
        f"<black><bg_cyan>{
            '-' *
            50} START PRD BOT </bg_cyan></black>")
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
    print_with_color_tags(
        f"<black><bg_cyan>{
            '-' *
            50} START PRD BOT STREAM </bg_cyan></black>")
    host = os.getenv("MSI_HOST")
    token = os.getenv("MSI_TOKEN")
    if not token or not host:
        return print_with_color_tags(
            f"<bg_red> PARA USAR O MSI CONFIGURE AS VARIAVEIS DE AMBIENTE CORRETAMENTE </bg_red>")

    task = argv[1] if len(argv) > 1 else ""
    url = host + "/rpa/stream"
    params = {"botname": botConfig.BOT_NAME, "task": task}

    try:
        with requests.get(url, stream=True, params=params) as response:
            clear_cmd_pattern = re.compile(
                r'(\x1bc|\x1b\[2J|\x1b\[H|\x1b\[2J\x1b\[H|\x1b\[3J|\x1b\[H\x1b\[J)')

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
