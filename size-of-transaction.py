# example data for first bitcoin transaction 4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b
scriptsInput = ["04ffff001d0104455468652054696d65732030332f4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f757420666f722062616e6b73"]
scriptsOutput = ["6504678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fAC"]

# wittness script
stackItems = [
#  ["aaaa", "bbbb", "cccc"]
] # as many stack items as numberOfInputs

def getSizeOfVarInt(val):
  if val <= 0xfc:
    return 1
  elif val <= 0xffff:
    return 3
  elif val <= 0xffffffff:
    return 5
  elif val <= 0xffffffffffffffff:
    return 9

flags = 0
extendedTransactionFormat = False
numberOfInputs = len(scriptsInput)
numberOfOutputs = len(scriptsOutput);

if len(stackItems) > 0:
  extendedTransactionFormat = True
  flags = 1 # can be zero or non-zero - when wittness script is used, flags is always 1

size = 8 # for version and lockTime
if extendedTransactionFormat:
  size = size + getSizeOfVarInt(0) # if number of inputs is zero then indicator for extended transaction format
else:
  size = size + getSizeOfVarInt(numberOfInputs)

size = size + getSizeOfVarInt(numberOfOutputs);
size = size + numberOfOutputs * 8 + numberOfInputs * 40 # input: previousHash, outId, seqNo; ouput: value

for outputIndex in range(0, numberOfOutputs):
  sizeScript = len(scriptsOutput[outputIndex]) / 2 # the script defined above is hex representation, so we devide it by 2 to get the byte length
  size = size + sizeScript + getSizeOfVarInt(sizeScript) # the length is also saved in the files so we have to add this too

for inputIndex in range(0, numberOfInputs):
  sizeScript = len(scriptsInput[outputIndex]) / 2
  size = size + sizeScript + getSizeOfVarInt(sizeScript)

if extendedTransactionFormat:
  size = size + 1 # flags
  if flags != 0:
    size = size + getSizeOfVarInt(numberOfInputs)
    if flags & 1:
      for inputIndex in range(0, numberOfInputs):
        countOfStackItems = len(stackItems[inputIndex])
        size = size + getSizeOfVarInt(countOfStackItems)
        for stackItemIndex in range(0, countOfStackItems):
          scriptSize = len(stackItems[inputIndex][stackItemIndex]) / 2
          size = size + getSizeOfVarInt(scriptSize)
          size = size + scriptSize

print str(size) + " byte"
