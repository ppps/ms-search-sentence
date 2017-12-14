#!/usr/bin/env python3

import gzip
import pathlib
import subprocess

import psycopg2


def most_recent_db_dump():
    sql_dir = pathlib.Path('/Volumes/HDD/morning_star_db_dumps')
    return max(sql_dir.glob('*.sql.gz'),
               key=lambda f: f.stat().st_mtime)


def clear_out_mysql():
    subprocess.run(
        args=['mysql', '-uroot', '-c'],
        input=('drop database if exists morningstaronline; '
               'create database morningstaronline;'),
        encoding='utf-8'
        )


def import_into_mysql(sql_dump):
    pass
