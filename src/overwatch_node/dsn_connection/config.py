import torch

from data_structures import ModelBackendConfig, ModelChatConfig, ModelConfig, ModelFrontendConfig, SubstrateConfig

default_chat_config = ModelChatConfig(
    max_session_length=8192,
    sep_token="###",
    stop_token="###",
    extra_stop_sequences=["</s>"],
    generation_params=dict(do_sample=1, temperature=0.6, top_p=0.9),
)

MODEL_FAMILIES = {
  ModelConfig(
    ModelBackendConfig(repository="Orenguteng/Llama-3.1-8B-Lexi-Uncensored-V2"),
    ModelFrontendConfig(
        name="Llama-3.1-8B-Lexi-Uncensored-V2",
        model_card="https://huggingface.co/Orenguteng/Llama-3.1-8B-Lexi-Uncensored-V2",
        license="https://bit.ly/llama3-license",
    ),
    ModelChatConfig(
        max_session_length=8192,
        sep_token="<|begin_of_text|>",
        stop_token="<|eot_id|>",
        extra_stop_sequences=None,
        generation_params=default_chat_config.generation_params,
    ),
    SubstrateConfig(subnet_id=1),
    ["/ip4/3.17.139.123/tcp/31330/p2p/12D3KooWGmoSHnvRsktrGzNTfCEwzY2TKAYPRtdaA9AwxHwLKfLa"],
  ),
}

# Set this to a list of multiaddrs to connect to a private swarm instead of the public one, for example:
INITIAL_PEERS = [
    "/ip4/3.17.139.123/tcp/31330/p2p/12D3KooWGmoSHnvRsktrGzNTfCEwzY2TKAYPRtdaA9AwxHwLKfLa"
]

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

try:
    from cpufeature import CPUFeature

    has_avx512 = CPUFeature["AVX512f"] and CPUFeature["OS_AVX512"]
except ImportError:
    has_avx512 = False

if DEVICE == "cuda":
    TORCH_DTYPE = "auto"
elif has_avx512:
    TORCH_DTYPE = torch.bfloat16
else:
    TORCH_DTYPE = torch.float32  # You can use bfloat16 in this case too, but it will be slow

STEP_TIMEOUT = 5 * 60
