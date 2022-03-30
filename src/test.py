import random as rand;

def generateTestData():
  arr = [];
  for i in range(0, 10):
    r = rand.randint(1, 3);
    if(r == 1): r = True;
    else: r = False;
    arr.append(r);
  return arr;

arr = generateTestData();
print("arr:", arr);

arr = [True]
lastones = arr[-3:];
print(lastones)
if(all(lastones) == True): print("HIYA")