import os
import json
import shutil

def sync():
    # 1. Find Obsidian configuration
    appdata = os.getenv('APPDATA')
    if not appdata:
        appdata = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
        
    obsidian_config_path = os.path.join(appdata, 'obsidian', 'obsidian.json')
    
    vault_paths = []
    if os.path.exists(obsidian_config_path):
        try:
            with open(obsidian_config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                vaults = data.get('vaults', {})
                for v in vaults.values():
                    path = v.get('path')
                    if path and os.path.exists(path):
                        vault_paths.append(path)
        except Exception as e:
            print(f"Error reading obsidian.json: {e}")
            
    # Fallback to default if config parsing fails but folder exists
    default_vault = r"C:\Users\SB\Documents\my_soul"
    if default_vault not in vault_paths and os.path.exists(default_vault):
        vault_paths.append(default_vault)
        
    if not vault_paths:
        print("No Obsidian vaults found.")
        return
        
    src_log = "development_log.md"
    if not os.path.exists(src_log):
        # Fallback if run from another subfolder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        src_log = os.path.join(script_dir, "development_log.md")
        if not os.path.exists(src_log):
            print("Source development_log.md file not found.")
            return
        
    # Copy log to each vault
    for vault in vault_paths:
        dest_log = os.path.join(vault, "laika_development_log.md")
        try:
            shutil.copy2(src_log, dest_log)
            print(f"Successfully synced to Obsidian: {dest_log}")
        except Exception as e:
            print(f"Failed to sync to {dest_log}: {e}")

if __name__ == "__main__":
    sync()
