import requests
import json
from kubernetes import client, config
from kubernetes.client.rest import ApiException

#Azion configs
AZION_URL = ""
AZION_PAYLOAD={}
AZION_HEADERS = {
  'Accept': 'application/json; version=3',
  'Authorization': 'Token '
}
AZION_RESPONSE = requests.request("GET", AZION_URL, headers=AZION_HEADERS, data=AZION_PAYLOAD)

#K8S configs
config.load_incluster_config()
CM_NAME = ""
NAMESPACE = ""
DATA_TO_UPDATE = {}

ips_azion_sorted = []

def get_api_azion():
    if AZION_RESPONSE.status_code == 200:
        json_list_azion = json.loads(AZION_RESPONSE.content)
        results = json_list_azion['results']
        ips_list_azion = json.dumps(results['items_values'])
        ips_azion = json.loads(ips_list_azion)
        ips_azion_sorted = sorted(ips_azion)
        print(f'AZION_ORIGIN_SITE_SHIELD_IPS: {ips_azion_sorted}')
        
    else:
        print(f'Erro na solicitação: {AZION_RESPONSE.status_code}')
        print(AZION_RESPONSE.text)

def update_cm():
    try:
        core_v1_api = client.CoreV1Api()
        current_configmap = core_v1_api.read_NAMESPACEd_config_map(name=CM_NAME, NAMESPACE=NAMESPACE)
        current_configmap.data.update(DATA_TO_UPDATE)
        core_v1_api.patch_NAMESPACEd_config_map(name=CM_NAME, NAMESPACE=NAMESPACE, body=current_configmap)
        print(f"ConfigMap '{CM_NAME}' atualizado com sucesso.")
    except ApiException as e:
        print(f"Erro ao atualizar o ConfigMap: {e.reason}")