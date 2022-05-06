
# This file has been generated at Thu Apr 23 20:39:57 2015

from openalea.core import *


__name__ = 'alinea.topvine'

__editable__ = True
__description__ = '3D reconstruction model of grapevine canopy'
__license__ = ''
__url__ = ''
__alias__ = ['topvine']
__version__ = '3.0'
__authors__ = 'Gaetan Louarn'
__institutes__ = ''
__icon__ = 'icon.png'


__all__ = ['write_table_write_table', 'write_geom_file_write_geom_file', 'extract_plant_extract_plant', 'IOtable_write_dict', 'groupOutput_phyto_groupOutput_phyto', 'copy_copy', 'get_vine_caracteristics_get_vine_caracteristics', 'gen_shoot_param_gen_shoot_param', 'scene2can_scene2can', 'primitive_add_assim_chamber', 'read_geom_file_read_geom_file', 'topologise_topologise', 'appendL_appendL', 'put_square_put_square', 'dict_param_vine_dict_param_vine', 'update_normal_canopy_update_normal_canopy', 'get_dl_shoot_get_dl_shoot', 'pickleD_pickleD', 'CxT_select_CxT_select', 'translate_shoots_translate_shoots', 'read_stand_file_read_stand_file', 'scene_to_can_scene_to_can', 'read_allometry_read_allometry', 'visu_digit_visu_digit', 'vine_topiary_vine_topiary', 'gen_normal_canopy_gen_normal_canopy', 'expandOutput_phyto_expandOutput_phyto', 'tortl_inst_vine_tortl_inst_vine', 'mef_skt_mef_skt', 'allometry_allometry', 'primitive_bunch', 'get_key_get_key', 'get_dl_get_dl', 'compute_TT_compute_TT']



