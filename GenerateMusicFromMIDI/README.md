# Generate-music-from-MIDI

[![hackmd-github-sync-badge](https://hackmd.io/Q_vsTH7ISTGCb3jv_k16XQ/badge)](https://hackmd.io/Q_vsTH7ISTGCb3jv_k16XQ)


Use LSTM to generate music from MIDI file in PyTorch, and convert the trained model to CoreML.

## Requirements
Training:
- torch==1.7.1
- music21
- numpy
- pickle
- tqdm
- glob
- csv

Converting (on macOX):
- torch==1.7.1
- coremltools
- numpy

## Workflow

1. Parse MIDI files and Store notes in .pkl file
    - `python3 build_note_dict.py classicMIDI`
    - should take dataset_name as cmd input
    - This step also builds note<->int bi-direction dictionaries from training set.

    > Prepare all the notes and dictionaries for reusing to save time in training and testing

3. Train
    - `python3 lstm_train.py classicMIDI`
    - This stage loads notes from .pkl and start training.

4. Generate
    - `python3 lstm_generate_single.py classicMIDI`
    - predict music from a single midi
    - This stage loads pre-trained model and dictionaries, and does prediction.

3. Convert
    - `python3 Pytorch2CoreML.py`
    - convert Pytorch model to CoreML framework