#!/usr/bin/env python
# -*- coding: utf-8 -*-

# system modules
import argparse
import ConfigParser
import os

# third-party modules
import pymongo

# package modules
import connectors as con

parser = argparse.ArgumentParser()
parser.add_argument('--connectors', action='store_true', help='Shows the list of supported connectors.')
parser.add_argument('--grepable', action='store_true', help='Prepend every line with a meaning-depending stable prefix.')
parser.add_argument('--bucket', type=str, help='Bucket to write the data to.')
parser.add_argument('--sysconfig', type=str, default='~/.bumblebee', help='Configuration file.')
parser.add_argument('--servername', type=str, default='default', help='The server alias in the config to write to.')
parser.add_argument('--rolefile', type=str, default='.rolefile', help='The file specifying which data to import.')
parser.add_argument('--runid', type=int, help='The running number of the run.')
parser.add_argument('--resultsdir', type=str, default='.', help='The directory to read the data files from.')

# counter (highest used values)
# E 13
# L 1
# O 1

def _print(args, prefix, string=None):
	if string is None:
		raise
		prefix, string = prefix.split(':', 1)
	if args.grepable:
		print prefix,'\t',
	print string
	if prefix.startswith('E'):
		print 'Process aborted due to an unrecoverable error.'
		exit(1)

def action_connectors(args):
	_print(args, 'L0001', 'Available connectors:')
	for connector in con.register:
		_print(args, 'O0001', '%s' % connector)

def get_config(args):
	try:
		config = ConfigParser.ConfigParser()
		config.read(os.path.expanduser(args.sysconfig))
	except:
		_print(args, 'E0003', 'Unable to read and parse config file.')

	args.config = config
	return config

def get_server(args):
	servername = args.servername
	try:
		host = args.config.get(servername, 'host')
		port = int(args.config.get(servername, 'port'))
		db = args.config.get(servername, 'database')
	except Exception as e:
		_print(args, 'E0004', 'Keyword missing in configuration file for server %s: %s' % (servername, e))

	try:
		client = pymongo.MongoClient(host, port)
	except:
		_print(args, 'E0005', 'Unable to connect to server %s.' % servername)

	return client[db]

def action_upload(args):
	# check requirements
	if args.rolefile is None:
		_print(args, 'E0001', 'No rolefile specified.')
	if args.bucket is None:
		_print(args, 'E0002', 'No target bucket specified.')
	if args.runid is None:
		_print(args, 'E0006', 'No run id specified.')

	# connect to MongoDB
	db = get_server(args)

	# select source connector
	try:
		rolefile = ConfigParser.ConfigParser()
		rolefile.read(os.path.expanduser(args.rolefile))
	except:
		_print(args, 'E0004', 'Unable to read and parse role file.')
	sections = rolefile.sections()
	if len(sections) < 1:
		_print(args, 'E0007', 'No connector specified in role file.')
	if len(sections) > 1:
		_print(args, 'E0008', 'Ambiguous connector specified in role file.')

	try:
		connector = con.find_connector(sections[0])
	except:
		_print(args, 'E0009', 'Invalid connector specified in role file.')

	try:
		connector = connector(rolefile, directory=args.resultsdir)
		connector.parse()
	except Exception as e:
		_print(args, e.message)

def main():
	args = parser.parse_args()
	if args.connectors:
		action_connectors(args)
		return
	get_config(args)

	action_upload(args)

if __name__ == '__main__':
	main()