import os,sys
import yaml

def create_frogbot_config_file(change_modules_path,root_dir,repo_name,source_branch_name):

    data = [{
        'params': {
            'git': {
                'branches': [source_branch_name],
                'repoName': repo_name
            },
            'scan': {
                'projects': [
                    {
                        'workingDirs': change_modules_path
                    }
                ]
            }
        }
    }]

    # Directory
    directory = ".frogbot"
    # Path
    path = os.path.join(root_dir, directory)
    file_path = os.path.join(path, 'frogbot-config.yml')
    # Create the folder
    os.makedirs(path, exist_ok=True)
    # Write data to YAML file
    with open(file_path, 'w') as file:
        yaml.dump(data, file)
    print(f"YAML file '{file_path}' created successfully!")

def main():
    path=sys.argv[1]
    change_modules_path=path.split(', ')
    root_dir= sys.argv[2]
    repo_name = sys.argv[3]        
    source_branch_name = sys.argv[4]  
    print(root_dir)
    create_frogbot_config_file(change_modules_path,root_dir,repo_name,source_branch_name)

if __name__ == "__main__":
    main()
