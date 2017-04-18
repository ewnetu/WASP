from keystoneauth1.identity import v2
from keystoneauth1 import session
from novaclient.client import Client as NovaClient
import datetime
username=‘put your username’
password=‘put your password’
tenant_name='CloudCourse’#make sure you are using the right project name
auth_url='http://94.246.116.242:5000/v2.0'
auth = v2.Password(username=username, password=password, tenant_name=tenant_name, auth_url=auth_url)
sess = session.Session(auth=auth)
nova = NovaClient("2", session = sess)

def monitoringInfo(tenant_name,start_date,end_date):
  usage = nova.usage.get(tenant_name,start_date,end_date)
  print usage


def createFloatingIP(VMName):
  nova.floating_ip_pools.list()
  floating_ip = nova.floating_ips.create(nova.floating_ip_pools.list()[0].name)
  print("floating IP %s is assigned to %s VM", floating_ip.ip, name)
  instance = nova.servers.find(name=VMName)
  instance.add_floating_ip(floating_ip)

def createVM(VMName):
 # nova.servers.list()
        image = nova.images.find(name="Ubuntu 16.04 LTS")#nova.images.find(name="Test") #
        flavor = nova.flavors.find(name="m1.medium")
        net = nova.networks.find(label="CloudCourse")
        nics = [{'net-id': net.id}]
        vm = nova.servers.create(name=VMName, image=image, flavor=flavor, key_name="ewnetu", nics=nics, userdata=open("vm-init.sh"))

def terminateVM(VMName):
  instance = nova.servers.find(name=VMName)
  if instance==None :
    print("server %s does not exist" % VMName)
  else:
    print("deleting server..........")
    nova.servers.delete(instance)
    print("server %s deleted" % VMName)

def listFloatingIPs(VMName):
   ip_list=nova.floating_ips.list()
   for ip in ip_list:
     print("fixed_ip : %s\n" % ip.fixed_ip)
     print("ip : %s" % ip.ip)
     print("instance_id : %s" % ip.instance_id)

def getVMIP(VMName):
  instance = nova.servers.find(name=VMName)
  ip=instance.networks['private']
  print ("ipaddress:"+ip);
def getVMDetail(VMName):
    instance = nova.servers.find(name=VMName)
    print("server id: %s\n" % instance.id)
    print("server name: %s\n" % instance.name)
    print("server image: %s\n" % instance.image)
    print("server flavor: %s\n" % instance.flavor)
    print("server key name: %s\n" % instance.key_name)
    print("user_id: %s\n" % instance.user_id)
if __name__ == '__main__':
      createVM(“WASP”)
