from argparse import parseArgs
import sys
import csv

def getProbePairs(inputPath, desiredSpaces):
    seq=[]
    seqf=[]
    seqpair=[]
    probeend = 0
    genefile = inputPath
    gap = int(desiredSpaces)
    with open (genefile) as gene:
        for line in gene:
            # if you want to split the line
            # assuming data is tab separated
            newline = line.rstrip("\n").split("\t")

            # if you want conditional printing
            if len(newline) > 0:
                seq.append(newline)
        for seqn in seq:
            if int(seqn[1]) >= int(probeend):
                seqf.append(seqn)
                probeend = (int(seqn[2]) + gap)
        count = len(seqf)
        for i in range(0, count-1):
            j = i+1
            k = i-1
            if int(seqf[i][2]) + gap == int(seqf[j][1]):
                seqpair.append(seqf[i][3])
            elif int(seqf[i][1]) - gap == int(seqf[k][2]):
                seqpair.append(seqf[i][3])
    writeProbesToCSV(seqf, seqpair)

def writeProbesToCSV(seqf, seqpair):
    with open('./probes.csv', 'w+') as probes:
        csv_writer = csv.writer(probes, delimiter=",")
        csv_writer.writerow(['SHH', 'start', 'stop', 'seq', 'tm', 'spacing', 'SHH name'])
        last_index = 0
        for line in seqf:
            space = int(line[1]) - int(last_index)
            if space >= 3:
                last_index = line[2] 
                line.append(space)
                csv_writer.writerow(line)

if __name__ == '__main__':
    inputPath, desiredSpaces = parseArgs(sys.argv[1:])
    getProbePairs(inputPath, desiredSpaces)
    print "hi"