import matplotlib.pyplot as plt

# Grid farm layout data
layout_x = [
    1347.6, 1640.9, 2248, 1934.2, 3149.3,
    2227.5, 4218.2, 2520.8, 4097, 4036.4
]

layout_y = [
    919, 1662.5, 1001, 2406, 1083.9,
    3149.5, 1564.4, 3893, 2666.3, 3711.2
]

# Plot
plt.figure()
plt.scatter(layout_x, layout_y)
plt.xlabel("X coordinate")
plt.ylabel("Y coordinate")
plt.title("Grid Farm Layout")
plt.axis("equal")
plt.grid(True)

# Optional: label each point
for i, (x, y) in enumerate(zip(layout_x, layout_y), start=1):
    plt.text(x, y, f"{i}", fontsize=9, ha="right", va="bottom")

plt.show()
