import sys, getopt

def parseArgs(argv):
   inputPath = ''
   desiredSpaces = 3
   initiator = ''
   left_init_seq = ''
   left_spacer = ''
   right_init_seq = ''
   right_spacer = ''
   try:
      opts, args = getopt.getopt(argv,"p:s:i:l:r:",["path=","spaces=","initiator=","left-seq=","left-spacer=","right-seq=","right-spacer="])
   except getopt.GetoptError:
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-p' or opt == '--path':
         inputPath = arg
      if opt == '-s' or opt == '--spaces':
         desiredSpaces = arg
      if opt == '-i' or opt == '--initiator':
         initiator = arg
      if opt == '-l' or opt == '--left-seq':
         left_init_seq = arg
      if opt == '--left-spacer':
         left_spacer = arg
      if opt == '-r' or opt == '--right-seq':
         right_init_seq = arg
      if opt == '--right-spacer':
         right_spacer = arg

   return inputPath, desiredSpaces, initiator, left_init_seq, left_spacer, right_init_seq, right_spacer