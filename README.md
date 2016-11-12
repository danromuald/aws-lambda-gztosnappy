# gzToSnappy

## 1. Introduction

This AWS Lambda function converts gzip files into Snappy. The gzip compression format is typical with web or application logs. For processing on the Hadoop Framework, gzip is not ideal due to its non-splittable nature.

This lambda function listens to an S3 bucket for ```PUT``` events, and ==if the object is has a ```.gz``` extension==, it downloads the file, uncompresses it and compresses it as ```.snappy```, then uploads the ```.snappy``` compressed file to S3 (in this case into a ```processed-snappy``` folder).
  

Below are the steps to create and deploy the function.

##2. Prerequisites

1. Have an AWS account.
2. Create an EC2 instance from one [Lambda Execution Environment](http://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html).
3. Install virtualenv.
4. Configure AWS Lambda execution role to:
	-	Read from the Input S3 bucket.
	- Write into the S3 output bucket.
5. Create a source and destination S3 buckets

## 3. Prepare the Lambda Package on the EC2 instance

###3.1 Install the necessary libraries

```
yum install python27-devel python27-pip
yum install snappy-devel
```

###3.2 Start a python2.7 virtualenv

```
virtualenv gztosnappy
source gztosnappy/bin/activate
```

### 3.3 Install python dependencies

```
pip install boto3 python-snappy
```

### 3.4 Create a deployment package

```
# Assuming you are working from your home directory (/home/ec2-user/)

cd $VIRTUAL_ENV/lib64/python2.7/dist-packages/ && zip -r9 ~/gziptosnappy.gz *

cd

cd /usr/lib64/ && zip -r9 ~gziptosnappy.gz libsnappy*
# 

cd
```

### 3.5 Clone this repository and add the lambda function to the package

```
git clone https://github.com/danromuald/aws-lambda-gztosnappy.git

cd aws-lambda-gztosnappy

# Add the lambda function to your package 

zip -g ~/gziptosnappy.zip gztosnappy.py

```

##4. Deploy the Lambda Function

###4.1 Upload the package to S3

```
aws s3 cp gztosnappy.zip <YOUR CODE BUCKET>/pub/gztosnappy.zip
```

###4.2 Deploy the Function

Use the Cloudformation template [gztosnappy.json](./gztosnappy.json) and deploy the lambda function in your AWS environment. Double check that you have set the parameters correctly.

###4.3 Test the Function

At this point you should have created an input folder ==**YOUR\_INPUT\_BUCKET/stg/input-gz/**==, and an output folder ==**YOUR\_OUTPUT\_BUCKET/stg/processed-snappy/**==.

Drop a ".gz" file in the input folder and watch AWS Lambda process and create the equivalent ".snappy" file!

