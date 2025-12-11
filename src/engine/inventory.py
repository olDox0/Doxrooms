import json
import random
import os

class ItemManager:
    def __init__(self, items_path="data/items.json"):
        self.items_data = self._load_items(items_path)

    def _load_items(self, path):
        if not os.path.exists(path):
            return {}
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_item_details(self, item_id):
        """Retorna os dados completos de um item pelo ID."""
        return self.items_data.get(item_id, {"name": "Item Glitchado", "desc": "Erro de dados."})

    def generate_random_loot(self):
        """
        Gera um item aleatório baseado na raridade (peso).
        Retorna o item_id ou None se falhar.
        """
        items = list(self.items_data.keys())
        # Simplificação: Escolhe um aleatório da lista
        # (Futuro: implementar algoritmo de peso real baseado na 'rarity')
        if not items:
            return None
        return random.choice(items)

class Inventory:
    def __init__(self):
        self.slots = [] # Lista de item_ids: ['agua_amendoa', 'sucata']
        self.capacity = 10

    def add_item(self, item_id):
        if len(self.slots) < self.capacity:
            self.slots.append(item_id)
            return True
        return False

    def remove_item(self, item_id):
        if item_id in self.slots:
            self.slots.remove(item_id)
            return True
        return False