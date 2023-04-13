from augment_text import augment_text
import json
import os
import time


def add_to_training_data(
    prompt: str,
    completion: str,
    fname: str = "training_data",
    augment_prompt: bool = False,
    augment_completion: bool = False,
) -> None:
    """
    Adds the given prompt and completion to the 'training_data.json' file.

    Args:
        prompt (str): The input prompt.
        completion (str): The input completion.
        fname (str): The file name or dir where the .json is saved
        augment_prompt (bool, optional): Whether to apply the augment_text function to the prompt. Defaults to False.
        augment_completion (bool, optional): Whether to apply the augment_text function to the completion. Defaults to False.
    """

    # Apply augment_text function on the inputs if specified
    if augment_prompt:
        prompt = augment_text(prompt)
    if augment_completion:
        completion = augment_text(completion)

    # Make sure prompt and completion have the required endings
    if not prompt.endswith("\n\n###\n\n"):
        prompt += " \n\n###\n\n"

    if not completion.endswith("END"):
        completion += " END"

    # Create the entry to be added to the JSON file
    entry = {"prompt": prompt, "completion": completion}

    # Load the existing JSON file, or create an empty list if the file doesn't exist
    if os.path.exists(fname):
        with open(fname, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Add the entry to the data and write it back to the JSON file
    data.append(entry)
    # Write the data back to the JSON file with the timestamp in its name
    with open(fname, "w") as f:
        json.dump(data, f, indent=2)


if False:
    prompts = [
        "What is the capital of France?",
        "What is the largest planet in our solar system?",
        "What is the smallest planet in our solar system?",
        "What is the chemical symbol for water?",
        "Which element has the atomic number 1?",
    ]

    completions = [
        "The capital of France is Paris.",
        "The largest planet in our solar system is Jupiter.",
        "The smallest planet in our solar system is Mercury.",
        "The chemical symbol for water is H2O.",
        "The element with the atomic number 1 is hydrogen.",
    ]

    # If you want to add all the prompts and completions to the JSON file, you can use a loop:
    # Get the current timestamp
    timestamp = int(time.time())
    fname = f"training_data_{timestamp}.json"
    DIR = "data/training_data"
    file_path = os.path.join(DIR, fname)

    for prompt, completion in zip(prompts, completions):
        add_to_training_data(
            prompt,
            completion,
            file_path,
            augment_prompt=True,
            augment_completion=False,
        )
