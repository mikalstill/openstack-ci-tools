#!/usr/bin/python

import utils


NEW_PATCH_EMAIL = """The CI watcher has discovered a new patchset!

%(subject)s by %(name)s
%(url)s

%(change_id)s number %(number)s
is_migration: %(is_migration)s

The following files are changed in the patchset:
    %(files_list)s"""


def Handle(change, files):
    is_migration = False

    for filename in files:
        if filename.find('nova/db/sqlalchemy/migrate_repo/versions') != -1:
            is_migration = True

    if is_migration:
        print 'Sending email'
        utils.send_email('New patchset discovered!',
                         'michael.still@rackspace.com',
                         NEW_PATCH_EMAIL
                         % {'change_id': change['id'],
                            'number': change['number'],
                            'subject': change['subject'],
                            'name': change['owner_name'],
                            'url': change['url'],
                            'is_migration': is_migration,
                            'files_list': '\n    '.join(files)})

        cursor = utils.get_cursor()
        for dataset in ['trivial']:
            utils.queue_work(cursor, change['id'], change['number'],
                             'sqlalchemy_migration_%s' % dataset)


def ExecuteWork(cursor, ident, number, workname, worker):
    if not workname in ['sqlalchemy_migration_trivial']:
        return False

    utils.log(cursor, worker, ident, number, workname,
              'Plugin for work queue item found.')

    change = utils.get_patchset_details(cursor, ident, number)
    utils.create_git(change['project'], change['refurl'])
    utils.log(cursor, worker, ident, number, workname,
              'Git checkout created')