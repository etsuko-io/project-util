from pathlib import Path

from project_util.artefact.artefact import Artefact
from project_util.constants import FILE_SYSTEM
from project_util.project.project import Project


class TestProject:
    def test_create_project(self, fs):
        project = Project(name="test", parent_dir=Path("."))
        assert project.backend == FILE_SYSTEM
        assert project.folders == {}
        assert project.path.as_posix() == "/test"
        assert project.path.exists()

    def test_create_file_name(self, fs):
        project = Project(name="test", parent_dir=Path("."))
        file_name = "my_result.png"
        path = project.create_file_name(file_name)
        assert path == "/test/my_result.png"
        assert not Path(path).exists()

    def test_add_remove_folder(self, fs):
        project = Project(name="test", parent_dir=Path("."))

        # add folder
        project.add_folder("results")
        assert isinstance(project.folders["results"], Project)
        subfolder_path = project.folders["results"].path
        assert subfolder_path.exists()

        # remove folder
        project.remove_folder("results")
        assert not subfolder_path.exists()

    def test_save_image__file_system(self, fs):
        project = Project(
            name="test", parent_dir=Path("."), backend=FILE_SYSTEM
        )
        # Create example image
        img = Artefact(name="test_image", project=project, size=(10, 10))
        path = project.save_image(
            data=img.data, file_name=Path("my-test-image.png")
        )
        assert Path(path).exists()
