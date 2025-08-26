from slack_lib import SlackLib
from bot_lib.config.vault import SlackVault
from bot_lib.database.orm import Log
from bot_lib.settings import botConfig
import bot_lib
import os
from bot_lib.libs.task import Task

def notify_slack(message):

    if bot_lib.IN_PRD:
        curr_task    = Task.current_task_info()
        if curr_task:
            slack = SlackLib(SlackVault.TOKEN)
            emails = (curr_task.notify_emails or "")
            for email in emails.split(";"):
                try:
                    message_slack = [
                        #f"{'─'*50}\n",
                        ":rotating_light: ALERTA! :rotating_light:\n\n",
                        f":robot_face: *Robô:* `{botConfig.BOT_ID} - {botConfig.BOT_NAME}`\n",
                        f":gear: *Task:*  `{curr_task}`\n",
                        f":warning: *Erro:*  `{message}`\n",
                        #f"{'─'*50}\n",
                    ]
                    slack.sendUserMessage(email,"".join(message_slack))
                except Exception as e:
                    Log(level="SYSTEM",message=f"Erro ao enviar mensagem no SLACK {str(e)}").save()

            pass

