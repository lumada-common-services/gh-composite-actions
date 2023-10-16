import json
import yaml
import sys
import os


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

        values_dict = json.loads(values)
        for key in values_dict:
            placeholder = f"${{{{ %s.%s }}}}" % (placeholder_type, key)
            data = data.replace(placeholder, values_dict[key])

    with open(json_file, 'w') as file:
        file.write(data)


def replace_placeholders(json_file: str):
    secrets_ctx = os.environ['SECRETS_CONTEXT']
    vars_ctx = os.environ['VARS_CONTEXT']

    replace_placeholders_in_file(json_file, secrets_ctx, 'secrets')
    replace_placeholders_in_file(json_file, vars_ctx, 'vars')


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
