import boto3
import json
import psycopg2
from datetime import datetime
from config import DBNAME, ENDPOINT, PASSWORD, PORT, USER


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else f'Added player to {res}',
        'headers': {'Content-Type': 'application/json',},
    }

def lambda_handler(event, context):
    '''
    Adds a player to a sqs queue that represents a lobby for their rank (skill level)

    event passes player id and game type -pvp or mp (multiplayer)
    '''

    sqs = boto3.client('sqs')
    if event['httpMethod'] == 'POST':
        playerid = event['playerid']
        conn = None
        try:
            # Connect to your postgres DB
            conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USER, password=PASSWORD)
            # Open a cursor to perform database operations
            cur = conn.cursor()
            # query rds for player rank
            sql = f'SELECT rank FROM players WHERE playerid={playerid};'
            cur.execute(sql, ())
            player_rank = cur.fetchall()[0]
            cur.close()
            # get the sqs queue the player will be put into
            if player_rank > 50:
                player_queue = '_advanced.fifo'
            elif player_rank >= 10 and player_rank < 50:
                player_queue = '_intermediate,fifo'
            else:
                player_queue = '_beginner.fifo'
            sqs = boto3.resource('sqs')
            queue_url = event['game_type'] + sqs.get_queue_by_name(QueueName=player_queue)
            # add player to lobby, aka sqs queue
            response = sqs.send_message(
                QueueUrl=queue_url,
                DelaySeconds=10,
                MessageBody=(
                    json.dumps({"PlayerId": playerid, "TimeStamp": datetime.now(), "PlayerRank": player_rank})
                )
            )
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return respond(None, queue_url)
    else:
        return respond(ValueError('Error adding player to queue'))
