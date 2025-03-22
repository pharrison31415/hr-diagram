import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def generate_HR(csv_files):
    # Concat the datasets
    dfs = []
    for filename in csv_files:
        data = pd.read_csv(filename)
        dfs.append(data)
    df = pd.concat(dfs, ignore_index=True)

    # Drop rows that are missing columns of interest
    df = df.dropna(subset=["teff_val",
                           "phot_g_mean_mag",
                           "parallax",
                           "bp_rp",
                           ])

    # Drop rows that have non-positive parallax
    df = df[df["parallax"] > 0]

    # Columns of interest
    teff = df["teff_val"]               # Temperature in Kelvin
    app_mag = df["phot_g_mean_mag"]     # Apparent G-band magnitude
    parallax = df["parallax"]           # Parallax in milliarcseconds
    bp_rp_color = df["bp_rp"]           # BP-RP color index

    # Distance in parsecs
    distance = 1000 / parallax

    # Absolute magnitude
    abs_mag = app_mag - 5 * (np.log10(distance) - 1)

    # Make the plot look pretty
    plt.gca().invert_yaxis()
    plt.gca().invert_xaxis()
    plt.xlabel("TEFF")
    plt.ylabel("Absolute Magnitude")
    plt.title("Hertzsprung-Russell (HR) Diagram")

    scatter = plt.scatter(teff, abs_mag, c=bp_rp_color, s=1, alpha=0.1)

    cbar = plt.colorbar(scatter)
    cbar.set_label('BP-RP Color Index')

    plt.show()


def main():
    # Check arg count
    if len(sys.argv) != 2:
        print("data directory path is a required arg", file=sys.stderr)
        sys.exit(1)

    data_directory = sys.argv[1]

    # List csv filenames; convert to paths
    csv_filenames = [f for f in os.listdir(
        data_directory) if f.endswith(".csv")]
    csv_paths = [os.path.join(data_directory, filename)
                 for filename in csv_filenames]

    # Generate HR diagram
    generate_HR(csv_paths)


if __name__ == "__main__":
    main()
