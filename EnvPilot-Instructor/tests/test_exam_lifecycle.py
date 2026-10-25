import datetime as dt
import importlib.util
from pathlib import Path
import json
import zipfile

spec=importlib.util.spec_from_file_location('exam',Path(__file__).resolve().parents[1]/'exam.py')
exam=importlib.util.module_from_spec(spec);spec.loader.exec_module(exam)


def test_clock_survives_resume_expiration_and_source_isolation(tmp_path):
    template=tmp_path/'template';template.mkdir();(template/'source.py').write_text('starter')
    root=tmp_path/'mock'
    first,created=exam.prepare(root,template)
    (root/'source.py').write_text('learner work')
    second,created2=exam.prepare(root,template)
    assert created and not created2 and first['started_at']==second['started_at']
    at=dt.datetime.fromisoformat(first['started_at'])+dt.timedelta(hours=4)
    assert exam.status(root,at)['expired'] and exam.status(root,at)['remaining_seconds']==0
    assert (root/'source.py').read_text()=='learner work'
    assert (template/'source.py').read_text()=='starter'
    archive=exam.snapshot(root)
    with zipfile.ZipFile(archive) as handle:assert handle.read('source.py')==b'learner work'


def test_submission_preserves_original_work_and_timestamp(tmp_path,monkeypatch):
    template=tmp_path/'template';template.mkdir();(template/'NOTES.md').write_text('Evidence')
    root=tmp_path/'mock';exam.prepare(root,template)
    monkeypatch.setattr(exam,'check',lambda root:{'provisional_earned':75,'points':{'api_correctness':25,'authorization':15,'ui':20,'incident':15},'evidence':{}})
    exam.submit(root)
    state=json.loads((root/'.exam'/'state.json').read_text());report=(root/'.exam'/'FEEDBACK.md').read_text()
    exam.submit(root)
    assert json.loads((root/'.exam'/'state.json').read_text())['submitted_at']==state['submitted_at']
    assert (root/'NOTES.md').read_text()=='Evidence'
    assert 'Top three' in report and '75/100 provisional' in report
