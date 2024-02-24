from server.common.utils import get_project_root


def test_get_project_root():
    project_root = get_project_root()
    assert project_root.name == 'dreamer'
