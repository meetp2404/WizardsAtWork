import matplotlib.pyplot as plt
import numpy as np
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
import torchvision.models as models
from PIL import Image
import json
from matplotlib.ticker import FormatStrFormatter
import os

def getResults():
    model = torch.load(r'D:\Sem_3\PRG800\code\resnet_final.pt')
    def process_image(image):
        pil_im = Image.open(f'{image}' + '.jpg')
        transform = transforms.Compose([transforms.Resize((244,244)),
                                        #transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406], 
                                                            [0.229, 0.224, 0.225])])
        pil_tfd = transform(pil_im)
        array_im_tfd = np.array(pil_tfd)
        return array_im_tfd
    def find_classes(dir):
        classes = os.listdir(dir)
        classes.sort()
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        return classes, class_to_idx
    classes, c_to_idx = find_classes("train")
    def predict(image_path, topk=5):
        image_path = image_path
        img = process_image(image_path)
        img_tensor = torch.from_numpy(img).type(torch.FloatTensor)
        img_add_dim = img_tensor.unsqueeze_(0)
        model.eval()
        with torch.no_grad():
            # Running image through network
            output = model.forward(img_add_dim)
        probs_top = output.topk(topk)[0]
        predicted_top = output.topk(topk)[1]

        # Converting probabilities and outputs to lists
        conf = np.array(probs_top)[0]
        predicted = np.array(predicted_top)[0]

        return conf, predicted
    conf2, predicted1 = predict(r"D:\Sem_3\PRG800\code\027687_2012_Hyundai_Sonata")
    return classes[predicted1[0]]
