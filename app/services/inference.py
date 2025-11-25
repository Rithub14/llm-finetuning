import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from app.utils.prompt import build_prompt
from loguru import logger
import os


# ------------------------
# Device Selection
# ------------------------
if torch.backends.mps.is_available():
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"

logger.info(f"Using device: {DEVICE}")


# ------------------------
# Model Paths
# ------------------------
# Determine absolute base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Base model from HF Hub
BASE_MODEL_NAME = "google/gemma-2b-it"

# Local LoRA path (absolute)
ADAPTER_PATH = os.path.join(
    BASE_DIR,
    "model",
    "adapters",
    "gemma2b-support-lora",
    "checkpoint-939"
)
logger.info(f"Resolved ABSOLUTE ADAPTER PATH: {ADAPTER_PATH}")

# ------------------------
# Lazy Loading Globals
# ------------------------
_model = None
_tokenizer = None


# ------------------------
# Load Model + LoRA + Tokenizer
# ------------------------
def load_model():
    global _model, _tokenizer

    if _model is not None:
        return _model, _tokenizer

    logger.info("Loading base model...")
    _model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_NAME,
        torch_dtype=torch.float16 if DEVICE != "cpu" else torch.float32,
        device_map=DEVICE,
        low_cpu_mem_usage=True
    )

    logger.info("Loading tokenizer...")
    _tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_NAME)

    logger.info(f"Applying LoRA adapter from: {ADAPTER_PATH}")
    _model = PeftModel.from_pretrained(_model, ADAPTER_PATH)
    _model.eval()

    logger.success("Model + LoRA loaded successfully.")

    return _model, _tokenizer


# ------------------------
# Generate Answer
# ------------------------
def generate_answer(user_query: str) -> str:
    """
    Main inference function.
    Takes a user query string → returns an assistant response.
    """

    model, tokenizer = load_model()

    prompt = build_prompt(user_query)

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).to(DEVICE)

    with torch.no_grad():
        output_tokens = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.2,
            top_p=0.9,
            do_sample=True
        )

    output_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

    # Remove the prompt portion → return only assistant's answer
    if "<assistant>" in output_text:
        answer = output_text.split("<assistant>")[-1].strip()
    else:
        answer = output_text

    return answer
