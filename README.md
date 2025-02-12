<div style="text-align: center;">

MistunaChan
---
A simple program to inherit AuraSR super resolution model and apply it to one or multiple image files.

</div>

## Summary
MitsunaChan is a Python out-of-the-box project that allows you to upscale images using the AuraSR super resolution model. The project is designed to be simple and easy to use, with a focus on providing a user-friendly interface for users to upscale images with minimal effort.  
Models are from [AuraSR](https://huggingface.co/fal/AuraSR) by [fal](https://huggingface.co/fal), based on Adobe's GigaGAN model.

## Requirements
### Hardware Requirements
- GPU: NVIDIA GeForce RTX 3050 (including Laptop version) or higher
- Disk Space: 7.5GB+ (for model weights)

### Software Requirements
- Python: 3.11+
- PyTorch: 2.6.0+ (using ``2.6.0+cu124`` for default)
- NumPy: 2.2.2+
- CUDA Toolkit: 12.4+ (use ``nvidia-smi`` to check the max supported version of the GPU hardware)

## How to use
1. Clone the repository.
2. Check if the ``requirements.txt`` doesn't meet the actual hardware you have, modify it if necessary.
3. Run ``pip install -r requirements.txt`` to install the required packages.
4. Install corresponding NVIDIA CUDA Toolkit from [here](https://developer.nvidia.com/cuda-downloads).  
   **Be sure you choose the correct version for your GPU hardware and PyTorch support.**
5. Run ``python main.py`` to start the program.  
   Program will firstly download the model weights from HuggingFace, which may take a while depending on your network speed.

## License
Project MistunaChan is licensed under [The MIT License](LICENSE).