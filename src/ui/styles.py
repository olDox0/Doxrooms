# src/ui/styles.py

def get_visual_theme(player, location_type):
    """
    Retorna o CSS do container principal baseado no estado.
    """
    css_classes = "w-full h-screen transition-all duration-1000 " # Base
    style_inline = ""

    # 1. Baseado no Local
    if location_type == "poolrooms":
        style_inline += "background-color: #e0f7fa; color: #006064; font-family: 'Courier New';"
    elif location_type == "level0":
        style_inline += "background-color: #fdf5e6; color: #3e2723; font-family: 'Mono';"

    # 2. Baseado na Sanidade (Sobrepõe ou adiciona efeitos)
    if 'alucinacao' in player.estados:
        # Exemplo: Fundo piscando ou fonte instável
        css_classes += " glitch-effect " 
        style_inline += "text-shadow: 2px 2px red;"
    
    if 'panico' in player.estados:
        style_inline += "font-size: 1.1em;" # Texto treme ou aumenta

    return css_classes, style_inline