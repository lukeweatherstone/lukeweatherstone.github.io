import numpy as np

B_road = 6          # clear width of the road carriageway, in metres
B_sup = 4           # clear width of the shared user path, in metres
B_barrier = 0.4     # distance from traffic barrier face to edge of deck, in metres
CF_road = 0.03      # cross fall for the road, as decimal
CF_sup = 0.025      # cross fall for the shared user path, as decimal

B_road_total = (B_road + B_barrier) / np.cos(np.arctan(CF_road))
B_sup_total = (B_sup + B_barrier) / np.cos(np.arctan(CF_sup))
B_total = B_road_total + B_sup_total

gap = 30        # gap between each girder
n_road = 3      # number of girders for the road bridge
n_sup = 2       # number of girders for the shared path

# Note that we'll minus half a girder here because the two bridges sides will "share" a gap between each girder.
flange_road = ((B_road_total * 1000) - ((n_road - 0.5) * gap)) / n_road
flange_sup = ((B_sup_total * 1000) - ((n_sup - 0.5) * gap)) / n_sup

space_road = flange_road + gap
space_sup = flange_sup + gap

print(space_sup)