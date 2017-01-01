inherit layer-hpccsystems-base and interface-hpccsystems-cluster

- 'layer:hpccsystems-base'
  - 'interface:hpccsystems-cluster'

# Implementation
This is abstract charm which provide cluster interface HPCCSystems cluster nodes
The concrete cluster charms will inherit this, for example hpccystems-cluster-manager .

![alt Hierarchy Diagram] (images/layer-hpccsystems-cluster-manager-base.jpg)
~

