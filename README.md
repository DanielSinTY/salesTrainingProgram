# Sales Training & Evaluation Program (STEP)
<img src="https://imgur.com/wT9rOxs.png" width="400">
A software using MLP (MultiLayer Perceptron) neural network,NLP and speech to text that can learn and evaluate past salesperson's speech patterns and their effect on customers' purchasing decisions and predict customers' purchasing decision from sales rep's speech.

## Table of Contents

[1. Features](#features)

[2. Windows Executable](#Windows-Executable)

[3. Usage](#Usage)

[4. Modules Used](#Modules-Used)


## Features

- **Support speech to text**
	allow companies to analyze sales rep's speech by simply recording it;
- **Customized AI model**
	users can train their AI model to make the prediction more accurate by fitting the industry;
- **Pretrained model**
	A pretrained model is also given for general use;
- **Usage across different devices**
	The model is stored on Google drive and can be loaded from different devices by using Google accounts having access to the same folder;

## Windows Executable
### Download the .exe
The Windows executable file can be downloaded here:
https://drive.google.com/drive/folders/1bmHq8j93-mv87ilJEhM17VJnQAVje5HQ?usp=sharing.
It is built using PyInstaller with `main.spec`.

## Open with Python
### 1. Cloning this repository
Clone this repo with `git clone https://github.com/DanielSinTY/salesTrainingProgram.git` or using GitHub desktop.
### 2. Installing required modules and packages
All required modules and packages are listed in requirements.txt. Use `pip install -r requirements.txt` to install all the packages and modules needed. You may want to use a virtual environment for this.

### 3. Configuring Google Drive API
Follow the instruction [here](https://pythonhosted.org/PyDrive/quickstart.html#authentication "here") (https://pythonhosted.org/PyDrive/quickstart.html#authentication) to create an API to be used by PyDrive to connect to Google Drive. Remember to rename the downloaded json file as `client_secrets.json` and place it in the working directory.




## Usage

[1. Configuring Google Drive](#1-Configuring-Google-Drive)

[2. Authetication for Google Drive](#2-Authetication-for-Google-Drive)

[3. General Usage](#3-General-Usage)

[4. Analysing sales speech](#4-Analysing-sales-speech)

[5. Training the AI model](#5-Training-the-AI-model)

[6. Deleting the AI model](#6-Deleting-the-AI-model)


### 1. Configuring Google Drive
A Google Drive Folder named `model` has to be created to store the model before using any of the functions. `model.joblib` in this repo can also be put in the folder for *STEP* to use the pretrained model.

### 2. Authetication for Google Drive

Open the .exe file or run main.py in `/salesTraining` and *STEP* will open your browser and prompt you to sign in to Google. Sign in using an account with access to the folder `model` and authorize the software. You can close the browser after the authetication flow has been completed (this will be shown in the browser).

<img src="https://i.imgur.com/nRAPGR5.png" width="200">

### 3. General Usage
After authetication, the GUI of *STEP* will pop up. Click **Analyse** to predict customers' purchasing decision from a sales rep's speech. Click **Train** to train the AI model with previous sales reps' speech. Click **Delete** to delete the AI model.

<img src="https://imgur.com/dkMPJD2.png" height="300">

### 4. Analysing sales speech
By clicking **Analyse**, you can either record a sales speech or upload an audio file of recording to predict customers' purchasing decision based on the speech.

<img src="https://imgur.com/hC20Svw.png" height="300">

After recording a speech of uploading an audio file, you can listen to the recording, restart recording or uploading, or start analysis on the sales speech.

<img src="https://imgur.com/baPdM3R.png" height="300">

By clicking **Start analysing**, *STEP* will load the model from Google Drive, extract features from the speech, and predict customers' purchasing decisions with the model based on the speech. After analysing, either of two outputs will be shown. <img src="https://imgur.com/34xm9VZ.png" height="20"> indicates that customers are likely to buy the product after hearing the speech or having the conversation, while <img src="https://imgur.com/6UrGkEC.png" height="20"> indicates that customers are not likely to buy. A transcript will also be shown for reference. After that, you can analyse a new recording or go back to the home page.

### 5. Training the AI model
By clicking **Train**, *STEP* will prompt you to upload files of previous successful (i.e. the customer purchased the product after that) and poor (i.e. the customer did not purchase) sales speech respectively to be used as data to train the MLP model. You can either upload audio recordings in .wav or transcript in .txt. 

<img src="https://imgur.com/pHcHYyK.png" height="300">

After uploading all the files, click **Start training** and *STEP* will start training the MLP model with the files uploaded. *STEP* will first extract features from all the files, and then feed into the MLP model to train it. Progress bar of feature extraction and iteration number during feeding will be shown on the screen. The process may take a few minutes to couple of hours depending on size of dataset (number of files uploaded) and computing power. If a model exists in the Google Drive, *STEP* will train that model using the new files uploaded. A new MLP model will be created otherwise.

When you see <img src="https://imgur.com/F9Jkgoy.png" height="20">, the MLP model has been successfully trained and uploaded to the Google Drive Folder named `model` and you can use it to analyse sales speech.

<img src="https://imgur.com/XRollWw.png" height="300">

### 6. Deleting the AI model
By clicking **Delete**, a warning box will be shown before deleting the model. Click `Yes` to delete the model from the Google Drive folder.

<img src="https://imgur.com/UiQdQgh.png" height="300">

After successfully deleting the model, another info box will be shown. You can train a new model after that.

<img src="https://imgur.com/FQQMcZ2.png" height="200">


## Modules Used
The following modules are used in STEP:
- **scikit-learn**
	to train and use the MLP model
- **Empath**
	to analyse and categorize the words in speech
- **SpaCy**
	to analyse sentence patterns
- **PyDrive**
	 to connect to Google Drive
- **soundDevice** and **soundFile**
	to record audio
- **pygame**
	to play the recording
- **Tkinter**
	to build the UI
- **PyInstaller**
	to package the program into exe
