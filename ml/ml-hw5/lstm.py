import torch
import torch.nn as nn
from dataaa import EMB_SIZE, PAD, START, END
import random

class LSTMModel(nn.Module):
    def __init__(self, hid_size, TEXT):
        super(LSTMModel, self).__init__()
        self.hid_size = hid_size
        self.TEXT = TEXT
        self.vocab_size = len(self.TEXT.vocab)
        self.embed = nn.Embedding(self.vocab_size, EMB_SIZE)
        self.embed.weight.data.copy_(TEXT.vocab.vectors)
        self.encoder = nn.LSTM(EMB_SIZE, self.hid_size)
        self.decoder = nn.LSTM(EMB_SIZE, self.hid_size)
        self.fc_out = nn.Linear(self.hid_size, self.vocab_size)
    
    def init_hidden(self, batch_size):
        return torch.zeros([batch_size, self.hid_size]).unsqueeze(0)

    def forward(self, src, tgt, teach_force_rate=0.1):
        batch_size = src.shape[1]
        embedded = self.embed(src)
        h, c = self.init_hidden(batch_size), self.init_hidden(batch_size)
        _, (h, c) = self.encoder(embedded, (h, c))

        outputs = []
        max_len = tgt.shape[0] if tgt is not None else 100  

        for t in range(max_len):
            if t == 0 or tgt is None:
                x = torch.tensor([[self.TEXT.vocab.stoi[START]]]).to(src.device)
                x = self.embed(x.long())
            else:
                if random.random() > teach_force_rate:
                    pred = out.argmax(2)
                    x = self.embed(pred)
                else:
                    x = self.embed(tgt[t].unsqueeze(0))
            
            dec_out, (h, c) = self.decoder(x, (h, c))
            out = self.fc_out(dec_out)
            outputs.append(out)

            if tgt is None and pred.item() == self.TEXT.vocab.stoi[END]:
                break

        outputs = torch.cat(outputs).permute(1, 2, 0)
        
        return outputs
