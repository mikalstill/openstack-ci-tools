#!/usr/bin/python

# Recheck the last 20 reviews

import sys

import utils
import workunit


cursor = utils.get_cursor()
subcursor = utils.get_cursor()
cursor.execute('select distinct(concat(id, "~", number)) as idnum from '
               'work_queue order by heartbeat desc limit 20;')
for row in cursor:
    id, number = row['idnum'].split('~')
    workunit.recheck(subcursor, id, int(number))
