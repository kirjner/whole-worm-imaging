import numpy as np
import nd2
from scipy.ndimage import gaussian_filter
from tqdm import tqdm
import os
import h5py
import argparse

def dog_filter_2d(im, sigma1, sigma2):
    """Apply a difference of Gaussians filter"""
    im1 = gaussian_filter(im.astype(np.float32), sigma1)
    im2 = gaussian_filter(im.astype(np.float32), sigma2)
    return im1 - im2

def process_nd2_to_h5(args):
    # Load the ND2 file
    worm_array = nd2.imread(args.input_path)

    # assert that the 

    # Crop the array
    array = worm_array[:, :, args.y_min:args.y_max, args.x_min:args.x_max]

    # Set up dimensions
    D = args.fpv
    num_frames = array.shape[0] - args.start_idx
    T = num_frames // args.fpv
    C = array.shape[1]
    H = array.shape[2]
    W = array.shape[3]

    # Prepare the array
    extra_frames = num_frames % args.fpv
    if extra_frames > 0:
        tmp_arr = array[args.start_idx:-extra_frames]
    else:
        tmp_arr = array[args.start_idx:]

    # Reshape and transpose the array
    tmp_arr = tmp_arr.reshape(T, D, C, H, W).transpose(0, 2, 1, 3, 4)
    # Align by flipping every other frame along the depth dimension
    tmp_arr[1::2] = np.flip(tmp_arr[1::2], axis=2)
    aligned_array = tmp_arr

    print(f"Aligned Array Shape: {aligned_array.shape} (T x C x D x H x W)")

    # Apply DoG filter
    filtered_array = np.zeros_like(aligned_array, dtype=np.float32)
    total_iterations = T * C * D

    with tqdm(total=total_iterations, desc="Applying DoG filter") as pbar:
        for t in range(T):
            for c in range(C):
                for d in range(D):
                    filtered_array[t, c, d] = dog_filter_2d(aligned_array[t, c, d], args.sig1, args.sig2)
                    pbar.update(1)

    # Normalize and scale the filtered array
    filtered_array -= np.min(filtered_array)
    filtered_array /= np.max(filtered_array)
    filtered_array *= 255

    # Convert to int8
    filtered_array = np.clip(filtered_array, 0, 255).astype(np.int8)

    # Ensure the output directory exists
    os.makedirs(args.output_path, exist_ok=True)

    # Save to HDF5 file
    with h5py.File(os.path.join(args.output_path, args.filename+".h5"), 'w') as h5:
        for i in range(T):
            print(f"Saving time point {i}")
            dset = h5.create_dataset(f"{i}/frame", (C, W, H, D), dtype="i2", compression="gzip")
            dset[...] = np.transpose(filtered_array[i], (0, 2, 3, 1))  # Reorder dimensions to (C, W, H, D)
        
        # Set metadata attributes
        h5.attrs["name"] = args.filename
        h5.attrs["C"] = C
        h5.attrs["W"] = W
        h5.attrs["H"] = H
        h5.attrs["D"] = D
        h5.attrs["T"] = T
        h5.attrs["N_neurons"] = args.n_neurons

    print(f"Finished saving the filtered array to HDF5 file: {args.filename}.h5")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert ND2 files to H5 format with preprocessing.")
    parser.add_argument("input_path", help="Path to input ND2 file")
    parser.add_argument("output_path", help="Path to output directory for H5 file")
    parser.add_argument("filename", help="Name of output H5 file (without extension)")
    parser.add_argument("--y_min", type=int, default=200, help="Y-axis minimum for cropping")
    parser.add_argument("--y_max", type=int, default=750, help="Y-axis maximum for cropping")
    parser.add_argument("--x_min", type=int, default=300, help="X-axis minimum for cropping")
    parser.add_argument("--x_max", type=int, default=850, help="X-axis maximum for cropping")
    parser.add_argument("--start_idx", type=int, default=20, help="Starting index for processing")
    parser.add_argument("--fpv", type=int, default=40, help="Frames per volume")
    parser.add_argument("--sig1", type=float, default=0.5, help="Sigma 1 for DoG filter")
    parser.add_argument("--sig2", type=float, default=4, help="Sigma 2 for DoG filter")
    parser.add_argument("--n_neurons", type=int, default=20, help="Number of neurons")

    args = parser.parse_args()
    process_nd2_to_h5(args)