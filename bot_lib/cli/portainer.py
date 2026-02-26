from bot_lib.common.colorama_print import print_with_color_tags
import requests
import os


def validade_portainer_credentials():
    # os.environ["PORTAINER_HOST"]     = "http://10.10.0.8:9000"  # URL do Portainer
    # os.environ["PORTAINER_USER"]     = "admin"  # Substitua pelo seu usuário do Portainer
    # os.environ["PORTAINER_PASSWORD"] = "Qwerty123!@#"  # Substitua pela sua
    # senha do Portainer

    portainer_host = os.getenv("PORTAINER_HOST")
    portainer_user = os.getenv("PORTAINER_USER")
    portainer_password = os.getenv("PORTAINER_PASSWORD")

    status = (None, None)
    if any([not portainer_host, not portainer_user, not portainer_password]):
        print_with_color_tags(
            f"<bg_red> PARA USAR O PORTAINER CONFIGURE AS VARIAVEIS DE AMBIENTE CORRETAMENTE </bg_red>")
        status = (False, None)
    print()
    if not portainer_host:
        print_with_color_tags(
            f" PORTAINER_HOST: \t<bg_red> NOT FOUND </bg_red>")
    if not portainer_user:
        print_with_color_tags(
            f" PORTAINER_USER: \t<bg_red> NOT FOUND </bg_red>")
    if not portainer_password:
        print_with_color_tags(
            f" PORTAINER_PASSWORD: \t<bg_red> NOT FOUND </bg_red>")

    status_api, token = get_portainer_token()
    if not status_api:
        print_with_color_tags(f"<bg_red> ERRO AO LOGAR NO PORTAINER </bg_red>")
        print_with_color_tags(f"<bg_red>ERRO: \t {token}</bg_red>")
        status = (False, None)
    else:
        status = (True, token)

    return status

# Função para obter o token de autenticação do Portainer


def get_portainer_token():
    portainer_host = os.getenv("PORTAINER_HOST")
    portainer_user = os.getenv("PORTAINER_USER")
    portainer_password = os.getenv("PORTAINER_PASSWORD")

    url = f"{portainer_host}/api/auth"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "username": portainer_user,
        "password": portainer_password
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return True, response.json()['jwt']  # Retorna o token JWT
    else:
        return False, response.text

# Função para fazer o redeploy de uma stack


def redeploy_stack(stack, token):
    portainer_host = os.getenv("PORTAINER_HOST")
    url = f"{portainer_host}/api/stacks/{
        stack['Id']}/git/redeploy?endpointId={
        stack['EndpointId']}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "env": [],
        "prune": False,
        "pullImage": False,
        "repositoryAuthentication": True,
        "RepositoryGitCredentialID": stack["GitConfig"]["Authentication"]["GitCredentialID"],
        "repositoryPassword": "",
        "repositoryReferenceName": stack["GitConfig"]["ReferenceName"],
        "repositoryUsername": stack["GitConfig"]["Authentication"]["Username"],

    }

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(
            f"Falha ao redeployar stack {
                stack['Name']}: {
                response.status_code} - {
                response.text}")


# Função para listar todas as stacks
def list_git_stacks(token):
    portainer_host = os.getenv("PORTAINER_HOST")
    url = f"{portainer_host}/api/stacks"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        stacks = response.json()
        if stacks:
            return [x for x in stacks if x["GitConfig"]]
        else:
            return []
    else:
        return []


def get_stack(token, botname):
    staks = list_git_stacks(token)
    stak = [x for x in staks if x["Name"] == botname]
    return stak[0] if stak else None


def create_git_stack(token, botname, giturl, reference):
    portainer_host = os.getenv("PORTAINER_HOST")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    # ----------- ENDPOINT ID
    response = requests.get(f"{portainer_host}/api/endpoints", headers=headers)
    if response.status_code != 200:
        return (False, f'Erro ao pesquisar endpointID: {response.text}')
    endpointId = response.json()[0]["Id"]

    url = f"{portainer_host}/api/stacks/create/standalone/repository?endpointId={endpointId}"

    payload = {
        "name": botname,
        "repositoryURL": giturl,
        "repositoryReferenceName": reference,
        "composeFile": "docker-compose.yml",
        "env": [],
        # "endpointId": 1,
        # "type": 1,
        # "accessControl": {
        # "public": True
        # }

        "prune": False,
        "pullImage": False,
        "repositoryAuthentication": True,
        "RepositoryGitCredentialID": 1,  # DEFINE QUAL A CREDENCIAL USAR
        # "autoUpdate": {
        #     "forcePullImage": False,
        #     "forceUpdate": False,
        #     "interval": "1m",
        #     "jobID": "15",
        #     "webhook": "05de31a2-79fa-4644-9c12-faa67e5c49f0"
        # },
        "filesystemPath": "/tmp",
        "fromAppTemplate": False,
        "repositoryAuthentication": True,
        "supportRelativePath": False,
        "tlsskipVerify": False
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return (True, None)
    else:
        return (False, response.json()["message"])
