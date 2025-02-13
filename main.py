from aura_sr import AuraSR
from PIL import Image
import numpy as np
import os

# begin of 'Model Initialization'
# If you want to allow hugging face model download through proxy, please uncomment the following lines and set the proxy address.
# os.environ['HTTP_PROXY'] = 'http://127.0.0.1:10809'
# os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:10809'

# Change the value of 'HF_HOME' to the directory where you want to save the downloaded models.
os.environ['HF_HOME'] = 'F:\\Python\\.huggingface'

print('Initialized proxy for huggingface model download.\n')


aura_sr = AuraSR.from_pretrained("fal-ai/AuraSR") # image upscaling model, based on Adobe's GigaGAN model
# end of 'Model Initialization'


def upscale_image(image):
    # 如果图片是 RGBA 模式，分离 RGB 和 Alpha 通道
    if image.mode == "RGBA":
        rgb_image = image.convert("RGB")  # 转换为 RGB 模式
        alpha_channel = np.array(image)[:, :, 3]  # 提取 Alpha 通道
    else:
        rgb_image = image
        alpha_channel = None

    # 调用模型进行 4x 放大
    upscaled_rgb_image = aura_sr.upscale_4x(rgb_image)
    print('image upscaled to 4x.\n')

    # 如果存在 Alpha 通道，重新合并 Alpha 通道
    if alpha_channel is not None:
        alpha_channel_image = Image.fromarray(alpha_channel)
        alpha_channel_resized = alpha_channel_image.resize(upscaled_rgb_image.size, Image.Resampling.LANCZOS)

        # 将放大后的 RGB 图像和 Alpha 通道合并
        upscaled_rgb_image_with_alpha = np.dstack([np.array(upscaled_rgb_image), np.array(alpha_channel_resized)])
        upscaled_image = Image.fromarray(upscaled_rgb_image_with_alpha, "RGBA")
    else:
        upscaled_image = upscaled_rgb_image  # 直接使用 upscaled_rgb_image

    return upscaled_image


def batch_upscale(image_paths_file):
	with open(image_paths_file, 'r') as file:
		paths = file.readlines() # one image path per line
		# ignore all paths begin with '#' (with is totally comment)
		paths = [path for path in paths if not path.startswith('#')]

	for path in paths:
		path = path.strip()
		if os.path.exists(path):
			try:
				image = Image.open(path)
				print(f'Batch process will not show the image. To show image before proceed, please use the interactive mode.\n')
				print(f'source image path: {path}\n')
				print(f'source image size: {image.size}\n')

				upscaled_image = upscale_image(image)

				output_path = path.split('.')[0] + '_upscaled(4x).png'
				upscaled_image.save(output_path)
				print(f'upscaled image saved to {output_path}\n')
			except Exception as ex:
				print(f'Error occurred when processing {path}: {ex}\n')
		else:
			print(f'file {path} does not exist, skipping.')

		print('\n')  # to separate the output of different images


if __name__ == '__main__':
	while True:
		print('Choose an option:')
		print('1. Input a single image path to upscale')
		print('2. Input the path to a text file containing image paths (one per line) to batch upscale')
		print('Q. Quit')

		choice = input().strip().upper()

		if choice == 'Q':
			break
		elif choice == '1':
			print('Input the path to the image you want to upscale, or import nothing to exit:')
			path = input().strip()
			if path == '':
				break
			elif os.path.exists(path):
				image = Image.open(path)
				image.show()
				print(f'source image path: {path}\n')
				print(f'source image size: {image.size}\n')

				upscaled_image = upscale_image(image)

				output_path = path.split('.')[0] + '_upscaled(4x).png'
				upscaled_image.save(output_path)
				print(f'upscaled image saved to {output_path}\n')

				print(f'Press Q to exit, P to preview the upscaled image (using PIL), or press any other key to upscale another image:')
				preview = input().strip().upper()
				if preview == 'P':
					upscaled_image.show()
			else:
				print(f'File {path} does not exist.')
		elif choice == '2':
			print('Input the path to the text file containing image paths (one per line), or import nothing to exit:')
			paths_file = input().strip()
			if paths_file == '':
				break
			elif os.path.exists(paths_file):
				batch_upscale(paths_file)
			else:
				print(f'File {paths_file} does not exist.')
		else:
			print('Invalid option. Please choose again.')