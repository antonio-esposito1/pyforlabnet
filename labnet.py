from ncclient import manager
from argparse import ArgumentParser

class Device():
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
    return device.get(('subtree', subtree_filter)).data_xml

if __name__ == '__main__':
  
  #python3.9 labnet.py --devicename mivpe015 --username antonio --password admin
  parser = ArgumentParser()
  parser.add_argument("--devicename", required = "True")
  parser.add_argument("--username", required = "True")
  parser.add_argument("--password", required = "True")
  args = parser.parse_args()
  
  devicename = args.devicename
  username = args.username
  password = args.password
   
  #definisco un istanza della classe Device che è a sua volta definita nel file Device.py
  dev = Device(devicename,username,password)
  
  # device è il metodo che si connette alla macchina in campo  
  device = dev.connectnetconf()

  D = dict()
  
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
 
  D['device'] = netconfrequest(stringaxml, device)
  
  

  print(D['device'])