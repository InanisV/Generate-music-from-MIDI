from flask import Flask, request, send_file, redirect, url_for
import boto3
import credentials  # Local file containing AWS access key id and secret access key
import sys, os
import torch
from tools import Tools

app = Flask(__name__)

# Bucket to store/get midi files
s3 = boto3.resource(
        's3',
        aws_access_key_id = credentials.aws_access_key_id,
        aws_secret_access_key = credentials.aws_secret_access_key,
        region_name = '<REGION>') # eg 'ap-southeast-1'
bucket_name = "<BUCKET_NAME>"

# Data set name on which training data was trained, e.g. should correspond with pt file 'lstm_pretrained_{data_set}.pt'
data_set = "LakhMIDI" 

# Retrieve generated midi file from s3 bucket
@app.route("/getfile/<midi_name>")
def get(midi_name):
    response = s3.Object(bucket_name, midi_name).get()
    print("Getting midi file: " + midi_name)
    return send_file(response['Body'], mimetype='audio/midi', attachment_filename=midi_name, as_attachment=True)

# Send midi file as input to pretrained model and store prediction in s3 bucket
@app.route("/generate", methods = ['POST'])
def generate_single_midi():
    file_obj = request.files['midi_object']
    script_dir = os.path.dirname(__file__)

    # Save input as input.mid in data directory
    rel_path = "data/input.mid"
    abs_path = os.path.join(script_dir, rel_path)
    data = file_obj.read()
    with open(abs_path, 'wb') as out_file:
        out_file.write(data)
    
    # Get notes from midi file
    # directory only consists of one midi file (simply to reuse code)
    notes = Tools.get_notes("data/*.mid")
    print("length of notes dictionary: " + str(len(notes)))

    # Get the number of pitch names
    n_vocab = len(set(notes))
    
    # Load dictionaries
    note_to_int = Tools.load_obj(f'{data_set}_note2int')
    int_to_note = Tools.load_obj(f'{data_set}_int2note')
   
    # convert notes into numerical input
    network_input = Tools.prepare_sequences_single(notes, note_to_int, n_vocab)
    network_input = network_input.tolist()
    
    # Use the model to generate a new midi
    model = torch.load(f'lstm_pretrained_{data_set}.pt')
    model.eval()
    prediction_output = Tools.generate_notes_single(model, int_to_note, network_input, len(set(notes)))
    Tools.create_midi(prediction_output, f'{data_set}_midi_g')
    
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(f'{data_set}_midi_g.mid', f'{data_set}_midi_g.mid')
    print("New midi file has been generated and uploaded to database")
    return f'/getfile/{data_set}_midi_g.mid'  

'''
@app.route("/", methods = ['POST'])
def main():
    file_obj = request.files['midi_object']
    print("Uploading midi file: " + file_obj.filename)
    bucket = s3.Bucket(bucket_name)
    bucket.upload_fileobj(file_obj, file_obj.filename, ExtraArgs={'ContentType': 'audio/midi'})
    return "<h1>MIDI file has been posted</h1>"
'''

if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=8080, debug=True)

