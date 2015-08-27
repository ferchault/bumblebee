#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cp2k
register = ('cp2k', )

def find_connector(register_string):
	if register_string not in register:
		raise ValueError('No such register entry.')
	if register_string == 'cp2k':
		return cp2k.Cp2kConnector