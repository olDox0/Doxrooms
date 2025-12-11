# src/engine/player.py

from src.engine.inventory import Inventory

class Player:
    def __init__(self):
        self.max_stats = 100
        self._sanidade = 100
        self.saude = 100
        self.fome = 0
        self.sede = 0
        
        # Novo: Sistema de Inventário
        self.inventory = Inventory()
        
        self.estados = [] 

    @property
    def sanidade(self):
        return self._sanidade

    @sanidade.setter
    def sanidade(self, valor):
        self._sanidade = max(0, min(valor, 100))
        self._check_sanity_states()

    def _check_sanity_states(self):
        # Lógica de Thresholds
        if self._sanidade < 20:
            if 'alucinacao' not in self.estados:
                self.estados.append('alucinacao')
        elif 'alucinacao' in self.estados:
            self.estados.remove('alucinacao')
        # Adicione aqui pânico, colapso, etc.