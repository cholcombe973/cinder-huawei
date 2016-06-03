#!/usr/bin/python

import sys
import json

from charmhelpers.core.hookenv import (
    Hooks,
    UnregisteredHookError,
    service_name,
    relation_set,
    relation_ids,
    log
)

from cinder_contexts import HuaweiSubordinateContext
from charmhelpers.payload.execd import execd_preinstall

hooks = Hooks()


@hooks.hook('install')
def install():
    execd_preinstall()


@hooks.hook('config-changed',
            'upgrade-charm')
def upgrade_charm():
    for rid in relation_ids('storage-backend'):
        storage_backend(rid)


@hooks.hook('storage-backend-relation-joined',
            'storage-backend-relation-changed')
def storage_backend(rel_id=None):
    relation_set(
        relation_id=rel_id,
        backend_name=service_name(),
        subordinate_configuration=json.dumps(HuaweiSubordinateContext())
    )


if __name__ == '__main__':
    try:
        hooks.execute(sys.argv)
    except UnregisteredHookError as e:
        log('Unknown hook {} - skipping.'.format(e))
