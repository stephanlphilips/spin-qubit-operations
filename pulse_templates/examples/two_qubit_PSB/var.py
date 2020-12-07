# how programmed in the experiment
# from core_tools.utility.variable_mgr.var_mgr import variable_mgr
# def variables():
# 	var_mngr = variable_mgr()
# 	gates = ('vB0','vP1', 'vB1', 'vP2', 'vSD1_P')

# 	vSD1_P_on  = var_mngr.SD1_P_on_11
# 	vSD1_P_ST_readout =  var_mngr.SD1_P_on_11+0.3
# 	vSD1_P_off = var_mngr.SD1_P_off

# 	vP1_anticrossing = var_mngr.PSB_12_P1
# 	vB1_anticrossing = var_mngr.PSB_12_B1
# 	vP2_anticrossing = var_mngr.PSB_12_P2

# 	vP1_01 = var_mngr.vP1_01

# 	_30 = (0,0,0,-25, vSD1_P_ST_readout)
# 	_30_load = (0,vP1_01, 0,-25, vSD1_P_ST_readout)
# 	_40 = (0,20,0,-25, vSD1_P_ST_readout)
# 	_31 = (0,0,0,0, vSD1_P_ST_readout)

# 	ST_anti_12 = (0, vP1_anticrossing, vB1_anticrossing, vP2_anticrossing, vSD1_P_ST_readout)
# 	ST_anti_12_tc_high_ = (0, vP1_anticrossing, vB1_anticrossing+30, vP2_anticrossing, vSD1_P_ST_readout)
# 	ST_anti_12_close = (0, vP1_anticrossing-2, vB1_anticrossing, vP2_anticrossing+2, vSD1_P_ST_readout)

# 	return gates, ST_anti_12, ST_anti_12_close, ST_anti_12_tc_high_, _30, _30_load, _40, _31


# dummy (but similar):
gates = ('vB0','vP1', 'vB1', 'vP2', 'vSD1_P')

def variables():
	gates = ('vB0','vP1', 'vB1', 'vP2', 'vSD1_P')

	vSD1_P_on  = 0.1
	vSD1_P_ST_readout =  0.4
	vSD1_P_off = -5

	vP1_anticrossing = 8.1
	vB1_anticrossing = 10
	vP2_anticrossing = -9.2

	vP1_01 = 10.3

	_30 = (0,0,0,-25, vSD1_P_ST_readout)
	_30_load = (0,vP1_01, 0,-25, vSD1_P_ST_readout)
	_40 = (0,20,0,-25, vSD1_P_ST_readout)
	_31 = (0,0,0,0, vSD1_P_ST_readout)

	ST_anti_12 = (0, vP1_anticrossing, vB1_anticrossing, vP2_anticrossing, vSD1_P_ST_readout)
	ST_anti_12_tc_high_ = (0, vP1_anticrossing, vB1_anticrossing+30, vP2_anticrossing, vSD1_P_ST_readout)
	ST_anti_12_close = (0, vP1_anticrossing-2, vB1_anticrossing, vP2_anticrossing+2, vSD1_P_ST_readout)
	
	return gates, ST_anti_12, ST_anti_12_close, ST_anti_12_tc_high_, _30, _30_load, _40, _31

