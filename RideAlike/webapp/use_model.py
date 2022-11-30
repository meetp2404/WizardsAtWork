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

def getResults(image_path, topk=5):
    model = torch.load(r'C:\Users\meetp\OneDrive - Seneca\Desktop\Test\RideAlike\resnet_final.pt')
    def process_image(image):
        pil_im = Image.open(f'{image}')
        transform = transforms.Compose([transforms.Resize((244,244)),
                                        #transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406], 
                                                            [0.229, 0.224, 0.225])])
        pil_tfd = transform(pil_im)
        array_im_tfd = np.array(pil_tfd)
        return array_im_tfd
    
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

