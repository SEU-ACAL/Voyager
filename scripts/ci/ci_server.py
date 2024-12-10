import os
import shutil
import yaml
import argparse
import sys

def load_config(config_path=None):
    """ 加载配置文件, 默认使用脚本所在路径的 server_config.yaml。"""
    if config_path is None:
        pwd_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(pwd_dir, 'server_config.yaml')

    if not os.path.exists(config_path):
        print(f"Configuration file does not exist: {config_path}")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(f"Error parsing configuration file: {e}")
            sys.exit(1)

def copy_files(source_base, target_base, mappings):
    """ 根据映射关系复制文件或目录。"""
    for mapping in mappings:
        zipper_path = mapping.get('source')
        project_path = mapping.get('target')

        if not zipper_path or not project_path:
            print(f"Invalid mapping: {mapping}")
            continue

        source = os.path.join(source_base, zipper_path)
        target = os.path.join(target_base, project_path)

        try:
            if os.path.isdir(source):
                if os.path.exists(target):
                    shutil.rmtree(target)
                shutil.copytree(source, target)
                print(f"Copied directory: {source} -> {target}")
            elif os.path.isfile(source):
                os.makedirs(os.path.dirname(target), exist_ok=True)
                shutil.copy2(source, target)
                print(f"Copied file: {source} -> {target}")
            else:
                print(f"Source path does not exist or is invalid: {source}")
        except Exception as e:
            print(f"Failed to copy: {source} -> {target}. Error: {e}")

def join(config):
    """ 执行代码合并操作。"""
    source = config['source_repo_path']
    target = config['join_target_path']
    mappings = config.get('file_mappings', [])

    if not mappings:
        print("No file mappings defined.")
        sys.exit(1)

    os.makedirs(target, exist_ok=True)
    copy_files(source, target, mappings)
    print(f"Code has been merged to: {target}")

def main():
    parser = argparse.ArgumentParser(description="Merge code to project")
    parser.add_argument(
        'action',
        choices=['server-join'],
        help="Choose action type: 'server-join' to merge code to the test environment"
    )
    parser.add_argument(
        '--config',
        default=None,
        help="Path to configuration file (default: server_config.yaml)"
    )

    args = parser.parse_args()
    config = load_config(args.config)

    if args.action == 'server-join':
        join(config)
    else:
        print("Invalid action type.")
        sys.exit(1)

if __name__ == "__main__":
    main()