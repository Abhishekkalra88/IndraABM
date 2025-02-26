"""
Filename: display_methods.py
Author: Gene Callahan
A collection of convenience functions
for using matplotlib.
"""
import io
import sys
import logging
from functools import wraps

import lib.user as usr
import lib.utils as utl

graphics_present = True
no_graphics_msg = ""

user_type = utl.get_user_type(usr.TERMINAL)
if user_type != usr.API:
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        # import matplotlib.animation as animation
        import numpy as np
        import pandas as pd
        import seaborn as sns
        if sys.platform == "linux":
            matplotlib.use('TKAgg')
        sns.set(style="darkgrid")
        plt.ion()
    except ImportError as e:
        graphics_present = False
        no_graphics_msg = e.msg

global imageIO

DEBUG = utl.Debug()

anim_func = None

PURPLE = 'purple'
NAVY = 'navy'
BLUE = 'blue'
CYAN = 'cyan'
GREEN = 'green'
SPRINGGREEN = 'springgreen'
LIMEGREEN = 'limegreen'
YELLOW = 'yellow'
TAN = 'tan'
ORANGE = 'orange'
ORANGERED = 'orangered'
TOMATO = 'tomato'
RED = 'red'
DARKRED = 'darkred'
MAGENTA = 'magenta'
WHITE = 'white'
GRAY = 'gray'
BLACK = 'black'

colors = [RED,
          BLUE,
          GREEN,
          NAVY,
          SPRINGGREEN,
          ORANGE,
          LIMEGREEN,
          YELLOW,
          CYAN,
          TAN,
          ORANGERED,
          TOMATO,
          DARKRED,
          MAGENTA,
          BLACK,
          GRAY,
          PURPLE,
          WHITE
          ]

# the following strange mapping is for seaborn:
colors_dict = {"purple": PURPLE,
               "navy": NAVY,
               "blue": BLUE,
               "cyan": CYAN,
               "green": GREEN,
               "springgreen": SPRINGGREEN,
               "limegreen": LIMEGREEN,
               "yellow": YELLOW,
               "tan": TAN,
               "orange": ORANGE,
               "orangered": ORANGERED,
               "tomato": TOMATO,
               "red": RED,
               "darkred": DARKRED,
               "magenta": MAGENTA,
               "white": WHITE,
               "gray": GRAY,
               "black": BLACK}

NUM_COLORS = len(colors)
X = 0
Y = 1

DEFAULT_MARKER = 'default'
SQUARE = 'square'
TREE = 'tree'
CIRCLE = 'circle'
PERSON = 'person'
DECEASED = 'deceased'

seaborn_markers = ['8', 's', '^', 'o', 'x']

markers = {DEFAULT_MARKER: '8',
           SQUARE: 's',
           TREE: '^',
           CIRCLE: 'o',
           PERSON: 'o',
           DECEASED: 'x',
           }


def are_graphics_present():
    return graphics_present


