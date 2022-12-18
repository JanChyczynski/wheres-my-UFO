# Where's my UFO?
Application for tracking the position of rockets (or weather baloons, UFOs etc.) during launches. It consists of 2 main modules:
1. Visualising the rocket's position based on the coordinates sent by the rocket


2. Calculating and visualising probable rocket's position
based only on the signal strength, used when coordinates cannot be retrieved from the data frames

## Screenshots

### Module "Position Visualiser"

#### Selecting the data source:
![image](https://user-images.githubusercontent.com/59477191/208299331-3cc78062-419f-465e-a3b3-8099da56819e.png)

#### Tracking the rocket during flight and predicting the landing spot:
![image](https://user-images.githubusercontent.com/59477191/208299410-db43e55f-95e0-47d4-984b-6c236fccd266.png)

### Module "Signal finder"

#### Heatmap of the probability of finding the signal source. The aliens mark the spots which we know the signal stregnth in. The upper alien has low signal stregth compared to the bottom ones so the algorithm predicted the source is further away from it.

![image](https://user-images.githubusercontent.com/59477191/208299856-c677c4e6-f7dd-4a14-b879-a146977d9f28.png)


## Installation:
1. run:
```
pip install -r requirements.txt 
```
2. for windows:
put the file `rtlsdr.dll` from this repository into your python istallation folder (the same folder as `python.exe`)
