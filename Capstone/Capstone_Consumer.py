from kafka import KafkaConsumer
import boto3

'''
It is important to note that boto3 is used to access any communications between Python and AWS. Additionally, once you install boto, you need a way to access 
your AWS information. For this instance, it was done by installing the AWS command line interface and following the steps outlined here:
https://aws.amazon.com/cli/ and here as well : https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation
'''

# set up boto3
Primary_column_name = 'Time'
Primary_Key = 1
columns = ['Date', 'Time', 'Ticker', 'Open', 'Close', 'High', 'Low', 'Vol']
client = boto3.client('dynamodb', region_name = 'us-east-2')
DB = boto3.resource('dynamodb',
                    region_name = 'us-east-2',
                    aws_access_key_id='AKIAS4YILQJT2LGMRROA',
                    aws_secret_access_key='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',
                    verify=False)
table = DB.Table('Crypto')

# To export information to DynamoDB and set up the consumer
Primary_Key = 5
consumer = KafkaConsumer('KafkaStreams', bootstrap_servers=['b-1.kafkastreams.cx66e3.c4.kafka.us-east-2.amazonaws.com:9092'])

def kafkaconsumer():
    for rec in consumer:
        rec_data = rec.value.decode('utf-8')
        rec_msg = rec_data.split(',')
        print(rec_msg[0],rec_msg[1],rec_msg[2],rec_msg[7])

        #first and last_msg is to remove characters
        first_msg = rec_msg[0].split("\"")
        last_msg = rec_msg[7].split("\"")
        print(first_msg[1], last_msg[0])

        # to send to AWS DynamoDB
        response = table.put_item(
            Item={
                Primary_column_name: Primary_Key,
                columns[0]: str(first_msg[1]),
                columns[1]: str(rec_msg[1]),
                columns[2]: rec_msg[2],
                columns[3]: str(round(float(rec_msg[3]),4)),
                columns[4]: str(round(float(rec_msg[4]),4)),
                columns[5]: str(round(float(rec_msg[5]),4)),
                columns[6]: str(round(float(rec_msg[6]),4)),
                columns[7]: str(round(float(last_msg[0]),4))
                }
            )

if __name__=='__main__':
    run=kafkaconsumer()




