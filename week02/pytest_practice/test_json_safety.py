import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

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


def test_load_models_corrupt_json(manager, tmp_path):
    target = tmp_path / "models.json"
    original = b'[{"name": "GPT", "score": 95},\r\n'
    target.write_bytes(original)

    with pytest.raises(json.JSONDecodeError, match="models.json JSON 文件格式错误") as exc:
        manager.load_models()

    assert exc.value.lineno == 2
    assert exc.value.colno == 1
    assert target.read_bytes() == original
    assert set(tmp_path.iterdir()) == {target}


def test_load_models_missing_file(manager, tmp_path):
    assert manager.load_models() == []
    assert list(tmp_path.iterdir()) == []


def test_load_models_success(manager, tmp_path):
    target = tmp_path / "models.json"
    models = [{"name": "中文模型", "score": 95}]
    original = json.dumps(models, ensure_ascii=False).encode("utf-8")
    target.write_bytes(original)

    assert manager.load_models() == models
    assert target.read_bytes() == original
    assert set(tmp_path.iterdir()) == {target}


def test_startup_corrupt_json_preserves_original(manager, tmp_path):
    target = tmp_path / "models.json"
    original = b'[{"name": "GPT", "score": 95},\r\n'
    target.write_bytes(original)

    result = subprocess.run(
        [sys.executable, manager.__file__], cwd=tmp_path,
        capture_output=True, text=True, encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )

    assert result.returncode != 0
    assert "加载失败" in result.stderr
    assert "models.json JSON 文件格式错误" in result.stderr
    assert "加载结果" not in result.stdout
    assert "数据保存成功" not in result.stdout
    assert target.read_bytes() == original
    assert set(tmp_path.iterdir()) == {target}
