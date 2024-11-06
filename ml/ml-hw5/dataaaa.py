import torchtext
from torchtext import data
import torch

EMB_SIZE = 200
PAD = '<pad>'
START = '<s>'
END = '</s>'

def get_dataset(use_pretrained=True):
    TEXT = data.Field(pad_token=PAD)

    train_data, dev_data, test_data = data.TabularDataset.splits(
        path='./',
        train='bobsue.seq2seq.train.tsv',
        validation='bobsue.seq2seq.dev.tsv',
        test='bobsue.seq2seq.test.tsv',
        format='tsv', fields=[('sent_1', TEXT), ('sent_2', TEXT)],
    )

    TEXT.build_vocab(train_data, dev_data, test_data)

    if use_pretrained:
        TEXT.vocab.load_vectors('glove.6B.200d')
    else:
        random_emb = [torch.rand(EMB_SIZE) / 5.0 - 0.1 for _ in range(len(TEXT.vocab))]
        TEXT.vocab.set_vectors(TEXT.vocab.stoi, random_emb, EMB_SIZE)

    return train_data, dev_data, test_data, TEXT

def get_iterators(train_bs=32, test_bs=1, use_pretrained=True):
    train_data, dev_data, test_data, TEXT = get_dataset(use_pretrained)

    train_iter, dev_iter, test_iter = data.BucketIterator.splits(
        (train_data, dev_data, test_data), sort=False,
        batch_sizes=(train_bs, test_bs, test_bs),
    )

    return train_iter, dev_iter, test_iter, TEXT

