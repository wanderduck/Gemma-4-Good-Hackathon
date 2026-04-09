Converting to GGUF (q4_k_m)...
INFO:hf-to-gguf:Loading model: merged
INFO:hf-to-gguf:Model architecture: Gemma4ForConditionalGeneration
INFO:hf-to-gguf:gguf: indexing model part 'model.safetensors'
INFO:gguf.gguf_writer:gguf: This GGUF file is for Little Endian only
INFO:hf-to-gguf:Exporting model...
INFO:hf-to-gguf:rope_freqs.weight,                 torch.float32 --> F32, shape = {256}
INFO:hf-to-gguf:token_embd.weight,                 torch.bfloat16 --> F16, shape = {2560, 262144}
INFO:hf-to-gguf:per_layer_token_embd.weight,       torch.bfloat16 --> F16, shape = {10752, 262144}
INFO:hf-to-gguf:blk.0.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.0.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.0.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.0.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.0.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.0.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.0.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.0.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.0.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.0.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.0.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.0.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.0.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.0.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.0.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.0.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.0.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.1.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.1.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.1.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.1.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.1.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.1.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.1.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.1.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.1.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.1.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.1.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.1.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.1.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.1.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.1.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.1.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.1.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.10.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.10.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.10.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.10.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.10.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.10.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.10.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.10.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.10.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.10.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.10.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.10.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.10.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.10.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.10.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.10.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.10.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.11.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.11.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.11.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.11.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.11.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.11.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.11.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.11.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.11.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.11.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.11.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.11.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.11.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.11.attn_output.weight,         torch.bfloat16 --> F16, shape = {4096, 2560}
INFO:hf-to-gguf:blk.11.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.11.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 4096}
INFO:hf-to-gguf:blk.11.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.12.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.12.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.12.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.12.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.12.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.12.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.12.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.12.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.12.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.12.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.12.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.12.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.12.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.12.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.12.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.12.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.12.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.13.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.13.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.13.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.13.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.13.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.13.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.13.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.13.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.13.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.13.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.13.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.13.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.13.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.13.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.13.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.13.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.13.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.14.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.14.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.14.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.14.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.14.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.14.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.14.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.14.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.14.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.14.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.14.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.14.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.14.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.14.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.14.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.14.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.14.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.15.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.15.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.15.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.15.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.15.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.15.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.15.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.15.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.15.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.15.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.15.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.15.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.15.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.15.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.15.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.15.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.15.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.16.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.16.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.16.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.16.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.16.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.16.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.16.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.16.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.16.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.16.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.16.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.16.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.16.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.16.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.16.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.16.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.16.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.17.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.17.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.17.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.17.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.17.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.17.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.17.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.17.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.17.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.17.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.17.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.17.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.17.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.17.attn_output.weight,         torch.bfloat16 --> F16, shape = {4096, 2560}
INFO:hf-to-gguf:blk.17.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.17.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 4096}
INFO:hf-to-gguf:blk.17.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.18.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.18.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.18.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.18.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.18.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.18.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.18.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.18.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.18.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.18.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.18.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.18.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.18.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.18.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.18.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.18.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.18.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.19.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.19.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.19.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.19.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.19.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.19.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.19.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.19.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.19.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.19.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.19.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.19.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.19.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.19.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.19.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.19.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.19.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.2.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.2.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.2.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.2.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.2.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.2.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.2.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.2.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.2.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.2.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.2.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.2.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.2.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.2.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.2.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.2.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.2.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.20.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.20.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.20.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.20.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.20.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.20.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.20.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.20.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.20.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.20.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.20.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.20.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.20.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.20.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.20.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.20.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.20.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.21.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.21.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.21.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.21.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.21.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.21.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.21.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.21.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.21.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.21.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.21.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.21.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.21.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.21.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.21.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.21.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.21.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.22.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.22.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.22.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.22.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.22.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.22.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.22.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.22.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.22.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.22.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.22.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.22.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.22.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.22.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.22.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.22.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.22.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.23.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.23.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.23.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.23.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.23.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.23.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.23.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.23.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.23.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.23.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.23.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.23.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.23.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.23.attn_output.weight,         torch.bfloat16 --> F16, shape = {4096, 2560}
INFO:hf-to-gguf:blk.23.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.23.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 4096}
INFO:hf-to-gguf:blk.23.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.24.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.24.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.24.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.24.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.24.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.24.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.24.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.24.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.24.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.24.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.24.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.24.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.24.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.24.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.24.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.24.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.24.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.25.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.25.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.25.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.25.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.25.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.25.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.25.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.25.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.25.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.25.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.25.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.25.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.25.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.25.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.25.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.25.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.25.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.26.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.26.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.26.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.26.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.26.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.26.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.26.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.26.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.26.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.26.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.26.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.26.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.26.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.26.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.26.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.26.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.26.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.27.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.27.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.27.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.27.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.27.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.27.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.27.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.27.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.27.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.27.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.27.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.27.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.27.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.27.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.27.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.27.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.27.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.28.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.28.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.28.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.28.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.28.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.28.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.28.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.28.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.28.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.28.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.28.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.28.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.28.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.28.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.28.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.28.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.28.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.29.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.29.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.29.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.29.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.29.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.29.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.29.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.29.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.29.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.29.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.29.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.29.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.29.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.29.attn_output.weight,         torch.bfloat16 --> F16, shape = {4096, 2560}
INFO:hf-to-gguf:blk.29.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.29.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 4096}
INFO:hf-to-gguf:blk.29.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.3.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.3.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.3.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.3.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.3.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.3.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.3.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.3.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.3.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.3.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.3.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.3.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.3.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.3.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.3.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.3.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.3.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.30.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.30.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.30.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.30.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.30.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.30.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.30.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.30.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.30.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.30.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.30.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.30.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.30.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.30.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.30.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.30.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.30.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.31.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.31.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.31.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.31.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.31.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.31.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.31.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.31.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.31.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.31.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.31.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.31.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.31.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.31.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.31.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.31.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.31.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.32.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.32.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.32.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.32.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.32.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.32.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.32.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.32.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.32.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.32.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.32.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.32.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.32.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.32.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.32.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.32.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.32.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.33.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.33.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.33.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.33.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.33.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.33.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.33.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.33.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.33.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.33.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.33.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.33.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.33.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.33.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.33.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.33.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.33.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.34.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.34.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.34.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.34.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.34.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.34.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.34.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.34.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.34.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.34.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.34.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.34.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.34.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.34.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.34.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.34.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.34.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.35.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.35.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.35.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.35.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.35.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.35.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.35.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.35.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.35.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.35.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.35.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.35.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.35.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.35.attn_output.weight,         torch.bfloat16 --> F16, shape = {4096, 2560}
INFO:hf-to-gguf:blk.35.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.35.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 4096}
INFO:hf-to-gguf:blk.35.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.36.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.36.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.36.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.36.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.36.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.36.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.36.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.36.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.36.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.36.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.36.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.36.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.36.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.36.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.36.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.36.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.36.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.37.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.37.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.37.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.37.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.37.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.37.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.37.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.37.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.37.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.37.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.37.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.37.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.37.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.37.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.37.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.37.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.37.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.38.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.38.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.38.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.38.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.38.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.38.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.38.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.38.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.38.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.38.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.38.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.38.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.38.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.38.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.38.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.38.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.38.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.39.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.39.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.39.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.39.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.39.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.39.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.39.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.39.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.39.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.39.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.39.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.39.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.39.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.39.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.39.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.39.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.39.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.4.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.4.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.4.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.4.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.4.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.4.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.4.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.4.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.4.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.4.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.4.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.4.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.4.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.4.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.4.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.4.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.4.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.40.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.40.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.40.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.40.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.40.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.40.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.40.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.40.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.40.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.40.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.40.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.40.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.40.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.40.attn_output.weight,         torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.40.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.40.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.40.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.41.attn_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.41.layer_output_scale.weight,  torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.41.ffn_down.weight,            torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.41.ffn_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.41.ffn_up.weight,              torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.41.inp_gate.weight,            torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.41.proj.weight,                torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.41.post_attention_norm.weight, torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.41.post_ffw_norm.weight,       torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.41.post_norm.weight,           torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.41.ffn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.41.attn_k_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.41.attn_k.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.41.attn_output.weight,         torch.bfloat16 --> F16, shape = {4096, 2560}
INFO:hf-to-gguf:blk.41.attn_q_norm.weight,         torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.41.attn_q.weight,              torch.bfloat16 --> F16, shape = {2560, 4096}
INFO:hf-to-gguf:blk.41.attn_v.weight,              torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.5.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.5.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.5.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.5.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.5.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.5.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.5.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.5.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.5.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.5.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.5.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.5.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.5.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.5.attn_output.weight,          torch.bfloat16 --> F16, shape = {4096, 2560}
INFO:hf-to-gguf:blk.5.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {512}
INFO:hf-to-gguf:blk.5.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 4096}
INFO:hf-to-gguf:blk.5.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 1024}
INFO:hf-to-gguf:blk.6.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.6.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.6.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.6.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.6.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.6.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.6.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.6.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.6.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.6.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.6.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.6.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.6.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.6.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.6.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.6.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.6.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.7.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.7.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.7.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.7.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.7.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.7.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.7.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.7.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.7.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.7.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.7.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.7.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.7.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.7.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.7.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.7.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.7.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.8.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.8.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.8.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.8.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.8.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.8.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.8.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.8.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.8.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.8.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.8.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.8.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.8.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.8.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.8.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.8.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.8.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.9.attn_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.9.layer_output_scale.weight,   torch.bfloat16 --> F32, shape = {1}
INFO:hf-to-gguf:blk.9.ffn_down.weight,             torch.bfloat16 --> F16, shape = {10240, 2560}
INFO:hf-to-gguf:blk.9.ffn_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.9.ffn_up.weight,               torch.bfloat16 --> F16, shape = {2560, 10240}
INFO:hf-to-gguf:blk.9.inp_gate.weight,             torch.bfloat16 --> F16, shape = {2560, 256}
INFO:hf-to-gguf:blk.9.proj.weight,                 torch.bfloat16 --> F16, shape = {256, 2560}
INFO:hf-to-gguf:blk.9.post_attention_norm.weight,  torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.9.post_ffw_norm.weight,        torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.9.post_norm.weight,            torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.9.ffn_norm.weight,             torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:blk.9.attn_k_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.9.attn_k.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:blk.9.attn_output.weight,          torch.bfloat16 --> F16, shape = {2048, 2560}
INFO:hf-to-gguf:blk.9.attn_q_norm.weight,          torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:blk.9.attn_q.weight,               torch.bfloat16 --> F16, shape = {2560, 2048}
INFO:hf-to-gguf:blk.9.attn_v.weight,               torch.bfloat16 --> F16, shape = {2560, 512}
INFO:hf-to-gguf:output_norm.weight,                torch.bfloat16 --> F32, shape = {2560}
INFO:hf-to-gguf:per_layer_model_proj.weight,       torch.bfloat16 --> F16, shape = {2560, 10752}
INFO:hf-to-gguf:per_layer_proj_norm.weight,        torch.bfloat16 --> F32, shape = {256}
INFO:hf-to-gguf:Set meta model
INFO:hf-to-gguf:Set model parameters
INFO:hf-to-gguf:gguf: context length = 131072
INFO:hf-to-gguf:gguf: embedding length = 2560
INFO:hf-to-gguf:gguf: feed forward length = 10240
INFO:hf-to-gguf:gguf: head count = 8
INFO:hf-to-gguf:gguf: key-value head count = 2
WARNING:hf-to-gguf:Unknown RoPE type: proportional
INFO:hf-to-gguf:gguf: rope scaling type = NONE
INFO:hf-to-gguf:gguf: rope theta = 1000000.0
INFO:hf-to-gguf:gguf: rope theta swa = 10000.0
INFO:hf-to-gguf:gguf: rms norm epsilon = 1e-06
INFO:hf-to-gguf:gguf: file type = 1
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.context_length', overwriting it with new value 131072 of type UINT32
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.attention.head_count', overwriting it with new value 8 of type UINT32
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.attention.layer_norm_rms_epsilon', overwriting it with new value 1e-06 of type FLOAT32
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.attention.key_length', overwriting it with new value 256 of type UINT32
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.attention.value_length', overwriting it with new value 256 of type UINT32
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.rope.freq_base', overwriting it with new value 1000000.0 of type FLOAT32
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.attention.head_count_kv', overwriting it with new value 2 of type UINT32
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.attention.key_length', overwriting it with new value 512 of type UINT32
WARNING:gguf.gguf_writer:Duplicated key name 'gemma4.attention.value_length', overwriting it with new value 512 of type UINT32
INFO:hf-to-gguf:Set model quantization version
INFO:hf-to-gguf:Set model tokenizer
INFO:hf-to-gguf:Token '<|tool_call>' is set to USER_DEFINED
INFO:hf-to-gguf:Token '<tool_call|>' is set to USER_DEFINED
INFO:hf-to-gguf:Token '<|tool_response>' is set to USER_DEFINED
INFO:hf-to-gguf:Token '<tool_response|>' is set to USER_DEFINED
INFO:hf-to-gguf:Token '<|"|>' is set to USER_DEFINED
INFO:hf-to-gguf:Token '<|channel>' is set to USER_DEFINED
INFO:hf-to-gguf:Token '<channel|>' is set to USER_DEFINED
INFO:gguf.vocab:Adding 514906 merge(s).
INFO:gguf.vocab:Setting special token type bos to 2
INFO:gguf.vocab:Setting special token type eos to 1
INFO:gguf.vocab:Setting special token type unk to 3
INFO:gguf.vocab:Setting special token type pad to 0
INFO:gguf.vocab:Setting special token type mask to 4
INFO:gguf.vocab:Setting chat_template to {%- macro format_parameters(properties, required) -%}
    {%- set standard_keys = ['description', 'type', 'properties', 'required', 'nullable'] -%}
    {%- set ns = namespace(found_first=false) -%}
    {%- for key, value in properties | dictsort -%}
        {%- set add_comma = false -%}
        {%- if key not in standard_keys -%}
            {%- if ns.found_first %},{% endif -%}
            {%- set ns.found_first = true -%}
            {{ key }}:{
            {%- if value['description'] -%}
                description:<|"|>{{ value['description'] }}<|"|>
                {%- set add_comma = true -%}
            {%- endif -%}
            {%- if value['nullable'] %}
                {%- if add_comma %},{%- else -%} {%- set add_comma = true -%} {% endif -%}
                nullable:true
            {%- endif -%}
            {%- if value['type'] | upper == 'STRING' -%}
                {%- if value['enum'] -%}
                    {%- if add_comma %},{%- else -%} {%- set add_comma = true -%} {% endif -%}
                    enum:{{ format_argument(value['enum']) }}
                {%- endif -%}
            {%- elif value['type'] | upper == 'OBJECT' -%}
                ,properties:{
                {%- if value['properties'] is defined and value['properties'] is mapping -%}
                    {{- format_parameters(value['properties'], value['required'] | default([])) -}}
                {%- elif value is mapping -%}
                    {{- format_parameters(value, value['required'] | default([])) -}}
                {%- endif -%}
                }
                {%- if value['required'] -%}
                    ,required:[
                    {%- for item in value['required'] | default([]) -%}
                        <|"|>{{- item -}}<|"|>
                        {%- if not loop.last %},{% endif -%}
                    {%- endfor -%}
                    ]
                {%- endif -%}
            {%- elif value['type'] | upper == 'ARRAY' -%}
                {%- if value['items'] is mapping and value['items'] -%}
                    ,items:{
                    {%- set ns_items = namespace(found_first=false) -%}
                    {%- for item_key, item_value in value['items'] | dictsort -%}
                        {%- if item_value is not none -%}
                            {%- if ns_items.found_first %},{% endif -%}
                            {%- set ns_items.found_first = true -%}
                            {%- if item_key == 'properties' -%}
                                properties:{
                                {%- if item_value is mapping -%}
                                    {{- format_parameters(item_value, value['items']['required'] | default([])) -}}
                                {%- endif -%}
                                }
                            {%- elif item_key == 'required' -%}
                                required:[
                                {%- for req_item in item_value -%}
                                    <|"|>{{- req_item -}}<|"|>
                                    {%- if not loop.last %},{% endif -%}
                                {%- endfor -%}
                                ]
                            {%- elif item_key == 'type' -%}
                                {%- if item_value is string -%}
                                    type:{{ format_argument(item_value | upper) }}
                                {%- else -%}
                                    type:{{ format_argument(item_value | map('upper') | list) }}
                                {%- endif -%}
                            {%- else -%}
                                {{ item_key }}:{{ format_argument(item_value) }}
                            {%- endif -%}
                        {%- endif -%}
                    {%- endfor -%}
                    }
                {%- endif -%}
            {%- endif -%}
            {%- if add_comma %},{%- else -%} {%- set add_comma = true -%} {% endif -%}
            type:<|"|>{{ value['type'] | upper }}<|"|>}
        {%- endif -%}
    {%- endfor -%}
{%- endmacro -%}
{%- macro format_function_declaration(tool_data) -%}
    declaration:{{- tool_data['function']['name'] -}}{description:<|"|>{{- tool_data['function']['description'] -}}<|"|>
    {%- set params = tool_data['function']['parameters'] -%}
    {%- if params -%}
        ,parameters:{
        {%- if params['properties'] -%}
            properties:{ {{- format_parameters(params['properties'], params['required']) -}} },
        {%- endif -%}
        {%- if params['required'] -%}
            required:[
            {%- for item in params['required'] -%}
                <|"|>{{- item -}}<|"|>
                {{- ',' if not loop.last -}}
            {%- endfor -%}
            ],
        {%- endif -%}
        {%- if params['type'] -%}
            type:<|"|>{{- params['type'] | upper -}}<|"|>}
        {%- endif -%}
    {%- endif -%}
    {%- if 'response' in tool_data['function'] -%}
        {%- set response_declaration = tool_data['function']['response'] -%}
        ,response:{
        {%- if response_declaration['description'] -%}
            description:<|"|>{{- response_declaration['description'] -}}<|"|>,
        {%- endif -%}
        {%- if response_declaration['type'] | upper == 'OBJECT' -%}
            type:<|"|>{{- response_declaration['type'] | upper -}}<|"|>}
        {%- endif -%}
    {%- endif -%}
    }
{%- endmacro -%}
{%- macro format_argument(argument, escape_keys=True) -%}
    {%- if argument is string -%}
        {{- '<|"|>' + argument + '<|"|>' -}}
    {%- elif argument is boolean -%}
        {{- 'true' if argument else 'false' -}}
    {%- elif argument is mapping -%}
        {{- '{' -}}
        {%- set ns = namespace(found_first=false) -%}
        {%- for key, value in argument | dictsort -%}
            {%- if ns.found_first %},{% endif -%}
            {%- set ns.found_first = true -%}
            {%- if escape_keys -%}
                {{- '<|"|>' + key + '<|"|>' -}}
            {%- else -%}
                {{- key -}}
            {%- endif -%}
            :{{- format_argument(value, escape_keys=escape_keys) -}}
        {%- endfor -%}
        {{- '}' -}}
    {%- elif argument is sequence -%}
        {{- '[' -}}
        {%- for item in argument -%}
            {{- format_argument(item, escape_keys=escape_keys) -}}
            {%- if not loop.last %},{% endif -%}
        {%- endfor -%}
        {{- ']' -}}
    {%- else -%}
        {{- argument -}}
    {%- endif -%}
{%- endmacro -%}
{%- macro strip_thinking(text) -%}
    {%- set ns = namespace(result='') -%}
    {%- for part in text.split('<channel|>') -%}
        {%- if '<|channel>' in part -%}
            {%- set ns.result = ns.result + part.split('<|channel>')[0] -%}
        {%- else -%}
            {%- set ns.result = ns.result + part -%}
        {%- endif -%}
    {%- endfor -%}
    {{- ns.result | trim -}}
{%- endmacro -%}

