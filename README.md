# WASP
This is prepared as a tutorial for  <a href="http://wasp-sweden.org/graduate-school/courses/software-engineering-and-cloud-computing/cloud-computing/"> Cloud Computing</a> course which is offered under  the WASP Graduate School in Umeå University [2017].

rabbitMQ.sh:to setup rabbitMQ server (starting from installation of prequisite libraries to creating users).

receiverRabbit.py: Consumer of messages sent to RabbitMQ server

senderRabbit.py: producer(sender) of messages to RabbitMQ server

vm-init.sh: installs the necessary libraries while creating vm (used during VM initilization, see "createVM(self, VMName)" method inside vm-operations.py file to see how this is used.

vm-operations.py: provides different openstack operations such as create, terminate, list VMs, etc using python. It is based on python-novaclient 7.1.0 and some of the operations may not work if you use a different version (for more: https://docs.openstack.org/developer/python-novaclient/ref/v2/).
