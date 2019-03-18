from pss_io import pss_group_force
from geo_io import GeoData, get_date, get_date_range, daterange, swath_selection
from pss_plot_jpg import add_basemap
from Utils.plogger import Logger, timed
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image
from datetime import date, timedelta

PREFIX = r'plots_jpg\pss_plot_'
MAP_FILE = r'BackgroundMap/3D_31256.jpg'
EDGECOLOR = 'black'
EPSG_31256_adapted = "+proj=tmerc +lat_0=0 +lon_0=16.33333333333333"\
                     " +k=1 +x_0=+500000 +y_0=0 +ellps=bessel "\
                     "+towgs84=577.326,90.129,463.919,5.137,1.474,5.297,2.4232 +units=m +no_defs"
EPSG_WGS84 = 4326
Image.MAX_IMAGE_PIXELS = 2000000000
MARKERSIZE = 0.02
MARKERSCALE = 5.0
FIGSIZE = 8
HIGH_FORCE=60
MEDIUM_FORCE=35
maptitle = ('VPs 3D Schonkirchen', 12)
logger = Logger.getlogger()
nl = '\n'

class PlotMap:
    '''  class contains method to plot the pss data, swath boundary, map and 
         active patch
    '''
    def __init__(self, initial_date):
        self.initial_date = initial_date

        self.fig, self.ax = self.setup_map(figsize=(FIGSIZE, FIGSIZE))
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)

        self.force_attrs = { '1HIGH': ['red', f'high > {HIGH_FORCE}'],
                             '2MEDIUM': ['cyan', f'medium > {MEDIUM_FORCE}'],
                             '3LOW': ['yellow', f'low <= {MEDIUM_FORCE}'],}
        self.force_levels = ['3LOW', '2MEDIUM', '1HIGH']


    def setup_map(self, figsize):
        ''' setup the map and background '''
        fig, ax = plt.subplots(figsize=figsize)

        # plot the swath boundary
        _, _, _, swaths_bnd_gpd = GeoData().filter_geo_data_by_swaths(swaths_selected=[0], 
                                                                      swaths_only=True,
                                                                      source_boundary=False,)
        swaths_bnd_gpd.crs = EPSG_31256_adapted 
        swaths_bnd_gpd.plot(ax=ax, facecolor='none', edgecolor=EDGECOLOR)

        # obtain the extent of the data based on swaths_bnd_gdf
        extent_map = ax.axis()
        logger.info(f'extent data swaths: {extent_map}')

        # plot the basemap background
        add_basemap(ax)

        # restore original x/y limits
        ax.axis(extent_map)

        return fig, ax

    @timed(logger)  #pylint: disable=no-value-for-parameter
    def plot_pss_data(self, from_date, to_date):
        '''  plot pss force data in three ranges LOW, MEDIUM, HIGH '''
        logger.info(f'---------{to_date.strftime("%d-%B-%y")}-----------------------------')

        vib_pss_gpd = pss_group_force(from_date, to_date, HIGH_FORCE, MEDIUM_FORCE)
        vib_pss_gpd = vib_pss_gpd.to_crs(EPSG_31256_adapted)

        # plot the VP grouped by force_level

        # for force_level, vib_pss in vib_pss_gpd.groupby('force_level'):
        #     print(force_level)
        #     vib_pss.plot(ax=self.ax,
        #                  color=force_attrs[force_level][0],
        #                  markersize=MARKERSIZE, gid='pss')

        for force_level in self.force_levels:
            try:
                vib_pss = vib_pss_gpd[vib_pss_gpd['force_level'] == force_level]
            except TypeError:
                continue
            
            vib_pss.plot(ax=self.ax, 
                         color=self.force_attrs[force_level][0],
                         markersize=MARKERSIZE, gid='pss')

        self.plt_save(to_date)

    def add_legend(self):
        force_legend = []
        for force_level in self.force_levels:
            force_legend.append(Line2D([], [], marker='o', linestyle='',
                                       color='white',
                                       markerfacecolor=self.force_attrs[force_level][0], 
                                       label=self.force_attrs[force_level][1],
                                       markersize=MARKERSCALE))

        self.legend_gid = self.ax.legend(handles=force_legend)

    @timed(logger)  #pylint: disable=no-value-for-parameter
    def plt_save(self, _date):
        self.fig.canvas.restore_region(self.background)

        if self.initial_date:
            plotfile = PREFIX + ''.join([self.initial_date.strftime("%y%m%d"),
                                        '_', _date.strftime("%y%m%d"), '.png'])
        else:
            plotfile = PREFIX + ''.join([_date.strftime("%y%m%d"), '.png'])

        self.ax.set_title(''.join([maptitle[0], ' ', _date.strftime("%d-%b-%y")]), 
                          fontsize=maptitle[1])
        self.add_legend()
        plt.savefig(plotfile)

        # in case self.initial date is None then delete pss data from map to show single days
        if self.initial_date == None:
            self.delete_from_map('pss')
        else:
            pass # keep the points for cumulated plot
        self.legend_gid.remove()

    def delete_from_map(self, gid):
        for plot_object in reversed(self.ax.collections):
            if plot_object.get_gid() == gid:
                plot_object.remove()


def main():
    print('What is the plot range? ')
    start_date = -1
    while start_date == -1:
        start_date, end_date = get_date_range()

    if input('Single days [y/n]? ')[0] in ['y', 'Y']:
        initial_date = None
    else:
        print('What is the initial date? ', end='')
        initial_date = get_date()
        assert initial_date <= start_date, "initial date must be before start date"

    plt_map = PlotMap(initial_date)

    if initial_date != None:
        plt_map.plot_pss_data(initial_date, start_date)
        print(f'plotted map for {start_date.strftime("%d-%B-%y")}')
        start_date += timedelta(1)

    for day in daterange(start_date, end_date):
        plt_map.plot_pss_data(day, day)
        print(f'plotted map for {day.strftime("%d-%B-%y")}')


if __name__ == "__main__":
    logger.info(f'{nl}============================================'\
                f'{nl}===>   Running: pss_plot_range_jpg      <==='\
                f'{nl}============================================')

    main()
    