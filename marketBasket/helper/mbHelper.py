import sys
from collections import namedtuple

iDat = namedtuple('iDat', ['time', 'cluster', 'record'])
oDat = namedtuple('oDat', ['transaction', 'cluster'])


def outputSet(oFile, cSet, transaction):
    oFile.write('%s,%s\n' % (transaction, ','.join(str(s) for s in cSet)))


def main(argv):
    iFile = open(argv[0], 'r')
    oFile = open(argv[1], 'w')
    seconds = int(float(argv[2]))

    oldTime = -1
    transaction = 0
    setup = False

    clustersSeen = set()

    for l in iFile.xreadlines():
        x = l.strip().split(',', 2)
        data = iDat(*x)
        currentTime = int(float(data.time)) % seconds

        # 1x setup
        if not setup:
            oldTime = currentTime
            setup = True

        # time to write out the old
        if currentTime != oldTime:
            transaction += 1
            outputSet(oFile, clustersSeen, transaction)
            clustersSeen.clear()

        clustersSeen.add(data.cluster)

        oldTime = currentTime

    # any leftovers needs to be written out
    if len(clustersSeen) > 0:
        outputSet(oFile, clustersSeen, transaction)

    iFile.close()
    oFile.close()

if __name__ == '__main__':
    main(sys.argv[1:])