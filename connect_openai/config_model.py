import re

groups = {
    "model_temperature": {
        0.1: ["protocol", "method", "list", "report"],
        0.7: ["explore", "envision"],
    },
    "model_type": {
        "gpt-3.5-turbo": [
            "gpt-3.5",
        ],
        "gpt-4": [
            "gpt-4",
        ],
    },
    "biology": {
        # Ideally we want to do a similiarty based classification of topics
        "microbiology": ["e.coli", "escherichia coli", "bacteria", "microbiology"],
        "cancer": ["oncology", "tumor", "cancer"],
        "neurobiology": ["neurobiology", "neuron"],
    },
}
# Function to process the sentence and extract keywords
def extract_keywords(sentence: str, groups: dict):
    # Here we need a dict with subgroups:
    keywords = []
    for group in groups.values():
        for subgroup in group.values():
            for keyword in subgroup:
                if re.search(r"\b" + keyword + r"\b", sentence, re.IGNORECASE):
                    keywords.append(keyword)
    return keywords


# Function to map extracted keywords to their respective groups and subgroups
def map_keywords_to_groups(keywords, groups):
    mapped_groups = {}
    for keyword in keywords:
        for group_name, group in groups.items():
            for subgroup_name, subgroup_keywords in group.items():
                if keyword in subgroup_keywords:
                    if group_name not in mapped_groups:
                        mapped_groups[group_name] = {}
                    if subgroup_name not in mapped_groups[group_name]:
                        mapped_groups[group_name][subgroup_name] = []
                    mapped_groups[group_name][subgroup_name].append(keyword)
    return mapped_groups


def convert_sentence_to_config(sentence: str, groups):

    default_params = {
        "model_temperature": 0.5,
        "model_type": "gpt-3.5-turbo",
        "biology": "general",
    }

    # Extract keywords and map them to groups and subgroups
    keywords = extract_keywords(sentence, groups)
    # Define groups, subgroups, and keywords
    # To be replaced with embeddings
    mapped_groups = map_keywords_to_groups(keywords, groups)
    return get_model_params(mapped_groups, default_params)


def get_model_params(mapped_groups, default_params):
    for k, v in default_params.items():
        if isinstance(mapped_groups.get(k), dict):
            default_params[k] = next(iter(mapped_groups.get(k)))
    return default_params
