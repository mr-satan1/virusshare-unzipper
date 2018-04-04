from zipfile import ZipFile
import os
import argparse

# Currently optimized for VirusShare.com files.
## If you want to add for other services,
### adjust the listZip function as it looks for "VirusShare" string


TypicalMalwareSharingPassword = 'infected'


parser = argparse.ArgumentParser()
parser.add_argument('--indir', help='Input directory containing zip samples from VirusShare',
                    required=True)
parser.add_argument('--outdir', help='Output directory for the malware samples.',
                    required=True)
args = parser.parse_args()

def unzipFile(file):
    if os.path.exists(file):
        with ZipFile(file) as zippedFile:
            zippedFile.extractall(args.outdir, pwd=TypicalMalwareSharingPassword.encode())


def listZip(directory):
    global UnzipCounter
    UnzipCounter = 0
    print("[*] - Checking directory: %s" % directory)
    for f in os.listdir(directory):
        FullFilePath = os.path.join(directory, f)
        if "VirusShare" in f and f.endswith(".zip"):
            print("VirusShare sample found: %s" % f)
            # Add to counter
            UnzipCounter += 1
            unzipFile(FullFilePath)

if __name__ == "__main__":
    if os.path.exists(args.indir):
        listZip(args.indir)
        print("[*] Completed unzip operations on %s amount of files" % UnzipCounter)
        print('[*] Your malware is ready: %s' % args.outdir)






