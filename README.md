# Local LLM API

Allows to easily run local REST API with a custom LLM, running locally or remotely, with user defined system instructions.

Useful for quick local autmations that require problem solving with large langague models and interaction via a REST API.

## Installation with local inference

Requirements:

- Apple Silicon Machine with at least 16GB RAM (M1/M2/M3)
  - OR an Nvidia CUDA GPU
- Locally downloaded LLAMA Compatible GGUF model
  - [Download Mistral-7B-Instruct Q8.0](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/tree/main)

### Setup

#### Run the following in the terminal

For Apple Silicon

```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install -r requirements.txt
```

For CUDA:

```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install -r requirements.txt
```

#### Setup the env config:

Update the `system_prompt.txt` with instructions of your choice

rename `.env.example` to `.env`

Modify the `MODEL_PATH` var to point it to your locally downloaded `gguf` file

#### Run the web server:

```bash
uvicorn main:app
```

Inference endpoint is available at: `http://127.0.0.1:8000/v1/chat/completions`

Make a `POST` request with a JSON body containing your input

CURL Example:

```bash
curl --location 'http://127.0.0.1:8000/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data-raw '{
  "user_input": "YOU INPUT HERE"
}'

```

## Remote inference with a OpenAI compatible API

In `.env`, set inference mode to `remote`:

```
LLM_INFERENCE_MODE = 'remote'
```

Define the remote server configuration:

```
LLM_API_URL = 'https://api.openai.com/v1/'
LLM_API_KEY = 'YOUR_KEY'
LLM_MODEL = 'gpt-3.5-turbo'
```

## Test example

`system_prompt.txt`:

```
You are a code redactoring expert that takes user input code in any language, and refactors all function parameters called `user` to DEPRECATED_user.
---EXAMPLES---
Example input:
UpdateUser(user: newUserParams)

Example output:
UpdateUser(DEPRECATED_user: newUserParams)
---
Respond only with refactored code output and nothing else.

```

```bash
curl --location 'http://127.0.0.1:8000/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data-raw '{
  "user_input": "UpdateUser(user: newUserParams)\ndeleteUser(user: user)\ncreateUser({user: {...userParams}})"
}'
```

Response JSON:

```json
{
  "inference_output": " UpdateUser(DEPRECATED_user: newUserParams)\ndeleteUser(DEPRECATED_user: DEPRECATED_user)\ncreateUser({DEPRECATED_user: {...newUserParams}})"
}
```

---

Author: Vatsaev Aslan (@avatsaev)
