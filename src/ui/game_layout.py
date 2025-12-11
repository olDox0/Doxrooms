from nicegui import ui

class GameLayout:
    """
    Componente: GameLayout
    Gerado por Doxoade Scaffold
    """
    def __init__(self):
        self.build()

    def build(self):
        with ui.card().classes('w-full p-4'):
            ui.label('GameLayout').classes('text-xl font-bold')
            # TODO: Implementar lógica visual aqui
            ui.button('Ação', on_click=self.on_action)

    def on_action(self):
        ui.notify('GameLayout Action Triggered!')

def create():
    return GameLayout()
