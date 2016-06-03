# Huawei Storage Backend for Cinder

## Overview

This charm provides a Huawei storage backend for use with the Cinder
charm.

To use:

    juju deploy cinder
    juju deploy --config config.yaml cinder-huawei
    juju add-relation cinder-huawei cinder

NOTE: This charm only works with OpenStack Juno or better.

## Configuration

The cinder-huawei charm has mandatory configuration to support access
to the vCenter server managing the vSphere deployment:

    cinder-huawei:
        host-ip: myvcenter.vsphere
        host-username: accessusername
        host-password: accesspassword

The charm also provides a configuration option for the folder under
which created volumes will be stored:

        volume-folder: cinder-volumes

Place this configuration in the config.yaml file specified when
deploying the charm.
