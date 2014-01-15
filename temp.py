from io import StringIO

from configobj import ConfigObj

a = '''
    key1 = (1, 2, 3)    # comment
    key2 = True
    key3 = 'a string'
    key4 = [1, 2, 3, 'a mixed list']
'''.splitlines()
b = ConfigObj(a, unrepr=True)
