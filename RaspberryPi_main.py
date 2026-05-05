from ultralytics import YOLO
from picamera2 import Picamera2
import cv2
import networkx as nx
import matplotlib.pyplot as plt
import math
from itertools import combinations

"""
AUTHOR: Ahmed Boudjrda
Class: Sp26 Math 215-51 Discrete Mathematics

MY DISCRETE MATH PROJECT:
Computer Vision as Graph Theory:
Using YOLOv11 to Build and Analyze Real-Time Object Relationship Graphs

CORE IDEA:
- YOLOv11 detects objects from the camera.
- Each detected object becomes a vertex/node on the graphzy.
- If two detected objects are close enough, an edge is created.
- The edge weight is the pixel distance between object centers.

My REFERENCES:
1. Bondy & Murty, Graph Theory with Applications, p. 1:
   Reason: They define a graph as vertices and edges. This justifies
   turning detected objects into vertices and object relationships into edges.

2. Bondy & Murty, Graph Theory with Applications, p. 7-8:
   Reason: They discuss incidence/adjacency matrices and note that
   adjacency matrices are commonly used to store graphs in computers.
   This supports the program's use of NetworkX graph structures.

3. Chen, "Dijkstra's Shortest Path Algorithm and Its Application on Bus Routing,"
   p. 321-322:
   Reason: Chen explains weighted graphs, shortest path problems,
   and Dijkstra's algorithm. This supports using pixel distance as edge weight
   and using Dijkstra to find the shortest object-to-object path.

4. Biswas, Alam, and Doja, "Generalization of Dijkstra's Algorithm..."
   p. 377-378:
   Reason: They explain that some real networks are better modeled as
   multigraphs when multiple edges can exist between the same vertices.
   This supports the optional multigraph extension idea in this project.
"""


# CONFIGS 

# Using the YOLOv11 model which is currently the most stable for most projects(IMO).
model = YOLO("yolo11n.pt")

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

# Maximum pixel distance for creating an edge between two detected objects.
# Smaller number = fewer edges.
# Bigger number = more edges.
distance_limit = 250
confidence_limit = 0.40 # Minimum confidence score for accepting a YOLO detection.

# Save the most recent graph so we can analyze it when keys are pressed.
latest_graph = None
latest_objects = []

# FUNCTIONS BELOW....
def euclidean_distance(obj1, obj2):
    """
    Distance between two object centers.

    Chen, p. 322:
    Edge weights in a weighted graph can represent distance, cost, or time.
    Here, the weight represents pixel distance between detected objects.
    """
    return math.sqrt(
        (obj1["x"] - obj2["x"]) ** 2 +
        (obj1["y"] - obj2["y"]) ** 2
    )


def build_object_graph(objects):
    """
    Builds weighted graph from YOLO detected objects.

    Each object is an  vertex.
    Each nearby object pair is an weighted edge.

    Bondy & Murty, p. 1:
    A graph uses a vertex set and an edge set. This function creates both.
    """

    G = nx.Graph() #created graph set as G 

    # Add every detected object as a graph node using for loop.
    for obj in objects:
        G.add_node(
            obj["name"],
            label=obj["label"],
            x=obj["x"],
            y=obj["y"],
            confidence=obj["confidence"]
        )

    # Create edges between nearby objects.
    # This uses combinations to avoid any duplicate edges.
    for obj1, obj2 in combinations(objects, 2):
        distance = euclidean_distance(obj1, obj2)

        if distance <= distance_limit:
            G.add_edge(
                obj1["name"],
                obj2["name"],
                weight=round(distance, 2)
            )

    return G


def print_graph_report(G):
    """
    Prints a graph for the current frame.
    - number of vertices
    - number of edges
    - graph density
    - connected components
    - degree of each node
    - highest-degree object
    - cliques
    - coloring
    """

    print("\nGRAPH output")
    """
    >o)
    (_>
    rubber ducky debugger 
    """
    # v and e counts.
    print(f"Number of vertices |V|: {G.number_of_nodes()}")
    print(f"Number of edges |E|: {G.number_of_edges()}")

    # Density tells how close the graph is to being complete.
    # A complete graph has every vertex connected to every other vertex.
    density = nx.density(G)
    print(f"Graph density: {density:.3f}")

    # Degree of each vertex.
    print("\nVertex degrees:")
    for node, degree in G.degree():
        print(f"  {node}: degree {degree}")

    # Find the most connected object.
    if G.number_of_nodes() > 0:
        highest_degree_node = max(G.degree, key=lambda item: item[1])
        print(f"\nMost connected object: {highest_degree_node[0]} with degree {highest_degree_node[1]}")

    # Connected components.
    components = list(nx.connected_components(G))
    print(f"\nConnected components: {len(components)}")
    for i, component in enumerate(components, start=1):
        print(f"  Component {i}: {sorted(component)}")

    # Cliques are groups where every node is connected to every other node.
    cliques = list(nx.find_cliques(G))
    print("\nCliques:")
    for clique in cliques:
        if len(clique) >= 2:
            print(f"  {clique}")

    # coloring assigns colors soo that adj vertices do not share a color.
    coloring = nx.coloring.greedy_color(G, strategy="largest_first")
    color_count = len(set(coloring.values())) if coloring else 0

    print("\ncoloring result:")
    print(f"  Colors used: {color_count}")

    for node, color in coloring.items():
        print(f"\n  {node}: color {color}")


