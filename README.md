# table-tennis-eventTracker

[![python-image]][python-url]
[![pytorch-image]][pytorch-url]

The implementation for the paper _**"TTNet: Real-time temporal and spatial video analysis of table tennis"**_ <br>
An introduction of the project could be found 

---

## Demo
![docs1_edjz0BYt-2_3NmfpC03xug](./docs/1_edjz0BYt-2_3NmfpC03xug.gif)

![demo](./docs/demo.gif)

```shell script
pip install -U -r requirement.txt

$ sudo apt-get install libturbojpeg
...
$ pip install PyTurboJPEG
...
```

## How to Run

- Single Machine, Single GPU
python main.py --gpu_idx 0

- Multi-Processing Distributed Data Parallel Training
python main.py --gpu_idx 0 --no_local --no_seg --no_event
python main.py --dist-url 'tcp://127.0.0.1:29500' --dist-backend 'nccl'

- Multiprocessing-distributed --world-size 1 --rank 0
python main.py --dist-url 'tcp://IP_OF_NODE1:FREEPORT' --dist-backend 'nccl' --multiprocessing-distributed --world-size 2 --rank 0


## Evaluation

Set thresholds for segmentation and event spotting before running:   ./test_3rd_phase.sh
