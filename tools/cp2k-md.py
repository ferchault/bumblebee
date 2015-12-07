#!/usr/bin/env python

import argparse
import requests as r
import MDAnalysis as mda
import os

parser = argparse.ArgumentParser()
parser.add_argument('system', help='Name of the physical system.')
parser.add_argument('token', help='Token to identify the bucket.')
parser.add_argument('bucket', help='Bucket to save the data to.')
parser.add_argument('series', help='Series to append to.')
parser.add_argument('basepath', help='Path to read the data from.')
parser.add_argument('baseurl', help='Server URL of the API listing.')
parser.add_argument('--httpuser', help='Username for HTTP Basic Auth.')
parser.add_argument('--httppass', help='Password for HTTP Basic Auth.')
parser.add_argument('--logfile', help='CP2K log file name in basepath.', default='run.log')
parser.add_argument('--restartfile', help='CP2K restart file name in basepath.', default='run.base')
parser.add_argument('--inputfile', help='CP2K input file name.', default='run.inp')
parser.add_argument('--coordfile', help='DCD file with coordinates.', default='traj/pos-pos-1.dcd')
parser.add_argument('--xyzfile', help='XYZ file with the atom list.', default='../input/input.xyz')


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
			result = result.json()
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
			raise ValueError('Unable to add new entry because of the following server answer: ' + str(result.json()))
		return result.json()


class CP2KParser(object):
	def __init__(self, logfile=None, inputfile=None, restartfile=None, coordfile=None, xyzfile=None):
		self._logfile = open(logfile).readlines()
		self._inputfile = [_.strip() for _ in open(inputfile).readlines()]
		#self._restartfile = open(restartfile).readlines()
		try:
			self._coordfile = mda.coordinates.DCD.DCDReader(coordfile)
		except:
			self._coordfile = None
		self._xyzfile = xyzfile
		self._xyzfileparsed = False
		self._pos = 0
		self._framedata = None
		self._noatoms = None

	def get_atom_list(self):
		if self._xyzfile is None:
			raise ValueError('No atom list information available.')

		if not self._xyzfileparsed:
			try:
				self._xyzfile = open(self._xyzfile).readlines()
			except:
				raise ValueError('Unable to open XYZ file %s.' % self._xyzfile)

		try:
			noatoms = int(self._xyzfile[0].strip())
			if noatoms != len(self._xyzfile) - 2:
				raise ValueError()
		except:
			raise ValueError('Invalid XYZ file.')

		kinds = [_.split()[0] for _ in self._xyzfile[2:]]
		self._xyzfileparsed = True
		self._noatoms = noatoms
		return kinds

	def get_coordinates(self, frame):
		if self._coordfile is not None:
			return self._coordfile[frame]._pos

	def skip_header(self):
		""" Set the internal cursor to the beginning of the MD run.	"""
		if self._pos != 0:
			return
		for idx in range(len(self._logfile)):
			if 'GO CP2K GO!' in self._logfile[idx]:
				self._pos = idx
				return

	def find_next_frame(self):
		""" Sets the next complete frame for analysis.
		:return: Boolean. True if a frame could be loaded.
		"""
		first = False
		for idx in range(self._pos, len(self._logfile)):
			if '*' * 79 in self._logfile[idx]:
				if first:
					self._framedata = self._logfile[self._pos:idx]
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
		return float(self._pos) / len(self._logfile)*100

	def get_frame_desired(self, kind):
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
		for idx in range(len(self._framedata))[::-1][:20]:
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
		if self._inputfile is not None:
			return self.get_path(path)

	def get_path(self, path):
		elements = path.split(' / ')
		sections = []
		line_numbers = []
		collect = []
		for no, line in enumerate(self._inputfile):
			if len(line) == 0 or line.startswith('#') or line.startswith('!'):
				continue
			if line.startswith('&END'):
				ending = line[4:].strip()
				if ending != '' and ending != sections[-1]:
					raise ValueError('Trying to end the %s section from line %d with %s in line %d' % (
					sections[-1], line_numbers[-1] + 1, ending, no + 1))
				sections = sections[:-1]
				line_numbers = line_numbers[:-1]
				continue

			if line.startswith('&'):
				sections.append(line.split()[0][1:])
				line_numbers.append(no)
				continue

			if sections == elements[:-1]:
				if elements[-1] == '*':
					collect.append(line)
					continue
				parts = line.split()
				if parts[0] == elements[-1]:
					return ' '.join(parts[1:])
		if elements[-1] == '*':
			return collect
		return None


if __name__ == '__main__':
	args = parser.parse_args()
	baseurl, system, bucket, bucket_name, series = args.baseurl, args.system, args.token, args.bucket, args.series
	logfile, restartfile, inputfile, coordfile, xyzfile = args.logfile, args.restartfile, args.inputfile, args.coordfile, args.xyzfile

	# check basepath
	basepath = args.basepath
	if basepath[-1] != os.path.sep:
		basepath += os.path.sep

	if args.httpuser != None:
		auth = args.httpuser, args.httppass
	else:
		auth = None

	bb = BumblebeeApi(baseurl, auth=auth)

	# get meta data
	server_system = bb.create_if_missing('system', name=system)
	server_bucket = bb.create_if_missing('bucket', token=bucket, name=bucket_name, system=server_system['id'])
	server_series = bb.create_if_missing('series', bucket=server_bucket['id'], name=series)

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
	cp = CP2KParser(os.path.join(basepath, logfile), os.path.join(basepath, inputfile), os.path.join(basepath, restartfile), os.path.join(basepath, coordfile), os.path.join(basepath, xyzfile))
	settings = dict()
	for setting in 'temperature pressure multiplicity timestep'.split():
		try:
			settings[setting] = float(cp.get_mdrun_desired(setting))
		except:
			settings[setting] = None
	server_settings = bb.create('mdrunsettings', mdrun=server_mdrun['id'], **settings)

	# check system definition
	server_atoms = bb.get_if_exists('atom', multiple=True, system=server_system['id'], ordering='number')
	if server_atoms is None:
		print 'First import for this system. Creating atoms.'
		for idx, kind in enumerate(cp.get_atom_list()):
			server_atoms = bb.create('atom', kind=kind, number=idx+1, system=server_system['id'])
		server_atoms = bb.get_if_exists('atom', multiple=True, system=server_system['id'], ordering='number')

	# import frames
	cp.skip_header()
	output_frame = 0
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
