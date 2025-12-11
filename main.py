import random
from src.ui.story_log import StoryLog 
from src.engine.world import WorldEngine
from src.engine.inventory import ItemManager
from nicegui import ui
from dataclasses import dataclass

# --- CONFIGURAÇÃO DE ESTILOS (CSS AVANÇADO) ---
# Aqui definimos as animações e classes que o Python vai "ligar" ou "desligar"
CSS_GLOBAL = """
<style>
    /* Fonte Padrão - Estilo Terminal Retro */
    @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
    
    body {
        font-family: 'VT323', monospace;
        transition: background-color 1.5s ease; /* Transição suave de cor */
    }

    /* Efeito de CRT (Scanlines) - Sempre sutil na tela */
    .crt::before {
        content: " ";
        display: block;
        position: absolute;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
        z-index: 2;
        background-size: 100% 2px, 3px 100%;
        pointer-events: none;
    }

    /* Animação de Pânico (Texto tremendo) */
    @keyframes shake {
        0% { transform: translate(1px, 1px) rotate(0deg); }
        10% { transform: translate(-1px, -2px) rotate(-1deg); }
        20% { transform: translate(-3px, 0px) rotate(1deg); }
        30% { transform: translate(3px, 2px) rotate(0deg); }
        40% { transform: translate(1px, -1px) rotate(1deg); }
        50% { transform: translate(-1px, 2px) rotate(-1deg); }
        60% { transform: translate(-3px, 1px) rotate(0deg); }
        70% { transform: translate(3px, 1px) rotate(-1deg); }
        80% { transform: translate(-1px, -1px) rotate(1deg); }
        90% { transform: translate(1px, 2px) rotate(0deg); }
        100% { transform: translate(1px, -2px) rotate(-1deg); }
    }
    
    .shake-effect {
        animation: shake 0.5s;
        animation-iteration-count: infinite;
        color: #ff4444 !important; /* Texto fica vermelho */
    }

    /* Efeito de Alucinação (Blur/Distorção) */
    .hallucination-effect {
        filter: blur(1.5px) contrast(150%);
        text-shadow: 2px 0 red, -2px 0 blue;
        transition: all 0.5s;
    }
</style>
"""

# Inicializações Globais
item_manager = ItemManager()
world = WorldEngine()

# --- DADOS DO MUNDO E JOGADOR (SIMULAÇÃO) ---
@dataclass
class PlayerState:
    sanidade: int = 100
    saude: int = 100
    local: str = "Nivel 0" # Ex: Nivel 0, Poolrooms, Boiler

player = PlayerState()

# --- LÓGICA DE ATUALIZAÇÃO VISUAL ---
def update_visuals(container_principal, texto_narrativa, painel_status):
    """
    Esta função é o CÉREBRO visual. Ela lê os dados do player
    e injeta o CSS correspondente na hora.
    """
    
    # 1. Definição do Ambiente (Cores de Fundo e Fontes Base)
    # Cores Hexadecimais: Amarelo Doente (Backrooms), Azul Hospital (Poolrooms), Preto (Dark)
    estilo_base = "height: 100vh; width: 100%; padding: 2rem; display: flex; gap: 20px;"
    
    if player.local == "Nivel 0":
        # Amarelo Mono-tom clássico
        container_principal.style(estilo_base + "background-color: #c2b280; color: #3e3216;")
    elif player.local == "Poolrooms":
        # Azul azulejo claro
        container_principal.style(estilo_base + "background-color: #e0f7fa; color: #006064;")
    elif player.local == "Escuridão":
        # Quase preto
        container_principal.style(estilo_base + "background-color: #121212; color: #a0a0a0;")

    # 2. Definição de Efeitos de Estado (Sanidade)
    classes_efeito = "crt" # Sempre tem scanlines
    
    if player.sanidade < 50:
        classes_efeito += " hallucination-effect" # Visão embaçada/3D
        texto_narrativa.classes('font-bold') # Muda peso da fonte
    else:
        texto_narrativa.classes(remove='font-bold')

    if player.sanidade < 20:
        classes_efeito += " shake-effect" # Tela tremendo
    
    # Aplica as classes no container principal
    container_principal.classes(classes_efeito)
    
    # Atualiza barras de progresso (Cores mudam conforme o valor)
    cor_sanidade = "green" if player.sanidade > 50 else ("orange" if player.sanidade > 20 else "red")
    painel_status.content = f"""
        <div style='border: 2px solid currentColor; padding: 10px; margin-bottom: 10px;'>
            <strong>STATUS</strong><br>
            LOCAL: {player.local}<br>
            SAÚDE: {player.saude}%<br>
            SANIDADE: <span style='color:{cor_sanidade}'>{player.sanidade}%</span>
        </div>
    """

