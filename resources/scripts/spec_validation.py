import os
import json
from yaml import safe_load


def load_config(path:str, base_path:str='resource/configurations'):
    """Helper function that loads configuration file"""
    with open(f"{base_path}/{path}", "r", encoding="utf-8") as conf:
        config = safe_load(conf)
    return config

def key_exists(spec, key_string):
    try:
        result = eval("spec" + key_string, {'spec': spec})
        if result:
            return result
        else:
            raise Exception
    except Exception:
        return f'Required {key_string} key is missing from spec'


FINANCE_ANALIST_CPU_LIMIT = 30

def validate_data_product_spec():
    # Load spec
    spec = json.loads(
        os.environ.get("DATA_PRODUCT_SPEC")
    )

    # Keys check
    owner = key_exists(spec, "['info']['owner']")
    cpus = key_exists(spec, "['transform']['cpus']")

    # Types check
    assert isinstance(float(cpus), float), f"CPUs ({cpus}) cannot be interpreted as a float"
    assert owner in ['finance_analist', 'finance_scientist', 'finance_engineer'], f"Role {owner} does not exist" 
    
    # Conditional checks
    try:
        if owner == 'finance_analist' and float(cpus) > FINANCE_ANALIST_CPU_LIMIT:
            return f'The {spec['info']['owner']} role has a limit of {FINANCE_ANALIST_CPU_LIMIT} CPUs'
    except Exception as e:
        return f"Validation failed: {repr(e)}"

    return True


print(f'validity={validate_data_product_spec()}')