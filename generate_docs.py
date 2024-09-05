from dataclasses import asdict, fields, is_dataclass, MISSING
import json
import logging
import re
import typing
from nexura.providers import nexura_provider


API_URL = "https://nexura.dev/api"


def get_docstring(obj):
    if obj.__doc__:
        return obj.__doc__.strip()
    return None


def is_field_optional(field):
    return typing.get_origin(field) is typing.Union and type(None) in typing.get_args(field)


def human_readable_list_type(_type):
    first_element = typing.get_args(_type)[0]

    all_elements_are_dataclasses = all(is_dataclass(e) for e in typing.get_args(_type))

    return "list of " + ("objects" if (is_dataclass(first_element) or all_elements_are_dataclasses) else human_readable_type(first_element))


def human_readable_dict_type(_type):
    key_element = typing.get_args(_type)[0]
    value_element = typing.get_args(_type)[1]

    return "map of " + human_readable_type(key_element) + ":" + human_readable_type(value_element)


def human_readable_type(_type):
    if _type is typing.Any:
        return "Any"
    if hasattr(_type, "__origin__"):
        origin = typing.get_origin(_type)

        if origin is typing.Union:
            return get_union_values(_type)
        if origin is typing.Literal:
            return get_literal_values(_type)
        if origin is list:
            return human_readable_list_type(_type)
        if origin is dict:
            return human_readable_dict_type(_type)

    return str(_type.__name__) if hasattr(_type, "__name__") else str(_type)


def generic_human_readable_type(_type):
    # Different than human_readable_type, return generic type instead of the detailed type
    # return string if it's string, instead of "gpt-4" for example
    if _type is typing.Any:
        return "Any"
    if hasattr(_type, "__origin__"):
        origin = typing.get_origin(_type)

        if origin is typing.Union:
            return "Union"
        if origin is typing.Literal:
            return "Literal"
        if origin is list:
            return "List"
        if origin is dict:
            return "Dict"
        if origin is str:
            return "String"
        if origin is int:
            return "Integer"

    return str(_type.__name__) if hasattr(_type, "__name__") else str(_type)


def get_union_values(_type):
    return ", ".join(human_readable_type(t) for t in typing.get_args(_type))


def get_literal_values(_type):
    return ", ".join(str(v) for v in typing.get_args(_type))


def parse_comment(comment):
    result = {
        "striped_comment": None,
        "disabled": False,
        "hidden": False,
        "additional_meta": [],
    }

    disabled_match = re.search(r'\[DISABLED(?:\s*:\s*"?([^"]*)")?\]', comment)
    hidden_match = re.search(r'\[HIDDEN(?:\s*:\s*"?([^"]*)")?\]', comment)

    if disabled_match:
        explanation = disabled_match.group(1)
        result["disabled"] = explanation.strip() if explanation else True

    if hidden_match:
        explanation = hidden_match.group(1)
        result["hidden"] = explanation.strip() if explanation else True

    beta_match = re.search(r"\[BETA\]", comment)
    if beta_match:
        result["additional_meta"].append("BETA")

    striped_comment = re.sub(r"\[.*?\]", "", comment).strip()
    result["striped_comment"] = striped_comment

    return result


def get_default_value(field):
    if field.default is not MISSING:
        return "null" if field.default is None else field.default
    elif field.default_factory is not MISSING:
        return field.default_factory
    return None


def get_dataclass_fields(dataclass_type):
    fields_info = []
    for field in fields(dataclass_type):
        field_type = field.type
        is_optional = False
        if is_field_optional(field_type):
            is_optional = True
            field_type = typing.get_args(field_type)[0]

        comment_above = dataclass_type.DOC().get(field.name, None)["comment_above"]
        comment_above = comment_above.strip()
        comment_meta = parse_comment(comment_above)

        field_info = {
            "name": field.name,
            "type": human_readable_type(field_type),
            "genericType": generic_human_readable_type(field_type),
            "description": comment_meta["striped_comment"],
            "default": get_default_value(field),
            "required": not is_optional,
            "disabled": comment_meta["disabled"],
            "hidden": comment_meta["hidden"],
            "additional_meta": comment_meta["additional_meta"],
            "values": None,
        }

        field_type_origin = typing.get_origin(field_type)
        if field_type_origin is list:
            primary_type = typing.get_args(field_type)[0]
        elif field_type_origin is dict:
            primary_type = typing.get_args(field_type)[1]
        else:
            primary_type = field_type

        if is_dataclass(primary_type):
            field_info["values"] = get_dataclass_fields(primary_type)

        if typing.get_origin(primary_type) is typing.Union:
            union_values = typing.get_args(primary_type)

            dataclass_union_values = [v for v in union_values if is_dataclass(v)]
            if len(dataclass_union_values) > 0:
                field_info["values"] = {}

            for union_value in dataclass_union_values:
                if is_dataclass(union_value):
                    field_info["values"][union_value.__name__] = get_dataclass_fields(union_value)

        fields_info.append(field_info)
    return fields_info


def get_type_as_json(func, key: str):
    return get_dataclass_fields(func.__annotations__[key])


def read_providers():
    data = {}
    for provider in nexura_provider.providers:
        if not provider.enabled:
            logging.info(f"Skipping provider {provider.id} because it is disabled")
            continue

        data[provider.id] = {
            "name": provider.name,
            "description": get_docstring(provider),
            "endpoints": {},
        }

        for path, endpoint in provider.endpoints.items():
            if not endpoint.enabled:
                logging.info(f"Skipping endpoint {endpoint.name} because it is disabled")
                continue

            data[provider.id]["endpoints"][endpoint.name] = {
                "name": endpoint.name,
                "method": endpoint.method,
                "path": path,
                "nexuraPath": f"{API_URL}/{provider.id}/{endpoint.id}",
                "category": endpoint.category,
                "description": get_docstring(endpoint),
                "original_docs_url": endpoint.original_docs_url,
                "request_type": get_type_as_json(endpoint.handle_request, "body"),
                "return_type": get_type_as_json(endpoint.handle_request, "return"),
                "examples": [asdict(example) for example in endpoint.examples],
            }

    return data


if __name__ == "__main__":
    logging.info("Generating documentation")
    data = read_providers()

    with open("docs/src/docs.json", "w") as f:
        json.dump(data, f, indent=4)
