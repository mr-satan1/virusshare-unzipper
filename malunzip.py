from zipfile import ZipFile
from shutil import make_archive
import os
import argparse
import sys

# Currently optimized for VirusShare.com files.
## If you want to add for other services,
### adjust the listZip function as it looks for "VirusShare" string
TypicalMalwareSharingPassword = 'infected'
parser = argparse.ArgumentParser()
parser.add_argument('--indir', help='Input directory containing zip samples from VirusShare',
                    required=True)
parser.add_argument('--outdir', help='Output directory for the malware samples.',
                    required=True)
parser.add_argument('--glacier', help='Provide the AWS Glacier Vault name for long term malware storage. Note - uploads take ~24hrs to complete.')


args = parser.parse_args()

def unzipFile(filename):
    if os.path.exists(filename):
        with ZipFile(file) as zippedFile:
            zippedFile.extractall(args.outdir, pwd=TypicalMalwareSharingPassword.encode())

def zipDirGlacier(archiveName, archiveDir):
    archName = os.path.expanduser(os.path.join('~', archiveName))
    make_archive(archName, 'zip', archiveDir)
    print('[*] Archive done! Sending to Glacier.')
    try:
        archName = os.path.expanduser(os.path.join('~', archiveName)) + '.zip'
        with open(archName, 'rb') as upload:
            response = client.upload_archive(vaultName=args.glacier,
            archiveDescription=archName, body=upload)
        print('[*] Archived to Glacier! It takes ~24 hours for the archive to be uploaded!')
    except Exception as e:
        print(e)

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
    if args.glacier:
        try:
            import boto3
            client = boto3.client('glacier')
            print("[*] Using Glacier VaultName: %s" % args.glacier)
            accept = input('>>> Would you like to archive everything in >> %s << to AWS Glacier VaultName: %s (y/n)? ' % (args.indir, args.glacier)).lower()
            if accept.startswith('y'):
                print('[*] Beginning Glacier upload process...')
                zipDirGlacier(args.glacier, args.indir)
            else:
                print("User input != 'y'. Exiting.")
                sys.exit(1)
        except Exception as e:
            print(e)



    elif os.path.exists(args.indir):
        listZip(args.indir)
        print("[*] Completed unzip operations on %s amount of files" % UnzipCounter)
        print('[*] Your malware is ready: %s' % args.outdir)
