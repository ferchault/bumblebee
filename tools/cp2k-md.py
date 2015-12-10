#!/usr/bin/env python

import argparse
import requests as r
import MDAnalysis as mda
import os
import json

parser = argparse.ArgumentParser()
parser.add_argument('--basepath', help='Path to read the data and any optional config from.', default='.')
parser.add_argument('--system', help='Name of the physical system. Takes precedence over configuration.')
parser.add_argument('--token', help='Token to identify the bucket. Takes precedence over configuration.')
parser.add_argument('--bucket', help='Bucket to save the data to. Takes precedence over configuration.')
parser.add_argument('--series', help='Series to append to. Takes precedence over configuration.')
parser.add_argument('--baseurl', help='Server URL of the API listing. Takes precedence over configuration.')
parser.add_argument('--httpuser', help='Username for HTTP Basic Auth. Takes precedence over configuration.')
parser.add_argument('--httppass', help='Password for HTTP Basic Auth. Takes precedence over configuration.')
parser.add_argument('--logfile', help='CP2K log file name in basepath.', default='run.log')
parser.add_argument('--restartfile', help='CP2K restart file name in basepath.')
parser.add_argument('--inputfile', help='CP2K input file name.', default='run.inp')


class BumblebeeApi(object):
	def __init__(self, baseurl, auth=None):
		try:
			self._auth = auth
			self._urls = r.get(baseurl, auth=self._auth).json()
		except:
			raise ValueError('Unable to connect to server.')

	def get_if_exists(self, objecttype, multiple=False, **kwargs):
		if objecttype not in self._urls:
			raise ValueError('Object type not known on server side.')

		result = r.get(self._urls[objecttype], auth=self._auth, params=kwargs)
		try:
			result = json.loads(result.content)
		except:
			print result.content
			raise ValueError('No JSON answer from server.')
		if not multiple and len(result) > 1:
			raise ValueError('Filter criteria not narrow enough: non-unique answer from server.')
		if len(result) == 0:
			return None
		if multiple:
			return result
		else:
			return result[0]

	def create_if_missing(self, objecttype, **kwargs):
		instance = self.get_if_exists(objecttype, **kwargs)
		if instance is None:
			instance = self.create(objecttype, **kwargs)
		return instance

	def create(self, objecttype, **kwargs):
		if objecttype not in self._urls:
			raise ValueError('Object type not known on server side.')

		result = r.post(self._urls[objecttype], auth=self._auth, data=kwargs)
		if result.status_code != 201:
			raise ValueError('Unable to add new entry because of the following server answer: ' + str(result.json()))
		return result.json()

	def create_bulk(self, objecttype, data):
		if objecttype not in self._urls:
			raise ValueError('Object type not known on server side.')

		result = r.post(self._urls[objecttype], auth=self._auth, json=data)
		result = r.post(self._urls[objecttype], auth=self._auth, json=data)
		if result.status_code != 201:
			raise ValueError('Unable to add new entry because of the following server answer: ' + str(result.content))
		return result.json()


