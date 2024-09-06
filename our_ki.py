from pathlib import Path
from typing import Optional, Tuple, Union
from pydub.audio_segment import AUDIO_FILE_EXT_ALIASES
import torch
from torch.functional import Tensor
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset
import torchaudio
import sys

import matplotlib.pyplot as plt
import IPython.display as ipd

from tqdm import tqdm

from pydub import AudioSegment
from torchaudio.datasets import SPEECHCOMMANDS
from torchaudio.datasets.speechcommands import _load_list, _load_waveform, _get_speechcommands_metadata
import os

AUDIO_FILE_ENDINGS = (".wav", ".mp3")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)



class AudioData(Dataset):
    def __init__(
        self,
        subset: str,
        root: Union[str, Path] = ".",
        subfolder: str = "data",
    ) -> None:

        # Get string representation of 'root' in case Path object is passed
        root = os.fspath(root)
        self.archive = os.path.join(root, subfolder)

        self.path = os.path.join(self.archive, subset)

        if not os.path.exists(self.path):
            raise RuntimeError(
                f"The path {self.path} doesn't exist. "
                "Please make sure no typos have been done"
                )

        self.files = [os.path.join(self.path, f) for f in os.listdir(self.path) if f.endswith(AUDIO_FILE_ENDINGS)]
        self.temp_files = []
        fs = []
        for f in self.files:
            if f.endswith(".mp3"):
                sound = AudioSegment.from_mp3(f)
                nf = f[:-4] + ".wav"

                sound.export(nf, format="wav")
                fs.append(nf)
                self.temp_files.append(nf)
            else:
                fs.append(f)
        self.files = sorted(fs)


    def __getitem__(self, n: int) -> Tuple[Tensor, int, int, int, int]:
        metadata = torchaudio.info(self.files[n])
        waveform = _load_waveform(self.archive, self.files[n], 0)
        return (waveform, metadata.sample_rate, metadata.num_channels, metadata.num_frames, metadata.bits_per_sample)

    def __len__(self) -> int:
        return len(self.files)

# Create training and testing split of the data. We do not use validation in this tutorial.
train_set = AudioData("training")  # type: ignore
test_set = AudioData("test")
validation_set = AudioData("validation")

waveform, sample_rate, label, speaker_id, utterance_number = validation_set[0]


# print("Shape of waveform: {}".format(waveform.size()))
# print("Sample rate of waveform: {}".format(sample_rate))
#
# plt.plot(waveform.t().numpy())
