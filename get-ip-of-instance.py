import json
import os

cmd = 'aws ec2 describe-instances --filters "Name=tag:Name,Values=*" --query "Reservations[*].Instances[*].{Ip:PublicIpAddress,Tags:Tags[?Key == \'Name\'] | [0].Value}" --region ap-south-1'

output_stream = os.popen(cmd)
result = output_stream.read()
output_stream.close()

result2 = result.replace("\n", "")
rj = json.loads(result2)

for i in rj:
    ival=i[0]
    if ival['Tags'] == 'gui-dev-instance':
        print(ival)