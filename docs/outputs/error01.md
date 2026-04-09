onverting to GGUF (q4_k_m)...
INFO:hf-to-gguf:Loading model: merged
INFO:hf-to-gguf:Model architecture: Gemma4ForConditionalGeneration
INFO:hf-to-gguf:gguf: indexing model part 'model.safetensors'
INFO:gguf.gguf_writer:gguf: This GGUF file is for Little Endian only
INFO:hf-to-gguf:Exporting model...
INFO:hf-to-gguf:rope_freqs.weight,                 torch.float32 --> F32, shape = {256}
Traceback (most recent call last):
  File "/llama.cpp/convert_hf_to_gguf.py", line 13197, in <module>
    main()
  File "/llama.cpp/convert_hf_to_gguf.py", line 13191, in main
    model_instance.write()
  File "/llama.cpp/convert_hf_to_gguf.py", line 934, in write
    self.prepare_tensors()
  File "/llama.cpp/convert_hf_to_gguf.py", line 794, in prepare_tensors
    for new_name, data_torch in (self.modify_tensors(data_torch, name, bid)):
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/llama.cpp/convert_hf_to_gguf.py", line 7638, in modify_tensors
    yield from super().modify_tensors(data_torch, name, bid)
  File "/llama.cpp/convert_hf_to_gguf.py", line 7003, in modify_tensors
    with open(self.dir_model / "tokenizer.json", "r", encoding="utf-8") as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: '/output/merged/tokenizer.json'
WARNING: HF-to-GGUF conversion failed.

--- Test Inference ---
Traceback (most recent call last):
Stopping app - uncaught exception raised in remote container: SafetensorError('Error while deserializing header: incomplete metadata, file not fully covered').
  File "/pkg/modal/_runtime/container_io_manager.py", line 947, in handle_input_exception
    yield
  File "/pkg/modal/_container_entrypoint.py", line 172, in run_input_sync
    values = io_context.call_function_sync()
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/pkg/modal/_runtime/container_io_manager.py", line 225, in call_function_sync
    expected_value_or_values = self.finalized_function.callable(*args, **kwargs)
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/root/modal_finetune_plain.py", line 319, in convert_gguf
    model = AutoModelForCausalLM.from_pretrained(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/transformers/models/auto/auto_factory.py", line 387, in from_pretrained
    return model_class.from_pretrained(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/transformers/modeling_utils.py", line 4135, in from_pretrained
    loading_info, disk_offload_index = cls._load_pretrained_model(model, state_dict, checkpoint_files, load_config)
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/transformers/modeling_utils.py", line 4243, in _load_pretrained_model
    file_pointer = safe_open(file, framework="pt", device="cpu")
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
safetensors_rust.SafetensorError: Error while deserializing header: incomplete metadata, file not fully covered