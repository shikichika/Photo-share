import boto3

def judge_images(image):
    client = boto3.client('rekognition', 'ap-northeast-1')
    response = client.detect_moderation_labels(Image={'Bytes':image.read()})

    if response['ModerationLabels'] == []:
        return True
    else:
        return False
