#!/usr/bin/env python3
#import os
#import platform
#import yaml
#from subprocess import check_call

from charms.reactive.helpers import is_state
from charms.reactive.bus import set_state
from charms.reactive.bus import get_state
from charms.reactive.bus import remove_state
from charms.reactive.decorators import hook
from charms.reactive.decorators import when
from charms.reactive.decorators import when_not

from charmhelpers.core.hookenv import (
    log,
    CRITICAL,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
    remote_unit,
    status_set,
    related_units
)

from charms.layer.jujuenv import JujuEnv

#from charms.layer.hpccsystems_platform import HPCCSystemsPlatformConfig
@when('hpcc-cluster.configure')
def configure_cluster(cluster):

    log('Will configure hpcc cluster', INFO)
    conv = cluster.conversation()

    # to do call envgen to generate environment.xml

    log('Notify all units except dali stop hpcc and fetch environment.xml', INFO)
    action = 'envxml.available'
    conv.set_remote('action', action)
    conv.set_local('action', action)
    status_set('active', JujuEnv.STATUS_MSG['CLUSTER_CONFIGURED'])
    cluster.remove_state('hpcc-cluster.configure')


@when('hpcc-cluster.envxml.fetched')
def update_dali(cluster):
    conv = cluster.conversation()
    action = 'envxml.available.dali'
    conv.set_remote('action', action)
    conv.set_local('action', action)
    cluster.remove_state('hpcc-cluster.envxml.fetched')

@when('hpcc-cluster.envxml.fetched.dali')
def start_dali(cluster):
    log('Notify dali stop hpcc and fetch environment.xml', INFO)
    conv = cluster.conversation()

    # if local node is dali
    #   start hpcc and set state to {relation_name}.dali.started
    # else
    #   notify remote dali node to start hpcc
    action =  'dali.start'
    conv.set_remote('action', action)
    conv.set_local('action', action)
    status_set('active', JujuEnv.STATUS_MSG['DALI_START'])
    cluster.remove_state('hpcc-cluster.envxml.fetched.dali')

@when('hpcc-cluster.dali.started')
def start_non_dali_nodes(cluster):
    log('Notify all nodes to start hpcc', INFO)
    conv = cluster.conversation()
    action = 'cluster.start'
    conv.set_remote('action', action)
    conv.set_local('action', action)
    status_set('active', JujuEnv.STATUS_MSG['CLUSTER_START'])
    cluster.remove_state('hpcc-cluster.dali.started')

@when('hpcc-cluster.started')
def start_non_dali_nodes(cluster):
    log('All nodes are started', INFO)
    conv = cluster.conversation()
    status_set('active', JujuEnv.STATUS_MSG['CLUSTER_STARTED'])

@when('hpcc-cluster.node.error')
def node_error(cluster):
    status_set('active', JujuEnv.STATUS_MSG['NODE_ACTION_ERR'])
    conv = cluster.conversation()
    results = conv.get_local('results')

    #to do ...

    cluster.remove_state('hpcc-cluster.error')




