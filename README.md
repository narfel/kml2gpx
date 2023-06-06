# kml2gpx

Simple command line script to convert KML file to GPX

## Description

> Convert KML file containing a path to a GPX file. It looks for a LineString and extracts the coordinates. If multiple paths are present the first one is used

## Installation

```sh
~$ git clone https://github.com/narfel/kml2gpx.git
~$ cd kml2gpx
~$ pip install kml2gpx .
```

Since it is just a simple script, you can also just grab the app.py file from the src folder and run it with "python app.py [input_file.kml]"

## Dependencies

None

## How to use

```sh
kml2gpx [input_file.kml]
```

### Windows

As "Open with" target:

>You can use it as "Open with" target by right clicking a kml file and providing the binary as path. When installed via pip the binary will be located usually in %APPDATA%\Python\Scripts\.

As a batch file:

>Create a file kml2gpx.bat with the content below and drag and simply drop the kml onto it:

```sh
@echo off
python "<path to script>\app.py" %*
pause
```

## License

Copyright (c) 2023 Narfel

Usage is provided under the MIT License. See [LICENSE](https://github.com/kml2gpx/blob/master/LICENSE) for the full details.
