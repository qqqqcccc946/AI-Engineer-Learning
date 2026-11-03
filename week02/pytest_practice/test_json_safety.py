import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def manager(tmp_path, monkeypatch):
    module_path = Path(__file__).resolve().parents[2] / "week01/model_manager_v3.py"
    spec = importlib.util.spec_from_file_location("model_manager_v3", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.chdir(tmp_path)
    return module


@pytest.mark.parametrize("existing", [False, True])
def test_save_models_success(manager, tmp_path, existing):
    target = tmp_path / "models.json"
    if existing:
        target.write_text('[{"name": "old", "score": 1}]', encoding="utf-8")
    models = [{"name": "中文模型", "score": 95}]

    manager.save_models(models)

    content = target.read_text(encoding="utf-8")
    assert json.loads(content) == models
    assert "中文模型" in content
    assert set(tmp_path.iterdir()) == {target}


@pytest.mark.parametrize("existing", [False, True])
def test_serialization_failure_preserves_original(manager, tmp_path, existing, capsys):
    target = tmp_path / "models.json"
    original = b'[\r\n  {"name": "GPT", "score": 95}\r\n]\r\n'
    if existing:
        target.write_bytes(original)
    invalid_models = [{"name": "valid", "score": 90}, {"score": {88}}]

    with pytest.raises(TypeError):
        manager.save_models(invalid_models)

    if existing:
        assert target.read_bytes() == original
        assert json.loads(target.read_bytes()) == [{"name": "GPT", "score": 95}]
    else:
        assert not target.exists()
    assert set(tmp_path.iterdir()) == ({target} if existing else set())
    assert "数据保存成功" not in capsys.readouterr().out


@pytest.mark.parametrize("failure_stage", ["fsync", "replace"])
def test_io_failure_preserves_original(manager, tmp_path, monkeypatch, failure_stage):
    target = tmp_path / "models.json"
    original = b'[{"name": "GPT", "score": 95}]\n'
    target.write_bytes(original)

    def fail(*args):
        raise OSError("simulated save failure")

    monkeypatch.setattr(manager.os, failure_stage, fail)

    with pytest.raises(OSError, match="simulated save failure"):
        manager.save_models([{"name": "new", "score": 88}])

    assert target.read_bytes() == original
    assert set(tmp_path.iterdir()) == {target}


def test_replace_uses_complete_file_in_same_directory(manager, tmp_path, monkeypatch):
    target = tmp_path / "models.json"
    models = [{"name": "Claude", "score": 88}]
    real_replace = manager.os.replace
    calls = []

    def checked_replace(source, destination):
        assert source.parent == target.parent
        assert destination == target
        assert json.loads(source.read_text(encoding="utf-8")) == models
        calls.append(source)
        real_replace(source, destination)

    monkeypatch.setattr(manager.os, "replace", checked_replace)
    manager.save_models(models)

    assert len(calls) == 1
    assert json.loads(target.read_text(encoding="utf-8")) == models
