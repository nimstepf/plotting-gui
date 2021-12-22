# plotting-gui

Short introduction/explanation will be added


## Install the requirements

### Using conda

```
conda create --name plotting-gui --file requirements.txt
```

### Using pip

```
pip install -r requirements.txt
```



## Running plotting-gui.py

```
python plotting-gui.py
```


## Using plotting-gui.py

explanation how to use the plotting-gui will be added



### Load and select files

With the _Open Folder_ button or _Menu>Open_, a directory containing raw data can be selected. The .csv files of all subfolders will be listed in the _Raw Data_ box. Selected files will be shown in the _Selected files_ box. 

With _Number of subplots_, the number of different plots can be chosen. Using drag and drop, selected files can be added to the different plots (boxes of _Subplots_). The order in the boxes defines the order in the resulting plot. 

Files can be deleted from the _Selected files_ and _Subplots_ boxes by double-clicking.

The title and common labels of the plot can be set in the _Set Labels_ box. 

### Menu bar

The following functions can be called from the menu bar or by shortcuts:
- Open: open a directory (similar to _Open Folder_ button)
- Update: updates plot (similar to _Update_ button)
- Restart: complete restart of the application
- Exit: close the application

As standard delimiter/separator, the comma "," is defined. In the _Delimiter_ menu, different delimiters can be selected. To avoid errors, the delimiter should be selected before loading the data. However, plotting files with different delimiters at once is not possible yet. If needed, the _Delimiter_ menu can be extended with further separators.

# TODO: Delimiter exception handling



