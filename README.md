# wacl
World Atlas of Classifier Languages



Code used by Marc so far to generate the cldf dataset (currently running it in on a backup computer with Windows, minor changes have to be made for Linux):

python -m virtualenv .venv2
.venv2\Scripts\activate
pip install cldfbench
cd OneDrive\Documents\GitHub\wacl
pip install pyglottolog
cldfbench makecldf cldfbench_wacl.py --glottolog C:\Users\marct\OneDrive\Documents\GitHub\glottolog\


# use for git errors
set GIT_PYTHON_REFRESH=quiet

# check the output
cldfbench readme cldfbench_wacl.py

The following can be used to generate the website projection

python -m virtualenv .venv2
.venv2\Scripts\activate
pip install "clld>=7.1.1"
pip install cookiecutter
cd OneDrive\Documents\GitHub\wacl
clld create myapp cldf_module=StructureDataset
cd myapp
pip install -r requirements.txt
clld initdb development.ini --cldf C:\Users\marct\OneDrive\Documents\GitHub\wacl\cldf\StructureDataset-metadata.json --glottolog C:\Users\marct\OneDrive\Documents\GitHub\glottolog\