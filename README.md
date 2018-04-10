# virusshare-unzipper
This simple application is targeted for individuals who deal with large VirusShare.com malware samples.

This application does bulk unzipping of password protected malware zip samples. Sure as hell beats typing 'infected' dozens of times...

In addition to bulk unzipping operations, you can also provide this application your AWS Glacier VaultName and have the malware samples be uploaded for long term archiving purposes.

## Basic Usage
Provide the input directory argument with a directory containing the VirusShare.com zip files. Provide an output directory for the location where the samples will be uncompressed.


`python malunzip.py --indir ~/Malware/ --outdir ~/Malware/samples/`

### Archving to AWS Glacier
Note - you will need to ensure that the boto3 library is installed and that you have configured your the IAM role your client uses to have the ability to upload to Glacier VaultName ARN.

`python malunzip.py --indir ~/Malware/ --outdir ~/Malware/samples/ --glacier $VAULT_NAME`
