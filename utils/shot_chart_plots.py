import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from draw_court import draw_court


def plot_scatter(made, miss, title=None, filename="", color='sienna'):
    """
    Scatter plot of made and missed shots
    """
    plt.figure()
    draw_court()
    plt.plot(miss['COORD_X'], miss['COORD_Y'], 'x', color=color, markerfacecolor='none',
             label='Missed')
    plt.plot(made['COORD_X'], made['COORD_Y'], 'o', label='Made')

    plt.legend()
    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    plt.title(title)
    if filename != "":
        plt.savefig(filename)
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
        plt.savefig(filename)
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


def fg_perc_hex_heatmap(df, gridsize=10, mincnt=10, title=None, background=False):
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
    ax = draw_court(ax=ax, background=background)
    plt.title(title)
    plt.show()
    return


def plot_leading_scorers_by_zone(shot_df, lead_scorers_df):
    plt.figure()
    draw_court()
    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    for zone in lead_scorers_df.ZONE.unique():
        if zone not in [" ", "J"]:
            zone_df = shot_df[shot_df["ZONE"] == zone]
            y_annot = zone_df['COORD_Y'].median()
            if zone in ["B", "D", "F", "H"]:
                x_annot = zone_df['COORD_X'].median() - 150
            elif zone == "A":
                x_annot = -70
                y_annot = -70
            else:
                x_annot = zone_df['COORD_X'].median()
            player = lead_scorers_df.loc[lead_scorers_df["ZONE"] == zone, "PLAYER"].iloc[0]
            last, first = player.split(", ")
            player = f"{last} {first[:1]}."
            plt.annotate(player, (x_annot, y_annot), fontsize=8)
            plt.plot(zone_df['COORD_X'], zone_df['COORD_Y'], 'o', mfc='none', zorder=0)
    plt.show()
    return
