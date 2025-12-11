from nicegui import ui
import asyncio

class StoryLog(ui.element):
    def __init__(self):
        super().__init__('div')
        # CSS para a área de log: Fundo semitransparente, fonte mono, scroll
        self.style('height: 60vh; overflow-y: auto; padding: 1rem; background-color: rgba(0,0,0,0.1); border: 1px solid #444;')
        self.classes('font-mono text-sm w-full rounded')
        
        # Lista interna de mensagens
        self.messages = []
        
        # O container onde o texto real vai entrar
        with self:
            self.log_container = ui.column().classes('w-full gap-1')

    async def add_entry(self, text: str, type: str = "normal"):
        """
        Adiciona uma linha ao log com efeito de digitação e cor baseada no tipo.
        Types: 'normal', 'danger', 'info', 'whisper'
        """
        # Define a cor baseada no tipo (CSS inline para garantir)
        color = "#e0e0e0" # Padrão
        if type == "danger": color = "#ff4444" # Vermelho
        elif type == "info": color = "#44ccff"   # Azul Cyan
        elif type == "whisper": color = "#888888; font-style: italic" # Cinza itálico
        elif type == "success": color = "#44ff44" # Verde

        # Cria o elemento de texto vazio
        with self.log_container:
            # Usamos ui.html para permitir formatação rica se precisar
            entry = ui.html('').style(f'color: {color}; line-height: 1.4;')
        
        # Efeito Typewriter (Digitação)
        current_text = ""
        # Adiciona um timestamp falso estilo log de sistema
        prefix = ">> " 
        
        entry.set_content(prefix)
        
        # Simula digitação rápida
        for char in text:
            current_text += char
            # Se for HTML tag, não pausa (para não quebrar a tag no meio)
            if char == "<": 
                # Lógica simplificada: apenas imprime rápido, melhoria futura: regex
                pass 
            
            entry.set_content(prefix + current_text + "█") # █ cursor piscando
            if len(self.messages) == 0: # Só anima lento se for a primeira msg ou muito importante
                await asyncio.sleep(0.01) 
            else:
                await asyncio.sleep(0.001) # Digitação rápida para logs comuns

        # Remove o cursor no final
        entry.set_content(prefix + current_text)
        
        # Auto-scroll para o final
        entry.run_method('scrollIntoView')
        
    def clear(self):
        self.log_container.clear()