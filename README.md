![cloth with a marked point](http://i.imgur.com/JK6B7p5.png)

![3d cloth hanging](http://i.imgur.com/1kNY4iY.png)

# Description

These scripts simulate a cloth being held from different points.

The `gen_points.csv` script will generate a list of evenly spaced points 
in a 3d mesh to a file called `points.csv`.

# Usage

## 1. Generate a list of evenly spaced points

Run in background mode to quickly get results

    $ blender --background --python gen_points.py <file.3ds>

Or, run with blender open to see which points were chosen.
In Blender, change to Weight Paint mode to see these points.

    $ blender --python gen_points.py <file.3ds>

## 2. Simulate a cloth being held from these points

Run the following

    $ cd cloth_simulation
    $ python3 simulate_all.py ../<file>.3d ../points.csv

Or, equivalently

    $ cd cloth_simulation
    $ cp ../<file>.3ds res
    $ cp ../points.csv res
    $ python run.py

# Expected Output

The `gen_points.csv` script generates a `points.csv` file to be used.

The `run.py` script starts the simulation on these points, and 
saves each generated mesh to an output folder.