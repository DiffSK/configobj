import sys
import configobj

print(configobj.ConfigObj(sys.argv[1]))
