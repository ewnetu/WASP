from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient.client import Client as NovaClient
import datetime
import argparse
import ConfigParser
class OpenStackVMOperations:
    def readConf(self):
       
        config = ConfigParser.RawConfigParser()
        config.read('config.properties')
        self.openStackUsername=config.get('user', 'username')
        self.openStackPassword=config.get('user', 'password')
        self.projectName=config.get('openstack', 'projectName')
        self.openStackAuthUrl=config.get('openstack','authUrl')
        self.openStackKeyName=config.get('openstack','keyName')
        self.openStackNetId=config.get('openstack','netId')
        self.openStackProjectDomainName=config.get('openstack','project_domain_name')
        self.openStackProjectDomainId=config.get('openstack','project_domain_id')
        self.openStackUserDomainName=config.get('openstack','user_domain_name')
       
    def __init__(self):
        self.readConf()
        self.auth = v3.Password(
            username=self.openStackUsername,
            password=self.openStackPassword,
            project_name=self.projectName,
            auth_url= self.openStackAuthUrl,
            user_domain_name = self.openStackUserDomainName,
            # domain_name = 'xerces',
            project_domain_name = self.openStackProjectDomainName,
            project_id =self.openStackProjectDomainId
        )
        self.sess = session.Session(auth=self.auth)
        self.nova = NovaClient("2", session=self.sess)
        
    def monitoringInfo( self,  start_date, end_date):
        usage = self.nova.usage.get( self.projectName, start_date, end_date)
        print usage
    
    
    def createFloatingIP(self, VMName):
        self.nova.floating_ip_pools.list()
        floating_ip = self.nova.floating_ips.create(self.nova.floating_ip_pools.list()[0].name)
        print("floating IP %s is assigned to %s VM", floating_ip.ip, name)
        instance = self.nova.servers.find(name=VMName)
        instance.add_floating_ip(floating_ip)
        
    def createVM(self, VMName):
     # nova.servers.list()
        image = self.nova.images.find(name="ubuntu 16.04")  # nova.images.find(name="Test") #
        flavor = self.nova.flavors.find(name="c2m2")
        net = self.nova.networks.find(label=self.openStackNetId)
        nics = [{'net-id': net.id}]
        vm = self.nova.servers.create(name=VMName, image=image, flavor=flavor, key_name=self.openStackKeyName, nics=nics, userdata=open("vm-init.sh"))
    
    def terminateVM(self,VMName):
        instance = nova.servers.find(name=VMName)
        if instance == None :
            print("server %s does not exist" % VMName)
        else:
            print("deleting server..........")
            nova.servers.delete(instance)
            print("server %s deleted" % VMName)
        
    def listFloatingIPs(self):
        ip_list = self.nova.floating_ips.list()
        for ip in ip_list:
             print("fixed_ip : %s\n" % ip.fixed_ip)
             print("ip : %s" % ip.ip)
             print("instance_id : %s" % ip.instance_id)
    
    def listVMs(self):
        vm_list = self.nova.servers.list()
        for instance in vm_list:
            print("########################## #################\n")
            print("server id: %s\n" % instance.id)
            print("server name: %s\n" % instance.name)
            print("server image: %s\n" % instance.image)
            print("server flavor: %s\n" % instance.flavor)
            print("server key name: %s\n" % instance.key_name)
            print("user_id: %s\n" % instance.user_id)
            print("network info (mac + ip) : %s\n" % instance.networks)
            print("########################## #################\n\n")
          
    
    def getVMIP(self,VMName):
        instance = self.nova.servers.find(name=VMName)
    
        print("Network address info: %s\n" % instance.addresses)
        print("fixed ip: %s\n" % instance.networks[self.openStackNetId])
    
        
    def getVMDetail(self,VMName):
        instance = self.nova.servers.find(name=VMName)
        print("server id: %s\n" % instance.id)
        print("server name: %s\n" % instance.name)
        print("server image: %s\n" % instance.image)
        print("server flavor: %s\n" % instance.flavor)
        print("server key name: %s\n" % instance.key_name)
        print("user_id: %s\n" % instance.user_id)
        print("user network info: %s\n" % instance.networks)
     
    def  getOperation(self, args): 
        if args.operation == "listIP":
            self.listFloatingIPs()
        elif args.operation == "listVM":
            self.listVMs()
        elif args.operation == "create":
            self.createVM(args.name)
        elif args.operation == "terminate":
            self.terminateVM(args.name)
        elif args.operation == "assignFIP":
            self.createFloatingIP(args.name)
        elif args.operation == "VMIP":
            self.getVMIP(args.name)
        elif args.operation == "monitor":
            self.monitoringInfo(datetime.datetime.strptime('2017-04-04 00:00:00',"%Y-%m-%d %H:%M:%S"),datetime.datetime.strptime('2017-04-05 00:00:00',"%Y-%m-%d %H:%M:%S"))
     
   
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operation",
        metavar = "VM_OPERATION",
        help = "The operation that you want to perform",
        required = True,
        choices=["create","listVM","VMIP","terminate","listIP","assignFIP","monitor"],
        dest="operation")

    parser.add_argument("-n", "--name",
        metavar = "VM_NAME",
        help = "The name  for the VM that you want to perform the operation",
        dest="name")
    args = parser.parse_args()
    ops =OpenStackVMOperations()
    ops.getOperation(args)
