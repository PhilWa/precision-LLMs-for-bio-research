import pytest
from enhance_answer import knowledge_to_prompt


def test_knowledge_to_prompt_empty():
    assert knowledge_to_prompt({}) == ""


def test_knowledge_to_prompt_no_synonyms():
    input_pairs = {
        "What": [{}],
        "is": [{}],
        "e.coli": "",
        "doing": "",
        "in": [{}],
        "cells": "",
    }
    expected_output = "What is e.coli doing in cells "
    assert knowledge_to_prompt(input_pairs) == expected_output


def test_knowledge_to_prompt_with_synonyms():
    input_pairs = {
        "What": [{}],
        "is": [{}],
        "glutamine": {
            "Metabolite_Name": "L-Glutamine",
            "HMDB_ID": "HMDB0000641",
            "KEGG_ID": "C00064",
            "ChEBI_ID": 18050.0,
            "DrugBank_ID": "DB00130",
            "CAS": "56-85-9",
            "Formula": "C5H10N2O3",
            "PathBank_ID": "SMP0000067",
        },
        "doing": "",
        "in": [{}],
        "cells": "",
    }
    expected_output = (
        "What is glutamine , also referred to as: Metabolite_Name : L-Glutamine, "
        "HMDB_ID : HMDB0000641, KEGG_ID : C00064, ChEBI_ID : 18050.0, "
        "DrugBank_ID : DB00130, CAS : 56-85-9, Formula : C5H10N2O3, "
        "PathBank_ID : SMP0000067, doing in cells "
    )
    assert knowledge_to_prompt(input_pairs) == expected_output


if __name__ == "__main__":
    pytest.main([__file__])
