import os
import pandas as pd
import numpy as np
import torch
import csv

'''
file_name: 'xxx.csv'
folder: folder name ('xxx.csv' will be saved in this folder)
'''

def save_step_DC(file_name, folder, epoch, step, loss, discrim_empi, compress_empi, discrim_theo, compress_theo):
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filename = os.path.join(folder,file_name)
    with open(filename, mode ='a', newline='') as file:
        writer = csv.writer(file)
        if step == 0 and epoch == 0:
            writer.writerow(['Epoch', 'Step', 'Loss', 
                             'Discrim_empi', 'Compress_empi', 
                             'Discrim_theo', 'Compress_theo'])
        
        writer.writerow([epoch, step, loss, discrim_empi, compress_empi, discrim_theo, compress_theo])
        


def save_parameters_to_csv(file_name, folder, epoch, loss_s, learning_rate):
    
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = os.path.join(folder, file_name)
    with open(filename, mode ='a', newline='') as file:
        writer = csv.writer(file)
        if epoch == 0:
            writer.writerow(['Epoch', 'Loss', 'Learning_rate'])
        writer.writerow([epoch, loss_s, learning_rate])

        
def save_model_state(file_name, folder, epoch, model, optimizer):
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = os.path.join(folder, file_name)
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
    }
    torch.save(checkpoint, filename)