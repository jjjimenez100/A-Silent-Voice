<p align="center">
<img src="https://lh5.googleusercontent.com/aNqldAd74sZGsWgYJ0W5wNhpa51vr166KcIMO7QczwIxVmIKtDJMlBSMYtR6RTMo_GNPVVRDVgJx5_VeHcKx=w1366-h662-rw" alt="A Silent Voice Logo" width="200" height="200">
</p>

<h1 align="center">A Silent Voice</h1>

An application of **Convolutional Neural Networks** along with various
**computer vision algorithms** for recognizing **American Sign Language**.
The project serves as an undergraduate thesis of the developers in partial
fulfillment of the requirements for the degree of Bachelor of Science in
Computer Science at Holy Angel University.

## Project Scope and Delimitation
1. Best results are acquired on a simple white background.
2. A-Z, 0-9, Best of Luck, You, I/Me, Like, Remember, Love, I Love You are the only gestures known to this model.

## Project Dependencies
* opencv-python 3.4.1.15
* pywin32 223
* pyttsx3 2.7
* scikit-learn 0.19.1
* tensorflow 1.8.0 (non-gpu)
* keras 2.2.0
* pyqt5 4.19.8
* matplotlib 2.2.2

**Note:** Additional dependencies may be required by the above listed modules.

## Installing Project Dependencies
As of the moment, automatic installation of the project's dependencies is only available to the Windows OS.
Simply run the **wininstall.bat** included in the project by double clicking or using the command prompt.
```
cd MainDirectoryOfASilentVoice
wininstall
```

## Datasets
For each gesture, 1200 greyscaled and thresholded images were used to train the model.
The developers have decided to flip 1200 of these images to give consideration to both
right and left handed users. A total of 2400 images are used per gesture. Datasets are uploaded
on google drive as the developers consider them too large to be uploaded on an online repository.
The datasets can be found [here](www.google.com).

## Developers
* Diaz, Jericho Hans
* De Leon, Julius
* Jimenez, John Joshua
* Olsen, Ola

## License
To be updated in the near future.

## Acknowledgements
To be updated in the near future.