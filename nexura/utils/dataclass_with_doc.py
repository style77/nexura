from dataclasses import dataclass

from simple_parsing.docstring import get_attribute_docstring, AttributeDocString
from typing import get_type_hints
from dataclasses import asdict


# https://stackoverflow.com/questions/66239221/how-to-access-a-dataclass-docstring-and-comments
def get_dataclass_attributes_doc(some_dataclass):
    def get_attribute_unified_doc(some_dataclass, key):
        """Returns a string that chains the above-comment, inline-comment and docstring """
        all_docstrings: AttributeDocString = get_attribute_docstring(some_dataclass, key)
        doc_list = asdict(all_docstrings)
        return doc_list

    attribute_docs = {}
    for key in get_type_hints(some_dataclass).keys():
        attribute_docs[key] = get_attribute_unified_doc(some_dataclass, key)
    return attribute_docs


@dataclass
class DataclassWithDoc():
    DOC = classmethod(get_dataclass_attributes_doc)
