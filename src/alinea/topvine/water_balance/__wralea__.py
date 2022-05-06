
# This file has been generated at Thu Dec 16 11:16:57 2010

from __future__ import absolute_import
from openalea.core import *


__name__ = 'alinea.topvine.water_balance'

__editable__ = True
__description__ = 'Lebeon et al 2003 water balance model'
__license__ = ''
__url__ = ''
__alias__ = []
__version__ = ''
__authors__ = ''
__institutes__ = ''
__icon__ = ''


__all__ = ['wb_1C_TSW_1C', 'open_meteo_file_open_meteo_wb', 'plot_res_1C_plot_res_1C', 'open_meteo_file_mef_meteo_wb', 'wb_1C_soil_EV_1C', 'turbid_vine_turbid_vineCyl', 'turbid_vine_turbid_vineVSP', 'wb_1C_vine_T_1C']



wb_1C_TSW_1C = Factory(name='TSW_1C',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.water_balance.wb_1C',
                nodeclass='TSW_1C',
                inputs=[{'interface': IFloat, 'name': 'PreviousTSW', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Precip', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'ES', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'TV', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'TSWmax', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'TSW', 'desc': ''}, {'interface': None, 'name': 'FTSW', 'desc': ''}, {'interface': None, 'name': 'D', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




open_meteo_file_open_meteo_wb = Factory(name='open_meteo_wb',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.water_balance.open_meteo_file',
                nodeclass='open_meteo_wb',
                inputs=[{'interface': IFileStr, 'name': 'meteo_day', 'value': None, 'desc': ''}, {'interface': IFileStr, 'name': 'meteo_hour', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'meteo_dict_day', 'desc': ''}, {'interface': None, 'name': 'Rg_hourly', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




plot_res_1C_plot_res_1C = Factory(name='plot_res_1C',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.water_balance.plot_res_1C',
                nodeclass='plot_res_1C',
                inputs=[{'interface': None, 'name': 'res', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'opt', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




open_meteo_file_mef_meteo_wb = Factory(name='mef_meteo_wb',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.water_balance.open_meteo_file',
                nodeclass='mef_meteo_wb',
                inputs=[{'interface': None, 'name': 'meteo_dict', 'value': None, 'desc': ''}, {'interface': None, 'name': 'dayly_Rg', 'value': None, 'desc': ''}, {'interface': IInt, 'name': 'DOY', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'meteo_dat', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




wb_1C_soil_EV_1C = Factory(name='soil_EV_1C',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.water_balance.wb_1C',
                nodeclass='soil_EV_1C',
                inputs=[{'interface': IFloat, 'name': 'Et0', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Precip', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'epsi', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'previous_state', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'albedo', 'value': 0.14999999999999999, 'desc': ''}, {'interface': IFloat, 'name': 'U', 'value': 5, 'desc': ''}, {'interface': IFloat, 'name': 'b', 'value': 0.63, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'ES', 'desc': ''}, {'interface': None, 'name': 'prev', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




turbid_vine_turbid_vineCyl = Factory(name='turbid_vineCyl',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.water_balance.turbid_vine',
                nodeclass='turbid_vineCyl',
                inputs=[{'interface': IFloat, 'name': 'TT', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'LADini', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'LAImax', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Hmax', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Hpied', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'ouverture', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dazi', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dincli', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'dsize', 'value': 0.001, 'desc': ''}, {'interface': IInt, 'name': 'seed', 'value': 0, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




turbid_vine_turbid_vineVSP = Factory(name='turbid_vineVSP',
                description='',
                category='modelling',
                nodemodule='alinea.topvine.water_balance.turbid_vine',
                nodeclass='turbid_vineVSP',
                inputs=[{'interface': IFloat, 'name': 'TT', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'LADini', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'LAImax', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Hmax', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Largmax', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Hpied', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dazi', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dincli', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'dsize', 'value': 0.001, 'desc': ''}, {'interface': IInt, 'name': 'seed', 'value': 0, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




wb_1C_vine_T_1C = Factory(name='vine_T_1C',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.water_balance.wb_1C',
                nodeclass='vine_T_1C',
                inputs=[{'interface': IFloat, 'name': 'Et0', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'epsi', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'FTSW', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'albedo', 'value': 0.14999999999999999, 'desc': ''}, {'interface': IFloat, 'name': 'FTSWthreshold', 'value': 0.40000000000000002, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'TV', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




