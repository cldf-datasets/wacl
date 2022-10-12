from pathlib import Path

from clld.web.assets import environment

import myapp


environment.append_path(
    Path(myapp.__file__).parent.joinpath('static').as_posix(),
    url='/myapp:static/')
environment.load_path = list(reversed(environment.load_path))
