import onnxruntime_genai as og
import time
from typing import Optional
import os

def infer(conv: list, verbose: int = 1, option: Optional[int] = None):
    if not isinstance(conv, list):
        raise TypeError("conv must be a list")
    if not conv:
        raise ValueError("conv list must not be empty")
    for item in conv:
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError("Each element of the conv list must be a tuple with two elements")
    if not isinstance(verbose, int) or verbose not in {0, 1, 2}:
        raise ValueError("verbose must be an integer either 0, 1, or 2")
    
    module_dir = os.path.dirname(os.path.realpath(__file__))

    models_folder = os.path.join(module_dir, "models")
    if not os.path.exists(models_folder):
        print("The model is not currently available")
        return
    
    indices = []
    for folder_name in os.listdir(models_folder):
        if folder_name.startswith("model_"):
            index_str = folder_name.split("_")[1]
            indices.append(int(index_str))
    if not indices:
        print("The model is not currently available")
        return
    indices.sort()
    
    if option:
        if len(indices) == 1:
            if not isinstance(option, int) or option != indices[0]:
                raise ValueError(f"Only option {indices[0]} is available")
        else:
            if not isinstance(option, int) or option not in indices:
                options = ", ".join(str(i) for i in indices)
                raise ValueError(f"option must be an integer either {options}")
    else:
        option = indices[0]

    model_folder = os.path.join(models_folder, "model_"+str(option))

    started_timestamp = 0
    first_token_timestamp = 0
    model = og.Model(model_folder)

    tokenizer = og.Tokenizer(model)
    tokenizer_stream = tokenizer.create_stream()

    search_options = {}
    search_options['max_length'] = 2048

    started_timestamp = time.time()

    prompt = ''
    for c in conv:
        prompt += f'<|user|>{c[0]} <|end|>\n'
        if c[1]:
            prompt += f'<|assistant|>{c[1]} <|end|>\n'
        else:
            prompt += '<|assistant|>'

    if verbose == 2:
        print(prompt)

    input_tokens = tokenizer.encode(prompt)

    params = og.GeneratorParams(model)

    params.set_search_options(**search_options)
    params.input_ids = input_tokens
    generator = og.Generator(model, params)

    first = True
    new_tokens = []

    if verbose != 0:
        print("utilityai: \n", end='', flush=True)

    try:
        while not generator.is_done():
            generator.compute_logits()
            generator.generate_next_token()
            if first:
                first_token_timestamp = time.time()
                first = False
            new_token = generator.get_next_tokens()[0]
            if verbose != 0:
                print(tokenizer_stream.decode(new_token), end='', flush=True)
            new_tokens.append(new_token)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")

    del generator
    prompt_time = first_token_timestamp - started_timestamp
    run_time = time.time() - first_token_timestamp
    
    if verbose != 0: 
        print("\n\n")
    if verbose == 2:
        print(f"Prompt length: {len(input_tokens)}, New tokens: {len(new_tokens)}, Time to first: {(prompt_time):.2f}s, Prompt tokens per second: {len(input_tokens)/prompt_time:.2f} tps, New tokens per second: {len(new_tokens)/run_time:.2f} tps")
    
    return tokenizer.decode(new_tokens)[1:]
