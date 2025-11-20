import pika, json, tempfile, os
from bson.objectid import ObjectId
from moviepy import *

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)
    
    #empty temp files
    tf = tempfile.NamedTemporaryFile()
    
    # Video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))
    
    #add video contents to temp file
    tf.write(out.read())
    
    # create audio from temp video file 
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()
    
    # write audio to another temp file
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)
    
    # SAVE TO GRIDFS
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)
    
    message["mp3_fid"] = str(fid)
    
    try:
        channel.basic_publish(
            exchange='',
            routing_key=os.environ.get("MP3_Queue"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # make message persistent
            ),
        )
        
    except Exception as err:
        fs_mp3s.delete(fid)
        return "failed to publish message to mp3 queue"