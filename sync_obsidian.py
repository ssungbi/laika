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
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Files to sync: (local_file_name, obsidian_file_name)
    files_to_sync = [
        ("development_log.md", "개발_기록_업데이트_노트.md"),
        ("walkthrough.md", "변경_보고서_워크스루.md"),
        ("task.md", "작업_태스크_리스트.md")
    ]
    
    # Sync to each vault under '역중력프로젝트/laika'
    for vault in vault_paths:
        dest_dir = os.path.join(vault, "역중력프로젝트", "laika")
        try:
            os.makedirs(dest_dir, exist_ok=True)
            print(f"Ensured target folder exists: {dest_dir}")
        except Exception as e:
            print(f"Failed to create directory {dest_dir}: {e}")
            continue
            
        for src_name, dest_name in files_to_sync:
            src_path = os.path.join(script_dir, src_name)
            if not os.path.exists(src_path):
                src_path = src_name # try current working directory
                if not os.path.exists(src_path):
                    print(f"Source file {src_name} not found.")
                    continue
                    
            dest_path = os.path.join(dest_dir, dest_name)
            try:
                shutil.copy2(src_path, dest_path)
                print(f"Successfully synced: {src_name} -> {dest_path}")
            except Exception as e:
                print(f"Failed to sync {src_name} to {dest_path}: {e}")

if __name__ == "__main__":
    sync()
