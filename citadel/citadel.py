import json
import yaml
import sys
import os
import logging
import subprocess
import re

def deep_merge_lists(original, incoming):
    """
    Deep merge two lists. Modifies original.
    Recursively call deep merge on each correlated element of list.
    If item type in both elements are
     a. dict: Call deep_merge_dicts on both values.
     b. list: Recursively call deep_merge_lists on both values.
     c. any other type: Value is overridden.
     d. conflicting types: Value is overridden.

    If length of incoming list is more that of original then extra values are appended.
    """
    common_length = min(len(original), len(incoming))
    for idx in range(common_length):
        if isinstance(original[idx], dict) and isinstance(incoming[idx], dict):
            deep_merge_dicts(original[idx], incoming[idx])

        elif isinstance(original[idx], list) and isinstance(incoming[idx], list):
            deep_merge_lists(original[idx], incoming[idx])

        else:
            original[idx] = incoming[idx]

    for idx in range(common_length, len(incoming)):
        original.append(incoming[idx])


def deep_merge_dicts(original, incoming):
    """
    Deep merge two dictionaries. Modifies original.
    For key conflicts if both values are:
     a. dict: Recursively call deep_merge_dicts on both values.
     b. list: Call deep_merge_lists on both values.
     c. any other type: Value is overridden.
     d. conflicting types: Value is overridden.

    """
    for key in incoming:
        if key in original:
            if isinstance(original[key], dict) and isinstance(incoming[key], dict):
                deep_merge_dicts(original[key], incoming[key])

            elif isinstance(original[key], list) and isinstance(incoming[key], list):
                deep_merge_lists(original[key], incoming[key])

            else:
                original[key] = incoming[key]
        else:
            original[key] = incoming[key]

    return original


def get_data_structure(original_data, end_dic):
    return deep_merge_dicts(original_data, end_dic)


def get_project_data(path_value: str, projects_data, config_data):
    if projects_data is None:
        return config_data

    data = list(filter(lambda d: d['path'] in [path_value], projects_data))
    if len(data) == 0:
        print("Can't determine which path to apply for the given path value")
        return config_data

    data = data[0]
    del data['path']

    return get_data_structure(config_data, data)


def replace_placeholders_in_file(json_file: str, values: str, placeholder_type: str):
    with open(json_file, 'r') as file:
        data = file.read()

        # Replace placeholders in JSON data with provided values
        values_dict = json.loads(values)
        for key in values_dict:
            placeholder = f"${{{{ %s.%s }}}}" % (placeholder_type, key)
            data = data.replace(placeholder, values_dict[key]) 
    
    # Write the modified JSON data back to the file
    with open(json_file, 'w') as file:
        file.write(data)


def get_artifact_info_json(build_name, build_number, rt_auth=(None, None), rt_base_url=None, jf_cli_rt_name=None, build_suffix=None):
   
    # adding artifactory cli config
    logging.info(f'Adding artifactory CLI name {jf_cli_rt_name}')

    # Define the command and arguments
    command = [
        'jf', 'config', 'add', f'{jf_cli_rt_name}',
        '--interactive=false', '--enc-password=false', '--basic-auth-only',
        '--artifactory-url', f'{rt_base_url}/',
        '--user', f'{rt_auth[0]}',
        '--password', f'{rt_auth[1]}'
    ]
    # Execute the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    logging.debug(result)

    # Define jf command and arguments
    command = ['jf', 'rt', 'search', '--server-id', f'{jf_cli_rt_name}', '--props',
               f'build.name={build_name};build.number={build_number}',
               f'*-{build_suffix}.zip']

    output_file = 'artifacts.json'

    # Execute the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # log result
    logging.debug(f'jf execution result {result}')

    # Parse the command output as JSON
    output_json = json.loads(result.stdout)

    # Save the JSON object to a file
    with open(output_file, 'w') as file:
        json.dump(output_json, file, indent=4)

    logging.debug(f'Artifacts in artifactory with build.name={build_name};build.number={build_number}: {output_json}')

    return output_json, set([artifact['path'].split('/')[-1] for artifact in output_json])


def fetch_plugin_names(manifest_file=None):
    with open(manifest_file, 'r') as file:
        yaml_data = yaml.safe_load(file)

    plugin_files_with_version = set()
    plugin_files_without_version = set()

    def extract_plugins(data):
        if isinstance(data, dict):
            for value in data.values():
                if isinstance(value, list):
                    # If the value is a list, it contains plugin file names
                    for plugin_file in value:
                        # Extract plugin name with version number using regex
                        plugin_files_with_version.add(plugin_file)
                        # Extract plugin name without version number using regex
                        plugin_name = re.match(r'(.+?)(?:-\d+(\.\d+)*-\d+)?\.zip', plugin_file).group(1)
                        plugin_files_without_version.add(plugin_name)
                elif isinstance(value, dict):
                    # If the value is a dictionary, recursively search for plugins
                    extract_plugins(value)

    extract_plugins(yaml_data)

    # Join the plugin files lists using commas
    return (
        ','.join(plugin_files_with_version),
        ','.join(plugin_files_without_version)
    )


def find_full_zip_path(file_names, data):
    full_paths = []
    for file_name in file_names:
        for item in data:
            file_path = item.get('path', '')
            if file_name.strip() in file_path:
                full_paths.append(file_path)
                break  # Break the loop once the file is found to avoid unnecessary iterations
    return ','.join(full_paths)
   

