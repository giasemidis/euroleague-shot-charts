import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from draw_court import draw_court
from matplotlib.patches import Polygon, Arc
from scipy.spatial import ConvexHull
import shapely
import shapely.plotting


def plot_scatter(made, miss, title=None, filename="", color='sienna'):
    """
    Scatter plot of made and missed shots
    """
    plt.figure(figsize=(475, 435))
    draw_court()
    plt.plot(miss['COORD_X'], miss['COORD_Y'], 'x', color=color, markerfacecolor='none',
             label='Missed')
    plt.plot(made['COORD_X'], made['COORD_Y'], 'o', label='Made')

    plt.legend()
    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    plt.title(title)
    if filename != "":
        plt.savefig(filename, bbox_inches='tight')
    plt.show()
    return


def plot_scatter_single_df(df, title=None, filename="", color='sienna'):
    """
    Scatter plot all attemps
    """
    plt.figure()
    draw_court()
    plt.plot(df['COORD_X'], df['COORD_Y'], 'o', color=color, zorder=0)
    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    plt.title(title)
    if filename != "":
        plt.savefig(filename, bbox_inches='tight')
    plt.show()
    return


def joint_plot(df, kind='hex', gridsize=10, title=None, background=False):
    """
    Density plot of shots as joint distributions of x and y coordinates
    """
    cmap = plt.cm.Oranges
    joint_shot_chart = sns.jointplot(x=df['COORD_X'], y=df['COORD_Y'],
                                     kind=kind, space=0, color=cmap(.5),
                                     xlim=[-800, 800], ylim=[-200, 1300],
                                     cmap=cmap, joint_kws={"gridsize": gridsize})
    joint_shot_chart.fig.suptitle(title, horizontalalignment='center')

    # A joint plot has 3 Axes, the first one called ax_joint
    # is the one we want to draw our court onto
    ax = joint_shot_chart.ax_joint
    draw_court(ax, background=background)
    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    plt.show()
    # return plot object for saving
    return joint_shot_chart


def fg_perc_hex_heatmap(df, gridsize=10, mincnt=10, title=None,
                        background=False, elogo=False):
    """
    The FG% by location in a hex grid
    """
    x = df["COORD_X"]
    y = df["COORD_Y"]
    z = np.where(df["POINTS"] > 0, 1, 0)

    cmap = plt.cm.Oranges
    fig, ax = plt.subplots()
    hb = ax.hexbin(x=x, y=y, C=z, gridsize=gridsize,
                   mincnt=mincnt, extent=[-800, 800, -200, 1300],
                   cmap=cmap, alpha=0.8, vmin=0., vmax=1.)
    cb = fig.colorbar(hb)
    ax = draw_court(ax=ax, background=background, elogo=elogo)
    plt.title(title)
    plt.show()
    return


def plot_leading_scorers_by_zone(shot_df, lead_scorers_df, zone_col="ZONE", title=None):
    """
    Plots the name of the leadings scorer by zone.

    Args:
        shot_df (pd.DataFrame): The dataframe with the shot data
        lead_scorers_df (pd.DataFrame): A dataframe with the zone and the name of the
            leadings scorer.
        zone_col (str, optional): The name of the "zone" column. Defaults to "ZONE".
            It allows for different definitions of the zones
    """
    plt.figure()
    # draw_court()
    plot_zones()
    for zone in lead_scorers_df[zone_col].unique():
        if zone not in [" ", "J"]:
            zone_df = shot_df[shot_df[zone_col] == zone]
            y_annot = zone_df['COORD_Y'].median()
            rotation = 0
            if zone in ["B", "D", "F", "H"]:
                x_annot = zone_df['COORD_X'].median() - 150
            elif zone == "A":
                x_annot = -70
                y_annot = -70
            elif zone == "H-Corner3":
                x_annot = -700
                y_annot = -100
                rotation = 90
            elif zone == "I-Corner3":
                x_annot = 700
                y_annot = -100
                rotation = 90
            else:
                x_annot = zone_df['COORD_X'].median()
            player = lead_scorers_df.loc[lead_scorers_df[zone_col] == zone, "PLAYER"].iloc[0]
            last, first = player.split(", ")
            player = f"{last} {first[:1]}."
            plt.annotate(player, (x_annot, y_annot), fontsize=8, rotation=rotation)
            # plt.plot(zone_df['COORD_X'], zone_df['COORD_Y'], 'o', mfc='none', zorder=0)
    plt.title(title)
    plt.show()
    return


