#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
import sys

############################################################
# COMMAND LINE PARAMETER
############################################################
if len(sys.argv) != 2:
    sys.exit("Please give a movie filename as output")

moviefile = sys.argv[1]


############################################################
# GLOBAL PARAMETERS
############################################################
# funnel size
s = 0.0001
H = 1
vol = 2 / 3 * np.pi
# physics
alpha = 0.6  # 0 < alpha <= sqrt(2) ?
g = 9.81  # gravitation
# animation
fps = 20
dt = 1000 / fps  # in milliseconds. The rest is in seconds.
resolution = 1000  # resolution to plot


############################################################
# GLOBAL FUNCTIONS (the physics behind)
############################################################
def v(h):
    """velocity of drainage when fluid of height h left"""
    return alpha * np.sqrt(g * h)


def area(h, r):
    """area of the funnel at height h"""
    return np.pi * r(h) ** 2


def dh(h, r):
    """ODE defining the system"""
    return -s * v(h) / area(h, r) * dt


############################################################
# FUNNEL as class
############################################################
class Funnel:
    """
    Defines a shape for a funnel, how it's plotted and animated.
    """
    frame_number = 0

    def __init__(self, r, h_max=H, h_min=0, res=resolution):
        """
        basic creation of a funnel.
        :param r: function defining the surface of rotation (radius at height)
        :param h_max: upper bound
        :param h_min: lower bound
        :param res: number of points to calculate the polygon
        """
        self.r = r
        self.h_max = h_max
        self.h_min = h_min
        self.res = res
        # calculate heights for animation
        self._calc_height()
        # variables to be set later by other functions.
        self.ax = None
        self.poly = None
        self.timer_text = None

    def cross_section(self, h):
        """
        Returns the cross_section of the funnel
        having the shape of a surface of rotation of the function self.r

        :param h: upper bound of definition
        :return: polygon as a list of vertices
        """
        y = np.linspace(self.h_min, h, self.res)
        # x = f(y)  # usually works, but gives cryptic error when max used in f
        x = np.array([self.r(yel) for yel in y])
        xx = np.append(x, np.flip(-x, 0))
        yy = np.append(y, np.flip(y, 0))
        return xx, yy

    #########################
    # HEIGHT CALCULATION
    #########################
    def _calc_height(self):
        """calculate array of heights for funnel given by radius r"""
        self.height = np.array([self.h_max])
        new_height = self.height[-1] + dh(self.height[-1], self.r)
        while new_height > 0:
            self.height = np.append(self.height, new_height)
            new_height = self.height[-1] + dh(self.height[-1], self.r)
        np.append(self.height, 0)
        if Funnel.frame_number <= len(self.height):
            Funnel.frame_number = len(self.height)
        return self.height

    #########################
    # DRAW FUNNEL
    #########################
    def add_funnel(self, ax):
        """
        adds the full funnel to ax and draws the first one.
        only supposed to be run once
        """
        ax.axis("equal")
        ax.set_xlim(-2, 2)
        ax.set_ylim(-0.5, 1.5)
        vertices = np.array(self.cross_section(self.h_max)).transpose()
        poly = ax.add_patch(patches.Polygon(vertices))
        border = ax.add_patch(patches.Polygon(vertices, fill=False, color='r'))
        v_pipe = np.array([[np.sqrt(s / np.pi), 0],
                           [-np.sqrt(s / np.pi), 0],
                           [-np.sqrt(s / np.pi), -0.3],
                           [np.sqrt(s / np.pi), -0.3]])
        ax.add_patch(patches.Polygon(v_pipe))
        tt = ax.text(0, 1.25, f"t = 0 s")
        self.ax = ax
        self.poly = poly
        self.timer_text = tt
        return poly, tt, border

    def draw_funnel(self, i):
        if i >= len(self.height):
            return self.poly, self.timer_text
        t = i * dt / 1000
        self.timer_text.set_text("t = {:5.2f} s".format(t))
        verts = np.array(self.cross_section(h=self.height[i])).transpose()
        self.poly.set_xy(verts)
        return self.poly, self.timer_text


############################################################
# EXAMPLE FUNNELS
############################################################
# normalise a function
def normalise(radius, h_max=H, h_min=0, res=resolution):
    hh = np.linspace(h_min, h_max, resolution)
    vol_actually = np.pi*sum(map(lambda x: x**2, map(radius, hh)))*(h_max - h_min)/res
    return lambda x: radius(x)*np.sqrt(vol/vol_actually)


# different funnels:
def radius_standard(h):
    """standard funnel"""
    return np.sqrt(s / np.pi) + h


def radius_half_sphere(h):
    return max(np.sqrt(s / np.pi), np.sqrt(H**2 - (H - h) ** 2))


def radius_sphere(h):
    eps = 0.001 # ugly but somehow necessary :(
    R = H+eps
    return max(np.sqrt(s / np.pi), np.sqrt(R**2/4 - (h - R/2) ** 2))


def get_radius_monomial(beta):
    """returns a function giving the volume as a monomial h**beta"""
    return lambda x: x**beta


# normalised radii
def radius_norm(h, low_r=np.sqrt(s / np.pi), volume=vol):
    big_r = -low_r / 2 + np.sqrt(
        (low_r / 2) ** 2 - low_r ** 2 + volume / (np.pi * H / 3))
    return low_r + h / H * (big_r - low_r)


# normalised sphere
radius_sphere_norm = normalise(radius_sphere)


# normalised cylinder funnel
def radius_cylinder(h):
    """ h is only needed because it needs this input"""
    return np.sqrt(vol/(np.pi*H))


############################################################
# EXAMPLE
############################################################
funnels = [Funnel(radius_norm),
           Funnel(radius_half_sphere),
           Funnel(radius_cylinder),
           Funnel(radius_sphere_norm)]
#funnels = [Funnel(normalise(get_radius_monomial(beta))) for beta in [1, 2, 4, 10]]

n = len(funnels)

############################################################
# ANIMATION
############################################################
fig = plt.figure(figsize=(16, 9))
axes = np.hstack(fig.subplots(2, 2))

for i, f in enumerate(funnels):
    f.add_funnel(axes[i])


def animate(i):
    for f in funnels:
        f.draw_funnel(i)
    return [f.poly for f in funnels]


ani = animation.FuncAnimation(fig, animate,
                              frames=Funnel.frame_number,
                              interval=dt, repeat=False)

# Set up formatting for the movie files
Writer = animation.writers['ffmpeg']
writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
ani.save(moviefile, writer=writer)