class CP2KParser(object):
	def __init__(self, basepath, logfile, inputfile, restartfile=None):
		""" Reads the input files and starts searching for dependent files.
		:param basepath: Absolute path all relative file paths refer to.
		:param logfile: The plain text output from CP2K.
		:param inputfile: The plain text input for CP2K.
		:param restartfile: The plain text external restart file for CP2K.
		"""
		self._basepath = basepath
		self._loglines = open(logfile).readlines()
		self._inputlines = [_.strip() for _ in open(inputfile).readlines()]
		self._restartlines = []
		if restartfile is not None:
			self._restartlines = [_.strip() for _ in open(restartfile).readlines()]

		self._skip = []
		self._fix_MDAnalysis()
		self._discover_information()
		self._framedata = None
		self._noatoms = None
		self._pos = 0

	def _fix_MDAnalysis(self):
		""" Monkey patching of the MDAnalysis exception handling.
		"""
		non_permissive_del = mda.coordinates.DCD.DCDReader.__del__

		def permissive_del(self):
			try:
				non_permissive_del(self)
			except:
				pass
		mda.coordinates.DCD.DCDReader.__del__ = permissive_del

	def _discover_information(self):
		""" Parses the CP2K input file for path information.
		"""
		# coordinate file path
		coordfile = self.get_path('MOTION / PRINT / TRAJECTORY / FILENAME')
		if coordfile is None:
			print 'Not enough information to parse coordinate data. Skipping it.'
			self._skip.append('coordinates')
		else:
			try:
				self._coordfile = mda.coordinates.DCD.DCDReader(os.path.join(self._basepath, coordfile + '-pos-1.dcd'))
			except:
				print 'Unable to read coordinate file or corrupted DCD. Currently, only DCD supported. Skipping coordinates'
				self._skip.append('coordinates')

		# velocity file path
		velfile = self.get_path('MOTION / PRINT / VELOCITIES / FILENAME')
		if velfile is None:
			print 'Not enough information to parse velocity data. Skipping it.'
			self._skip.append('velocities')
		else:
			try:
				self._velfile = mda.coordinates.DCD.DCDReader(os.path.join(self._basepath, velfile + '-vel-1.dcd'))
			except IOError:
				print 'Unable to read velocity file or corrupted DCD. Currently, only DCD supported. Skipping velocities'
				self._skip.append('velocities')

		# forces file path
		forfile = self.get_path('MOTION / PRINT / FORCES / FILENAME')
		if velfile is None:
			print 'Not enough information to parse force data. Skipping it.'
			self._skip.append('forces')
		else:
			try:
				self._forfile = mda.coordinates.DCD.DCDReader(os.path.join(self._basepath, forfile + '-frc-1.dcd'))
			except:
				print 'Unable to read forces file or corrupted DCD. Currently, only DCD supported. Skipping forces'
				self._skip.append('forces')

		# atom kinds and elements
		coordlines = self.get_path('FORCE_EVAL / SUBSYS / COORD / *')
		self._atomkinds = [_.split()[0] for _ in coordlines]
		kindmapping = dict()
		for kind in set(self._atomkinds):
			element = self.get_path('FORCE_EVAL / SUBSYS / KIND|%s / ELEMENT' % kind)
			if element is None:
				kindmapping[kind] = kind
			else:
				kindmapping[kind] = element
		self._atomelements = [kindmapping[kind] for kind in self._atomkinds]

	def get_atom_list(self):
		""" Builds a list of element - kind pairs of all known atoms.
		:return: List of tuples. First entries are elements, the second entries are kinds.
		"""
		return zip(self._atomelements, self._atomkinds)

	def get_coordinates(self, frame):
		if self._coordfile is not None:
			return self._coordfile[frame]._pos

	def skip_header(self):
		""" Set the internal cursor to the beginning of the MD run.	"""
		if self._pos != 0:
			return
		for idx in range(len(self._loglines)):
			if 'GO CP2K GO!' in self._loglines[idx]:
				self._pos = idx
				return

	def find_next_frame(self):
		""" Sets the next complete frame for analysis.

		:return: Boolean. True if a frame could be loaded.
		"""
		first = False
		for idx in range(self._pos, len(self._loglines)):
			if '*' * 79 in self._loglines[idx]:
				if first:
					self._framedata = self._loglines[self._pos:idx]
					self._pos = idx + 1
					return True
				else:
					first = True
		self._framedata = None
		return False

	def progress(self):
		""" Gives an estimate for the parsing progress.
		:return: Float (percent).
		"""
		return float(self._pos) / len(self._loglines) * 100

	def get_frame_desired(self, kind):
		""" Looks up specified properties from the input file tree.

		:param kind: The key to look for. Check the source for known keys.
		:return: Converted value in Angstrom/eV/K/mu_B
		"""
		def keep_float(var):
			try:
				val = float(var)
			except:
				return None
			return val

		keyword = dict((
			('stepnumber', 'STEP NUMBER'),
			('steptime', 'TIME [fs]'),
			('celllengths', 'CELL LNTHS[bohr]'),
			('cellangles', 'CELL ANGLS[deg]'),
			('temperature', 'TEMPERATURE [K]'),
			('pressure', 'PRESSURE [bar]'),
			('volume', 'VOLUME[bohr^3]'),
			('conserved', 'CONSERVED QUANTITY [hartree]'),
			('coreselfenergy', 'Self energy of the core charge distribution:'),
			('corehamiltonian', 'Core Hamiltonian energy:'),
			('hartree', 'Hartree energy:'),
			('xc', 'Exchange-correlation energy:'),
			('hfx', 'Hartree-Fock Exchange energy:'),
			('dispersion', 'Dispersion energy:'),
			('etot', 'ENERGY| Total FORCE_EVAL ( QS ) energy (a.u.):'),
			('epot', 'POTENTIAL ENERGY[hartree]'),
			('ekin', 'KINETIC ENERGY [hartree]'),
			('drift', 'ENERGY DRIFT PER ATOM [K]'),
			('iasd', 'Integrated absolute spin density  :'),
			('s2', 'Ideal and single determinant S**2 :'),
			('scfcycles', 'outer SCF loop converged in'),
			('otcycles', 'outer SCF loop converged in'),
		))[kind]
		converter = dict((
			('celllengths', lambda _: _ * 0.52917721967),
			('volume', lambda _: _ * 0.52917721967**3),
			('conserved', lambda _: _ * 27.21138602),
			('coreselfenergy', lambda _: _ * 27.21138602),
			('corehamiltonian', lambda _: _ * 27.21138602),
			('hartree', lambda _: _ * 27.21138602),
			('xc', lambda _: _ * 27.21138602),
			('hfx', lambda _: _ * 27.21138602),
			('etot', lambda _: _ * 27.21138602),
			('epot', lambda _: _ * 27.21138602),
			('ekin', lambda _: _ * 27.21138602),
			('drift', lambda _: _ * 27.21138602),
		))
		if kind in converter:
			converter = converter[kind]
		else:
			converter = lambda _: _
		if self._framedata is None:
			return None
		for idx in range(len(self._framedata))[::-1]:
			if keyword in self._framedata[idx]:
				parts = self._framedata[idx].split()
				parts = [converter(_) for _ in map(keep_float, parts) if _ is not None]
				if kind == 'scfcycles':
					parts = [parts[1]]
				if kind == 'otcycles':
					parts = [parts[0]]
				if len(parts) == 1:
					return parts[0]
				return parts
		return None

	def get_frame_mulliken_charges(self):
		if self._framedata is None:
			raise ValueError('No frame loaded.')

		chargelines = []
		begin = None
		for idx in range(len(self._framedata)):
			if 'MULLIKEN POPULATION ANALYSIS' in self._framedata[idx]:
				begin = idx + 3
			if '# Total charge and spin' in self._framedata[idx] and begin is not None:
				chargelines = self._framedata[begin:idx]
		if len(chargelines) == 0:
			return None

		objs = list()
		for line in chargelines:
			parts = line.strip().split()
			objs.append({
				'alpha': float(parts[3]),
				'beta': float(parts[4]),
				'charge': float(parts[5]),
				'spin': float(parts[6]),
			})
		return objs

	def get_frame_dimensions(self):
		if self._framedata is None:
			raise ValueError('No frame loaded.')

		a, b, c = self.get_frame_desired('celllengths')
		alpha, beta, gamma = self.get_frame_desired('cellangles')
		return a, b, c, alpha, beta, gamma

	def get_mdrun_desired(self, kind):
		path = dict((
			('timestep', 'MOTION / MD / TIMESTEP'),
			('temperature', 'MOTION / MD / TEMPERATURE'),
			('pressure', 'MOTION / MD / BAROSTAT / PRESSURE'),
			('multiplicity', 'FORCE_EVAL / DFT / MULTIPLICITY')
		))[kind]
		return self.get_path(path)

	def skip_coordinates(self):
		return 'coordinates' in self._skip

	def skip_charges(self):
		return 'charges' in self._skip

	def get_path(self, path):
		""" Reads a path from a CP2K input file.

		Takes * as final level to collect all matching entries. Use key|filter to specify a filter on the key arguments.

		:param path: The tree path to look up. Levels separated by ` / `. Example: `MOTION / MD / TIMESTEP`
		:return: List if * is used, otherwise string of the value in the input file. None if path not found.
		"""
		# separate elements and filters
		elements = path.split(' / ')
		filters = [None for _ in elements]
		for idx, element in enumerate(elements):
			if '|' in element:
				parts = element.split('|')
				elements[idx] = parts[0]
				filters[idx] = parts[1]

		# iterate over paths
		sections = []
		line_numbers = []
		collect = []
		filter_valid = []
		for no, line in enumerate(self._inputlines):
			if len(line) == 0 or line.startswith('#') or line.startswith('!'):
				continue
			if line.startswith('&END'):
				ending = line[4:].strip()
				if ending != '' and ending != sections[-1]:
					raise ValueError('Trying to end the %s section from line %d with %s in line %d' % (
					sections[-1], line_numbers[-1] + 1, ending, no + 1))
				sections = sections[:-1]
				line_numbers = line_numbers[:-1]

				# clear filter for this section
				filter_valid.pop()
				continue

			if line.startswith('&'):
				sections.append(line.split()[0][1:])
				line_numbers.append(no)

				# does this newly opened section match the filter?
				if len(sections) > len(filters):
					filter_valid.append(False)
				else:
					if filters[len(sections) - 1] is None:
						filter_valid.append(True)
					else:
						if len(line.split()) == 1:
							filter_valid.append(False)
						else:
							if line.split()[1] == filters[len(sections) - 1]:
								filter_valid.append(True)
							else:
								filter_valid.append(False)
				continue

			if sections == elements[:-1] and False not in filter_valid:
				if elements[-1] == '*':
					collect.append(line)
					continue
				parts = line.split()
				if parts[0] == elements[-1]:
					return ' '.join(parts[1:])
		if elements[-1] == '*':
			return collect
		return None


