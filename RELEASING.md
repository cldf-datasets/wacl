# Releasing the World Atlas of Classifier Languages dataset

- Make sure dependencies are met:
  ```shell
  pip install -e .[test]
  ```
- Recreate the CLDF data:
  ```shell
  cldfbench makecldf --with-zenodo --with-cldfreadme --glottolog-version v4.6 cldfbench_wacl.py
  ```
- Validate the data:
  ```shell
  pytest
  ```
- Recreate README.md
  ```shell
  cldfbench readme cldfbench_wacl.py
  ```
- create the release commit:
  ```shell
  git commit -a -m "release <VERSION>"
  ```
- create a release tag:
  ```shell
  git tag -a v<VERSION> -m"<VERSION> release"
  ```
- push to GitHub:
  ```shell
  git push origin
  git push --tags
  ```
- Create a release on GitHub.
- Make sure the release is picked up by Zenodo and add the Zenodo DOI to the release description on GitHub.
