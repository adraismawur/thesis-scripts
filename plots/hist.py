import matplotlib.pyplot as plt

def from_distances(full_distances, max=1000, bins=50, title=None, xlab=None, ylab=None):
    distances = []
    for idx, distance_entry in enumerate(full_distances):
        if idx == max:
            break
        distances.append(distance_entry[2])
    
    plt.hist(distances, bins=bins)

    if title is not None:
        plt.title(title)
    
    if xlab is not None:
        plt.xlabel(xlab)
    
    if ylab is not None:
        plt.ylabel(ylab)

    plt.show()
