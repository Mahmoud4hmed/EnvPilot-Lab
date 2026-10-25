import importlib.util
from pathlib import Path
import zipfile

spec=importlib.util.spec_from_file_location('labcli',Path(__file__).resolve().parents[2]/'EnvPilot-Lab'/'lab.py')
labcli=importlib.util.module_from_spec(spec);spec.loader.exec_module(labcli)


def test_reset_requires_flag_backs_up_and_preserves_notes(tmp_path,monkeypatch):
    root=tmp_path/'lab';state=root/'.lab';state.mkdir(parents=True)
    source=root/'backend/lab/assistant.py';source.parent.mkdir(parents=True);source.write_text('my work')
    notes=root/'notes.md';notes.write_text('important evidence')
    with zipfile.ZipFile(state/'starter.zip','w') as archive:archive.writestr('backend/lab/assistant.py','starter')
    monkeypatch.setattr(labcli,'ROOT',root);monkeypatch.setattr(labcli,'STATE',state)
    labcli.reset('7',False);assert source.read_text()=='my work' and not (state/'backups').exists()
    labcli.reset('7',True);assert source.read_text()=='starter' and notes.read_text()=='important evidence'
    backups=list((state/'backups').glob('*.zip'));assert len(backups)==1
    with zipfile.ZipFile(backups[0]) as archive:assert archive.read('backend/lab/assistant.py')==b'my work'


def test_incident_toggle_does_not_touch_source_or_notes(tmp_path,monkeypatch):
    state=tmp_path/'.lab';source=tmp_path/'views.py';source.write_text('learner changes')
    monkeypatch.setattr(labcli,'STATE',state);calls=[]
    monkeypatch.setattr(labcli,'compose',lambda args:calls.append(args) or 0)
    labcli.incident('start','proxy');labcli.incident('start','queue');labcli.incident('stop','proxy')
    assert labcli.active()==['queue'] and source.read_text()=='learner changes'
    assert calls[-1][-1]=='proxy'
