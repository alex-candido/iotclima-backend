import re
from typing import Any, Dict, List


def parse_cli_fields(fields_str: str) -> List[Dict[str, Any]]:
    if not fields_str:
        return []

    fields = []
    field_pattern = re.compile(r'([^=;]+)=([^:]+)(?::([^;]+(?:,[^=;]+=[^,]+)*))?(?=;|$)')

    for match in field_pattern.finditer(fields_str):
        name = match.group(1).strip()
        field_type = match.group(2).strip()
        params_str = match.group(3)
        params = {}

        if params_str:
            param_regex = re.compile(r'([^=,]+)=([^,]+)')
            param_matches = param_regex.findall(params_str)

            for param_name, param_value in param_matches:
                param_name = param_name.strip()
                param_value = param_value.strip()

                if param_name.lower() == 'null':
                    params[param_name] = param_value.lower() == 'true'
                elif param_value.lower() == 'true':
                    params[param_name] = True
                elif param_value.lower() == 'false':
                    params[param_name] = False
                elif param_value.isdigit():
                    params[param_name] = int(param_value)
                else:
                    params[param_name] = param_value

        fields.append({
            "name": name,
            "type": field_type,
            "params": params
        })

    return fields