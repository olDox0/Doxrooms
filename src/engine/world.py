import json
import os

class WorldEngine:
    def __init__(self, data_path="data/levels.json"):
        self.data_path = data_path
        self.world_data = self._load_data()
        self.current_node_id = self.world_data.get("start_node", "lobby_start")
    
    def _load_data(self):
        """Carrega o JSON de níveis de forma segura."""
        if not os.path.exists(self.data_path):
            # Fallback de emergência se o arquivo sumir
            return {"nodes": {"lobby_start": {"name": "ERRO", "description": "Arquivo de dados não encontrado.", "exits": {}}}}
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_current_node(self):
        """Retorna o dicionário de dados da sala atual."""
        return self.world_data["nodes"].get(self.current_node_id)

    def try_move(self, direction):
        """
        Tenta mover o jogador.
        Retorna (Sucesso: bool, Mensagem: str)
        """
        current_node = self.get_current_node()
        exits = current_node.get("exits", {})
        
        if direction in exits:
            destination_id = exits[direction]
            if destination_id in self.world_data["nodes"]:
                self.current_node_id = destination_id
                return True, f"Você segue para {direction}..."
            else:
                return False, "O caminho leva ao vazio (Erro de Mapa)."
        else:
            return False, "Não há passagem nessa direção."

    def get_available_exits(self):
        """Retorna lista de direções possíveis (ex: ['norte', 'leste'])"""
        return list(self.get_current_node().get("exits", {}).keys())