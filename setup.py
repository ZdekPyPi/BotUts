from setuptools import setup, find_packages
import os

# Substitua "gitlab.com" por "${GIT_TOKEN}@gitlab.com" no arquivo
GIT_TOKEN = os.getenv("GIT_TOKEN")
gitlabhost = 'gitlab.com' if not GIT_TOKEN else f"{GIT_TOKEN}@gitlab.com"
githubhost = 'github.com' if not GIT_TOKEN else f"{GIT_TOKEN}@github.com"


setup(
    name='botUts',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "colorama         == 0.4.6",
        "httplib2         >= 0.15.0",
        "urllib3          >= 2.2.1",
        "sqlUts           >= 1.0.8",
        "SQLAlchemy       >= 1.4.50",
        "SQLAlchemy-Utils >= 0.38.2",
        "python-dotenv    >= 1.0.1",
        "psycopg2         >= 2.9.6",
        "pycron           >= 3.0.0",
        "dateUts          >= 0.3.1",
        "iniUts           >= 1.2.1",
        "loguru           >= 0.7.2",
        "psutil           >= 5.9.6",
        "requests         >= 2.32.4",
        "vaultUts         >= 1.1.2",
    ],
    entry_points={
        "console_scripts": [
            "gitup          = bot_lib.cli:gitup",
            "upreq          = bot_lib.cli:upreq",  # OK
            "setupy         = bot_lib.cli:setupy",  # OK
            # PORTAINER
            "bot-deploy      = bot_lib.cli:pull_redeploy",  # OK
            "bot-stack       = bot_lib.cli:create_stack",  # OK
            "bot-run-prd     = bot_lib.cli:run_prd",  # OK
            "bot-stream      = bot_lib.cli:run_prd_stream",  # OK

            # LOCAL
            "bot-help       = bot_lib.cli:botlib_commands",
            "bot-tasks      = bot_lib.cli:bot_tasks",
            "bot-loop       = bot_lib.cli:task_loop",
            "bot-run        = bot_lib.cli:run_task",
            "bot-run-all    = bot_lib.cli:run_all_tasks",

            # SELENOID
            "clearselenoid  = bot_lib.selenoid:deletar_todas"
        ],
    },
    author='Zdek Development team',
    description='Zdek Util libraries for Python coding',
    url='https://github.com/ZdekPyPi/BotUts',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.10',
    author_email='melque_ex@yahoo.com.br',
    license='MIT'
)
