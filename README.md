### Learning about Agent loops

#### Example - 
Turn 3 ("And what is that result times 100"): the agent called calculator with the right input, presumably 25 * 100. It correctly inferred "that result" referred to 25 from turn 2's tool_result. Good.

Turn 4 ("What was the original question?"): the agent did NOT call any tool. It just answered from message history. Stop reason end_turn, content blocks ['text']. Cost: 17 output tokens.

**System prompt says "do not compute answers yourself"** — but Claude answered "what was the original question" from the message history without consulting any tool. Strictly speaking, that violates the prompt. Loosely speaking, it's the right behavior because there's no tool that could answer it and the answer is in context.
So the system prompt has two failure modes I've now empirically observed:

Information leakage from priors
Information from prior context that no tool could provide

Both are technically "computing answers without tools." Both are also reasonable agent behavior. The lesson: soft prompts are guidelines the model interprets, not rules it enforces. We cannot prompt our way to deterministic guarantees. If we need a guarantee, you need code-level enforcement (e.g., refuse to print any final response that didn't have ≥1 successful tool call) — and even that is brittle.