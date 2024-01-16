from ncclient import manager
from argparse import ArgumentParser
import shelve

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
   print(device.isis_neighbors)
   return device.isis_neighbors

if __name__ == '__main__':
  
  #python3.9 labnet.py --devicename mivpe015 --username antonio --password admin
  #parser = ArgumentParser()
  #parser.add_argument("--devicename", required = "True")
  #parser.add_argument("--username", required = "True")
  #parser.add_argument("--password", required = "True")
  #args = parser.parse_args()
  
  #devicename = args.devicename
  #username = args.username
  #password = args.password
   
  #definisco un istanza della classe Device che è a sua volta definita nel file Device.py
  #dev = Device(devicename,username,password)
  
  # device è il metodo che si connette alla macchina in campo  
  #device = dev.connectnetconf()

  #D = dict()
  
  #Questo ciclo for è il cuore del programma, mi crea un dizionario D con tutti i dati estratti dal device.
  
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
 
  #D['device'] = netconfrequest(stringaxml, device)
  
  

  #print(D['device'])
  """
  mivpe015 = Device('mivpe015', 'antonio', 'admin')
  nc_get_reply = netconfrequest(stringaxml, mivpe015.connectnetconf())
  #mivpe015.data = netconfrequest(stringaxml, mivpe015.connectnetconf())
  #mivpe015.isisinstancename = nc_get_reply.data.find('.//{http://cisco.com/ns/yang/Cisco-IOS-XR-clns-isis-oper}instance-name')
  #print(mivpe015.isisinstancename.text)
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
  mivpe015.isis_neighbors = isis_neighbors
  print(mivpe015.isis_neighbors)

  
  #print(netconfrequest(stringaxml, mivpe015.connectnetconf()))
  #print(mivpe015)

  mivpe016 = Device('mivpe016', 'antonio', 'admin')
  nc_get_reply = netconf_requests_isis_neighbors(mivpe016.connectnetconf())
  xmlns = "http://cisco.com/ns/yang/Cisco-IOS-XR-clns-isis-oper"
  neighbors = nc_get_reply.data.findall(f'.//{{{xmlns}}}neighbor')


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
  mivpe016.isis_neighbors = isis_neighbors

  print(mivpe016.isis_neighbors)
  #mivpe016.data = netconfrequest(stringaxml, mivpe015.connectnetconf())
  #print(netconfrequest(stringaxml, mivpe016.connectnetconf()))
  #print(mivpe016)

  """

  mivpe015 = Device('mivpe015', 'antonio', 'admin')
  netconf_requests_isis_neighbors(mivpe015)
  mivpe016 = Device('mivpe016', 'antonio', 'admin')
  netconf_requests_isis_neighbors(mivpe016)
  mivar102 = Device('mivar102', 'antonio', 'admin')
  netconf_requests_isis_neighbors(mivar102)
  mivar202 = Device('mivar202', 'antonio', 'admin')
  netconf_requests_isis_neighbors(mivar202)

  db = shelve.open('devicedb')
  for obj in (mivpe015, mivpe016, mivar102, mivar202):
      db[obj.devicename] = obj
  db.close()

  db = shelve.open('devicedb')
  print(len(db))
  for key in db:
     print(key, '=>', db[key])
  print(list(db.keys()))
