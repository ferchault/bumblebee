#!/usr/bin/env python
# -*- coding: utf-8 -*-

# package modules
import base

class Cp2kConnector(base.Connector):
	def __init__(self, rolefile, directory=None):
		super(Cp2kConnector, self).__init__()
		self._directory = directory
		self._type = 'cp2k'
		self.add_filerole('logfile', at_least=1, at_most=1)
		self._parse_rolefile(rolefile)

	def parse(self):
		loglines = self._read_textfile_in_memory(self._filenames['logfile'][0])

		print len(loglines)
