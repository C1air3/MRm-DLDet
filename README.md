# MRm-DLDet

MRm-DLDet is a memory-resident malware detection framework, MRm-DLDet first deduplicates memory data, then converts them to high-resolution RGB images, followed by a neural network (ResNet 18+GRU+Attention) to fully extract high-dimensional features from memory dump files and classify them.

## Installation

### Dependencies

#### General

Please install the following tools:

- [VMware Workstation](https://www.vmware.com/cn.html) (version 16.0.0)
- [python](https://www.python.org/) (version 3.7)

## Usage

MRm-DLDet runs without any special installation. However, you have to ensure several things before first usage.

If you would like to create your own models, then you need to setup virtual machines (VMs). Install at least one Windows 10 VM with VMware Workstation. Configure and harden VM as needed. Take a snapshot of the VM, MRm-DLDet will utilize this snapshot as clean base to start samples.

### Memory generation (VMware_Control.py)

After placing the malicious and benign samples to be detected in the virtual machine, run this script to roll back the virtual machine to the 'clean' state, and after running the malicious or benign program, this script takes a snapshot of the virtual machine to obtain a memory dump of the malicious samples as they run.

### Memory dumps to image (binary2RGBimg.py)

This script covert one dump file to an RGB image.

### Cutting Ultra-High Resolution RGB image (cut_photo.py)

Cut Ultra-High Resolution RGB image with non-overlapping sliding window.