def expects_plt(fn):
    """
    Should be used to decorate any function that uses matplotlib's pyplot.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not graphics_present:
            print("Graphics packages not found: install seaborn, pandas and "
                  + "matplotlib to do graphics.")
            return
        return fn(*args, **kwargs)
    return wrapper


def hierarchy_pos(graph, root, width=1., vert_gap=0.2, vert_loc=0.,
                  xcenter=0.5, pos=None, parent=None):
    """
    This is an attempt to get a tree graph from networkx.
    If there is a cycle that is reachable from root, then this will
    infinitely recurse.
    graph: the graph
    root: the root node of current branch
    width: horizontal space allocated for this branch
            - avoids overlap with other branches
    vert_gap: gap between levels of hierarchy
    vert_loc: vertical location of root
    xcenter: horizontal location of root
    pos: a dict saying where all nodes go if they have been assigned
    parent: parent of this branch.
    """
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = graph.neighbors(root)
    if parent is not None:
        neighbors.remove(parent)
    n_len = len(neighbors)
    dx = 0
    if n_len != 0:
        dx = width / n_len
        nextx = xcenter - width / 2 + dx / 2
        for neighbor in neighbors:
            pos = hierarchy_pos(graph, neighbor, width=dx,
                                vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap,
                                xcenter=nextx, pos=pos, parent=root)
            nextx += dx
    return pos


@expects_plt
def draw_graph(graph, title, hierarchy=False, root=None):
    """
    Drawing networkx graphs.
    graph is the graph to draw.
    hierarchy is whether we should draw it as a tree.
    Network drawings not yet implemented in V3.
    """
    # pos = None
    plt.title(title)
    # if hierarchy:
    #     pos = hierarchy_pos(graph, root)
    # out for now:
    # nx.draw(graph, pos=pos, with_labels=True)
    plt.show()


def get_color(var, i):
    if "color" in var:
        # Make sure it's a valid color
        if DEBUG.debug_lib:
            print("Checking to see if {} is in {}".format(var["color"],
                                                          colors))
        if var["color"] in colors:
            return var["color"]
    return colors[i % NUM_COLORS]


def get_marker(var, i):
    if "marker" in var:
        print("Getting a marker of", var["marker"])
        if var["marker"] in markers:
            mark = markers[var["marker"]]
            print("from markers, result = ", mark)
            return mark
    return markers[DEFAULT_MARKER]


class BarGraph():
    def __init__(self, title, varieties, data_points,
                 anim=False, data_func=None, is_headless=False, legend_pos=4):
        global anim_func
        self.title = title
        self.anim = anim
        self.data_func = data_func
        for i in varieties:
            data_points = len(varieties[i]["data"])
            break
        self.draw_graph(data_points, varieties)
        self.headless = is_headless

    @expects_plt
    def draw_graph(self, data_points, varieties):
        """
        Draw all elements of the graph.
        """
        self.fig, self.ax = plt.subplots()
        x = np.arange(0, data_points)
        self.create_bars(x, self.ax, varieties)
        self.ax.legend()
        self.ax.set_title(self.title)

    @expects_plt
    def create_bars(self, x, ax, varieties):
        bar_coordinates = 0
        steps = 1 / len(varieties)
        for i, var in enumerate(varieties):
            # take care of this kluge later
            data = varieties[var]["data"]
            color = get_color(varieties[var], i)
            if len(x) > 40:
                ax.bar(x[-40:] + bar_coordinates,
                       height=data[-40:], label=var,
                       color=color, width=steps)
            else:
                ax.bar(x + bar_coordinates,
                       height=data, label=var, color=color, width=steps)
            bar_coordinates += steps

    @expects_plt
    def show(self):
        """
        Display the barGraph.
        """
        if not self.headless:
            plt.show()
        else:
            file = io.BytesIO()
            plt.savefig(file, format="png")
            return file

    @expects_plt
    def update_plot(self, i):
        """
        This is our animation function.
        For line graphs, redraw the whole thing.
        """
        plt.clf()
        (data_points, varieties) = self.data_func()
        self.draw_graph(data_points, varieties)
        self.show()


class LineGraph():
    """
    We create a class here to save state for animation.
    Display a simple matplotlib line graph.
    The data is a dictionary with the label
    as the key and a list of numbers as the
    thing to graph.
    data_points is the length of the x-axis.
    """

    def __init__(self, title, varieties, data_points, attrs,
                 anim=False, data_func=None, is_headless=False):
        global anim_func

        plt.close()
        self.legend = []
        self.title = title
        self.anim = anim
        self.data_func = data_func
        for key in varieties:
            # Since all varieties have the same length, we just need the length
            # of one of them:
            data_points = len(varieties[key]["data"])
            break
        self.headless = is_headless
        self.draw_graph(data_points, varieties, attrs)

    def _handle_attrs(self, g, ax, leg_pos, attrs):
        """
        By default:
        Hides x and y labels (x on x axis and y on y axis).
        Shows x and y ticks (numbers on x and y axis).
        Shows grid lines (line on the ticks on x and y axis).
        Legend is located on top left.
        Shows legend.
        """
        if "show_special_points" in attrs:
            special_points = attrs["show_special_points"]
            for point in special_points:
                plt.plot(point[0], point[1], 'ro')
            special_points_name = attrs["special_points_name"]
            anno_x, anno_y = special_points[0][0], special_points[0][1]
            plt.annotate(special_points_name, xy=(anno_x, anno_y),
                         xytext=(3, 1.5),
                         arrowprops=dict(facecolor='black', shrink=0.05)
                         )
        if "show_xy_labels" not in attrs:
            ax.set_xlabel('')
            ax.set_ylabel('')
        if "hide_xy_ticks" in attrs:
            ax.set_yticklabels([])
            ax.set_xticklabels([])
        if "hide_grid_lines" in attrs:
            sns.set_style("whitegrid", {"axes.grid": False})
        if "legend_pos" in attrs:
            leg_pos = attrs["legend_pos"]
        if "hide_legend" not in attrs:
            handles, _ = g.get_legend_handles_labels()
            g.legend(handles, self.legend, loc=leg_pos)
        elif "hide_legend" in attrs:
            g.legend_.remove()

    @expects_plt
    def draw_graph(self, data_points, varieties, attrs):
        """
        Draw all elements of the graph.
        """
        leg_pos = "upper left"

        fig, ax = plt.subplots()
        ax.legend(self.legend)
        ax.set_title(self.title)
        x = np.arange(0, data_points)
        lines = self.create_lines(x, varieties)
        g = sns.lineplot(x="x", y="y", data=lines,
                         hue="color", palette=colors_dict)
        if attrs is not None:
            self._handle_attrs(g, ax, leg_pos, attrs)

    def create_lines(self, x, varieties):
        """
        Draw just the data portion.
        """
        lines = pd.DataFrame()
        for i, var in enumerate(varieties):
            self.legend.append(var)
            data = varieties[var]["data"]
            color = get_color(varieties[var], i)
            x_array = np.array(x)
            y_array = np.array(data)
            line = pd.DataFrame({"x": x_array,
                                 "y": y_array,
                                 "color": color,
                                 "var": var})
            lines = lines.append(line, ignore_index=True, sort=False)
        return lines

    @expects_plt
    def show(self):
        """
        Display the plot.
        """
        if not self.headless:
            plt.show()
        else:
            file = io.BytesIO()
            plt.savefig(file, format="png")
            return file

    @expects_plt
    def update_plot(self, i):
        """
        This is our animation function.
        For line graphs, redraw the whole thing.
        """
        plt.clf()
        (data_points, varieties) = self.data_func()
        self.draw_graph(data_points, varieties)
        self.show()


DEF_SIZE = 40


class ScatterPlot():
    """
    We are going to use a class here to save state for our animation
    """
    @expects_plt
    def __init__(self, title, varieties, width, height, attrs,
                 anim=True, data_func=None, is_headless=False):
        """
        Setup a scatter plot.
        `varieties` contains the different types of entities to show in the
        plot, which will get assigned different colors and perhaps markers.
        """
        global anim_func

        plt.close()
        self.scats = None
        self.anim = anim
        self.data_func = data_func
        self.headless = is_headless
        self.draw_graph(title, width, height, varieties, attrs)

    def _handle_attrs(self, g, ax, leg_pos, attrs):
        """
        By default:
        Grid spacing is every 10, starting from 0 (the begin index).
        Hides x and y labels (x on x axis and y on y axis).
        Shows x and y ticks (numbers on x and y axis).
        Shows grid lines (line on the ticks on x and y axis).
        Legend is located on top left.
        Shows legend.
        """
        if "change_grid_spacing" in attrs:
            """
            Begin index is where the grid spacing would start from.
            For example, if begin index is 6 and grid spacing is 9,
                the axis lines would be drawn from 6, then 15, 21, etc.
            """
            begin_index = attrs["change_grid_spacing"][0]
            grid_spacing = attrs["change_grid_spacing"][1]
            start, end = ax.get_xlim()
            ax.xaxis.set_ticks(np.arange(begin_index,
                                         end, grid_spacing))
            ax.yaxis.set_ticks(np.arange(begin_index,
                                         end, grid_spacing))
        if "show_xy_labels" not in attrs:
            ax.set_xlabel('')
            ax.set_ylabel('')
        if "hide_xy_ticks" in attrs:
            ax.set_yticklabels([])
            ax.set_xticklabels([])
        if "hide_grid_lines" in attrs:
            sns.set_style("whitegrid", {"axes.grid": False})
        if "legend_pos" in attrs:
            leg_pos = attrs["legend_pos"]
        if "hide_legend" not in attrs:
            handles, _ = g.get_legend_handles_labels()
            g.legend(handles, self.legend, loc=leg_pos)
        elif "hide_legend" in attrs:
            g.legend_.remove()

    @expects_plt
    def draw_graph(self, title, width, height, varieties, attrs):
        self.legend = []
        leg_pos = "upper left"

        fig, ax = plt.subplots()
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        self.create_scats(varieties)

        size = DEF_SIZE
        if attrs is not None and "size" in attrs:
            size = attrs["size"]

        g = sns.scatterplot(x="x", y="y", data=self.scats,
                            hue="color", palette=colors_dict,
                            style="marker", markers=seaborn_markers,
                            s=size)
        ax.set_title(title)
        if attrs is not None:
            self._handle_attrs(g, ax, leg_pos, attrs)

    def get_arrays(self, varieties, var):
        x_array = np.array(varieties[var][X])
        y_array = np.array(varieties[var][Y])
        return (x_array, y_array)

    @expects_plt
    def create_scats(self, varieties):
        self.scats = pd.DataFrame(columns=["x", "y", "color", "marker", "var"])
        for i, var in enumerate(varieties):
            if DEBUG.debug_lib:
                print("Appending {} to legend".format(var))
            self.legend.append(var)
            (x_array, y_array) = self.get_arrays(varieties, var)
            if len(x_array) <= 0:  # no data to graph!
                '''
                I am creating a single "position" for an agent that cannot
                be seen. This seems to fix the issue of colors being
                missmatched in the occasion that a group has no agents.
                '''
                x_array = [-1]
                y_array = [-1]
            elif len(x_array) != len(y_array):
                logging.debug("Array length mismatch in scatter plot")
                return
            # marker = get_marker(varieties[var], i)
            # print("After call to get_marker(), marker =", marker)
            scat = pd.DataFrame({"x": pd.Series(x_array),
                                 "y": pd.Series(y_array),
                                 "color": get_color(varieties[var], i),
                                 # "marker": marker,
                                 "var": var})
            self.scats = self.scats.append(scat, ignore_index=True,
                                           sort=False)

    @expects_plt
    def show(self):
        """
        Display the plot.
        """
        if not self.headless:
            plt.show()
        else:
            file = io.BytesIO()
            plt.savefig(file, format="png")
            return file

    @expects_plt
    def update_plot(self, i):
        """
        This is our animation function.
        """
        if self.scats is not None:
            for scat in self.scats:
                if scat is not None:
                    scat.remove()
        self.create_scats(self.data_func())
        return self.scats
