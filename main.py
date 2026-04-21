import anthropic
from tools import tools, get_weather, calculate
from prompts import SYSTEM_PROMPT

client = anthropic.Anthropic()

MAX_ITER = 5
END_TURN = "end_turn"
TOOL_USE = "tool_use"
tool_functions = {
	"get_weather": get_weather,
	"calculator": calculate,
}

messages = []

while True:
	user_prompt = input("You: ")
	if user_prompt.lower() == "exit":
		break
	messages.append({"role": "user", "content": user_prompt})

	for i in range(MAX_ITER):
		response = client.messages.create(
			model="claude-sonnet-4-5",
			max_tokens=1024,
			tools=tools,
			messages=messages,
			system=SYSTEM_PROMPT
		)
		print(f"Messages: {len(messages)}, input tokens: {response.usage.input_tokens}, output tokens: {response.usage.output_tokens}")
		messages.append({"role": "assistant", "content": response.content})

		if response.stop_reason == END_TURN:
			break
		if response.stop_reason == TOOL_USE:
			tool_results = []
			for block in response.content:
				if block.type == TOOL_USE:
					result = None
					if block.name in tool_functions:
						print(f"Using tool: {block.name}")
						try:
							result = tool_functions[block.name](**block.input)
						except Exception as e:
							result = f"Error: {e}"
					else:
						result = f"Unknown tool: {block.name}"
					tool_results.append({
						"type": "tool_result",
						"tool_use_id": block.id,
						"content": result
					})

			messages.append({"role": "user", "content": tool_results})
	text_parts = [b.text for b in response.content if b.type == "text"]
	final_text = "\n".join(text_parts) if text_parts else "(no text response)"
	print(f"Assistant: {final_text}")
