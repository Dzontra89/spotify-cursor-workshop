import json
import boto3
import os
from datetime import datetime

s3 = boto3.client('s3')
output_bucket = os.environ['OUTPUT_BUCKET']

def categorize_playlist(name):
    name = name.lower()
    categories = {
        'workout': ['workout', 'gym', 'fitness', 'exercise'],
        'party': ['party', 'dance', 'club'],
        'relax': ['relax', 'chill', 'sleep', 'ambient'],
        'focus': ['focus', 'study', 'work', 'concentration'],
        'mood': ['happy', 'sad', 'angry', 'emotional'],
        'decade': ['60s', '70s', '80s', '90s', '00s'],
        'genre': ['rock', 'pop', 'hip hop', 'jazz', 'classical', 'country']
    }
    
    for category, keywords in categories.items():
        if any(keyword in name for keyword in keywords):
            return category
    return 'other'

def handler(event, context):
    for record in event['Records']:
        # Get the S3 bucket and key from the SQS message
        sqs_message = json.loads(record['body'])
        bucket = sqs_message['Records'][0]['s3']['bucket']['name']
        key = sqs_message['Records'][0]['s3']['object']['key']

        # Read the content of the S3 file
        response = s3.get_object(Bucket=bucket, Key=key)
        content = json.loads(response['Body'].read().decode('utf-8'))

        # Remove 'info' key
        if 'info' in content:
            del content['info']

        # Filter playlists and perform transformations
        transformed_playlists = []
        for playlist in content.get('playlists', []):
            if playlist.get('num_followers', 0) > 1:
                # Calculate total duration in seconds
                total_duration_seconds = sum(track.get('duration_ms', 0) for track in playlist.get('tracks', [])) / 1000

                # Categorize playlist
                category = categorize_playlist(playlist.get('name', ''))

                transformed_playlist = {
                    'name': playlist.get('name'),
                    'collaborative': playlist.get('collaborative'),
                    'pid': playlist.get('pid'),
                    'modified_at': playlist.get('modified_at'),
                    'num_tracks': playlist.get('num_tracks'),
                    'num_albums': playlist.get('num_albums'),
                    'num_followers': playlist.get('num_followers'),
                    'tracks': playlist.get('tracks'),
                    'num_edits': playlist.get('num_edits'),
                    'total_duration_seconds': total_duration_seconds,
                    'num_artists': playlist.get('num_artists'),
                    'category': category
                }
                transformed_playlists.append(transformed_playlist)

        # Write to output bucket as a JSON Lines file
        output_key = f"processed_{datetime.now().isoformat()}_{key}"
        output_content = '\n'.join(json.dumps(playlist) for playlist in transformed_playlists)
        
        s3.put_object(
            Bucket=output_bucket,
            Key=output_key,
            Body=output_content,
            ContentType='application/x-ndjson'
        )

        print(f"Processed file {key} and wrote results to {output_key}")
