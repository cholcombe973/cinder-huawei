import os

from charmhelpers.core.hookenv import (
    config,
    service_name
)
from charmhelpers.contrib.openstack.context import (
    OSContextGenerator,
)
from charmhelpers.core.templating import render


class HuaweiIncompleteConfiguration(Exception):
    pass


class HuaweiSubordinateContext(OSContextGenerator):
    interfaces = ['ceph-huawei']
    products = ['T', 'TV2', 'V3', '18000']

    # Driver matrix
    t_v1_drivers = {
        'iscsi': 'cinder.volume.drivers.huawei.huawei_t.HuaweiTISCSIDriver',
        'fc': 'cinder.volume.drivers.huawei.huawei_t.HuaweiTFCDriver',
    }
    t_v2_drivers = {
        'iscsi': 'cinder.volume.drivers.huawei.huawei_driver.HuaweiTV2ISCSIDriver',
        'fc': 'cinder.volume.drivers.huawei.huawei_driver.HuaweiTV2FCDriver',
    }
    v3_drivers = {
        'iscsi': 'cinder.volume.drivers.huawei.huawei_driver.HuaweiV3ISCSIDriver',
        'fc': 'cinder.volume.drivers.huawei.huawei_driver.HuaweiV3FCDriver',
    }
    oceanstor_drivers = {
        'iscsi': 'cinder.volume.drivers.huawei.huawei_driver.HuaweiISCSIDriver',
        'fc': 'cinder.volume.drivers.huawei.huawei_driver.HuaweiFCDriver',
    }

    _config_keys = [
        'host-ip',
        'host-username',
        'host-password',
        'protocol',
        'rest-url',
        'product-type',
    ]

    def __call__(self):
        ctxt = []
        missing = []
        for k in self._config_keys:
            if config(k):
                ctxt.append(("huawei_{}".format(k.replace('-', '_')),
                             config(k)))
            else:
                missing.append(k)
        if missing:
            raise HuaweiIncompleteConfiguration('Missing configuration: {}.'.format(missing))

        service = service_name()
        volume_driver = 'cinder.volume.drivers.huawei.HuaweiVolumeDriver'
        # conf_file = '/etc/cinder/huawei.xml'

        render(source='', target='', context='')
        config_path = os.path.join('etc', 'cinder', 'huawei.xml')
        cinder_huawei_context = {
            'product': config('product-type'),
            'protocol': config('protocol'),
            'controller_ip': config('host-ip'),
            'username': config('host-username'),
            'password': config('host-password'),
            'lun_type': config('lun-type'),
            'stripe_size': config('stripe-unit-size'),
            'write_type': config('write-type'),
            'mirror_switch': config('mirror-switch'),
            'prefetch_type': config('prefetch-type'),
            'prefetch_value': config('prefetch-value'),
            'storage_pool': config('storage-pool'),
            'iscsi_target': config(''),
            'initiator': config('initiator-name'),
            'target_ip': config('initiator-target-ip'),
            'hosts_ip_list': config(''),
        }
        render('huawei.xml', "/etc/cinder", cinder_huawei_context, perms=0o644)

        ctxt.append(('volume_backend_name', service))
        ctxt.append(('volume_driver', volume_driver))
        ctxt.append(('cinder_huawei_conf_file', ''))
        return {
            "cinder": {
                "/etc/cinder/cinder.conf": {
                    "sections": {
                        service: ctxt
                    }
                }
            }
        }
