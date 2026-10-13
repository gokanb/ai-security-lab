import ollama

# Stores the whole conversation so the AI can "remember"
history = []

while True:
    question = input("You: ")

    if question == "quit":
        break

    # Add your message to the conversation
    history.append({"role": "user", "content": question})

    # Send the WHOLE conversation, not just the last message
    response = ollama.chat(
        model="llama3.2",
        messages=history
    )

    answer = response["message"]["content"]

    # Save the AI's reply so it remembers what it said
    history.append({"role": "assistant", "content": answer})

    print("AI:", answer)