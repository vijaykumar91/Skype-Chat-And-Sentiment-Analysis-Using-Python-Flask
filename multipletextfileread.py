import glob
import errno
path = 'C:/data_analytics/files/june/*.txt' #note C:
files = glob.glob(path)
#print(files)
for name in files:
    try:
        with open(name) as f:
            for line in f:
                print(line.split())
    except IOError as exc: #Not sure what error this is
        if exc.errno != errno.EISDIR:
            raise