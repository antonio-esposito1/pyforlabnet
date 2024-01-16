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
    
  mivpe015 = Device('mivpe015', 'antonio', 'admin')
  netconf_requests_isis_neighbors(mivpe015)
  mivpe016 = Device('mivpe016', 'antonio', 'admin')
  netconf_requests_isis_neighbors(mivpe016)
  mivar102 = Device('mivar102', 'antonio', 'admin')
  netconf_requests_isis_neighbors(mivar102)
  mivar202 = Device('mivar202', 'antonio', 'admin')
  netconf_requests_isis_neighbors(mivar202)
  navpe225 = Device('navpe225', 'antonio', 'admin')
  netconf_requests_isis_neighbors(navpe225)
  navpe226 = Device('navpe226', 'antonio', 'admin')
  netconf_requests_isis_neighbors(navpe226)
  navar101 = Device('navar101', 'antonio', 'admin')
  netconf_requests_isis_neighbors(navar101)
  navar201 = Device('navar201', 'antonio', 'admin')
  netconf_requests_isis_neighbors(navar201)

  db = shelve.open('devicedb')
  for obj in (mivpe015, mivpe016, mivar102, mivar202, navar101, navar201, navpe225, navpe226):
      db[obj.devicename] = obj
  db.close()

  db = shelve.open('devicedb')
  print(len(db))
  for key in db:
     print(key, '=>', db[key])
  print(list(db.keys()))
