#!/usr/bin/env python3.10
# -*- coding: utf-8 -*-

"""
Calorinator - Diet tracker
Copyright (C) 2023 Markus Ottela

This file is part of Calorinator.
Calorinator is free software: you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version. Calorinator is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License
along with Calorinator. If not, see <https://www.gnu.org/licenses/>.
"""

import typing

from datetime import datetime

# noinspection PyPackageRequirements
import pylab  # type: ignore
import pygame

import matplotlib  # type: ignore
import matplotlib.backends.backend_agg as agg  # type: ignore
import matplotlib.pyplot               as plt  # type: ignore
import numpy                           as np   # type: ignore

from src.common.exceptions import EscPressed
from src.common.statics    import Format, Program

if typing.TYPE_CHECKING:
    from matplotlib.figure import Figure  # type: ignore
    from src.ui.gui        import GUI


# Graph colors
grey       = '#1E1E1E'
light_grey = '#B4B4B4'


def draw_graph(measurement_log: dict) -> pygame.Surface:
    """Draw graph for measurement log."""
    figure = init_figure()

    dt_log = {}
    for date_string, value in measurement_log.items():
        dt        = datetime.strptime(date_string, Format.DATETIME_DATE.value)
        dt_log[dt] = value

    start_date = list(dt_log.keys())[0]

    days         = []
    measurements = []

    for dt, measurement in dt_log.items():
        days.append((dt - start_date).days)
        measurements.append(measurement)

    if len(days) == 1:  # Mock previous day on day 1 to get a line visible
        days         = [-1]              + days
        measurements = [measurements[0]] + measurements

    plt.plot(days, measurements,
             linestyle='', color=light_grey,
             marker='+', label='')  # Scatter plot
    plt.plot(days, measurements, linestyle='-', linewidth=1)

    x_min = -1
    x_max = (datetime.now() - start_date).days + 1
    y_min = min(measurement_log.values()) - 1
    y_max = max(measurement_log.values()) + 2

    if y_min == y_max:
        y_min -= 1

    plt.suptitle(f'Weight', fontsize=14, fontweight='bold', color=light_grey)

    create_axes(days[-1], x_min, x_max, y_min, y_max)

    return render_figure(figure)


# -----------------------------------------------------------------------------


def create_axes(days  : int,
                x_min : int,
                x_max : int,
                y_min : int,
                y_max : int
                ) -> None:
    """Mark axis tick marks."""

    plt.yticks([])

    x_max = max(x_max, 30)

    # Mark axes' lengths
    plt.axis([x_min, x_max, y_min, y_max])

    x_tick_freq = 1 if days < 30 else 7
    y_tick_freq = 1

    plt.xticks(np.arange(x_min, x_max, x_tick_freq))
    plt.yticks(np.arange(y_min, y_max, y_tick_freq))

    x_ticks = list(plt.xticks()[0])
    y_ticks = list(plt.yticks()[0])

    plt.xticks(x_ticks + [days, x_max])
    plt.yticks(y_ticks)

    # Create axes' labels
    plt.xlabel('Days',         color=light_grey)
    plt.ylabel(f'Weight (kg)', color=light_grey)


def render_figure(figure: 'Figure') -> pygame.Surface:
    """Render the figure into a pygame surface."""
    canvas = agg.FigureCanvasAgg(figure)
    canvas.draw()

    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size     = canvas.get_width_height()

    # noinspection PyTypeChecker
    frame = pygame.image.fromstring(raw_data, size, 'RGB')
    return frame


def init_figure(dpi: int = 100) -> 'Figure':
    """Initialize figure."""
    plt.clf()
    matplotlib.use("Agg")
    figure_size = list(map(lambda x: x / dpi, Program.RESOLUTION.value))
    figure      = pylab.figure(figsize=figure_size, dpi=dpi, facecolor=grey)

    set_colors()  # We set colors here just to ensure we can't accidentally mess up the order.
    return figure


def set_colors() -> None:
    """Set global colors for the graph."""
    # Axes' colors
    ax = plt.axes()
    ax.set_facecolor(grey)
    ax.spines['bottom'].set_color(light_grey)
    ax.spines['top'].set_color(light_grey)
    ax.spines['left'].set_color(light_grey)
    ax.spines['right'].set_color(light_grey)
    ax.tick_params(axis='x', colors=light_grey)
    ax.tick_params(axis='y', colors=light_grey)

    # Label colors
    plt.rcParams.update({'text.color'      : light_grey,
                         'axes.labelcolor' : light_grey})


def show_weight_progress(gui: 'GUI', weight_log: dict) -> None:
    """Plot weight data on a line chart."""
    frame = draw_graph(weight_log)

    gui.display.blit(frame, (0, 0))
    gui.draw_screen()

    while True:
        try:
            gui.check_events()
            gui.tick()

        except EscPressed:
            return
