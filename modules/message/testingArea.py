# from datetime import datetime

# import time

# x=time.time() 
# y=x+ 50*24*3600 
# # x = datetime.datetime.now()
# print(datetime.fromtimestamp(x))
# print(datetime.fromtimestamp(y))

import pprint 

stuff={0:'dfsdfs',
1:{'g':43434,'t':'erere'},'dfdf':[2,2,2,22,3,4,5,5,[6,6,6,6,6]]}

Print = pprint.PrettyPrinter(indent=4).pprint
Print(stuff)