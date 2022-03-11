import argparse
import json
import fasttext

def get_model_parameters(model):
    train_parameters = ['lr', 'dim', 'ws', 'epoch', 'minCount', 'minCountLabel',
                        'minn', 'maxn', 'neg', 'wordNgrams', 'bucket', 'thread',
                        'lrUpdateRate', 't', 'label', 'verbose', 'pretrainedVectors',
                         'seed']

    args_getter = model.f.getArgs()

    parameters = {}
    for param in train_parameters:
        attr = getattr(args_getter, param)
        if param == 'loss':
            attr = attr.name
        parameters[param] = attr

    return parameters


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='fasttext autotune test.')
    general = parser.add_argument_group("general")
    general.add_argument("--input_train", default='/workspace/datasets/100/train.data',  help="The directory containing training data")
    general.add_argument("--input_test", default='/workspace/datasets/100/test.data',  help="The directory containing test data")
    general.add_argument("--output_params", default='/workspace/datasets/100/params.file',  help="The directory containing training data")
    general.add_argument("--metric", default='f1',  help="metric objective")
    general.add_argument("--output_model", default="/workspace/datasets/100/autotune_model", help="the file to output to")

    args = parser.parse_args()

    input_train_path = args.input_train
    output_test_path = args.input_test
    metric = args.metric
    output_parameters_path = args.output_params
    output_model_path = args.output_model

    model = fasttext.train_supervised(
            input=input_train_path,
            autotuneValidationFile=output_test_path,
            autotuneMetric=metric)

    n, p, r = model.test(output_test_path)
    print(json.dumps(
        {'n': n, 'precision': p, 'recall': r}))


    with open(output_parameters_path, 'w') as f:
        json.dump(get_model_parameters(model), f)

    model.save_model(output_model_path)  