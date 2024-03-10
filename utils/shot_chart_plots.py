from matplotlib import pyplot as plt
import seaborn as sns
from draw_court import draw_court


def plot_scatter(made, miss, title=None, filename=""):
    """
    Scatter plot of made and missed shots
    """
    plt.figure()
    draw_court()
    plt.plot(miss['COORD_X'], miss['COORD_Y'], 'x', markerfacecolor='none',
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


def joint_plot(df, kind='hex', title=None):
    """
    Density plot of shots as joint distributions of x and y coordinates
    """
    cmap = plt.cm.gist_heat_r
    joint_shot_chart = sns.jointplot(x=df['COORD_X'], y=df['COORD_Y'],
                                     kind=kind, space=0, color=cmap(.2),
                                     cmap=cmap, joint_kws={"gridsize": 15})
    joint_shot_chart.fig.suptitle(title, horizontalalignment='center')

    # A joint plot has 3 Axes, the first one called ax_joint
    # is the one we want to draw our court onto
    ax = joint_shot_chart.ax_joint
    draw_court(ax)
    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    plt.show()
    # return plot object for saving
    return joint_shot_chart
