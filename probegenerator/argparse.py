import sys, getopt

def parseArgs(argv):
   inputPath = ''
   desiredSpaces = 2
   try:
      opts, args = getopt.getopt(argv,"p:s:",["path=","spaces="])
   except getopt.GetoptError:
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-p' or opt == '--path':
         inputPath = arg
      if opt == '-s' or opt == '--spaces':
         desiredSpaces = arg
   return inputPath, desiredSpaces