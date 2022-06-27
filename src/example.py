from pathlib import Path

from project_util.artefact.artefact import Artefact
from project_util.project.project import Project

if __name__ == "__main__":
    proj = Project(name="black-white-figures", parent_dir=Path("."))
    proj.add_folder("sketches")
    proj.add_folder("highres")
    proj.add_folder("animation")
    art = Artefact(name="trapezoid.png", size=(100, 100))

    art.fill((0, 24, 45))
    art.save(proj.folders["sketches"])

    # get a super-resolution version
    for upscale in (2, 3, 4, 6, 8, 9, 12, 16):
        super_version = art.get_superres(upscale)
        super_version.save(proj.folders["highres"])

    super_version16 = art.get_superres(16)
    super_version16.save(proj.folders["highres"])

    for g in range(96):
        art.fill((0, g, 0))
        art.save(proj.folders["animation"], suffix=f"{g:02d}")

    proj.folders["animation"].export_frames_as_video(name="animation.mp4")
