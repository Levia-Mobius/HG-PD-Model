import numpy as np
import torch


class AugmentLoader():
    def __init__(self, data, batch_size, aug_num, shuffle=False):
        self.data = data
        self.batch_size = batch_size
        self.aug_num = aug_num
        self.shuffle = shuffle
    
    def __iter__(self):
        allocated_batch = AllocateBatch(self.data)
        batches = allocated_batch.batch_allocate(self.batch_size)
        return _Iter(self, batches, self.batch_size, self.aug_num)
    
    def noise_augment(self, batch, aug_num, repre_dim):
        '''Data augmentation via Standard Normal Distribution'''
        aug_list = []
        for row in batch:
            repeat_data = row.repeat(aug_num,1)
            aug_list.append(repeat_data)
        aug_data = torch.cat(aug_list,dim=0)
        zero_idx = list(range(0,len(aug_data),aug_num))
        data_noise = torch.randn(len(aug_data),repre_dim)
        data_noise[zero_idx] = 0
        aug_data = torch.add(aug_data, data_noise)
        return aug_data

class _Iter:
    def __init__(self, loader, data, batch_size, aug_num):
        self.data = data
        self.loader = loader
        self.batch_size = batch_size
        self.aug_num = aug_num
        self.current_batch = 0
        self.repre_dim = self.data[self.current_batch].shape[1]

    def __iter__(self):
        return self

    def __next__(self):
        '''
        Check whether all batches have been processed.
        True: return StopIteraction
        False: call noise_augment for each batch and generate pseudo labels (aug_idx)
        '''
        if self.current_batch >= len(self.data):
            raise StopIteration

        batch = self.data[self.current_batch]
        self.current_batch += 1

        aug_batch = self.loader.noise_augment(batch, self.aug_num, self.repre_dim)
        aug_idx = torch.from_numpy(np.arange(0, len(aug_batch) // self.aug_num).repeat(self.aug_num))


        return (aug_batch, aug_idx)

class AllocateBatch():
    def __init__(self, data):
        self.data = data
        self.num_sample = self.data.shape[0]
        
    def batch_allocate(self, batch_size):
        shuffle_idx = torch.randperm(self.num_sample)
        shuffle_data = self.data[shuffle_idx]
        batch_list = [shuffle_data[i:(i + batch_size),:] for i in range(0, self.num_sample, batch_size)]
        return batch_list