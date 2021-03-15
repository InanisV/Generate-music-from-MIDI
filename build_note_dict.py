import sys
from tools import Tools

""" Build and save note dictionarys """
# Get notes from midi files
dataset_name = sys.argv[1]
notes = Tools.get_notes("/data1/zhengdao/cs4347/datasets/" +
                        dataset_name + "/*.mid")

Tools.save_obj(notes, f'{dataset_name}_notes')

# Get the number of pitch names
n_vocab = len(set(notes))

# Convert notes into numerical input
note_to_int, int_to_note = Tools.get_note_dicts(notes)

Tools.save_obj(note_to_int, f'{dataset_name}_note2int')
Tools.save_obj(int_to_note, f'{dataset_name}_int2note')
