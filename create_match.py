import boto3
import psycopg2
import json
from datetime import datetime
from time import sleep
from config import DBNAME, ENDPOINT, PASSWORD, PORT, USER


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else f'Game and leaderboard created for {res[0]} and {res[1]}',
        'headers': {'Content-Type': 'application/json',},
    }


def lambda_handler(event, context):
    '''
    Gets player from rdb and places them into the beginner pvp queue

    Creates event and leaderboard objects in rds
    '''

    num_players = 2
    game_name = 'pvp_beginner.fifo'
    sqs = boto3.client('sqs')

    # Get the queue. This returns an SQS.Queue instance
    response = sqs.get_queue_url(QueueName=game_name)
    queue_url = response['QueueUrl']

    # You can now access identifiers and attributes
    player_ids = []
    receipt_handles = []
    response = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=['ApproximateNumberOfMessages'])
    size = int(response['Attributes']['ApproximateNumberOfMessages'])
    print(size)
    for i in range(120):
        if size < num_players:
            sleep(5)
        else:
            # Get players from queue
            response = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=num_players,
                VisibilityTimeout=0,
                WaitTimeSeconds=0
            )
            for message in response['Messages']:
                body = message['Body']
                body = body.split(',')
                player_id = body[0].split(':')[1].strip()
                player_id = int(player_id)
                player_ids.append(player_id)
                break

    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD)
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # TODO: Check if players are already in leaderboards
        # Create Game Object
        pvp_match_sql = "f'INSERT INTO pvp_match (players, game_type, creation_time()) VALUES (%s, %s, %s);"
        game_type = game_name.split('.')[0]
        cur.execute(pvp_match_sql, (player_ids, game_type, datetime.now()))

        # Create Leaderboard Object
        leaderboard_name = f'{game_name}_{datetime.now()}'
        pvp_match_sql = "f'INSERT INTO leaderboards (name, start_date) VALUES (%s, %s);"
        cur.execute(pvp_match_sql, (leaderboard_name, datetime.now()))
        cur.close()

        #Delete received message from queue
        for rh in receipt_handles:
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=rh
            )

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return respond(None, player_ids)
