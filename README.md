## Project Description:

We are designing a software which will boost the experience of renting a car. To build a system which looks more into customer's as well as the owner's convenience. Our proposed system will provide the car owner an option to upload two images on the interface. First, image of the Vehicle identification number (VIN) which will be converted into plain text form, extracting all the information of the car such as car build, model, year of make etc.
Second image will be photo of the car, which will send out the same information as the first image. This will verify the car's legitimacy. So, this will boost the level of trust among customers and the owners.

## System Architecture:

![MicrosoftTeams-image](https://user-images.githubusercontent.com/41479691/205125468-378987da-3a75-4105-a5fc-7928fb2e8fd0.png)

# Front-end: 
HTML, CSS, JS
# Back-end : 
Python Django
# Database: 
PostgreSQL
# Dataset for ML: 
Standford Car dataser with contains 16000 car images with 196 classes
# ML models used:
VGG16: Took a long time for training,
EfficientNet B1: Much faster than VGG16, but low accuracy(40%),
Resnet: relatively faster and accurate. 77% accuracy with 8000 images in test data

## Back-end Pipeline:

![MicrosoftTeams-image (1)](https://user-images.githubusercontent.com/41479691/205126243-5f6faa30-31d9-4074-8626-8b5c33101cb0.png)
