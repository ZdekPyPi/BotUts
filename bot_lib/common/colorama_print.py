from colorama import init, Fore, Back

# Inicializa o colorama para garantir que funciona no Windows
init(autoreset=True)

def parse_color_tag(tag):
    """
    Converte as tags de cor em códigos do colorama.
    """
    # Mapeamento das cores de texto
    text_color_dict = {
        "black": Fore.BLACK,
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "reset": Fore.RESET
    }

    # Mapeamento das cores de fundo
    bg_color_dict = {
        "black": Back.BLACK,
        "red": Back.RED,
        "green": Back.GREEN,
        "yellow": Back.YELLOW,
        "blue": Back.BLUE,
        "magenta": Back.MAGENTA,
        "cyan": Back.CYAN,
        "white": Back.WHITE,
        "reset": Back.RESET
    }

    if "bg_" in tag:
        # Se a tag é de fundo, usa o dicionário de cores de fundo
        return bg_color_dict.get(tag[3:], Back.RESET)
    else:
        # Caso contrário, usa o dicionário de cores de texto
        return text_color_dict.get(tag, Fore.RESET)


def print_with_color_tags(text):
    """
    Recebe o texto com tags de cor no formato <cor_texto> e <cor_fundo>.
    Exemplo de uso: <red><yellow>Texto colorido</yellow></red>
    """
    left_tags = []  # Lista para armazenar as tags aplicadas
    formatted_text = ""  # Texto formatado para exibição





    i = 0  # Índice para percorrer o texto
    
    while i < len(text):
        if text[i] == "<":  # Encontrar o início da tag
            start_tag = i + 1
            end_tag = text.find(">", start_tag)
            if end_tag == -1:
                break  # Caso a tag esteja mal formada, sai do loop
                
            # Pega a tag da cor
            tag = text[start_tag:end_tag]
            
            # Verifica se a tag contém o comando de fechamento
            if tag.startswith("/"):
                if left_tags:
                    left_tags.pop()  # Remove o último comando da lista de tags
                    # Aplica as tags restantes
                    formatted_text += parse_color_tag(tag)
                    formatted_text += "".join(left_tags)
            else:
                # Adiciona a nova tag à lista de tags aplicadas
                color_code = parse_color_tag(tag)
                left_tags.append(color_code)  # Armazena a tag na lista
                formatted_text += color_code
            i = end_tag + 1  # Avança para o próximo caractere após a tag
        else:
            formatted_text += text[i]
            i += 1

    # Imprime o texto formatado
    print(formatted_text)


# Exemplo de uso
if __name__ == "__main__":
    print_with_color_tags("<green><bg_red>Texto com fundo vermelho</bg_red> texto sem background")
    print_with_color_tags("<blue><bg_yellow>Texto azul com fundo amarelo</bg_yellow></blue>")
    print_with_color_tags("<red>Texto vermelho <bg_green>com fundo verde</bg_green> e mais texto vermelho</red>")



# # Exemplo de uso
# if __name__ == "__main__":
#     print_with_color_tags("<red>Texto vermelho</red>")
#     print_with_color_tags("<blue><yellow>Texto azul com fundo amarelo</yellow></blue>")
#     print_with_color_tags("<green><bg_red>Texto com fundo vermelho</bg_red>texto sem background</green>")
#     print_with_color_tags("<cyan>Texto ciano</cyan>")
#     print_with_color_tags("<bg_white><red>Texto com fundo branco e texto vermelho</red></bg_white>")