def build_settings(args):
	""" Merges settings from command line and config file.

	:param args: Argparse object.
	:return: Dictionary with settings in values.
	"""
	baseparams = 'system token bucket series baseurl httpuser httppass logfile restartfile inputfile'.split()
	settings = {baseparam: None for (baseparam, _) in zip(baseparams, baseparams)}
	settings['basepath'] = os.path.abspath(args.basepath)

	# read settings file
	try:
		settingsfilename = os.path.join(settings['basepath'], 'bb.conf')
		lines = open(settingsfilename).readlines()
		for line in lines:
			if line.startswith('#'):
				continue
			parts = line.strip().split('=')
			if len(parts) != 2:
				raise ValueError('Invalid config file bb.conf in basepath.')
			settings[parts[0].strip()] = parts[1].strip().strip('"')
	except:
		pass

	# check basepath
	if settings['basepath'][-1] != os.path.sep:
		settings['basepath'] += os.path.sep

	for attr in baseparams:
		if getattr(args, attr) is None:
			continue
		settings[attr] = getattr(args, attr)

	# make paths absolute
	for filetype in 'logfile restartfile inputfile'.split():
		try:
			settings[filetype] = os.path.join(settings['basepath'], settings[filetype])
		except AttributeError:
			# empty path
			pass
	return settings