def update_project_info_section(json_file: str, updates: dict):
    with open(json_file, 'r') as file:
        data = file.read()

        # Update JSON data with the provided updates
        json_data = json.loads(data)
        project_info = json_data.get("project-info", [])
        if not project_info:
            print("No 'project-info' key found in the JSON file.")
            return

        project_info_entry = project_info[0]
        for key, value in updates.items():
            if key in project_info_entry:
                if project_info_entry[key] == f'${key}':
                    if isinstance(value, list):
                        value = ','.join(value)  # Join multiple values with commas
                    project_info_entry[key] = value
                    print(f"Updated '{key}', value - '{value}'")
                else:
                    print(f"Key '{key}' will not be updated, as it not have a expected placeholder '${key}' in citadel config file.")
        
    # Write the modified JSON data back to the file
    with open(json_file, 'w') as file:
        file.write(json.dumps(json_data))


def replace_placeholders(json_file: str):
    secrets_ctx = os.environ['SECRETS_CONTEXT']
    vars_ctx = os.environ['VARS_CONTEXT']

    codedx_branch = sys.argv[5] if sys.argv[5] != "" else "null"
    org = sys.argv[6] if sys.argv[6] != "" else "null"
    repo_paths_branch = sys.argv[7] if sys.argv[7] != "" else "null"
     
    build_name = sys.argv[10]  # for rt buildinfo query
    build_number = sys.argv[11] # for rt buildinfo query
    build_version = sys.argv[12]
    rt_auth = (sys.argv[13], sys.argv[14])
    rt_base_url = sys.argv[15]
    jf_cli_rt_name = sys.argv[16] if sys.argv[16] != "" else "artifactory"
    logging_level = sys.argv[17] if sys.argv[17] != "" else "INFO"
    manifest_file_path = sys.argv[18]
 
    if manifest_file_path:

        print("Fetching Artifact URLs using manifest file")

        ######### logging ############
        string_to_level = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }

        logging.basicConfig(
            level=string_to_level[logging_level],
            format='[%(asctime)s] [%(filename)s:%(lineno)d] %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )

        ####### End of logging #######

        build_suffix = build_version + '-' + build_number

        # downloads artifacts
        builds_output_json, artifacts_in_build_info = get_artifact_info_json(build_name, build_number, rt_auth=rt_auth,
                                                                         rt_base_url=rt_base_url,
                                                                         jf_cli_rt_name=jf_cli_rt_name,
                                                                         build_suffix=build_suffix)
        
        # Fetch plugins_names using manifest
        plugins_names, plugins_names_only = fetch_plugin_names(manifest_file=manifest_file_path)
        print("Plugins Names", plugins_names_only)

        # Fetch Artifact URLs using manifest
        file_names = plugins_names.split(',')
        full_zip_path = find_full_zip_path(file_names, builds_output_json)
        print("plugins Zip paths:", full_zip_path)
        repo_paths_includes = plugins_names_only if plugins_names_only != "" else "null"
        artifact_url = full_zip_path if full_zip_path != "" else "null"
             
    else:
        # If a manifest file is not provided, check whether environmental variables ARTIFACT_URLS and REPO_PATHS_INCLUDES are present
        # If empty, set null values
        repo_paths_includes = sys.argv[8] if sys.argv[8] != "" else "null"
        artifact_url =sys.argv[9] if sys.argv[9] != "" else "null"

    updates = {
        "branch": codedx_branch,
        "org": org,
        "repoPathsandBranch": repo_paths_branch,
        "repoPathsIncludes": repo_paths_includes.split(','),  # Split comma-separated values into a list
        "artifactURL": artifact_url.split(',')  # Split comma-separated values into a list
    }

    replace_placeholders_in_file(json_file, secrets_ctx, 'secrets')
    replace_placeholders_in_file(json_file, vars_ctx, 'vars')
    update_project_info_section(json_file, updates)


def main():
    config_path = sys.argv[1]
    project_path = sys.argv[2]

    wf_name = sys.argv[3]  # gives us the ref path to the workflow. For example,
    # "octocat/hello-world/.github/workflows/my-workflow.yml@refs/heads/my_branch".
    wf_name = wf_name[0:wf_name.index("@")]  # discard everything after the '@'
    wf_name = wf_name[wf_name.rindex("/") + 1:len(wf_name)]  # discard everything before the last '/'

    citadel_temp_file_location = sys.argv[4]

    with open(config_path, 'r') as citadel_config_file:
        citadel_config_contents = yaml.safe_load(citadel_config_file)

    # defaults
    config_data = get_data_structure(citadel_config_contents['defaults'], dict())

    # Project level
    if 'projects' in citadel_config_contents:
        config_data = get_project_data(project_path, citadel_config_contents['projects'], config_data)

    # workflow type
    if wf_name in citadel_config_contents:
        wf_type_data = citadel_config_contents[wf_name]

        if wf_type_data is not None and 'projects' in wf_type_data:
            config_data = get_project_data(project_path, wf_type_data['projects'], config_data)
        else:
            print(f"No projects overwrites defined for %s" % wf_name)

    with open(citadel_temp_file_location + "/citadel.json", "w") as outfile:
        outfile.write(json.dumps(config_data))

    replace_placeholders(citadel_temp_file_location + "/citadel.json")


if __name__ == "__main__":
    main()
