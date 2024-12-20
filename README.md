# **3DBM-Plus**
Includes optimizations for improved performance on 3DBM

## Key Update(s):
- **New Feature(s)**:
     - Output Format(s): Added support for <ins>**CityJSON**</ins>, **CSV** and  <ins>**GPKG**</ins> (2D/3D)
     - New Parameter(s):
          -   -c / --output-cityjson
          -   -o / --output-csv
          -   -g / --output-gpkg
          -   -l / --filter-lod
          -   -f / --filter-building-id
          -   -i / --with-indices
          -   --precision
          -   ~~[--without-indices]~~ (removed)
     - Additional Semantic Surface Attribute(s): Now includes **area**, **azimuth**, **inclination** and **roof type** (sloped or flat)
- **Performance Improvement(s)**: Enhanced speed and efficiency throughout the tool
- **Dependency Change(s)**:
     - Replaced the *PyMesh* library with <ins>***Trimesh***</ins> for simplified installation and setup, as PyMesh has not been maintained for years, making it challenging to install
     - Updated compatibility with the latest versions of ***PyVista*** (0.44.1) and ***shapely*** (2.0.6)
     - This fork has been tested and is compatible with Python >= 3.10

## Usage Recommendation:
For optimal performance, I highly recommend using **multi-threading** with the **-j** argument, which significantly speeds up processing.

With these updates, 3DBM is now easier to use and fully operational!

## Installation
### Using `pip`
To install all dependencies, run the following command:
```
pip install -r requirements.txt
```
### Using `conda`
To create the environment from the environment.yml file, run:
```
conda env create --file=environment.yml
```
___
# 3DBM

<p align="center">
	<img src="./3dbm.png" width="200">
</p>

3D Building Metrics. Elevating geometric analysis for urban morphology, solar potential, CFD etc to the next level 😉


## Wat is het?

A cool script that computes a lot metrics from 3D geometries (mostly intended for buildings).

The following metrics are computed:

| Type | Metrics |
| --- | --- |
| Geometric Properties | Number of vertices, Number of surfaces, Number of vertices by semantic type (i.e. ground, roof, wall), Number of surfaces by semantic type (i.e. ground, roof, wall), Min/Max/Range/Mean/Median/Std/Mode height |
| Derived Properties | Footprint perimeter, Volume, Volume of convex hull, Volume of Object-Oriented Bounding Box, Volume of Axis-Oriented Bounding Box, Volume of voxelised building, Length and width of the Object-Oriented Bounding Box, Surface area, Surface area by semantic surface, Horizontal elongation, Min/Max vertical elongation, Form factor |
| Spatial distribution | Shared walls, Nearest neighbour |
| Shape indices | Circularity/Hemisphericality<sup>\*</sup>, Convexity 2D/3D<sup>\*</sup>, Fractality 2D/3D<sup>\*</sup>, Rectangularity/Cuboidness<sup>\*</sup>, Squareness/Cubeness<sup>\*</sup>, Cohesion 2D/3D<sup>\*</sup>, Proximity 2D/3D<sup>+</sup>, Exchange 2D/3D<sup>+</sup>, Spin 2D/3D<sup>+</sup>, Perimeter/Circumference<sup>\*</sup>, Depth 2D/3D<sup>+</sup>, Girth 2D/3D<sup>+</sup>, Dispersion 2D/3D<sup>x</sup>, Range 2D/3D<sup>\*</sup>, Equivalent Rectangular/Cuboid<sup>\*</sup>, Roughness<sup>x</sup> |

- <sup>\*</sup> formula-based index, size-independent by definition
- <sup>+</sup> index based on interior grid points (discretised), normalised
- <sup>x</sup> index based on surface grid points (discretised), normalised

## Omg, how amazing! Any issues?

Yeah:
- It works with only `MultiSurface` and `Solid` (the latter, only for the first shell)
- It only parses the first geometry
- Expects semantic surfaces

## How?

Running it, saving it, and including a [val3dity](https://github.com/tudelft3d/val3dity) report:

```
python cityStats.py [file_path] -o [output.csv] [-v val3dity_report.json]
```

Default is single-threaded, define the number of threads with:

```
python cityStats.py [file_path] -j [number]
```

Visualising a specific building, which can help with troubleshooting:

```
python cityStats.py [file_path] -p -f [unique_id]
```

Running multiple files in a folder and checking with [val3dity](https://github.com/tudelft3d/val3dity) (make sure you have val3dity installed):

```
for i in *.json; do val3dity $i --report "${i%.json}_v3.json"; python cityStats.py $i -o "${i%.json}.csv" -v "${i%.json}_v3.json"; done
```

## Can I visualise a model?

Tuurlijk! Just:

```
python cityPlot.py [file_path]
```

## Tutorial please!

1) Download or `git clone` this repository.

2) Install all dependencies: `pip install -r requirements.txt`.

3) Download a tile from 3D BAG: `wget --header='Accept-Encoding: gzip' https://data.3dbag.nl/cityjson/v210908_fd2cee53/3dbag_v210908_fd2cee53_5910.json`

4) Run the stats on the data: `python cityStats.py 3dbag_v210908_fd2cee53_5910.json -o 5910.csv`

5) The resutling file `5910.csv` contains all metrics computed for this tile.

You may also run this with a [val3dity](http://geovalidation.bk.tudelft.nl/val3dity/) report. You may download the val3dity report as a json file from the aforementioned website. Assuming the report's filename is `report.json` you can run:

```
python cityStats.py 3dbag_v210908_fd2cee53_5910.json -v report.json -o 5910.csv
```

Then the result will contain more info related to the validation of geometries.

## If you use 3DBM in a scientific context, please cite this article:

Anna Labetski, Stelios Vitalis, Filip Biljecki, Ken Arroyo Ohori & Jantien Stoter (2023): 3D building metrics for urban morphology. International Journal of Geographical Information Science, 37(1): 36-67. DOI: 10.1080/13658816.2022.2103818 

[Article available here.](https://doi.org/10.1080/13658816.2022.2103818)

```
@article{Labetski2023,
	Author = {Anna Labetski and Stelios Vitalis and Filip Biljecki and Ken {Arroyo Ohori} and Jantien Stoter},
	Title = {{3D} building metrics for urban morphology},
	Journal = {International Journal of Geographical Information Science},
	Volume = {37},
	Number = {1},
	Pages = {36-67},
	Year  = {2023},
	Publisher = {Taylor & Francis},
	Doi = {10.1080/13658816.2022.2103818}
```
