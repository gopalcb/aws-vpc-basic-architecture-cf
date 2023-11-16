import yaml


def load_aws_cf_template(template_path='vpc_basic_template.yaml'):
    """
    load aws cloud formation yaml template
    """
    with open(template_path, 'r') as stream:
        content_dict = None
        try:
            content_dict=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            content_dict = None
            print(exc)

        return content_dict


def override_values(content_dict, pair_list):
    """
    params:
        pair_list: list of key-value pair
            ex., [{'VpcName': 'value'}, ...]

    return:
        overridden template
    """
    for pair in pair_list:
        key = pair.keys()[0]
        value = pair[key]

        # validate if required key exists in template parameters section
        param_keys = content_dict['Parameters'].keys()
        if key not in param_keys: # the required key is missing in template
            print(f'{key} is missing in template parameters')
            raise Exception(f'{key} is missing in template parameters')

        # override template parameters only
        content_dict['Parameters'][key]['Default'] = value

    return content_dict


def main():
    """
    apply template override
    """
    content_dict = load_aws_cf_template()

    # set params to override
    override_params = [
        {'VpcName': 'my-vpc2'}, {'VpcCidr': '10.0.0.0/16'}
    ]
    content_dict = override_values(content_dict, override_params)


main()