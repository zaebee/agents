# @title
!pip install -U transformers

## Local Inference on GPU
Model page: https://huggingface.co/Salesforce/blip-image-captioning-base

⚠️ If the generated code snippets do not work, please open an issue on either the [model repo](https://huggingface.co/Salesforce/blip-image-captioning-base)
			and/or on [huggingface.js](https://github.com/huggingface/huggingface.js/blob/main/packages/tasks/src/model-libraries-snippets.ts) 🙏

# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

# recoginize text from image using `pipe`.


# Load model directly
from transformers import AutoProcessor, AutoModelForVision2Seq

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = AutoModelForVision2Seq.from_pretrained("Salesforce/blip-image-captioning-base")


import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'
raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

def generate_caption(text:str, raw_image:Image.Image):
    inputs = processor(raw_image, text, return_tensors="pt")
    out = model.generate(**inputs)
    return processor.decode(out[0], skip_special_tokens=True)

# conditional image captioning
text = "a photography of"
inputs = processor(raw_image, text, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))
# >>> a photography of a woman and her dog

# unconditional image captioning
inputs = processor(raw_image, return_tensors="pt")

out = model.generate(**inputs)
print(processor.decode(out[0], skip_special_tokens=True))

url = 'https://space.zae.life/manifestof-digit-onto.jpg'
url = 'https://stage.ownima.com/vehicles/a92ca8b8-3081-4c87-b8ae-2c1b4917cc75/f4d1e5ff-5990-4441-ab6a-b58d35bc37e6.jpg'

text= ""  # "list of words from left side of the russian dictionary on tablet: "

raw_image = Image.open(requests.get(url, stream=True).raw).convert('RGB')
print(generate_caption(text, raw_image))

# recoginize text from image using `pipe`.
img_url = 'https://storage.googleapis.com/sfr-vision-language-research/BLIP/demo.jpg'
img_url = 'https://space.zae.life/manifestof-digit-onto.jpg'
img_url = url

image = Image.open(requests.get(img_url, stream=True).raw)

result = pipe(image)
print(result)