{%- set ns = namespace(prev_message_type=None) -%}
{%- set loop_messages = messages -%}
{{ bos_token }}
{#- Handle System/Tool Definitions Block -#}
{%- if (enable_thinking is defined and enable_thinking) or tools or messages[0]['role'] in ['system', 'developer'] -%}
    {{- '<|turn>system\n' -}}

    {#- Inject Thinking token at the very top of the FIRST system turn -#}
    {%- if enable_thinking is defined and enable_thinking -%}
        {{- '<|think|>' -}}
        {%- set ns.prev_message_type = 'think' -%}
    {%- endif -%}

    {%- if messages[0]['role'] in ['system', 'developer'] -%}
        {{- messages[0]['content'] | trim -}}
        {%- set loop_messages = messages[1:] -%}
    {%- endif -%}

    {%- if tools -%}
        {%- for tool in tools %}
            {{- '<|tool>' -}}
            {{- format_function_declaration(tool) | trim -}}
            {{- '<tool|>' -}}
        {%- endfor %}
        {%- set ns.prev_message_type = 'tool' -%}
    {%- endif -%}

    {{- '<turn|>\n' -}}
{%- endif %}

{#- Loop through messages -#}
{%- for message in loop_messages -%}
    {%- set ns.prev_message_type = None -%}
    {%- set role = 'model' if message['role'] == 'assistant' else message['role'] -%}
        {{- '<|turn>' + role + '\n' }}

            {%- if message['tool_calls'] -%}
                {%- for tool_call in message['tool_calls'] -%}
                    {%- set function = tool_call['function'] -%}
                    {{- '<|tool_call>call:' + function['name'] + '{' -}}
                    {%- if function['arguments'] is mapping -%}
                        {%- set ns_args = namespace(found_first=false) -%}
                        {%- for key, value in function['arguments'] | dictsort -%}
                            {%- if ns_args.found_first %},{% endif -%}
                            {%- set ns_args.found_first = true -%}
                            {{- key -}}:{{- format_argument(value, escape_keys=False) -}}
                        {%- endfor -%}
                    {%- elif function['arguments'] is string -%}
                        {{- function['arguments'] -}}
                    {%- endif -%}
                    {{- '}<tool_call|>' -}}
                {%- endfor -%}
                {%- set ns.prev_message_type = 'tool_call' -%}
            {%- endif -%}

            {%- if message['tool_responses'] -%}
                {#- Tool Response handling -#}
                {%- for tool_response in message['tool_responses'] -%}
                    {{- '<|tool_response>' -}}
                    {%- if tool_response['response'] is mapping -%}
                        {{- 'response:' + tool_response['name'] | default('unknown') + '{' -}}
                        {%- for key, value in tool_response['response'] | dictsort -%}
                            {{- key -}}:{{- format_argument(value, escape_keys=False) -}}
                            {%- if not loop.last %},{% endif -%}
                        {%- endfor -%}
                        {{- '}' -}}
                    {%- else -%}
                        {{- 'response:' + tool_response['name'] | default('unknown') + '{value:' + format_argument(tool_response['response'], escape_keys=False) + '}' -}}
                    {%- endif -%}
                    {{- '<tool_response|>' -}}
                {%- endfor -%}
                {%- set ns.prev_message_type = 'tool_response' -%}
            {%- endif -%}

            {%- if message['content'] is string -%}
                {%- if role == 'model' -%}
                    {{- strip_thinking(message['content']) -}}
                {%- else -%}
                    {{- message['content'] | trim -}}
                {%- endif -%}
            {%- elif message['content'] is sequence -%}
                {%- for item in message['content'] -%}
                    {%- if item['type'] == 'text' -%}
                        {%- if role == 'model' -%}
                            {{- strip_thinking(item['text']) -}}
                        {%- else -%}
                            {{- item['text'] | trim -}}
                        {%- endif -%}
                    {%- elif item['type'] == 'image' -%}
                        {{- '\n\n<|image|>\n\n' -}}
                        {%- set ns.prev_message_type = 'image' -%}
                    {%- elif item['type'] == 'audio' -%}
                        {{- '<|audio|>' -}}
                        {%- set ns.prev_message_type = 'audio' -%}
                    {%- elif item['type'] == 'video' -%}
                        {{- '\n\n<|video|>\n\n' -}}
                        {%- set ns.prev_message_type = 'video' -%}
                    {%- endif -%}
                {%- endfor -%}
            {%- endif -%}

        {%- if not (message['tool_responses'] and not message['content']) -%}
            {{- '<turn|>\n' -}}
        {%- endif -%}
{%- endfor -%}

{%- if add_generation_prompt -%}
    {%- if ns.prev_message_type != 'tool_response' -%}
        {{- '<|turn>model\n' -}}
    {%- endif -%}
{%- endif -%}
INFO:gguf.gguf_writer:Writing the following files:
INFO:gguf.gguf_writer:/output/gguf/model-f16.gguf: n_tensors = 720, total_size = 15.0G
Traceback (most recent call last):
  File "/llama.cpp/convert_hf_to_gguf.py", line 13197, in <module>
    main()
  File "/llama.cpp/convert_hf_to_gguf.py", line 13191, in main
    model_instance.write()
  File "/llama.cpp/convert_hf_to_gguf.py", line 936, in write
    self.gguf_writer.write_header_to_file(path=self.fname_out)
  File "/llama.cpp/gguf-py/gguf/gguf_writer.py", line 218, in write_header_to_file
    self.open_output_file(path)
  File "/llama.cpp/gguf-py/gguf/gguf_writer.py", line 182, in open_output_file
    self.fout = [open(filename, "wb") for filename in filenames]
                 ^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/output/gguf/model-f16.gguf'
Stopping app - uncaught exception raised locally: AttributeError().
WARNING: HF-to-GGUF conversion failed. LoRA adapters still available at /output/lora

--- Test Inference ---
Traceback (most recent call last):
  File "/usr/local/lib/python3.12/site-packages/transformers/tokenization_utils_base.py", line 275, in __getattr__
    return self.data[item]
           ~~~~~~~~~^^^^^^
KeyError: 'shape'
During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/pkg/modal/_runtime/container_io_manager.py", line 947, in handle_input_exception
    yield
  File "/pkg/modal/_container_entrypoint.py", line 172, in run_input_sync
    values = io_context.call_function_sync()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/pkg/modal/_runtime/container_io_manager.py", line 225, in call_function_sync
    expected_value_or_values = self.finalized_function.callable(*args, **kwargs)
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/modal_finetune_plain.py", line 238, in finetune
    outputs = model.generate(
              ^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/peft/peft_model.py", line 2048, in generate
    outputs = self.base_model.generate(*args, **kwargs)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/torch/utils/_contextlib.py", line 124, in decorate_context
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/transformers/generation/utils.py", line 2398, in generate
    batch_size = inputs_tensor.shape[0]
                 ^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/transformers/tokenization_utils_base.py", line 277, in __getattr__
    raise AttributeError
AttributeError