@ui.page('/') # Garante que é a página principal
def main_game_ui():
    ui.add_head_html(CSS_GLOBAL) # Aquele CSS que fizemos antes

    # Layout Principal
    with ui.row().classes('w-full h-screen no-wrap items-stretch') as game_container:
        
        # --- PAINEL ESQUERDO (Status + Inventário) ---
        with ui.column().classes('w-1/4') as left_panel:
            status_display = ui.html() # (Seu código antigo de status)
            
            ui.separator()
            
            # UI DO INVENTÁRIO
            ui.label("MOCHILA").classes('font-bold mt-4')
            inventory_list = ui.column().classes('w-full gap-1 text-sm')
    
            def refresh_inventory_ui():
                inventory_list.clear()
                if not player.inventory.slots:
                    with inventory_list:
                        ui.label("- Vazio -").classes('italic opacity-50')
                    return
    
                for item_id in player.inventory.slots:
                    data = item_manager.get_item_details(item_id)
                    with inventory_list:
                        # Cria um item clicável (futuro: para usar/consumir)
                        ui.label(f"• {data['name']}").classes('cursor-pointer hover:text-green-400 transition')
    
        # --- PAINEL CENTRAL ---
        with ui.card().classes('w-2/4 h-full bg-transparent shadow-none border-2 border-current overflow-hidden column'):
            # Nome do Local (Cabeçalho)
            location_label = ui.label("Carregando...").classes('text-2xl font-bold mb-2')
            
            # O Log de História
            game_log = StoryLog() 
            
        # --- LÓGICA DE INVESTIGAÇÃO (LOOT) ---
        # Precisamos saber se a sala já foi lootada para evitar spam de itens infinitos
        # Vamos usar um set simples na memória para esta sessão
        looted_rooms = set() 

    async def investigate_room():
        current_node_id = world.current_node_id # Pega o ID da sala atual (ex: 'lobby_start')
        
        # 1. Verifica se já investigou
        if current_node_id in looted_rooms:
            await game_log.add_entry("Você já revirou tudo aqui. Não há mais nada.", "whisper")
            return

        # 2. Rola os dados (Loot Chance da sala)
        node_data = world.get_current_node()
        chance = node_data.get("loot_chance", 0.0)
        dice = random.random() # 0.0 a 1.0

        await game_log.add_entry("Investigando o ambiente...", "info")
        
        if dice < chance:
            # Sucesso! Gera item
            item_found = item_manager.generate_random_loot()
            if item_found:
                item_details = item_manager.get_item_details(item_found)
                
                if player.inventory.add_item(item_found):
                    await game_log.add_entry(f"Encontrado: {item_details['name']}", "success")
                    looted_rooms.add(current_node_id) # Marca sala como visitada
                    refresh_inventory_ui() # Atualiza visual da mochila
                else:
                    await game_log.add_entry(f"Achou {item_details['name']}, mas a mochila está cheia!", "danger")
        else:
            # Falha
            await game_log.add_entry("Você encontra apenas poeira e lixo inútil.", "whisper")
            looted_rooms.add(current_node_id) # Marca como visitada mesmo se não achou nada
        
    # --- PAINEL DIREITO (CONTROLES) ---
    with ui.column().classes('w-1/4 gap-2 p-4') as controls:
        ui.label("NAVEGAÇÃO").classes('font-bold')
        ui.button("INVESTIGAR", on_click=investigate_room).classes('w-full mt-4 border-2 border-dotted border-current')
        
        # Botões de Movimento
        with ui.grid(columns=3).classes('w-full'):
            ui.label() # Espaço vazio
            btn_norte = ui.button("N", on_click=lambda: move_player("norte"))
            ui.label() # Espaço vazio
            btn_oeste = ui.button("O", on_click=lambda: move_player("oeste"))
            ui.button("SUL", on_click=lambda: move_player("sul")).props('disabled') # Exemplo
            btn_leste = ui.button("L", on_click=lambda: move_player("leste"))

    # --- LÓGICA DE CONTROLE (O CÉREBRO) ---
    async def refresh_interface():
        """Atualiza TUDO na tela baseado no node atual"""
        node = world.get_current_node()
        
        # 1. Atualiza Texto do Local
        location_label.set_text(node['name'])
        
        # 2. Atualiza o Visual (Fundo e Cores)
        # Chama aquela função update_visuals que criamos antes, passando o tema do JSON
        # update_visuals(game_container, game_log, status_display, theme=node['visual_theme']) 
        # (Obs: Você precisará adaptar a update_visuals para receber o tema como argumento)

        # 3. Gerencia Botões (Ativa/Desativa dependendo das saídas)
        exits = world.get_available_exits()
        btn_norte.set_enabled("norte" in exits)
        btn_sul.set_enabled("sul" in exits) # Ops, esqueci de criar btn_sul no grid acima, adicione lá!
        btn_leste.set_enabled("leste" in exits)
        btn_oeste.set_enabled("oeste" in exits)

    async def move_player(direction):
        success, msg = world.try_move(direction)
        if success:
            # Texto descritivo da nova sala
            node = world.get_current_node()
            await game_log.add_entry(msg, "info")
            await game_log.add_entry(node['description'], "normal")
            await refresh_interface()
        else:
            # Feedback de erro (bateu na parede)
            await game_log.add_entry(msg, "whisper")

    # Start inicial
    await refresh_interface()
    # Adiciona a descrição inicial no log
    await game_log.add_entry(world.get_current_node()['description'])

ui.run(title="Doxrooms RPG")