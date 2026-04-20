def get_weather(city: str) -> str:
	response = f"It's 70 degress in {city}"
	return response

def calculate(expression: str) -> str:
	return str(eval(expression))


tools = [{
	    "name": "get_weather",
	    "description": "Get current weather for a city",
	    "input_schema": {
	        "type": "object",
	        "properties": {"city": {"type": "string"}},
	        "required": ["city"]
	    }
	},
	{
	    "name": "calculator",
	    "description": "Calculate the current expression",
	    "input_schema": {
	        "type": "object",
	        "properties": {"expression": {"type": "string"}},
	        "required": ["expression"]
	    }
	}

]