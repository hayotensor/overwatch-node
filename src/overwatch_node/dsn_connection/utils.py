from typing import Dict, List, Tuple, Union

import torch
from subnet import AutoDistributedModelForCausalLM
from transformers import AutoTokenizer, PreTrainedModel, PreTrainedTokenizer

import config
from data_structures import ModelConfig

from pathlib import Path
import os
from dotenv import load_dotenv

import logging
logger = logging.getLogger(__name__)

load_dotenv(os.path.join(Path.cwd(), '.env'))

PRIVATE_KEY_PATH = os.getenv('PRIVATE_KEY_PATH')
RPC = os.getenv('RPC')


def load_models() -> Dict[str, Tuple[PreTrainedModel, PreTrainedTokenizer, ModelConfig]]:
    models = {}
    for family in config.MODEL_FAMILIES.values():
        for model_config in family:
            backend_config = model_config.backend
            subnet_id = model_config.substrate.subnet_id
            boostrap_peers = model_config.boostrap_peers

            logger.info(f"Loading tokenizer for {backend_config.repository}")
            tokenizer = AutoTokenizer.from_pretrained(
                backend_config.repository, 
                add_bos_token=False, 
                use_fast=False,
            )

            logger.info(
                f"Loading model {backend_config.repository} with adapter {backend_config.adapter} in {config.TORCH_DTYPE}"
            )

            # We set use_fast=False since LlamaTokenizerFast takes a long time to init
            model = AutoDistributedModelForCausalLM.from_pretrained(
                backend_config.repository,
                active_adapter=backend_config.adapter,
                torch_dtype=config.TORCH_DTYPE,
                initial_peers=boostrap_peers,
                max_retries=3,
                subnet_id=subnet_id,
                identity_path=PRIVATE_KEY_PATH,
                rpc=RPC,
            )
            
            model = model.to(config.DEVICE)

            for key in [backend_config.key] + list(backend_config.aliases):
                models[key] = model, tokenizer, backend_config
    return models


def safe_decode(tokenizer: PreTrainedTokenizer, outputs: Union[torch.Tensor, List[int]]) -> str:
    # Workaround to make SentencePiece .decode() keep leading spaces in a token
    fake_token = tokenizer("^")["input_ids"][0]
    outputs = outputs.tolist() if isinstance(outputs, torch.Tensor) else outputs
    result = tokenizer.decode([fake_token] + outputs)
    print("result", result)
    # We use .lstrip() since SentencePiece may add leading spaces, e.g. if the outputs are "</s>"
    # return result.lstrip()[1:]
    return result
