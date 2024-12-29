from setup_llama import setup_llama

# Step 1: Load the LLaMA pipeline
print("Initializing the LLaMA pipeline...")
llama_pipeline = setup_llama()

if not llama_pipeline:
    print("Failed to initialize the pipeline. Exiting.")
else:
    print("Pipeline initialized. Ready for input!")
    
    # Step 2: Initialize conversation history
    conversation_history = [
        {"role": "system", "content": "You are a pirate chatbot. Respond in pirate speak in 50 words or less. Make controversial statements."}
    ]
    
    # Step 3: Accept new inputs dynamically
    while True:
        input_text = input("Enter your text (or type 'exit' to quit): ")
        if input_text.lower() == "exit":
            print("Exiting...")
            break

        # Append the user's input to the conversation history
        conversation_history.append({"role": "user", "content": input_text})

        # Generate a reply
        try:
            response = llama_pipeline(
                conversation_history,
                truncation=True,
                num_return_sequences=1,
                do_sample=True,
                top_p=0.9,
                temperature=1.0,
                max_new_tokens=256,
            )
            
            # Extract and print the generated response
            reply = response[0]['generated_text']
            print("Generated Reply:", reply)

            # Add the assistant's reply to the conversation history
            conversation_history.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"Error during text generation: {e}")