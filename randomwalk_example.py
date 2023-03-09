import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

text_to_test = """<|endoftext|>RandomWalk
A new bot assistant named RandomWalk
- RandomWalk will give you great advice
- RandomWalk won't insult you (too much)
- RandomWalk can code!
- RandomWalk enjoys chatting, say hello! <BACKGROUND_INDEX_TOKEN> AverageRedditGPTEnjoyer
I can't believe there's a bot here <SELECTED_UTTERANCE> BotHater42
"""


if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained(r"dmayhem93/RandomWalkADC")
    model = AutoModelForCausalLM.from_pretrained(
        r"dmayhem93/RandomWalkADC",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True,
    ).cuda()
    generator = pipeline(
        "text-generation", model=model, tokenizer=tokenizer, device=0
    )  # type: TextGenerationPipeline
    items = generator(
        text_to_test, max_new_tokens=1024, num_return_sequences=2, suppress_tokens=[50257]
    )
    for item in items:
        print(item["generated_text"])
        print("------------")
