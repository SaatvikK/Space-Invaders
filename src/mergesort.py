def merge(arr, LeftIndex, RightIndex, middle):
  # Make copies of both arrays that are being merged:
  LeftArrCopy = arr[LeftIndex:middle + 1];
  RightArrCopy = arr[middle + 1:RightIndex + 1];
  
  # Variables that are used to keep track of where we are in each array:
  LeftCopyIndex, RightCopyIndex, SortedIndex = 0, 0, LeftIndex;

  # While-loop through both copies until no more elements in either copy:
  while(LeftCopyIndex < len(LeftArrCopy) and RightCopyIndex < len(RightArrCopy)):
    # If LeftArrCopy has smaller element, put it in sorted part. 
    # Then, increment the left copy pointer (LeftCopyIndex):

    if(LeftArrCopy[LeftCopyIndex]["score"] <= RightArrCopy[RightCopyIndex]["score"]):
      arr[SortedIndex]["score"] = LeftArrCopy[LeftCopyIndex]["score"];
      LeftCopyIndex += 1;
    
    else: #This is just the opposite of the above if-statement
      arr[SortedIndex]["score"] = RightArrCopy[RightCopyIndex]["score"];
      RightCopyIndex += 1;
    
    # Increment sorted index pointer:
    SortedIndex += 1;

  # Ran out of elements in one of the left/right copies so look at the remaining elements and sort them:
  while(LeftCopyIndex < len(LeftArrCopy)):
    arr[SortedIndex]["score"] = LeftArrCopy[LeftCopyIndex]["score"];
    LeftCopyIndex += 1;
    SortedIndex += 1;
  
  while(RightCopyIndex < len(RightArrCopy)):
    arr[SortedIndex]["score"] = RightArrCopy[RightCopyIndex]["score"];
    RightCopyIndex += 1;
    SortedIndex += 1;  

def mergeSort(arr, LeftIndex, RightIndex):
  if(LeftIndex >= RightIndex):
    return;
  
  middle = (LeftIndex + RightIndex)//2
  mergeSort(arr, LeftIndex, middle);
  mergeSort(arr, middle + 1, RightIndex);
  merge(arr, LeftIndex, RightIndex, middle);



def driverMethod(arr):
  # Merge sort is O(n.logn) time
  mergeSort(arr, 0, len(arr) - 1); #0 = left pointer, len(arr) - 1 = right pointer
  return arr;


