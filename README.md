# AutoGen HR Assistant Agent

My first AutoGen agent: an `AssistantAgent` with the system message "You are an HR assistant." that writes a 5-line job description for a Junior Python Developer.

## Overview

This project is the start of the AutoGen week. Instead of CrewAI's agent, task and crew setup, AutoGen uses an agent that you give a task to and run inside an async function.

| Part | What it is |
|---|---|
| Agent | `AssistantAgent` named `hr_assistant` |
| System message | `You are an HR assistant.` (exactly) |
| Model client | `OpenAIChatCompletionClient` using `gpt-4o-mini` |
| Task | A 5-line job description for a Junior Python Developer |
| Output | Printed in the terminal with `Console` |

## How it works

1. **Model client:** `OpenAIChatCompletionClient` connects the agent to OpenAI. The API key is read from the `OPENAI_API_KEY` environment variable.
2. **Agent:** `AssistantAgent` gets a name, the model client and the system message.
3. **Task text:** "5 lines" is not obvious to a model, so the task defines it explicitly: a job title as a heading, then exactly 5 numbered lines, one short sentence each, with no introduction or closing text.
4. **Async:** AutoGen runs on asyncio, so the work happens inside `async def main()` and is started with `asyncio.run(main())`.
5. **Console:** `Console(agent.run_stream(task=...))` streams the reply and prints it in the terminal.
6. **Cleanup:** `await model_client.close()` closes the client. Without it, the script can hang at the end.

## Expected output

```
---------- TextMessage (hr_assistant) ----------
Junior Python Developer
1. Write and maintain Python services alongside a senior engineer.
2. ...
3. ...
4. ...
5. ...
```

The wording can differ between runs, but the reply is always a title followed by five numbered lines.

## System message experiment

The same request was tried with different system messages to see how much the system message shapes the reply:

| System message | Effect |
|---|---|
| `You are an HR assistant.` | Balanced, professional job description |
| `You are a recruiter.` | More candidate-facing and promotional tone |
| `You are a lawyer.` | More formal, legal wording and caveats |

The final version uses `You are an HR assistant.` exactly, as the assignment requires.

## Tech stack

- Python 3.10 or newer
- AutoGen (`autogen-agentchat`, `autogen-ext[openai]`)
- OpenAI API (`gpt-4o-mini`)
- python-dotenv

## Project structure

```
hr-agent/
├── hr_agent.py    # agent, model client and async run logic
├── .gitignore     # ignores .env, venv/, __pycache__/
└── README.md
```

## Setup

1. Clone the repo and open the folder.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```
3. Install dependencies:
   ```bash
   pip install -U "autogen-agentchat" "autogen-ext[openai]" python-dotenv
   ```
4. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your-openai-key
   ```

## Run

```bash
python hr_agent.py
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `run_stream() takes 1 positional argument but 2 were given` | Pass the task as a keyword: `run_stream(task="...")` |
| API key error | Check the `.env` file name, and that the key has no quotes or spaces |
| Script hangs at the end | Make sure `await model_client.close()` is called |
| Output is not exactly 5 lines | Re-run, or tighten the wording of the task text |

## Key learnings

- A model needs "5 lines" defined in the task text, not assumed.
- The system message strongly shapes tone and content. Swapping it for a recruiter or a lawyer changes the same request noticeably.
- AutoGen is async-first, and the model client should be closed when the work is done.

## Security

The API key is read from an environment variable loaded from `.env`. The `.env` file is listed in `.gitignore`, so the key is never hard-coded or committed.