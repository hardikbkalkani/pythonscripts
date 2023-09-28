####################################################################
##    Date:28-09-2023                                             ##
##    Owner:Hardik Kalkani                                        ##
##    Version: 1.0                                                ##
####################################################################

# This script finds all unused security groups in a single AWS Region
# For Different Region you need to configure your Region


import boto3

if __name__ == "__main__":
    ec2 = boto3.client("ec2")
    elb = boto3.client("elb")
    elbv2 = boto3.client("elbv2")
    rds = boto3.client("rds")

    used_SG = set()

    # Find EC2 instances security group in use.
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            for sg in instance["SecurityGroups"]:
                used_SG.add(sg["GroupId"])

    # Find Classic load balancer security group in use
    response = elb.describe_load_balancers()
    for lb in response["LoadBalancerDescriptions"]:
        for sg in lb["SecurityGroups"]:
            used_SG.add(sg)

    # Find Application load balancer security group in use
    response = elbv2.describe_load_balancers()
    for lb in response["LoadBalancers"]:
        for sg in lb["SecurityGroups"]:
            used_SG.add(sg)

    # Find RDS db security group in use
    response = rds.describe_db_instances()
    for instance in response["DBInstances"]:
        for sg in instance["VpcSecurityGroups"]:
            used_SG.add(sg["VpcSecurityGroupId"])

    response = ec2.describe_security_groups()
    total_SG = [sg["GroupId"] for sg in response["SecurityGroups"]]
    unused_SG = set(total_SG) - used_SG

    print(f"Total Security Groups: {len(total_SG)}")
    print(f"Used Security Groups: {len(used_SG)}\n")
    print(f"Unused Security Groups: {len(unused_SG)} compiled in the following list:")
    print(f"{list(unused_SG)}")

