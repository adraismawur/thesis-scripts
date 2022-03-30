import matplotlib.pyplot as plt

def from_distances(full_distances, max=1000, bins=50):
    distances = []
    for idx, distance_entry in enumerate(full_distances):
        if idx == max:
            break
        distances.append(distance_entry[2])
    
    plt.hist(distances, bins=bins)
    plt.show()
