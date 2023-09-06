import boto3
import json
import logging
import os
import pymysql.cursors
import sys
import time

# rds settings
user_name = os.environ['USER_NAME']
password = os.environ['PASSWORD']
rds_proxy_host = os.environ['RDS_PROXY_HOST']
db_name = os.environ['DB_NAME']
queue_url = os.environ['QUEUE_URL']

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else f'Created matched game and leaderboard for {res}',
        'headers': {'Content-Type': 'application/json', },
    }


def lambda_handler(event, context):
    '''
    Retrieves two players from the beginner pvp queue and sets up a match and leaderboard
    '''
    num_players = 2
    game_name = 'pvp_beginner.fifo'

    # You can now access identifiers and attributes
    player_ids = []

    # Get players from queue
    for message in event['Records']:
        body = message['body']
        player_ids.append(body['playerid'])

    player_ids_json = {'player_ids': player_ids}
    try:
        conn = pymysql.connect(host=rds_proxy_host, user=user_name, passwd=password, db=db_name, connect_timeout=5)
        with conn.cursor() as cursor:
            # Create Game Object
            game_type = game_name.split('.')[0]
            sql = "INSERT INTO `matched_games` (`players`, `game_type`, `creation_time`) VALUES (%s, %s, NOW())"
            cursor.execute(sql, (json.dumps(player_ids_json), game_type))
            conn.commit()
            # Create Leaderboard Object

            leaderboard_name = f'{game_name}_{time.time()}'
            pvp_match_sql = "INSERT INTO leaderboards (`name`, `start_date`) VALUES (%s, NOW())"
            cursor.execute(pvp_match_sql, (leaderboard_name))
            conn.commit()
            cursor.close()

    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    return respond(None, player_ids)
