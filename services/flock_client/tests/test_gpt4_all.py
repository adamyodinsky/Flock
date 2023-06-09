from gpt4all import GPT4All

gpt = GPT4All(
    model_name="ggml-gpt4all-l13b-snoozy",
    model_path="/Users/adamyodinsky/.flock/models/",
    model_type="llama",
)

messages = []

while True:
    user_input = input("\nUser: ")

    config = {
        "temp": 0.28,
        "top_p": 0.95,
        "top_k": 40,
        "repeat_penalty": 1.1,
    }

    message_obj = {"role": "user", "content": user_input}
    messages.append(message_obj)

    answer = gpt.chat_completion(messages, verbose=False, **config)
    bot_message = answer.get("choices", [{}])[0].get("message", {}).get("content", "")
    print(f"\nBot:\n{bot_message}")
