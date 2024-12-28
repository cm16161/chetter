from setup_llama import setup_llama

# Step 1: Load the LLaMA pipeline
print("Initializing the LLaMA pipeline...")
llama_pipeline = setup_llama()

if not llama_pipeline:
    print("Failed to initialize the pipeline. Exiting.")
else:
    print("Pipeline initialized. Ready for input!")

    # Step 2: Accept new inputs dynamically
    while True:
        input_text = input("Enter your text (or type 'exit' to quit): ")
        if input_text.lower() == "exit":
            print("Exiting...")
            break

        # Generate a reply
        try:
            response = llama_pipeline(
                input_text, 
                max_length=50, 
                num_return_sequences=1, 
                truncation=True,
                temperature=0.2,
                top_p=0.9,
                #top_k=50,
                )
            print("Generated Reply:", response[0]['generated_text'])
        except Exception as e:
            print(f"Error during text generation: {e}")
