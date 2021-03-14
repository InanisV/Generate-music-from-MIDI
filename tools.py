import glob
import torch
import numpy as np
from music21 import converter, instrument, note, chord, stream


class Tools:
    MIDI_path = "Pokemon MIDIs/*.mid"

    @staticmethod
    def get_notes(MIDI_path):
        """ Get all the notes and chords from the midi files """
        notes = []

        for file in glob.glob(MIDI_path):
            midi = converter.parse(file)

            print("Parsing %s" % file)

            notes_to_parse = None

            try:  # file has instrument parts
                s2 = instrument.partitionByInstrument(midi)
                notes_to_parse = s2.parts[0].recurse()
            except Exception:  # file has notes in a flat structure
                notes_to_parse = midi.flat.notes
                
            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))

        return notes

    @staticmethod
    def prepare_sequences(notes, n_vocab):
        """ Prepare the sequences used by the Neural Network """
        sequence_length = 100

        # get all pitch names
        pitchnames = sorted(set(item for item in notes))

        # create a dictionary to map pitches to integers
        note_to_int = dict((note, number) for number,
                           note in enumerate(pitchnames))

        network_input = []
        network_output = []

        # create input sequences and the corresponding outputs
        for i in range(0, len(notes) - sequence_length, 1):
            sequence_in = notes[i:i + sequence_length]
            sequence_out = notes[i + sequence_length]
            network_input.append([note_to_int[char] for char in sequence_in])
            network_output.append(note_to_int[sequence_out])

        # reshape the input into a format compatible with LSTM layers
        n_patterns = len(network_input)
        network_input = np.reshape(network_input,
                                   (n_patterns, sequence_length, 1))

        # normalize input between 0 and 1
        network_input = network_input / float(n_vocab)

        network_output = Tools.to_categorical(network_output,
                                              max(network_output)+1)

        return (network_input, network_output)
    
    @staticmethod
    def get_note_dicts(notes):
        """ Prepare the sequences used by the Neural Network """
        # get all pitch names
        pitchnames = sorted(set(item for item in notes))

        # create a dictionary to map pitches to integers
        note_to_int = dict((note, number) for number,
                           note in enumerate(pitchnames))
        int_to_note = dict((number, note) for number,
                           note in enumerate(pitchnames))

        return note_to_int, int_to_note
    
    @staticmethod
    def prepare_sequences_single(notes, note_to_int, n_vocab):
        """ Prepare the sequences used by the Neural Network """
        sequence_length = 100

        # # get all pitch names
        # pitchnames = sorted(set(item for item in notes))

        # # create a dictionary to map pitches to integers
        # note_to_int = dict((note, number) for number,
        #                    note in enumerate(pitchnames))

        network_input = []

        # create input sequences and the corresponding outputs
        for i in range(0, len(notes) - sequence_length, 1):
            sequence_in = notes[i:i + sequence_length]
            network_input.append([note_to_int[char] for char in sequence_in])

        # reshape the input into a format compatible with LSTM layers
        n_patterns = len(network_input)
        network_input = np.reshape(network_input,
                                   (n_patterns, sequence_length, 1))

        # normalize input between 0 and 1
        network_input = network_input / float(n_vocab)

        return network_input

    @staticmethod
    def generate_notes(model, notes, network_input, n_vocab):
        """ Generate notes from neural network based on sequence of notes """
        # pick a random sequence from input as starting point for prediction
        pitchnames = sorted(set(item for item in notes))

        start = np.random.randint(0, len(network_input)-1)

        int_to_note = dict((number, note) for number,
                           note in enumerate(pitchnames))

        pattern = network_input[start]
        prediction_output = []

        # generate 500 notes
        for note_index in range(500):
            prediction_input = np.reshape(pattern, (1, len(pattern), 1))
            prediction_input = prediction_input / float(n_vocab)
            my_input = torch.DoubleTensor(prediction_input.tolist())

            prediction = model(my_input).detach().cpu().numpy()

            index = np.argmax(prediction)
            result = int_to_note[index]
            prediction_output.append(result)

            pattern = np.append(pattern, index)
            pattern = pattern[1:len(pattern)]

        return prediction_output

    @staticmethod
    def generate_notes_single(model, int_to_note, network_input, n_vocab):
        """ Generate notes from neural network based on sequence of notes """
        # pick a random sequence from input as starting point for prediction
        start = np.random.randint(0, len(network_input)-1)

        # print(len(network_input[0]))
        pattern = network_input[start]
        prediction_output = []

        # generate 500 notes
        for note_index in range(500):
            prediction_input = np.reshape(pattern, (1, len(pattern), 1))
            prediction_input = prediction_input / float(n_vocab)
            my_input = torch.DoubleTensor(prediction_input.tolist())

            prediction = model(my_input).detach().cpu().numpy()

            index = np.argmax(prediction)
            result = int_to_note[index]
            prediction_output.append(result)

            pattern = np.append(pattern, index)
            pattern = pattern[1:len(pattern)]

        return prediction_output

    @staticmethod
    def create_midi(prediction_output, filename):
        """ convert the output from the prediction to notes and create a midi file
            from the notes """
        offset = 0
        output_notes = []

        # create note and chord objects based on values generated by model
        for pattern in prediction_output:
            # pattern is a chord
            if ('.' in pattern) or pattern.isdigit():
                notes_in_chord = pattern.split('.')
                notes = []
                for current_note in notes_in_chord:
                    new_note = note.Note(int(current_note))
                    new_note.storedInstrument = instrument.Piano()
                    notes.append(new_note)
                new_chord = chord.Chord(notes)
                new_chord.offset = offset
                output_notes.append(new_chord)
            # pattern is a note
            else:
                new_note = note.Note(pattern)
                new_note.offset = offset
                new_note.storedInstrument = instrument.Piano()
                output_notes.append(new_note)
            # increase offset each iteration so that notes do not stack
            offset += 0.5

        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp='{}.mid'.format(filename))

    @staticmethod
    def to_categorical(y, num_classes):
        """ 1-hot encodes a tensor """
        return np.eye(num_classes, dtype='float32')[y]
