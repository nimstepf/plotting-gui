# plotting-gui

Short introduction/explanation will be added

## Installation

### Using conda

```
git clone https://github.com/nimstepf/plotting-gui.git
cd plotting-gui

conda env create -f environment.yml
conda activate plotting-gui
conda env list
```

### Using pip

```
git clone https://github.com/nimstepf/plotting-gui.git
cd plotting-gui

pip install -r requirements.txt
```

### Running plotting-gui.py

```
python plotting-gui.py
```


## User guide

### Load and select files

With the ```Open Folder``` button or ```Menu>Open```, a directory containing raw data can be selected. The .csv files of all subfolders will be listed in the ```Raw Data``` box. Selected files will be shown in the ```Selected files``` box. 

With ```Number of subplots```, the number of different plots can be chosen. Using drag and drop, selected files can be added to the different plots (boxes of ```Subplots```). The order in the boxes defines the order in the resulting plot. 

Files can be deleted from the ```Selected files``` and ```Subplots``` boxes by double-clicking.


### Personalize plot

The title and labels of the plot can be set in the ```Set Labels``` box. 

#### Navigationbar

![image](https://user-images.githubusercontent.com/91268311/147067514-5d5f0b6a-fdf7-499d-ae01-6d0501363b9d.png)

In the navigation bar, different predefined styles can be selected. The colorset of the ```default``` style is optimized for color-blind individuals according to _Bang Wong nature methods | VOL.8 NO.6 | JUNE 2011 | 441._ I would be thankful for some feedback about the most useful predefined styles, to simplify and shorten the list.

![image][Configure subplots] With ```Configure subplots``` the borders and spacing of the plots can be adjusted.

![image][Edit axis] With ```Edit axis, curve and image parameters``` each plot can be personalized individually. After selecting the axis (subplot), limits and scaling of the axes can be adapted. Furthermore, in the ```Curves``` register, the label and line style for each curve of the subplot can be choosen.  

![image][Save the figue] With ```Save the figure```the plot can be exported for example as vector graphic.

[Configure subplots]: https://user-images.githubusercontent.com/91268311/147072567-3e5ba31a-d0b6-4597-8a68-84435565bef1.png
[Edit axis]: https://user-images.githubusercontent.com/91268311/147072701-a059f21a-aad6-40fc-8ab8-a0c249fdb3ff.png
[Save the figue]: https://user-images.githubusercontent.com/91268311/147072776-8ceb16c8-bc49-4c0e-8f87-20937da7de35.png

### Menu bar

The following functions can be called from the menu bar or by shortcuts:
- Open: open a directory (similar to ```Open Folder``` button)
- Update: updates plot (similar to ```Update``` button)
- Restart: complete restart of the application
- Exit: close the application

As standard delimiter/separator, the comma "," is defined. In the ```Delimiter``` menu, different delimiters can be selected. To avoid errors, the delimiter should be selected before loading the data. However, plotting files with different delimiters at once is not possible yet. If needed, the ```Delimiter``` menu can be extended with further separators.
