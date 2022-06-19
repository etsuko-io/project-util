from pathlib import Path

from src.artefact.artefact import Artefact
from src.project.project import Project

if __name__ == "__main__":
    proj = Project(name="black-white-figures", parent_dir=Path("."))
    proj.add_folder("sketches")
    proj.add_folder("highres")
    proj.add_folder("animation")
    art = Artefact(name="trapezoid.png", size=(100, 100))

    art.fill((0, 24, 45))
    art.save(proj.folders["sketches"])

    # get a super-resolution version
    super_version = art.get_superres()
    super_version.save(proj.folders["highres"])

    for g in range(96):
        art.fill((0, g, 0))
        art.save(proj.folders["animation"], suffix=f"{g:02d}")

    movie = proj.folders["animation"].export_frames_as_video(name="animation.mp4")
