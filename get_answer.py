from transformers import pipeline, set_seed
from transformers import BioGptTokenizer, BioGptForCausalLM


def get_answer(prompt: str = "Glutamine can affect cancer metabolism by"):
    model = BioGptForCausalLM.from_pretrained("microsoft/biogpt")
    tokenizer = BioGptTokenizer.from_pretrained("microsoft/biogpt")
    generator = pipeline("text-generation", model=model, tokenizer=tokenizer)
    set_seed(42)
    # prompt = "Glutamine can affect cancer metabolism by"
    return generator(prompt, max_length=100, num_return_sequences=1, do_sample=True)
