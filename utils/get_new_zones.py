import numpy as np
from matplotlib import pyplot as plt


def corner_three_zones(df, corner_three_y=147.5):
    """
    Split the two 3pt zones into corner three and wing three.

    Args:
        df (pd.DataFrame): The dataframe of the shooting data.
        corner_three_y (float, optional): The y coord defining the span of corner three.
            Defaults to 147.5.

    Returns:
        pd.DataFrame: The shooting data dataframe with an extra column the corrected
            zones with corder threes
    """
    df["ZONE_C"] = df["ZONE"].copy()
    corner_three_mask = df["ZONE"].isin(["H", "I"]) & (df["COORD_Y"] <= corner_three_y)
    df.loc[corner_three_mask, "ZONE_C"] += "-Corner3"
    return df


def hexagon_zones(df, gridsize=10):
    x = df["COORD_X"]
    y = df["COORD_Y"]
    z = np.where(df["POINTS"] > 0, 1, 0)

    # cmap = plt.cm.Oranges
    _, ax = plt.subplots()
    hb = ax.hexbin(x=x, y=y, C=z, gridsize=gridsize,
                   extent=[-800, 800, -200, 1300],
                   alpha=0.8, vmin=0., vmax=1.)
    plt.close()

    offsets = hb.get_offsets()
    # Create an empty array to store the indices of the bins
    indices = []

    # Loop through each point and find which bin it belongs to
    for x_, y_ in zip(x, y):
        dist = np.linalg.norm(offsets - np.array([x_, y_]), axis=1)
        closest_bin = np.argmin(dist)
        indices.append(hash((offsets[closest_bin][0], offsets[closest_bin][1])))

    df["ZONE_HEX"] = indices
    return df