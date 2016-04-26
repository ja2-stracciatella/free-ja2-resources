# Free Jagged Alliance 2 Resources

Containing free and open source resources for Jagged Alliance 2. Currently aiming at providing a free `editor.slf` file.

The build scripts are using Python3 and the ja2py library from [ja2-open-toolset](https://github.com/ja2-stracciatella/ja2-open-toolset).

The Ja2 Open Toolset Libraries and other dependencies need to be installed using pip:

```
pip install -r requirements.txt
```

To build the free editor.slf use 

```
python create_free_editorslf.py /path/to/original/editor.slf
```

which will build into the build folder.
