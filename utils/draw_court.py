import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc
from scipy import ndimage


def draw_court(ax=None, color='black', lw=1, outer_lines=True,
               background=True, elogo=True, watermark=True):
    """
    FIBA basketball court dimensions:
    https://www.msfsports.com.au/basketball-court-dimensions/
    It seems like the Euroleauge API returns the shooting positions
    in resolution of 1cm x 1cm.
    """
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        # ax = plt.gca()
        fig, ax = plt.subplots()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 45.72cm so it has a radius 45.72/2 cms
    hoop = Circle((0, 0), radius=45.72 / 2, linewidth=lw, color=color,
                  fill=False)

    # Create backboard
    backboard = Rectangle((-90, -157.5 + 120), 180, -1, linewidth=lw,
                          color=color)

    # The paint
    # Create the outer box of the paint
    outer_box = Rectangle((-490 / 2, -157.5), 490, 580, linewidth=lw,
                          color=color, fill=False)
    # Create the inner box of the paint, width=12ft, height=19ft
    inner_box = Rectangle((-360 / 2, -157.5), 360, 580, linewidth=lw,
                          color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 580 - 157.5), 360, 360, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 580 - 157.5), 360, 360, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 2 * 125, 2 * 125, theta1=0, theta2=180,
                     linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines
    corner_three_a = Rectangle((-750 + 90, -157.5), 0, 305, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((750 - 90, -157.5), 0, 305, linewidth=lw,
                               color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 2 * 675, 2 * 675, theta1=12, theta2=167.5,
                    linewidth=lw, color=color)

    # Center Court
    center_outer_arc = Arc((0, 1400-157.5), 2 * 180, 2 * 180, theta1=180,
                           theta2=0, linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box,
                      restricted, top_free_throw, bottom_free_throw,
                      corner_three_a, corner_three_b, three_arc,
                      center_outer_arc]
    if outer_lines:
        # Draw the half court line, baseline and side out bound lines
        outer_lines = Rectangle((-750, -157.5), 1500, 1400, linewidth=lw,
                                color=color, fill=False)
        court_elements.append(outer_lines)

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    plt.xlim([-800, 800])
    plt.ylim([-200, 1300])
    # tr = Affine2D().rotate_deg(90.)
    if background:
        file = os.path.split(__file__)[0] + "/stylistic-images/basketball-court-texture.jpg"
        if os.path.exists(file):
            img = plt.imread(file)
            img = ndimage.rotate(img, 90)
            ax.imshow(img, extent=[-750, 750, -157.5, 1557.4], alpha=0.9)
    if elogo:
        file = os.path.split(__file__)[0] + "/stylistic-images/ELB_Horizontal_1C_On Light_RGB.png"
        if os.path.exists(file):
            img = Image.open(file)
            f = 14
            sz1, sz2 = np.array(img.size) / f
            img = img.resize((int(np.floor(sz1)), int(np.floor(sz2))))
            img = img.rotate(270, Image.NEAREST, expand=1)
            # fig = fig.figimage(img, xo=65, yo=270)
            fig = fig.figimage(img, xo=80, yo=230)
    if watermark:
        ax.text(0.5, 0.9, '@g_giase', transform=ax.transAxes,
        fontsize=16, color='black', alpha=0.5,
        ha='center', va='center', rotation=0)


    return ax
