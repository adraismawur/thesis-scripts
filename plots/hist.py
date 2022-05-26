import matplotlib.pyplot as plt

def from_distances(full_distances, max=1000, bins=50, title=None, xlab=None, ylab=None, plot=plt):
    distances = []
    for idx, distance_entry in enumerate(full_distances):
        if idx == max:
            break
        distances.append(distance_entry[2])
    
    plot.hist(distances, bins=bins)

    if title is not None:
        plot.title(title)
    
    if xlab is not None:
        plot.xlabel(xlab)
    
    if ylab is not None:
        plot.ylabel(ylab)

    plot.show()