def connect(settings):
	""" Connects to REST API.

	:param settings: Settings dictionary with program options.
	:return: Bumblebee instance.
	"""
	if settings['httpuser'] is not None:
		auth = settings['httpuser'], settings['httppass']
	else:
		auth = None
	return BumblebeeApi(settings['baseurl'], auth=auth)


if __name__ == '__main__':
	args = parser.parse_args()
	settings = build_settings(args)
	bb = connect(settings)

	# get meta data
	server_system = bb.create_if_missing('system', name=settings['system'])
	server_bucket = bb.create_if_missing('bucket',
				token=settings['token'], name=settings['bucket'], system=server_system['id'])
	server_series = bb.create_if_missing('series', bucket=server_bucket['id'], name=settings['series'])

	# get MD run
	highest_part = bb.get_if_exists('mdrun', series=server_series['id'], multiple=True)
	if highest_part is None:
		highest_part = 1
	else:
		highest_part = max([_['part'] for _ in highest_part]) + 1
	server_mdrun = bb.create('mdrun', series=server_series['id'], part=highest_part)

	# notify user
	print 'Loading data into %s.%s.%s.%d' % (server_system['name'], server_bucket['token'], server_series['name'], server_mdrun['part'])

	# load CP2K data
	cp = CP2KParser(settings['basepath'], settings['logfile'], settings['inputfile'], settings['restartfile'])
	desired = dict()
	for setting in 'temperature pressure multiplicity timestep'.split():
		try:
			desired[setting] = float(cp.get_mdrun_desired(setting))
		except:
			desired[setting] = None
	server_settings = bb.create('mdrunsettings', mdrun=server_mdrun['id'], **desired)
	# check system definition
	server_atoms = bb.get_if_exists('atom', multiple=True, system=server_system['id'], ordering='number')
	if server_atoms is None:
		print 'First import for this system. Creating atoms.'
		for idx, elementkind in enumerate(cp.get_atom_list()):
			element, kind = elementkind
			server_atoms = bb.create('atom', kind=kind, element=element, number=idx+1, system=server_system['id'])
		server_atoms = bb.get_if_exists('atom', multiple=True, system=server_system['id'], ordering='number')

	# import frames
	output_frame = 0
	cp.skip_header()
	while cp.find_next_frame():
		print '\rProgress: %5.2f%%' % cp.progress(),

		# load metadata
		stepnumber = cp.get_frame_desired('stepnumber')
		steptime = cp.get_frame_desired('steptime')
		server_mdstep = bb.create('mdstep', mdrun=server_mdrun['id'], stepnumber=stepnumber, steptime=steptime)

		dimensions = cp.get_frame_dimensions()
		keys = 'a b c alpha beta gamma'.split()
		server_stepcell = bb.create('stepcell', mdstep=server_mdstep['id'], **dict(zip(keys, dimensions)))

		keys = 'temperature pressure volume'.split()
		data = [cp.get_frame_desired(_)[0] for _ in keys]
		server_stepensemble = bb.create('stepensemble', mdstep=server_mdstep['id'], conserved=cp.get_frame_desired('conserved'), **dict(zip(keys, data)))

		keys = 'coreselfenergy corehamiltonian hartree xc hfx dispersion'.split()
		data = [cp.get_frame_desired(_) for _ in keys]
		server_stepcontributionsqm = bb.create('stepcontributionsqm', mdstep=server_mdstep['id'], **dict(zip(keys, data)))

		keys = 'etot epot ekin drift'.split()
		data = [cp.get_frame_desired(_) for _ in keys]
		server_stepenergy = bb.create('stepenergy', mdstep=server_mdstep['id'], **dict(zip(keys, data)))

		keys = 'iasd s2 scfcycles otcycles'.split()
		data = [cp.get_frame_desired(_) for _ in keys]
		server_stepmetaqm = bb.create('stepmetaqm', mdstep=server_mdstep['id'], **dict(zip(keys, data)))

		# load coordinates
		if not cp.skip_coordinates():
			pos = cp.get_coordinates(output_frame)
			if pos is not None:
				assert(len(pos) == len(server_atoms))
				objects_cache = list()
				for atom_number, data in enumerate(zip(pos, server_atoms)):
					coord, server_atom = data
					x, y, z = map(float, coord)
					obj = {'x': x, 'y': y, 'z': z, 'atom': server_atom['id'], 'mdstep': server_mdstep['id']}
					objects_cache.append(obj)
				bb.create_bulk('coordinate', objects_cache)

		# load Mulliken charges
		if not cp.skip_charges():
			charges = cp.get_frame_mulliken_charges()
			if charges is not None:
				objects_cache = list()
				for charge, server_atom in zip(charges, server_atoms):
					charge['atom'] = server_atom['id']
					charge['mdstep'] = server_mdstep['id']
					objects_cache.append(charge)
				bb.create_bulk('mullikencharge', objects_cache)

		# counter
		output_frame += 1
	print '\nComplete'
