import os
import json
import requests

# Função para obter informações dos conectores Kafka Connect
def get_connector_info(connect_url):
    response = requests.get(f"{connect_url}/connectors")
    connectors = response.json()
    return connectors

# Função para criar backup dos conectores
def create_backup(connect_url, backup_dir):
    connectors = get_connector_info(connect_url)
    for connector in connectors:
        connector_name = connector
        response = requests.get(f"{connect_url}/connectors/{connector_name}")
        with open(f"{backup_dir}/{connector_name}.json", "w") as file:
            json.dump(response.json(), file)

# Função para migrar os conectores
def migrate_connectors(source_connect_url, target_connect_url):
    connectors = get_connector_info(source_connect_url)
    for connector in connectors:
        connector_name = connector
        with open(f"{backup_dir}/{connector_name}.json", "r") as file:
            connector_config = json.load(file)
        response = requests.post(f"{target_connect_url}/connectors", json=connector_config)
        if response.status_code != 201:
            print(f"Failed to migrate connector {connector_name}")

# Função para validar a migração
def validate_migration(target_connect_url):
    migrated_connectors = get_connector_info(target_connect_url)
    # Implementar validação conforme necessário

# URL do Kafka Connect de origem
source_connect_url = "http://source-kafka-connect:8083"
# URL do Kafka Connect de destino
target_connect_url = "http://target-kafka-connect:8083"
# Diretório para backup dos conectores
backup_dir = "connector_backup"

# Criar backup dos conectores
create_backup(source_connect_url, backup_dir)

# Migrar os conectores
migrate_connectors(source_connect_url, target_connect_url)

# Validar a migração
validate_migration(target_connect_url)