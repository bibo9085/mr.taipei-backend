# %%
import cv2
import matplotlib.pyplot as plt
import numpy as np
from openvino.runtime import Core

ie = Core()
model = ie.read_model(model="model/v3-small_224_1.0_float.xml")
compiled_model = ie.compile_model(model=model, device_name="CPU")

output_layer = compiled_model.output(0)
# The MobileNet model expects images in RGB format
image = cv2.cvtColor(cv2.imread(filename="data/nini.jpg"), code=cv2.COLOR_BGR2RGB)

# resize to MobileNet image shape
input_image = cv2.resize(src=image, dsize=(224, 224))

# reshape to model input shape
input_image = np.expand_dims(input_image, 0)
plt.imshow(image);

result_infer = compiled_model([input_image])[output_layer]
result_index = np.argmax(result_infer)

# Convert the inference result to a class name.
imagenet_classes = open("utils/imagenet_2012.txt").read().splitlines()

# The model description states that for this model, class 0 is background,
# so we add background at the beginning of imagenet_classes
imagenet_classes = ['background'] + imagenet_classes

imagenet_classes[result_index]