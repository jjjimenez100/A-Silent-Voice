<p align="center">
<img src="https://cdn.discordapp.com/attachments/371642681514000384/457478865019863041/Icon.png" alt="A Silent Voice Logo" width="200" height="200">
</p>

<h1 align="center">A Silent Voice</h1>

An application of **Convolutional Neural Networks** along with various
**computer vision algorithms** for recognizing **Filipino Sign Language**.
The project serves as an undergraduate thesis of the developers in partial
fulfillment of the requirements for the degree of Bachelor of Science in
Computer Science at Holy Angel University.

## Project Scope and Delimitation
1. Best results are acquired on a simple white background.
2. Filipino Sign Language Gestures of Letters A-Z

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
For each gesture, 1300 greyscaled and thresholded images were used to train the model.
The developers have decided to flip 1300 of these images to give consideration to both
right and left handed users. A total of 2400 images are used per gesture. Datasets are uploaded
on google drive as the developers consider them too large to be uploaded on an online repository.
The datasets can be found [here](www.google.com).

## Developers
* Diaz, Jericho Hans
* De Leon, Julius
* Jimenez, John Joshua
* Olsen, Ola

## License
GNU Affero General Public License v3.0. For a more detailed explanation, check it out [here.](https://github.com/jjjimenez100/A-Silent-Voice/blob/master/LICENSE)

## Acknowledgements
De Leon, J., Diaz, J. H., Jimenez, J. J., & Olsen, O. (2018). A Silent Voice: An Application of Computer Vision for Recognizing Filipino Sign Language (p. iii). Holy Angel University.  
>The researchers would like to express their utmost gratitude to the following instructors: Ms. Ma. Louella Salenga for providing advices and guidance during the initial stages of the research and Ms. Arcely Napalit for being the adviser and contributing her knowledge and expertise to make the research a success. The researchers extend their heartfelt gratitude to the Principal of Angeles Elementary School, Ms. Ofelia Canlas, for giving the researchers permission to conduct their research on the school, as well as the professional Filipino Sign Language interpreters/teachers: Ms. Editha Peña, Ms. Melodia Delfin and Ms. Lovely Katlin Garcia. The researchers express their gratitude to the representative of Philippine Registry of Interpreters for the Deaf (PRID), Ms. Vivian Saulo, for providing data as well as sharing her knowledge and resources about Filipino Sign Language. To the Machine Learning Professionals, Mr. Arian Yambao, Mr. John Paul Ada and Mr. Jake Abasolo, the researchers would like to expresses their gratitude for evaluating and providing professional feedback about the prototype and the model. Special thanks to the Hearing-Impaired Interviewees, Ms. Sanchez, Mr. Panlilio and Ms. Silvestre and to the Non-Hearing-Impaired Interviewees, Mrs. Sanchez, Mrs. Nicdao and Mrs. Panlilio for their continuous support throughout the multiple visitations of the researchers. Lastly, the researchers extend their heartfelt gratitude to their friends, classmates, family and most especially to God, for not with their support would have made the research possible.