def plot_zones():
    """
    Draws the court and the shooting zones, as defined by Euroleague.
    Threes are split into wing and corner threes per zone.
    The 2pt shot zones are found by drawing hundreds of shots since 2020
    and finding the boundary of these zones using geometry objects.
    Hence, this function depends on shot data since 2020.
    The imlementation is a bit ad-hoc at the moment.

    Returns:
        matplotlib.axes: The plot object
    """

    data_dir = "~/Documents/euroleague_api/notebooks/data"
    shot_df = pd.read_csv(os.path.join(data_dir, "shot_data_2007_2023.csv"))
    shot_df = shot_df[shot_df["Season"] >= 2020]
    shot_df = shot_df[~(shot_df["ZONE"].isin(["H", "I"]) & shot_df["ID_ACTION"].str.contains("2FG"))]
    shot_df = shot_df[~((shot_df["ZONE"] == "F") & (shot_df["COORD_X"] < -640))]

    threepointarc = Arc((0, 0), 2 * 675, 2 * 675, theta1=12, theta2=167.5)
    v = threepointarc.get_verts()
    ax = draw_court()
    left_corner3 = np.array([[-750, -157.5], [-750 + 90, -157.5], [-750 + 90, 147.5], [-750, 147.5], [-750, -157.5]])
    right_cornder3 = np.array([[750, -157.5], [750 - 90, -157.5], [750 - 90, 147.5], [750, 147.5], [750, -157.5]])
    left3 = np.concatenate(
        (
            np.array([[0, 675], [0, 1400-157.5], [-750, 1400-157.5], [-750, 147.5], [-750 + 90, 147.5]]),
            v[v[:, 0] <= 0][::-1]
        ),
        axis=0
    )
    right3 = np.concatenate(
        (
            np.array([[0, 675], [0, 1400 - 157.5], [750, 1400 - 157.5], [750, 147.5], [750 - 90, 147.5]]),
            v[v[:, 0] >= 0]
        ),
        axis=0
    )
    plc3 = Polygon(left_corner3, facecolor = 'blue', alpha=0.4)
    prc3 = Polygon(right_cornder3, facecolor = 'orange', alpha=0.4)
    pl3 = Polygon(left3, facecolor='green', alpha=0.4)
    pr3 = Polygon(right3, facecolor='red', alpha=0.4)
    ax.add_patch(plc3)
    ax.add_patch(prc3)
    ax.add_patch(pl3)
    ax.add_patch(pr3)

    colours = ["purple", "brown", "pink", "gray", "navy", "olive", "cyan"]
    zone_dependencies = {
        "B": "A", "C": "A", "D": "B", "E": "C", "F": "D", "G": "E"
    }
    zones_pols = {}
    for zone, c in zip(["A", "B", "C", "D", "E", "F", "G"], colours):
        zone_df = shot_df[shot_df["ZONE"] == zone]
        ch = ConvexHull(list(zip(zone_df["COORD_X"], zone_df["COORD_Y"])))
        pg = shapely.Polygon(ch.points[ch.vertices])
        zones_pols[zone] = pg
        if zone in zone_dependencies.keys():
            pg = shapely.difference(pg, zones_pols[zone_dependencies[zone]])
        ax.add_patch(shapely.plotting.patch_from_polygon(pg, facecolor=c, alpha=0.4))

    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    return ax