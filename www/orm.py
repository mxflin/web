#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'MXF.Lin'

import asyncio

#连接池
@asyncio.coroutine
def create_pool(loop, **kw):
	logging.info('create database connection pool...')
	global __pool
	__pool = yield from aiomysql.create_pool(
		host = kw.get('host', 'localhost'),
		port = kw.get('port', 3306),
		user = kw['user'],
		password = kw['123456'],
		db = kw['db'],
		charset = kw.get('charset', 'utf8'),
		autocommit = kw.get('autocommit', True),
		maxsize = kw.get('maxsize', 10),
		minsize = kw.get('minsize', 1),
		loop = loop
	)

#SELECT
@asyncio.coroutine
def select(sql, args, size=None):
	log(sql, args)
	global __pool
	with(yield from __pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?', '%s'), args or())
		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()
		yield from our.close()
		logging.info('rows returned: %s' % len(rs))
		return rs

#INSSERT UPDATE DELETE
@asyncio.coroutine
def execute(sql, args):
	log(sql)
	with(yield from __pool) as conn:
		try:
			cur = yield from conn.cursor()
			yield from cur.execute(sql.replace('?', '%s'), args)
			affected = cur.rowcount
			yield from cur.close()
		except BaseException as e:
			raise
		return affected


#定义ORM映射出来的Model
class Model(dict, metaclass=ModelMetaclass)
	def __init__(self, **kw):
		super(Model, self).__init__(**kw)
	
	def __getattr__(self, key):
		try:
			return self[key]
		execpt KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'"% key)
	
	def __setattr__(self, key, value):
		self[key] = value
		
	def getValue(self, key):
		return getattr(self, key, None)
		
	def getValueOrDefault(self, key):
		value = getattr(self, key, None)
		if value is None:
			field = self.__mappings__[key]
			if field.default() is not None:
				value = field.default() if callable(field,default) else field.default
				logging.debug('using default value for %s: %s' % (key, str(value)))
				setattr(self, key, value)
		return value





















