import numpy as np
from torch_geometric.data import HeteroData
import torch
from torch_geometric.nn import HeteroConv, GCNConv, SAGEConv
import torch.nn.functional as F

class MCR2_HGPD(torch.nn.Module):
    def __init__(self, node_num, feature_dim, cate_dim, hidden_dim, num_hop):
        super().__init__()

        self.embed_dim = feature_dim - 5 + 5 * cate_dim
        
        self.embedding = torch.nn.Embedding(node_num, self.embed_dim)

        self.e0 = torch.nn.Embedding(2, cate_dim)
        self.e3 = torch.nn.Embedding(2, cate_dim)
        self.e7 = torch.nn.Embedding(2, cate_dim)
        self.e8 = torch.nn.Embedding(2, cate_dim)
        self.e9 = torch.nn.Embedding(2, cate_dim)
        
        self.convs = torch.nn.ModuleList()
        for _ in range(num_hop):
            conv = HeteroConv({
                ('user','interact','user'): GCNConv(-1, hidden_dim, add_self_loops = False),
                ('user','post','comment'): SAGEConv((-1, -1), hidden_dim),
                ('comment','from','user'): SAGEConv((-1, -1), hidden_dim)
            }, aggr='sum')
            self.convs.append(conv)

        self.norm = torch.nn.BatchNorm1d(hidden_dim)
    
    def forward(self, no_Nidx, u_feature, heteData):
        
        node_prof = self.embedding(no_Nidx)
        
        em0 = self.e0(u_feature[:,0].long())
        em3 = self.e3(u_feature[:,3].long())
        em7 = self.e7(u_feature[:,7].long())
        em8 = self.e8(u_feature[:,8].long())
        em9 = self.e9(u_feature[:,9].long())
        newF = torch.cat((em0, u_feature[:,1:3], em3, u_feature[:,4:7],em7,em8,em9), dim=1)
        x_list = []
        userF = torch.cat((newF, node_prof), dim=0)
        heteData['user'].x = userF
        for conv in self.convs:
            x_dict = conv(heteData.x_dict, heteData.edge_index_dict)
            x_dict = {key: F.leaky_relu(x, negative_slope=0.3) for key, x in x_dict.items()}
            x_list.append(x_dict)
        node_user = x_list[0]['user']+x_list[1]['user']
        norm_user = self.norm(node_user)
        return norm_user