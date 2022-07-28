## Installation

    pip install git+https://github.com/etsuko-io/project-util.git




## Example usage (internal)

    from pathlib import Path

    from artefact.artefact import Artefact
    from project.project import Project


    if __name__ == "__main__":
        proj = Project(name="black-white-figures", parent_dir=Path("."))
        proj.add_folder("sketches")
        proj.add_folder("animations")
        art = Artefact(name="trapezoid.png", size=(100, 100))
        art.fill()
        art.save(proj.folders["sketches"])



## Development


Create venv, then


    pip install -e .
