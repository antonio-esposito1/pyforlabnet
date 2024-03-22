from ncclient import manager
import shelve, time, argparse
from getpass import getpass


class AttrDisplay:
    "Provides an inheritable display overload method that shows instances with their class names and a name=value pair for each attribute stored on the instances itself (but not attrs inherited from its classes). Can be mixed into any class, and will work on any instance."
    
    def gatherAttrs(self):
        attrs = []
        for key in sorted(self.__dict__):
            attrs.append('%s=%s' % (key, getattr(self, key)))
        return ', '.join(attrs)
    
    def __repr__(self):
        return '[%s: %s]' % (self.__class__.__name__, self.gatherAttrs())


class Device(AttrDisplay):
  "Questa classe descrive un device"
  def __init__(self, devicename, username, password):
    self.devicename = devicename
    self.username = username
    self.password = password

  def connectnetconf(self):
      "questo metodo restituisce il collegamento netconf al device in campo "
      return manager.connect(host=self.devicename, port=830, username=self.username, password=self.password, hostkey_verify=False, device_params={}, allow_agent=False, look_for_keys=False)

class XR_VPE(Device):
   def __init__(self, devicename, username, password):
      Device.__init__(self, devicename, username, password)
    
   def __repr__(self):
        return '[%s: %s]' % (self.devicename, self.gatherAttrs())

def netconfrequest(subtree_filter, device):

    #crea una string str_nc_get_reply contenete la risposta xml del device
    return device.get(('subtree', subtree_filter))

def netconf_requests_isis_neighbors(device):
   stringaxml = """
          <isis xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-clns-isis-oper">
            <instances>
              <instance>
                <instance-name>CORE</instance-name>
                <neighbors>
                  <neighbor>
                    <system-id/>
                    <interface-name/>
                    <neighbor-state/>
                    <neighbor-circuit-type/>
                    <neighbor-media-type/>
                  </neighbor>
                </neighbors>
                <checkpoint-adjacencies>
              <checkpoint-adjacency>
                <system-id/>
              </checkpoint-adjacency>
            </checkpoint-adjacencies>
              </instance>
            </instances>
          </isis>
          """
   nc_get_reply = netconfrequest(stringaxml, device.connectnetconf())
   isis_neighbors = []
   xmlns = "http://cisco.com/ns/yang/Cisco-IOS-XR-clns-isis-oper"
   neighbors = nc_get_reply.data.findall(f'.//{{{xmlns}}}neighbor')
   for neighbor in neighbors:
     temp = {}
     temp['system-id'] = neighbor.find(f'{{{xmlns}}}system-id').text
     temp['interface-name'] = neighbor.find(f'{{{xmlns}}}interface-name').text
     temp['neighbor-state'] = neighbor.find(f'{{{xmlns}}}neighbor-state').text
     temp['neighbor-circuit-type'] = neighbor.find(f'{{{xmlns}}}neighbor-circuit-type').text
     isis_neighbors.append(temp)
   device.isis_neighbors = isis_neighbors
   #print(device.isis_neighbors)
   return device.isis_neighbors

def netconf_requests_bgp_vpnv4_unicast_neighbors(device):
   stringaxml = """
          <bgp xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-oper">
        <instances>
          <instance>
            <instance-active>
              <default-vrf>
                <afs>
                  <af>
                    <af-name>vpnv4-unicast</af-name>
                    <neighbor-af-table>
                      <neighbor>
                        <neighbor-address/>
                        <description/>
                        <remote-as/>
                        <connection-state/>
                        <af-data>
                          <af-name>vpnv4</af-name>
                          <prefixes-accepted/>
                          <prefixes-advertised/>
                        </af-data>
                      </neighbor>
                    </neighbor-af-table>
                  </af>
                </afs>
              </default-vrf>
            </instance-active>
          </instance>
        </instances>
      </bgp>
          """
   nc_get_reply = netconfrequest(stringaxml, device.connectnetconf())
   bgp_vpnv4_unicast_neighbors = []
   xmlns = "http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-oper"
   neighbors = nc_get_reply.data.findall(f'.//{{{xmlns}}}neighbor')
   for neighbor in neighbors:
     temp = {}
     temp['neighbor-address'] = neighbor.find(f'{{{xmlns}}}neighbor-address').text
     temp['description'] = neighbor.find(f'{{{xmlns}}}description').text
     temp['remote-as'] = neighbor.find(f'{{{xmlns}}}remote-as').text
     temp['connection-state'] = neighbor.find(f'{{{xmlns}}}connection-state').text
     bgp_vpnv4_unicast_neighbors.append(temp)
   device.bgp_vpnv4_unicast_neighbors = bgp_vpnv4_unicast_neighbors
   #print(device.bgp_vpnv4_unicast_neighbor)
   return device.bgp_vpnv4_unicast_neighbors

if __name__ == '__main__':
  #print(interact())
  
  parser = argparse.ArgumentParser()
  parser.add_argument("--login", required = "True", help="TACACS login authentication")
  parser.add_argument("--password", help="TACACS password authentication")
  parser.add_argument('-a', '--ask-pass', action='store_true', help='Prompt for password to login to the device')
  args = parser.parse_args()
  
  if not args.ask_pass:
    args.password = input("Enter password: ")
  else:
    args.password = getpass ("Enter password: ")
    
  username = args.login
  userpassword = args.password
  
  DeviceList =[]
  print('Device list: ')
  while True:
    try:
      reply = input() #input('Insericei un device >')
    except EOFError:
      break
    else:
      DeviceList.append(reply)
  print(DeviceList)
  
  #creo le instnze della classe XR_VPE, le istanze vengono messe in un dizionairio che ha per chiave il nome del device    
  InstanceDictionary = {}    
  for name in DeviceList:
    InstanceDictionary[name] = XR_VPE(name, username, userpassword)
  
  #Contatti i device e raccolgo le informazioni in uno shelve
  timestr = time.strftime("%Y%m%d-%H%M%S")
  db = shelve.open('devicedb-' + timestr)    
  for dev in InstanceDictionary:
    netconf_requests_isis_neighbors(InstanceDictionary[dev])
    netconf_requests_bgp_vpnv4_unicast_neighbors(InstanceDictionary[dev])
    db[dev] = InstanceDictionary[dev]
  db.close()

 