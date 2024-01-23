from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from llama_cpp import Llama
from dotenv import load_dotenv
import os
from contextlib import asynccontextmanager
from helpers import get_system_prompt
from inference import local_inference, remote_inference
from openai import OpenAI


load_dotenv()
MODEL_PATH = os.environ.get("MODEL_PATH")
LLM_INFERENCE_MODE = os.environ.get("LLM_INFERENCE_MODE")
LLM_API_URL = os.environ.get("LLM_API_URL")
LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_API_MODEL = os.environ.get("LLM_API_MODEL")

print("LLM_INFERENCE_MODE: ", LLM_INFERENCE_MODE)
print("LLM_API_URL: ", LLM_API_URL)
print("LLM_API_KEY: ", LLM_API_KEY)
print("LLM_API_MODEL: ", LLM_API_MODEL)

SYSTEM_PROMPT = get_system_prompt()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    if (LLM_INFERENCE_MODE == "local"):
        print("Loading the ML model")
        spin_up_local_llm()
    else:
        print("Using remote LLM API")
        print("LLM_API_URL: ", LLM_API_URL)
    yield
    print("Cleaning up...")
    # Release local llm model from memory...


app = FastAPI(lifespan=lifespan)

if (LLM_INFERENCE_MODE == "local"):
    # initialized in context manager above
    app.local_llm = None
elif (LLM_INFERENCE_MODE == "remote"):
    app.remote_llm_client = OpenAI(base_url=LLM_API_URL, api_key=LLM_API_KEY)


def spin_up_local_llm():
    app.local_llm = Llama(
        model_path=MODEL_PATH,
        chat_format="llama-2",
        n_gpu_layers=1,
        n_ctx=2048,
        n_batch=512,
        temp=0,
        verbose=True
    )


class InferenceInput(BaseModel):
    user_input: str


class InferenceOutput(BaseModel):
    inference_output: str


@app.post("/v1/chat/completions")
async def completion(input_data: InferenceInput):
    # Your redaction logic goes here
    res = ''
    if (LLM_INFERENCE_MODE == "local"):
        res = local_inference(
            user_input=input_data.user_input, local_llm=app.local_llm, system_prompt=SYSTEM_PROMPT)
    elif (LLM_INFERENCE_MODE == "remote"):
        res = remote_inference(
            user_input=input_data.user_input, remote_llm_client=app.remote_llm_client, system_prompt=SYSTEM_PROMPT, model_name=LLM_API_MODEL)

    return InferenceOutput(inference_output=res)
