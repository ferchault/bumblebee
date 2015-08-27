#!/usr/bin/env python
# -*- coding: utf-8 -*-

# system modules
import argparse
import ConfigParser
import hashlib
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
parser.add_argument('--runno', type=int, help='The running number of the run.')
parser.add_argument('--token', type=str, help='Token for external bucket identification as string.')
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

def _get_token(args):
	if args.token is None:
		return hashlib.md5(args.bucket).hexdigest()
	return args.token

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
	if args.runno is None:
		_print(args, 'E0006', 'No run id specified.')

	# connect to MongoDB and prepare bucket with run
	db = get_server(args)
	buckets = db.buckets
	bucket_id = buckets.find_one({'name': args.bucket})
	if bucket_id is None:
		bucket_id = buckets.insert_one({
			'name': args.bucket,
			'token': _get_token(args)
		}).inserted_id
	runs = db.runs
	run_id = runs.find_one({'bucket_id': bucket_id['_id'], 'number': args.runno})
	if run_id is None:
		run_id = runs.insert_one({
			'bucket_id': bucket_id,
			'number': args.runno
		}).inserted_id

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

	# parse data, write to database
	try:
		connector = connector(rolefile, directory=args.resultsdir)
		connector.parse(db, bucket_id['_id'], run_id['_id'])
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