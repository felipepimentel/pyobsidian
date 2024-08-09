import os
import json
import requests

def list_installed_plugins(config):
    vault_path = config['vault_path']
    plugins_folder = os.path.join(vault_path, '.obsidian', 'plugins')
    
    if not os.path.exists(plugins_folder):
        return []
    
    return [f for f in os.listdir(plugins_folder) if os.path.isdir(os.path.join(plugins_folder, f))]

def get_plugin_info(plugin_id):
    url = f"https://raw.githubusercontent.com/obsidianmd/obsidian-releases/master/community-plugins.json"
    response = requests.get(url)
    plugins = json.loads(response.text)
    
    for plugin in plugins:
        if plugin['id'] == plugin_id:
            return plugin
    
    return None

def check_for_updates(config):
    installed_plugins = list_installed_plugins(config)
    updates_available = []
    
    for plugin_id in installed_plugins:
        plugin_info = get_plugin_info(plugin_id)
        if plugin_info:
            local_version = get_local_plugin_version(config, plugin_id)
            if local_version and local_version != plugin_info['version']:
                updates_available.append({
                    'id': plugin_id,
                    'name': plugin_info['name'],
                    'current_version': local_version,
                    'latest_version': plugin_info['version']
                })
    
    return updates_available

def get_local_plugin_version(config, plugin_id):
    vault_path = config['vault_path']
    manifest_path = os.path.join(vault_path, '.obsidian', 'plugins', plugin_id, 'manifest.json')
    
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
            return manifest.get('version')
    
    return None
