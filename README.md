# Generate-music-from-MIDI

Use LSTM to generate music from MIDI file

## Requirements
Training:
- torch==1.7.1
- music21
- numpy
- glob

Converting (on macOX):
- torch==1.7.1
- coremltools
- numpy

## Workflow

1. Train
    - `python3 lstm_train.py`
2. Generate
    - `python3 build_note_dict.py` （build note<->int bi-direction dictionaries from training set）
    - `python3 lstm_generate_single.py` (predict music from a single midi)

3. Convert
    - `python3 Pytorch2CoreML.py` (convert Pytorch model to CoreML framework)