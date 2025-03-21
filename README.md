# Hertzsprung-Russell (HR) Diagram

This repository contains tools for generating [HR diagrams](https://en.wikipedia.org/wiki/Hertzsprung%E2%80%93Russell_diagram) and downloading star data from the [Gaia ESA Archive](https://gea.esac.esa.int/archive/).

## `hr.py`

This program generates an HR diagram scatterplot. It takes one arg: a directory containing csv files.

## `hr.py` Example Output

![An HR Diagram](./HR_diagram.png)

## `download_gaia_source.py`

This program downloads `.csv.gz` archives from `gda2/` under the Gaia ESA Archvie to a specified directory.

Args:

- A directory to contain the download files. A directory will be created if the it does not already exist.
- An optional start and stop, specifying the start and stop index of `.csv.gz` files to download. Note: each csv contains multiple millions of rows.