def shortest_path_report(G):
    """
    Finds the shortest weighted path between two selected nodes.

    Chen, p. 321-322:
    The shortest path problem asks for the path with the smallest total
    weight between a start node and an end node.

    This function uses Dijkstra's algorithm through NetworkX.
    """

    nodes = list(G.nodes())

    if len(nodes) < 2:
        print("Need at least two nodes for shortest path.")
        return

    # Pick first and last node.
    start = nodes[0]
    end = nodes[-1]

    print("\nDIJKSTRA SHORTEST PATH")
    print(f"Start node: {start}")
    print(f"End node: {end}")

    try:
        path = nx.dijkstra_path(G, source=start, target=end, weight="weight")
        distance = nx.dijkstra_path_length(G, source=start, target=end, weight="weight")

        print("Shortest path:")
        print("  " + " -> ".join(path))
        print(f"Total weighted distance: {distance:.2f}")

    except nx.NetworkXNoPath:
        print("\n No path exists between these two nodes in the current graph.")


def draw_and_save_graph(G):
    """
    Draws and saves the object relationship graph.

    Bondy & Murty, p. 2:
    Graph diagrams help us understand graph properties visually.
    This function creates that visual representation.
    """

    if G.number_of_nodes() == 0:
        print("No objects detected. Nothing to draw.")
        return

    plt.figure(figsize=(12, 8))

    # Spring layout spaces nodes out nicely.
    pos = nx.spring_layout(G, seed=42)

    # Node labels.
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=1800,
        font_size=8,
        font_weight="bold"
    )

    # Edge labels show weights/distances.
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    plt.title("YOLOv11 Object Relationship Graph")
    
    # Save files for your paper.
    plt.savefig("object_graph.png", dpi=300, bbox_inches="tight")
    plt.savefig("object_graph.pdf", bbox_inches="tight")
    print("Saved graph as object_graph.png and object_graph.pdf")
    plt.show()


# MAIN CAMERA LOOP
while True:
    frame = picam2.capture_array()

    # Run YOLO object detection.
    results = model(frame, verbose=False)
    objects = []


    # OBJECT DETECTION TO VERTEX CREATION
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            label = model.names[class_id]
            confidence = float(box.conf[0])

            if confidence < confidence_limit:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            center_x = int((x1 + x2) / 2)
            center_y = int((y1 + y2) / 2)
            node_name = f"{label}_{len(objects)}"
            objects.append({

                "name": node_name,
                "label": label,
                "x": center_x,
                "y": center_y,
                "confidence": confidence,
                "box": (x1, y1, x2, y2)

            })
            # Draw box.
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            # Draw label.
            cv2.putText(
                frame,
                f"{node_name} {confidence:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

            # Draw object center.
            cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)

    # BUILd GRAPH FROM OBJECTS

    G = build_object_graph(objects)
    latest_graph = G
    latest_objects = objects

    # EDGES ON FRAME
    for u, v, data in G.edges(data=True):
        obj1 = next(obj for obj in objects if obj["name"] == u)
        obj2 = next(obj for obj in objects if obj["name"] == v)
        # Draw line between nearby obj.
        cv2.line(
            frame,
            (obj1["x"], obj1["y"]),
            (obj2["x"], obj2["y"]),
            (255, 0, 0),
            2
        )
        # Show weight near midpoint.
        mid_x = int((obj1["x"] + obj2["x"]) / 2)
        mid_y = int((obj1["y"] + obj2["y"]) / 2)
        cv2.putText(
            frame,
            str(data["weight"]),
            (mid_x, mid_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 0, 0),
            1
        )
    # Show instructions on screen.
    # MANUAL FUNCTIONALITY FOR GRAPHING 
    cv2.putText(frame, "G=save graph | R=report | D=Dijkstra | S=save frame | ESC=quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
    cv2.imshow("YOLOv11 Graph Theory Object Map ", frame)
    key = cv2.waitKey(1) & 0xFF

    # Press G to draw/save NetworkX graph.
    if key == ord("g"):
        draw_and_save_graph(latest_graph)
    # Press R to print graph theory report.
    if key == ord("r"):
        print_graph_report(latest_graph)
    # Press D to run Dijkstra shortest path.
    if key == ord("d"):
        shortest_path_report(latest_graph)
    # Press S to save camera frame.
    if key == ord("s"):
        cv2.imwrite("graph.png", frame)
        print("Saved camera image as graph.png")

    # Press ESC to quit.
    if key == 27:
        break

picam2.stop()
cv2.destroyAllWindows()
