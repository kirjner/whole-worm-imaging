# Whole-Worm Imaging

This repository contains tools and scripts for processing whole-worm imaging data, particularly for converting `.nd2` files from Nikon microscopes into `.h5` and `.nwb` formats.

## Data Location

The primary dataset is located on Engaging at:

```
/orcd/data/edboyden/002/Konstantinos/whole-worm-imaging
```

Within this directory, the `worm_data` folder contains subfolders:

- `nd2`: Raw data from the Nikon microscope.
- `h5`: Converted `.h5` files.

For assistance with the `nd2_to_h5.py` script, refer to its source code:

- [nd2_to_h5.py](https://github.com/kirjner/whole-worm-imaging/blob/main/nd2_to_h5.py)


## Environment Setup

To set up the environment for processing the data, follow these steps:

1. **Allocate Resources on Engaging**:

   ```bash
   salloc -t 2:00:00 -p ou_bcs_low --mem 64
   ```

2. **Load Miniforge Module**:

   ```bash
   module load miniforge
   ```

3. **Activate the `worm-env` Environment**:

   ```bash
   mamba activate worm-env
   ```

4. **Start Jupyter Lab**:

   ```bash
   jupyter-lab --ip 0.0.0.0 --no-browser --port 8889
   ```

   Copy the link provided by Jupyter Lab into VSCode or your preferred editor to connect.

5. **Install NWBElegans Package**:

   Ensure that the `worm-env` environment is active, then run:

   ```bash
   cd whole-worm-imaging/NWBelegans
   pip install -e .
   ```

## Data Processing

To process `.nd2` files into `.h5` format, use the provided script `nd2_to_h5.py`. This script applies preprocessing steps, including cropping, filtering, and normalization.

To convert `.nd2` files to `.nwb` format, additional scripts or tools may be required.

## Symlinking Data

To create a symbolic link to the data directory within the repository, run:

```bash
ln -s /orcd/data/edboyden/002/Konstantinos/whole-worm-imaging/worm_data ~/whole-worm-imaging/data
```

## Additional Resources

For more information and updates, visit the [whole-worm-imaging repository](https://github.com/kirjner/whole-worm-imaging).


