import anthropic
from tools import tools, get_weather, calculate

client = anthropic.Anthropic()

MAX_ITER = 5
END_TURN = "end_turn"
TOOL_USE = "tool_use"
tool_functions = {
	"get_weather": get_weather,
	"calculator": calculate,
}
messages = [{"role": "user", "content": "What's the weather in Mumbai, and what's 4234327 times 45433244?"}]

for i in range(MAX_ITER):
	print(f"==== Turn {i} =====")
	print(f"Messages so far: {len(messages)}")
	response = client.messages.create(
	    model="claude-sonnet-4-5",
	    max_tokens=1024,
	    tools=tools,
	    messages=messages
	    # system="You must ONLY use the provided tools to answer questions. If a tool fails or is unavailable, explicitly say you cannot answer. Do not compute answers yourself."
	)
	print(f"Stop reason: {response.stop_reason}")
	print(f"Content blocks: {[b.type for b in response.content]}")
	messages.append({"role": "assistant", "content": response.content})

	if response.stop_reason == END_TURN:
		break
	if response.stop_reason == TOOL_USE:
		tool_results = []
		for block in response.content:
			if block.type == TOOL_USE:
				result = None
				if block.name in tool_functions:
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
print(response)
