import math
import shutil
import struct
from collections import defaultdict
from functools import lru_cache
from pathlib import Path

import lmdb
import numpy as np
import torch.utils.data
from tqdm import tqdm


class CriteoSearchDataset(torch.utils.data.Dataset):
    """
    CRITEO SPONSORED SEARCH CONVERSION DATASET

    Data prepration:
        * Remove the infrequent features (appearing in less than threshold instances) and treat them as a single feature
        * Discretize numerical values by log2 transformation which is proposed by the winner of Criteo Competition

    :param dataset_path: criteo Criteo_Search.txt path.
    :param cache_path: lmdb cache path.
    :param rebuild_cache: If True, lmdb cache is refreshed.
    :param min_threshold: infrequent feature threshold.

    Reference:
        https://ailab.criteo.com/criteo-sponsored-search-conversion-log-dataset/
    """

    def __init__(self, dataset_path=None, cache_path='.criteo_search', rebuild_cache=False, min_threshold=5):
        self.NUM_FEATS = 20
        self.NUM_INT_FEATS = 2
        self.min_threshold = min_threshold
        self.defaults = None
        if rebuild_cache or not Path(cache_path).exists():
            shutil.rmtree(cache_path, ignore_errors=True)
            if dataset_path is None:
                raise ValueError('create cache: failed: dataset_path is None')
            self.__build_cache(dataset_path, cache_path)
        self.env = lmdb.open(cache_path, create=False, lock=False, readonly=True)
        with self.env.begin(write=False) as txn:
            self.length = txn.stat()['entries'] - 2 
            self.field_dims = np.frombuffer(txn.get(b'field_dims'), dtype=np.uint32)

    def __getitem__(self, index):
        with self.env.begin(write=False) as txn:
            np_array = np.frombuffer(
                txn.get(struct.pack('>I', index)), dtype=np.float32).astype(dtype=np.float32)
        x, y = np_array[1:], np_array[0]
        z = x[0:3]
        return x[3:].astype(dtype=np.int32), z, y
    
    def get_defaults(self):
        if self.defaults is None:
            with self.env.begin(write=False) as txn:
                defaults_key = b'defaults'
                defaults_data = txn.get(defaults_key)
                defaults = np.frombuffer(defaults_data, dtype=np.uint32)
        else:
            defaults = self.defaults
        return defaults
    
    def get_vocab(self):
        if self.defaults is None:
            with self.env.begin(write=False) as txn:
                defaults_key = b'defaults'
                defaults_data = txn.get(defaults_key)
                defaults = np.frombuffer(defaults_data, dtype=np.uint32)
                vocab = defaults.tolist()
        else:
            vocab = list(self.defaults.values())
        return vocab[2:]

    def __len__(self):
        return self.length

    def __build_cache(self, path, cache_path):
        feat_mapper, defaults = self.__get_feat_mapper(path)
        defaults_key = b'defaults'
        with lmdb.open(cache_path, map_size=int(1e11)) as env:
            try:
                with env.begin(write=True) as txn:
                    if defaults is not None:
                        txn.put(defaults_key, np.array(list(defaults.values()), dtype=np.uint32).tobytes())

                    field_dims = np.zeros(self.NUM_FEATS, dtype=np.uint32)
                    for i, fm in feat_mapper.items():
                        field_dims[i - 1] = len(fm) + 1
                    txn.put(b'field_dims', field_dims.tobytes())
                    for buffer in self.__yield_buffer(path, feat_mapper, defaults):
                        for key, value in buffer:
                            txn.put(key, value)

            except Exception as e:
                print(f"Error during LMDB write: {e}")

    def __get_feat_mapper(self, path):
        feat_cnts = defaultdict(lambda: defaultdict(int))
        with open(path) as f:
            f.readline()
            pbar = tqdm(f, mininterval=1, smoothing=0.1)
            pbar.set_description('Create criteo search dataset cache: counting features')
            for line in pbar:
                values = line.rstrip('\n').split('\t')
                if len(values) != self.NUM_FEATS + 1:
                    continue
                for i in range(1, self.NUM_INT_FEATS + 1):
                    feat_cnts[i][convert_numeric_feature(values[i])] += 1
                for i in range(self.NUM_INT_FEATS + 2, self.NUM_FEATS + 1):
                    feat_cnts[i][values[i]] += 1
        feat_mapper = {i: {feat for feat, c in cnt.items() if c >= self.min_threshold} for i, cnt in feat_cnts.items()}
        feat_mapper = {i: {feat: idx for idx, feat in enumerate(cnt)} for i, cnt in feat_mapper.items()}
        defaults = {i: len(cnt) for i, cnt in feat_mapper.items()}
        self.defaults = defaults
        return feat_mapper, defaults

    def __yield_buffer(self, path, feat_mapper, defaults, buffer_size=int(2e7)):
        item_idx = 0
        buffer = list()
        with open(path) as f:
            f.readline()
            pbar = tqdm(f, mininterval=1, smoothing=0.1)
            pbar.set_description('Create criteo search dataset cache: setup lmdb')
            for line in pbar:
                values = line.rstrip('\n').split('\t')
                if len(values) != self.NUM_FEATS + 1:
                    continue
                np_array = np.zeros(self.NUM_FEATS + 1, dtype=np.float32)
                np_array[0] = float(values[0])
                for i in range(1, self.NUM_INT_FEATS + 2):
                    np_array[i] = float(values[i])
                    
                for i in range(self.NUM_INT_FEATS + 2, self.NUM_FEATS + 1):
                    np_array[i] = feat_mapper[i].get(values[i], defaults[i])
                buffer.append((struct.pack('>I', item_idx), np_array.tobytes()))
                item_idx += 1
                if item_idx % buffer_size == 0:
                    yield buffer
                    buffer.clear()
            yield buffer


@lru_cache(maxsize=None)
def convert_numeric_feature(val: str):
    if val == '':
        return 'NULL'
    v = int(val)
    if v > 2:
        return str(int(math.log(v) ** 2))
    else:
        return str(v - 2)
