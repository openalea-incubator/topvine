
# This file has been generated at Thu Feb 03 18:33:41 2011

from __future__ import absolute_import
from openalea.core import *


__name__ = 'alinea.topvine.reconstr_digit'

__editable__ = True
__description__ = 'data for topvine'
__license__ = ''
__url__ = ''
__alias__ = []
__version__ = '0.1.0'
__authors__ = ''
__institutes__ = ''
__icon__ = ''


__all__ = ['visu_digit_visu_digit', 'sc_turtle36_compute_optim_angle', 'visu_digit_fromcane_visu_digit_fromcane', 'sc_turtle36_sc_turtle36']



visu_digit_visu_digit = Factory(name='visu_digit',
                description='visualise digitalisation data from .d3d file',
                category='Unclassified',
                nodemodule='alinea.topvine.reconstr_digit.visu_digit',
                nodeclass='visu_digit',
                inputs=[{'interface': IFileStr, 'name': 'd3d file', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'A angle correction', 'value': 0, 'desc': 'degree'}, {'interface': ISequence, 'name': 'coord', 'value': [0, 0, 0], 'desc': ''}, {'interface': None, 'name': 'scene', 'value': None, 'desc': ''}, {'interface': IInt, 'name': 'nump', 'value': 1, 'desc': ''}, {'interface': IFloat, 'name': 'teta_row', 'value': 0, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




sc_turtle36_compute_optim_angle = Factory(name='compute_optim_angle',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.reconstr_digit.sc_turtle36',
                nodeclass='compute_optim_angle',
                inputs=[{'interface': None, 'name': 'dict', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'dseuil', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'v_angles', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




visu_digit_fromcane_visu_digit_fromcane = Factory(name='visu_digit_fromcane',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.reconstr_digit.visu_digit_fromcane',
                nodeclass='visu_digit_fromcane',
                inputs=[{'interface': IFileStr, 'name': 'csv_digit', 'value': None, 'desc': ''}, {'interface': None, 'name': 'carto', 'value': None, 'desc': ''}, {'interface': None, 'name': 'topo', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dazi', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dincli', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'par_allo', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'l_pet', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'H_pied', 'value': None, 'desc': ''}, {'interface': None, 'name': 'scene', 'value': None, 'desc': ''}, {'interface': None, 'name': 'forced_or', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}, {'interface': None, 'name': 'pts_out', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




sc_turtle36_sc_turtle36 = Factory(name='sc_turtle36',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.reconstr_digit.sc_turtle36',
                nodeclass='sc_turtle36',
                inputs=[{'interface': None, 'name': 'ls_pt', 'value': None, 'desc': ''}, {'interface': None, 'name': 'scene', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'size', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




