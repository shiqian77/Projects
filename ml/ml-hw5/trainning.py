import torch
from collections import Counter
from dataaa import get_iterators, PAD
from lstm import LSTMModel
import time
from tqdm import tqdm

HID_SIZE = 64
LR = 0.5
EPOCHS = 12

def calc_acc(output, target, pad_idx=0):
    _, preds = output.max(1)
    correct = 0
    total = 0
    for i in range(preds.shape[0]):
        j = 0
        while j < preds.shape[1]:
            if target[i, j] != pad_idx:
                total += 1
                if target[i, j] == preds[i, j]:
                    correct += 1
            j += 1
    return correct / total

def train(data_iter, model, optimizer, loss_func, pad_idx=0):
    model.train()
    epoch_losses = []
    epoch_accs = []
    for batch in tqdm(data_iter):
        optimizer.zero_grad()
        output = model(batch.sent_1, batch.sent_2)
        loss = loss_func(output, batch.sent_2[1:])
        acc = calc_acc(output, batch.sent_2[1:], pad_idx)
        loss.backward()
        optimizer.step()
        epoch_losses.append(loss.item())
        epoch_accs.append(acc)
    avg_loss = sum(epoch_losses) / len(epoch_losses)
    avg_acc = sum(epoch_accs) / len(epoch_accs)
    return avg_loss, avg_acc

def pad_output(output, target, pad_idx):
    output = output[:min(output.shape[0], target.shape[0]), :, :]
    new_out = torch.full([target.shape[0], output.shape[1], output.shape[2]], pad_idx)
    new_out[:output.shape[0], :, :] = output
    return new_out

def eval(data_iter, model, loss_func, pad_idx=0):
    model.eval()
    epoch_losses = []
    epoch_accs = []
    with torch.no_grad():
        for batch in tqdm(data_iter):
            output = model(batch.sent_1, None)
            output = pad_output(output, batch.sent_2[1:], pad_idx)
            output = output.float()
            target = batch.sent_2[1:].long()
            loss = loss_func(output, target)
            acc = calc_acc(output, target, pad_idx)
            epoch_losses.append(loss.item())
            epoch_accs.append(acc)
    avg_loss = sum(epoch_losses) / len(epoch_losses)
    avg_acc = sum(epoch_accs) / len(epoch_accs)
    return avg_loss, avg_acc

def sort_words_by_accuracy(data_iter, model, pad_idx=0):
    model.eval()
    correct_counts = Counter()
    total_counts = Counter()
    with torch.no_grad():
        for batch in tqdm(data_iter):
            output = model(batch.sent_1, batch.sent_2)
            output = output.float()
            target = batch.sent_2[1:].long()
            pred = output.argmax(dim=1)
            correct = pred.eq(target).float()
            i = 0
            while i < target.size(0):
                t = target[i]
                c = correct[i]
                if t != pad_idx:
                    total_counts[t.item()] += 1
                    if c.item() == 1:
                        correct_counts[t.item()] += 1
                    else:
                        correct_counts[t.item()] -= 1
                i += 1
    word_accs = {word: correct_counts[word] / total_counts[word] for word in correct_counts.keys()}
    sorted_words = sorted(word_accs.items(), key=lambda x: x[1], reverse=True)
    return sorted_words

def predict_sentences(data_iter, model, vocab, file_name="ps.txt", pad_idx=0):
    def idx_to_words(indices, vocab):
        return [vocab.itos[idx] for idx in indices]

    model.eval()
    with torch.no_grad(), open(file_name, 'w', encoding='utf-8') as f:
        for batch in tqdm(data_iter):
            output = model(batch.sent_1, batch.sent_2)
            output = output.float()
            target = batch.sent_2[1:].long()
            pred = output.argmax(dim=1)

            sent_1_words = idx_to_words(batch.sent_1.view(-1).tolist(), vocab)
            target_words = idx_to_words(target.view(-1).tolist(), vocab)
            pred_words = idx_to_words(pred.view(-1).tolist(), vocab)

            f.write(f'<s>{' '.join(pred_words)}</s> {" ".join(tgt_words)}\n')
