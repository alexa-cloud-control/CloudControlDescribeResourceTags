""" Lambda function - Describe tags for resource """
import boto3

def cloud_control_describe_ec2_tags(event, context):
    """ Lambda function - Describe tags for resource """

    # validate instance name
    ec2 = boto3.resource('ec2')
    ec2_client = boto3.client('ec2')
    msg = ""
    response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [event["body"]["InstanceName"]]
            }
        ]
    )
    instance_list = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_list.append(instance['InstanceId'])
            try:
                if (instance['Tags']):
                    for tag in response['Tags']:
                        temp_msg = 'Key <voice name="Matthew">{}</voice> with value <voice name="Matthew">{}</voice>.'.format(
                            tag['Key'], tag['Value']
                        )
                        msg = "{} {}".format(msg, temp_msg)
            except Exception as e:
                msg = "I did not find any tags for instance {}".format(event["body"]["InstanceName"])
                return {"msg": msg}


    if not instance_list:
        msg = "I cannot find the instance with name {}.".format(event["body"]["InstanceName"])
        return {"msg": msg}

    temp_msg = "Here is the list of tags attached to {}.".format(event["body"]["InstanceName"])
    message = "<p>{}</p> <p>{}</p>".format(temp_msg, msg)
    return {"msg": message}
