import os

#CRIA AS PASTAS VAZIAS
if not os.path.isdir("./logs"): os.makedirs("./logs") 
if not os.path.isdir("./output"): os.makedirs("./output") 