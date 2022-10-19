# wacl
World Atlas of Classifier Languages



Code used by Marc so far to generate the cldf dataset. Marc is currently running it in on a backup computer with Windows, minor changes have to be made for Linux. The paths also need to be updated later on.

```
python -m virtualenv .venv2
.venv2\Scripts\activate
pip install cldfbench
cd OneDrive\Documents\GitHub\wacl
pip install pyglottolog
cldfbench makecldf cldfbench_wacl.py --glottolog C:\Users\marct\OneDrive\Documents\GitHub\glottolog\
```

use the following if you have git errors
```
set GIT_PYTHON_REFRESH=quiet
```

use the following to check the output
```
cldfbench readme cldfbench_wacl.py
```

The following should be used to generate the website projection, but Marc did not test it yet.


```
python -m virtualenv .venv2
.venv2\Scripts\activate
pip install "clld>=7.1.1"
pip install cookiecutter
cd OneDrive\Documents\GitHub\wacl
clld create myapp cldf_module=StructureDataset
cd myapp
pip install -r requirements.txt
clld initdb development.ini --cldf C:\Users\marct\OneDrive\Documents\GitHub\wacl\cldf\StructureDataset-metadata.json --glottolog C:\Users\marct\OneDrive\Documents\GitHub\glottolog\
pserve development.ini
```