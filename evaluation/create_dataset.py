# create a method that opens fine_tuning/technova_train.jsonl and creates a dataset
import json
def create_dataset(file_path='fine_tuning/technova_test.jsonl'):
    dataset = []
    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            messages = data.get('messages', [])
            inp = messages[1]["content"]
            outp = messages[2]["content"]
            dataset.append({"inputs_1": inp, "outputs_1": outp})
    # save dataset
    with open('evaluation/dataset.jsonl', 'w') as f:
        for item in dataset:
            f.write(json.dumps(item) + '\n')

create_dataset()