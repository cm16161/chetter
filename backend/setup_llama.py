import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoConfig
from huggingface_hub import login

import torch
from transformers import pipeline

def setup_llama(model_id="meta-llama/Llama-3.2-1B-Instruct", torch_dtype=torch.bfloat16, device_map="auto"):
    print("Ensure you have logged into huggingface-cli (with a token) before accessing gated models.")

        # Test access to the model
    print("Checking access to the model...")
    try:
        config = AutoConfig.from_pretrained(model_id)
        print(f"Successfully accessed model configuration for {model_id}")
    except Exception as e:
        print(f"Error accessing model configuration for {model_id}: {e}")
        return None

    # Download the model and tokenizer
    print("Downloading model and tokenizer...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch_dtype, device_map=device_map)
    except Exception as e:
        print(f"Error downloading model or tokenizer: {e}")
        return None

    # Initialize pipeline
    print("Initializing text-generation pipeline...")
    try:
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            pad_token_id=tokenizer.pad_token_id,
            torch_dtype=torch_dtype,
            device_map=device_map,
            #pad_token_id=tokenizer.eos_token_id  # Explicitly set pad_token_id
        )
        print("Setup complete. The pipeline is ready to use!")
        return pipe
    except Exception as e:
        print(f"Error initializing text-generation pipeline: {e}")
        return None

if __name__ == "__main__":
    llama_pipeline = setup_llama()

    if llama_pipeline:
        # Test the pipeline with a sample input
        try:
            input = "Is Trump the skibbidiest of them all?"
            print(f'Test input: {input}')

            prompt = [
                {"role": "system", "content": "You are a helpful assistant, that responds as a pirate. Respond in 50 words or fewer"},
                {"role": "user", "content": input},
            ]
            
            response = llama_pipeline(
                prompt, 
                truncation=True, # Works like max_length, in this case prevents exceeding the max context window of the model - this is good for robustness
                num_return_sequences=1, # Sets the number of responses e.g. top 1 responses, top 3, etc. In the case of a chatbot, we only need 1
                # Set do_sample=False if you want deterministic, predictable outputs (e.g., summarization or single-answer tasks).
                # Set do_sample=True if you want creative, diverse responses (e.g., storytelling, open-ended chat) - the model then samples tokens from a PD curve rather than taking the most likely responses
                do_sample=True,
                top_p=0.9, # Assigns probability distribution to token selection i.e. scales the creativity of the response by selecting more tokens on the PD curve - works in tandem with do_sample=True, the lower the figure only the deterministic tokens are selected, and the higher the figure more creative tokens are selected as well (between the range 0<n<=1)
                temperature=1.0, # Higher the value, more it smooths the PD curve i.e. increases chances for more creative tokens to be selected 
                max_new_tokens=256,
                )

            print(f"Response: {response[0]['generated_text']}")
        except Exception as e:
            print(f"Error during text generation: {e}")
    else:
        print("Pipeline setup failed.")