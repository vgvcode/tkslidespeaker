import boto3
import os

def downloadFile(s3f):
    #print("s3f:{}".format(s3f))
    elements = s3f.split('/')
    h = None
    for e in elements[0:-1]:
        if h is None:
            h = e
        else:
            h = h + "\\" + e
        if not os.path.isdir(h):
            #print("h:{}".format(h))
            os.mkdir(h)
    f = elements[-1]
    #print("f:{}".format(f))
    h = h + "\\" + f
    #print("h:{}".format(h))
    #download file from s3
    s3_client.download_file('pdp-speech-vgv', s3f, h)

boto3.setup_default_session(profile_name='vgvcode-admin') 
s3_client = boto3.client('s3') 

def downloadPresentation(presoName):
    print("Downloading presentation")
    paginator = s3_client.get_paginator('list_objects_v2') 
    pages = paginator.paginate(Bucket='pdp-speech-vgv', Prefix=presoName)
    count = 0
    for page in pages:
        for obj in page['Contents']:
            count = count + 1
            downloadFile(obj['Key'])
    print("Downloaded presentation: {}, total {} files".format(count, presoName))

# #list objects in an s3 bucket
# maxKeys = 1000

# session = boto3.Session(profile_name='vgvcode-admin')
# s3_client = session.client('s3')

# response = s3_client.list_objects_v2(
#     Bucket='pdp-speech-vgv',
#     Prefix='woc-full',
#     MaxKeys = maxKeys
#     )

# lg = len(response['Contents'])
# if (lg == maxKeys):
#     print("Files truncated to {}".format(maxKeys))
#     exit()

# for i in range(lg):
#     s3f = response['Contents'][i]['Key']
#     #print("s3f:{}".format(s3f))
#     elements = s3f.split('/')
#     h = None
#     for e in elements[0:-1]:
#         if h is None:
#             h = e
#         else:
#             h = h + "\\" + e
#         if not os.path.isdir(h):
#             #print("h:{}".format(h))
#             os.mkdir(h)
#     f = elements[-1]
#     #print("f:{}".format(f))
#     h = h + "\\" + f
#     #print("h:{}".format(h))
#     #download file from s3
#     s3_client.download_file('pdp-speech-vgv', response['Contents'][i]['Key'], h)
