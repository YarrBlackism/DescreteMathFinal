## Project Overview

My main demo for this project will use a Raspberry Pi with the Hailort AI 13 TOPS (based on the Hailo-8L) to handle computer vision processing, along with GPS functionality for additional graphing and informational purposes. This project connects ideas from **graph theory** and **computer vision** by using **YOLOv11** to detect objects , and then representing the detected objects as vertices in a graph. If two objects are close enough to each other, the program creates an edge between them.

The goal of this project is to show that graph theory is not only an abstract math topic used in class examples. It can also be used to model real-world visual environments. For example imagine detecting theft with the distance between an person or object. Or civilian object tracking for advertisment purpouses(unethical but math has no room for ethics, therfore its ok :>). 
<img width="1050" height="615" alt="image" src="https://github.com/user-attachments/assets/4cc842c1-c9c5-4878-a9f3-108cc3ca12b2" />

This means the camera scene is transformed into a **weighted object relationship graph**. 
<img width="295" height="405" alt="image" src="https://github.com/user-attachments/assets/db3afd71-17b5-417f-b518-2269e7323c7d" />

## requirments 
This project will have an raspberry pi and windows/unix verson if you so choose to run the program.
*BASIC REQ*
1. requires python 3.0 version or higher
2. working webcam
*EXTENDED FUNCTIONALITY*
1. working gps dongle
2. better gpu
3. raspberry pi for mobile features

## Works Cited

Bondy, J. A., and U. S. R. Murty. *Graph Theory with Applications*. North-Holland, 1976.

Chen, Ruiting. “Dijkstra’s Shortest Path Algorithm and Its Application on Bus Routing.” *Advances in Economics, Business and Management Research*, vol. 217, 2022, pp. 321–325.

Biswas, Siddhartha Sankar, Bashir Alam, and M. N. Doja. “Generalization of Dijkstra’s Algorithm for Extraction of Shortest Paths in Directed Multigraphs.” *Journal of Computer Science*, vol. 9, no. 3, 2013, pp. 377–382.

## video refrences for code 
## note these videos where used to help me understand the articles and coding.
*NetworkX Crash Course - Graph Theory in Python*
https://youtu.be/VetBkjcm9Go?si=1WEwSHnolnKKrc-l


How To Create Python Network Graphs || NetworkX Overview || Graph Plotting || Matplotlib || Advanced
https://youtu.be/7NWeLuG8tVo?si=PT8QUhVUUFRt0MhB


Dijkstras Shortest Path Algorithm Explained | With Example | Graph Theory
https://youtu.be/bZkzH5x0SKU?si=RgZ39GwfFVlVpsE7


Implementing Dijkstra's Algorithm from Scratch with Python: Graph Visualization Using NetworkX
https://youtu.be/nAYASV84ius?si=HJ9jty_Gh3ChP_Oj

Ultralytics YOLO Docs
https://docs.ultralytics.com/modes/predict/


## Main Idea
The project follows this process:

1. First A camera or image is passed into the YOLOv11 object detection model.
2. YOLOv11 identifies objects and gives each object a class label, confidence score, and bounding box.
3. The program calculates the center point of each bounding box.
4. Each detected object is added to a graph as a vertex.
5. The program measures the distance between objects.
6. If two objects are close enough, an edge is created between them.
7. The edge receives a weight based on the distance between the two objects.
8. The graph can then be analyzed using graph theory algorithms.