write_table_write_table = Factory(name='write_table',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.write_table',
                nodeclass='write_table',
                inputs=[{'interface': None, 'name': 'table', 'value': None, 'desc': ''}, {'interface': IDirStr, 'name': 'folder path', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'name', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




write_geom_file_write_geom_file = Factory(name='write_geom_file',
                authors='Gaetan Louarn (wralea authors)',
                description='save shoot params in a csv file',
                category='IO',
                nodemodule='alinea.topvine.write_geom_file',
                nodeclass='write_geom_file',
                inputs=[{'interface': ISequence, 'name': 'tab geom', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'file name', 'value': 'toto.csv', 'desc': ''}],
                outputs=[{'interface': IFileStr, 'name': 'file', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




extract_plant_extract_plant = Factory(name='extract_plant',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.extract_plant',
                nodeclass='extract_plant',
                inputs=[{'interface': None, 'name': 'dict', 'value': None, 'desc': ''}, {'interface': IInt, 'name': 'nump', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'plant dict', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




IOtable_write_dict = Factory(name='write_dict',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.IOtable',
                nodeclass='write_dict',
                inputs=[{'interface': None, 'name': 'dict', 'value': None, 'desc': ''}, {'interface': IDirStr, 'name': 'folder_path', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'name', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'file path', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




scene2can_scene2can = Factory(name='scene2can',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.scene_to_can',
                nodeclass='scene2can',
                inputs=[{'interface': None, 'name': 'scene', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'name', 'value': None, 'desc': ''}],
                outputs=[{'interface': IFileStr, 'name': 'can file', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




groupOutput_phyto_groupOutput_phyto = Factory(name='groupOutput_phyto',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.groupOutput_phyto',
                nodeclass='groupOutput_phyto',
                inputs=[{'interface': None, 'name': 'caribu_dict', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'key', 'value': None, 'desc': ''}, {'interface': IBool, 'name': 'sum', 'value': False, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'caribu_dict', 'desc': ''}, {'interface': None, 'name': 'av_disct', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




copy_copy = Factory(name='copy',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.copy',
                nodeclass='copy',
                inputs=[{'interface': None, 'name': 'obj', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'copy', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




get_vine_caracteristics_get_vine_caracteristics = Factory(name='get_vine_caracteristics',
                authors='Gaetan Louarn (wralea authors)',
                description='read stand table at rank n and return vine position and shoot number ',
                category='scene.topvine',
                nodemodule='alinea.topvine.get_vine_caracteristics',
                nodeclass='get_vine_caracteristics',
                inputs=[{'interface': ISequence, 'name': 'stand table', 'value': None, 'desc': ''}, {'interface': IInt, 'name': 'vine rank', 'value': 0, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'position', 'desc': ''}, {'interface': IInt, 'name': 'shoot number', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




gen_shoot_param_gen_shoot_param = Factory(name='gen_shoot_param',
                authors='Gaetan Louarn (wralea authors)',
                description='generates shoot parameters for a vine of n shoots',
                category='Unclassified',
                nodemodule='alinea.topvine.gen_shoot_param',
                nodeclass='gen_shoot_param',
                inputs=[{'interface': IInt, 'name': 'n', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'spurs0', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dspurs', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'f_azi', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'shoot laws', 'value': None, 'desc': ''}, {'interface': IInt, 'name': 'graine', 'value': 0, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'shoot params', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




primitive_add_assim_chamber = Factory(name='add_assim_chamber',
                authors='Gaetan Louarn (wralea authors)',
                description='add the structure the vine assimilation chamber into a scene',
                category='Unclassified',
                nodemodule='alinea.topvine.primitive',
                nodeclass='add_assim_chamber',
                inputs=[{'interface': None, 'name': 'scene', 'value': None, 'desc': ''}, {'interface': None, 'name': 'p0', 'value': [0, 0, 0], 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




read_geom_file_read_geom_file = Factory(name='read_geom_file',
                description='read geom file and return shoot params as a table',
                category='IO',
                nodemodule='alinea.topvine.read_geom_file',
                nodeclass='read_geom_file',
                inputs=[{'interface': IFileStr, 'name': 'geom file path', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'shoot params', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




topologise_topologise = Factory(name='read_shoot_file',
                authors='Gaetan Louarn (wralea authors)',
                description='topologise rammoy file',
                category='IO',
                nodemodule='alinea.topvine.topologise',
                nodeclass='topologise',
                inputs=[{'interface': IFileStr, 'name': 'path shoot file', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'topol', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




appendL_appendL = Factory(name='appendL',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.appendL',
                nodeclass='appendL',
                inputs=[{'interface': None, 'name': 'listout', 'value': None, 'desc': ''}, {'interface': None, 'name': 'item', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'listout', 'desc': ''}, {'interface': None, 'name': 'item', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




put_square_put_square = Factory(name='put_square',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.put_square',
                nodeclass='put_square',
                inputs=[{'interface': IFloat, 'name': 'azi', 'value': 0, 'desc': ''}, {'interface': IFloat, 'name': 'incli', 'value': 0, 'desc': ''}, {'interface': IFloat, 'name': 'x', 'value': 0, 'desc': ''}, {'interface': IFloat, 'name': 'y', 'value': 0, 'desc': ''}, {'interface': IFloat, 'name': 'z', 'value': 0, 'desc': ''}, {'interface': None, 'name': 'MaScene', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




dict_param_vine_dict_param_vine = Factory(name='dict_param_vine',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.dict_param_vine',
                nodeclass='dict_param_vine',
                inputs=[{'interface': None, 'name': 'IN1', 'value': None, 'desc': ''}, {'interface': None, 'name': 'IN2', 'value': None, 'desc': ''}, {'interface': None, 'name': 'IN3', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




update_normal_canopy_update_normal_canopy = Factory(name='update_normal_canopy',
                description='updates a list of normalised shoot objects with a new topology',
                category='scene.canopy',
                nodemodule='alinea.topvine.update_normal_canopy',
                nodeclass='update_normal_canopy',
                inputs=[{'interface': ISequence, 'name': 'canopy of normalised shoots', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'new topol', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dl_leaf', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'normalised canopy', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




get_dl_shoot_get_dl_shoot = Factory(name='read_dl_shoot',
                description='get distribution laws of spurs and shoot parameters from csv file',
                category='IO,scene.topvine',
                nodemodule='alinea.topvine.get_dl_shoot',
                nodeclass='get_dl_shoot',
                inputs=[{'interface': IFileStr, 'name': 'shoot dist file', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'spurs0', 'desc': ''}, {'interface': ISequence, 'name': 'dspurs', 'desc': ''}, {'interface': ISequence, 'name': 'f_azi', 'desc': ''}, {'interface': ISequence, 'name': 'shoot laws', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




pickleD_pickleD = Factory(name='pickleD',
                description='pickle dump python data and return file path',
                category='data i/o',
                nodemodule='alinea.topvine.pickleD',
                nodeclass='pickleD',
                inputs=[{'interface': None, 'name': 'path', 'value': None, 'desc': ''}, {'interface': IDirStr, 'name': 'folde', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'name', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'file path', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




CxT_select_CxT_select = Factory(name='CxT_select',
                description='Seletct CxT pair in a list',
                category='IO',
                nodemodule='alinea.topvine.CxT_select',
                nodeclass='CxT_select',
                inputs=[{'interface': IEnumStr(enum=['1W-Syrah', '1W-Grenache', '2W-Syrah', '2W-Grenache', 'BFC-Syrah', 'BFC-Grenache', 'Gobelet-Syrah', 'Gobelet-Grenache']), 'name': 'CxT list', 'value': '1W-Grenache', 'desc': ''}],
                outputs=[{'interface': IStr, 'name': 'CxT name', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




translate_shoots_translate_shoots = Factory(name='translate_shoots',
                description='translates all shoots prams of vector v',
                category='scene.topvine',
                nodemodule='alinea.topvine.translate_shoots',
                nodeclass='translate_shoots',
                inputs=[{'interface': ISequence, 'name': 'shoot params', 'value': None, 'desc': ''}, {'interface': None, 'name': 'v', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'shoot params', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




read_stand_file_read_stand_file = Factory(name='read_stand_file',
                description='get stand caracteristics from stand file',
                category='IO,scene.topvine',
                nodemodule='alinea.topvine.read_stand_file',
                nodeclass='read_stand_file',
                inputs=[{'interface': IFileStr, 'name': 'stand file', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'stand table', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




scene_to_can_scene_to_can = Factory(name='scene_to_can',
                description='converts a topvine scene into can file',
                category='visualisation,codec',
                nodemodule='alinea.topvine.scene_to_can',
                nodeclass='scene_to_can',
                inputs=[{'interface': None, 'name': 'pgl scene', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




read_allometry_read_allometry = Factory(name='read_allometry',
                description='set L-N allometric parameters from allometry file',
                category='IO',
                nodemodule='alinea.topvine.read_allometry',
                nodeclass='read_allometry',
                inputs=[{'interface': IFileStr, 'name': 'IN1', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




visu_digit_visu_digit = Factory(name='visu_digit',
                description='visualise digitalisation data from .d3d file',
                category='Unclassified',
                nodemodule='alinea.topvine.visu_digit',
                nodeclass='visu_digit',
                inputs=[{'interface': IFileStr, 'name': 'd3d file', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'A angle correction', 'value': 0, 'desc': 'degree'}, {'interface': ISequence, 'name': 'coord', 'value': [0, 0, 0], 'desc': ''}, {'interface': None, 'name': 'scene', 'value': None, 'desc': ''}, {'interface': IInt, 'name': 'nump', 'value': 1, 'desc': ''}, {'interface': IFloat, 'name': 'teta_row', 'value': 0, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




vine_topiary_vine_topiary = Factory(name='vine_topiary',
                description='Generates a scaled PGL scene from a list of normalised shoot objects',
                category='scene.topvine',
                nodemodule='alinea.topvine.vine_topiary',
                nodeclass='vine_topiary',
                inputs=[{'interface': ISequence, 'name': 'list of shoots', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dl_leaf', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'allometry', 'value': None, 'desc': ''}, {'interface': IBool, 'name': 'include primary axes', 'value': True, 'desc': ''}, {'interface': IBool, 'name': 'include trunks', 'value': True, 'desc': ''}, {'interface': IBool, 'name': 'include bunches', 'value': False, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'pgl scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




gen_normal_canopy_gen_normal_canopy = Factory(name='gen_normal_canopy',
                description='generates a list of normalised shoot objects associationg average topology with geometric features',
                category='scene.canopy',
                nodemodule='alinea.topvine.gen_normal_canopy',
                nodeclass='gen_normal_canopy',
                inputs=[{'interface': ISequence, 'name': 'tab_geom', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'topol', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'dl_leaf', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




expandOutput_phyto_expandOutput_phyto = Factory(name='expandOutput_phyto',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.expandOutput_phyto',
                nodeclass='expandOutput_phyto',
                inputs=[{'interface': None, 'name': 'caribu_dict', 'value': None, 'desc': ''}, {'interface': None, 'name': 'keys', 'value': None, 'desc': ''}, {'interface': None, 'name': 'values', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'caribu_dict', 'desc': ''}, {'interface': None, 'name': 'phto_dict', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




tortl_inst_vine_tortl_inst_vine = Factory(name='tortl_inst_vine',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.tortl_inst_vine',
                nodeclass='tortl_inst_vine',
                inputs=[{'interface': None, 'name': 'list of shoots', 'value': None, 'desc': ''}, {'interface': None, 'name': 'dl', 'value': None, 'desc': ''}, {'interface': None, 'name': 'allometry', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




mef_skt_mef_skt = Factory(name='mef_skt',
                description='format meteo data for sky_tools',
                category='Unclassified',
                nodemodule='alinea.topvine.mef_skt',
                nodeclass='mef_skt',
                inputs=[{'interface': IInt, 'name': 'DOY', 'value': None, 'desc': ''}, {'interface': IInt, 'name': 'HU', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Rg', 'value': None, 'desc': ''}, {'interface': IInt, 'name': 'Group', 'value': 0, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'OUT1', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




allometry_allometry = Factory(name='get_allometry',
                description='set L-N allometric parameters with specified inputs',
                category='scene',
                nodemodule='alinea.topvine.allometry',
                nodeclass='allometry',
                inputs=[{'interface': IFloat, 'name': 'a', 'value': 65, 'desc': ''}, {'interface': IFloat, 'name': 'b', 'value': -243, 'desc': ''}, {'interface': IFloat, 'name': "a'", 'value': 37, 'desc': ''}, {'interface': IFloat, 'name': "b'", 'value': -52, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'params', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




primitive_bunch = Factory(name='gen_bunch',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.primitive',
                nodeclass='bunch',
                inputs=[{'interface': None, 'name': 'scene', 'value': None, 'desc': ''}, {'interface': None, 'name': 'coord', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'opt', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'id', 'value': 200000000000L, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'scene', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




get_key_get_key = Factory(name='get_key',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.get_key',
                nodeclass='get_key',
                inputs=[{'interface': None, 'name': 'dict', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'key', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'val', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




get_dl_get_dl = Factory(name='read_dl_leaf',
                authors='Gaetan Louarn (wralea authors)',
                description='read distribution laws of leaf angles from input file',
                category='IO',
                nodemodule='alinea.topvine.get_dl',
                nodeclass='get_dl',
                inputs=[{'interface': IFileStr, 'name': 'dl leaf file', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'tab_dl_leaf', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




compute_TT_compute_TT = Factory(name='compute_TT',
                authors='Gaetan Louarn (wralea authors)',
                description='',
                category='Unclassified',
                nodemodule='alinea.topvine.compute_TT',
                nodeclass='compute_TT',
                inputs=[{'interface': IFloat, 'name': 'previousTT', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Tmoy', 'value': None, 'desc': ''}, {'interface': IFloat, 'name': 'Tbase', 'value': 10.0, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'TT', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




