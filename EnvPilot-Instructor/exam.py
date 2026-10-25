"""Independent mock lifecycle. No dependency on learner exercise implementations."""
import argparse
import datetime as dt
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

HERE = Path(__file__).resolve().parent


def now():
    return dt.datetime.now(dt.timezone.utc)


def prepare(root, template=None):
    root = Path(root)
    state = root / '.exam' / 'state.json'
    if state.exists():
        return json.loads(state.read_text()), False
    if root.exists():
        raise RuntimeError(f'{root} exists without exam state. Refusing to overwrite it; preserve/rename it explicitly before starting.')
    shutil.copytree(template or HERE / 'mock-template', root, ignore=shutil.ignore_patterns('__pycache__','node_modules','.next','*.sqlite3'))
    state.parent.mkdir()
    data = {'started_at':now().isoformat(), 'duration_seconds':10800, 'submitted_at':None}
    with state.open('x', encoding='utf-8') as handle:
        json.dump(data, handle, indent=2)
    return data, True


def status(root, at=None):
    state = Path(root) / '.exam' / 'state.json'
    if not state.exists():
        return {'started':False, 'next_command':'python lab.py exam start'}
    data = json.loads(state.read_text())
    elapsed = max(0, int(((at or now()) - dt.datetime.fromisoformat(data['started_at'])).total_seconds()))
    return {**data, 'started':True, 'elapsed_seconds':elapsed, 'remaining_seconds':max(0,data['duration_seconds']-elapsed), 'expired':elapsed>=data['duration_seconds'], 'workspace':str(Path(root).resolve()), 'work_preserved':True}


def run(root, args):
    return subprocess.call(['docker','compose',*args], cwd=root)


def bring_up(root):
    probe=subprocess.run(['docker','version','--format','{{.Server.Os}}'],capture_output=True,text=True,timeout=20)
    if probe.returncode or probe.stdout.strip()!='linux':
        raise RuntimeError('Linux Docker Engine unavailable. Start time/work saved; resolve Docker Desktop startup error, then rerun start to resume.')
    for args in [
        ['up','-d','--wait','db','redis'],
        ['build','api','web'],
        ['run','--rm','--no-deps','api','python','manage.py','migrate','--noinput'],
        ['run','--rm','--no-deps','api','python','manage.py','seed'],
        ['up','-d'],
    ]:
        code = run(root,args)
        if code:
            raise RuntimeError(f'Mock setup command exited {code}. Start time/work saved; resolve setup and rerun start to resume.')


def cases(path):
    if not path.exists():
        return []
    result=[]
    for case in ET.parse(path).iter('testcase'):
        child = case.find('failure')
        error = case.find('error')
        passed = child is None and error is None and case.find('skipped') is None
        result.append({'name':case.get('name',''), 'passed':passed, 'infrastructure_error':error is not None, 'evidence':(child if child is not None else error).get('message','') if child is not None or error is not None else ''})
    return result


def check(root):
    reports = root / '.exam'
    reports.mkdir(exist_ok=True)
    # Remove stale reports; these contain evidence, not learner source.
    for filename in ['api.xml','ui.xml']:
        (reports/filename).unlink(missing_ok=True)
    api_code = run(root,['run','--rm','--no-deps','-v',f'{HERE / "mock-grader"}:/grader:ro','-v',f'{reports}:/reports','-e','PYTHONPATH=/app','api','pytest','-c','/app/pytest.ini','/grader/test_api.py','--junitxml=/reports/api.xml'])
    ui_code = run(root,['run','--rm','--no-deps','-v',f'{reports}:/reports','web','npm','test','--','--reporter=default','--reporter=junit','--outputFile=/reports/ui.xml'])
    service_code = run(root,['up','-d','--no-deps','--force-recreate','proxy'])
    service_evidence=''
    if service_code==0:
        for _ in range(15):
            try:
                body=json.dumps({'username':'owner','password':'LabPass123!'}).encode()
                login=urllib.request.Request('http://localhost:8091/api/login/',data=body,headers={'Content-Type':'application/json'})
                token=json.load(urllib.request.urlopen(login,timeout=2))['token']
                request=urllib.request.Request('http://localhost:8091/api/memos/',headers={'Authorization':'Token '+token})
                response=urllib.request.urlopen(request,timeout=2)
                assert response.status==200 and isinstance(json.load(response),list)
                service_evidence='PASS: login and scoped memo list through recreated gateway';break
            except Exception as exc:
                service_evidence=str(exc);time.sleep(.2)
        else:service_code=1
    api_cases=cases(reports/'api.xml');ui_cases=cases(reports/'ui.xml')
    auth=[c for c in api_cases if any(n in c['name'] for n in ['authorization','anonymous','missing'])]
    behavior=[c for c in api_cases if c not in auth]
    def portion(group,weight):return round(weight*sum(c['passed'] for c in group)/len(group),2) if group else 0
    points={'api_correctness':portion(behavior,25),'authorization':portion(auth,15),'ui':portion(ui_cases,20),'incident':15 if service_code==0 else 0}
    evidence={'api_exit':api_code,'ui_exit':ui_code,'service_exit':service_code,'service_evidence':service_evidence,'api':api_cases,'ui':ui_cases}
    if api_code not in [0,1] or ui_code not in [0,1] or not api_cases or not ui_cases or any(c['infrastructure_error'] for c in api_cases+ui_cases):
        evidence['infrastructure_failure']=True
    result={'provisional_earned':sum(points.values()),'scale':100,'automatic_maximum':75,'manual_pending':{'meaningful_tests':10,'diagnosis':10,'engineering_explanation':5},'points':points,'evidence':evidence}
    (reports/'checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))
    return result


def snapshot(root):
    target=root/'.exam'/(now().strftime('submission-%Y%m%dT%H%M%S%fZ')+'.zip')
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as archive:
        for path in root.rglob('*'):
            rel=path.relative_to(root)
            if path.is_file() and not any(p in {'.exam','node_modules','.next','__pycache__','.pytest_cache','test-results'} for p in rel.parts) and path.suffix not in ['.sqlite3','.pyc']:
                archive.write(path,rel)
    return target


def submit(root):
    state_path=root/'.exam'/'state.json'
    if not state_path.exists():raise RuntimeError('Start the mock before submission.')
    data=json.loads(state_path.read_text())
    if data.get('submitted_at'):
        print('Already submitted; preserving original timestamp and report.')
        print((root/'.exam'/'FEEDBACK.md').read_text(encoding='utf-8'));return
    backup=snapshot(root)
    data['submitted_at']=now().isoformat();data['snapshot']=str(backup)
    state_path.write_text(json.dumps(data,indent=2))
    try:
        result=check(root)
    except Exception as exc:
        result={'provisional_earned':0,'points':{},'evidence':{'infrastructure_failure':True,'message':str(exc)},'manual_pending':{'meaningful_tests':10,'diagnosis':10,'engineering_explanation':5}}
    weights={'api_correctness':25,'authorization':15,'ui':20,'incident':15}
    priorities=[]
    guidance={'api_correctness':'Reproduce archive/replay failures and test the transition against PostgreSQL concurrency.','authorization':'Add a permission matrix with valid owner, viewer, anonymous and foreign-object cases.','ui':'Use deferred promises to test failed and overlapping saves without losing drafts.','incident':'Collect gateway/upstream evidence and verify the configuration survives service recreation.'}
    for key in sorted(weights,key=lambda k:result['points'].get(k,0)/weights[k]):
        if result['points'].get(key,0)<weights[key]:priorities.append(guidance[key])
    priorities+=['Review your added tests for negative cases and meaningful assertions.','Turn diagnosis evidence into a concise root-cause note with reproduction and verification.','Explain tradeoffs and list the next production risks you would address.']
    ungraded=bool(result['evidence'].get('infrastructure_failure'))
    score='UNGRADED — infrastructure evidence incomplete' if ungraded else f"{result['provisional_earned']}/100 provisional (automatic maximum 75; manual 25 pending)"
    text=f'# Independent mock feedback\n\nScore: {score}.\n\nSubmitted UTC: {data["submitted_at"]}\n\nSource snapshot: {backup.name}\n\n## Evidence\n\nSee checks.json for each passed/failed criterion and command exit status. Infrastructure failures do not count as learner failures.\n\n## Top three improvement priorities\n\n'+''.join(f'{i}. {p}\n' for i,p in enumerate(priorities[:3],1))+'\n## Manual review required\n\nMeaningful tests /10; evidence-based diagnosis /10; engineering explanation /5. Award partial credit from NOTES.md and tests, then add to automatic points. No source-keyword or exact-prose scoring.\n'
    (root/'.exam'/'FEEDBACK.md').write_text(text,encoding='utf-8')
    print(text)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['start','status','submit','check']);parser.add_argument('--lab-root',type=Path);parser.add_argument('--mock-root',type=Path)
    args=parser.parse_args()
    root=args.mock_root or ((args.lab_root or HERE.parent/'EnvPilot-Lab').parent/'EnvPilot-Mock')
    root=root.resolve()
    if args.action=='start':
        data,created=prepare(root);print('Started new mock' if created else 'Resuming original mock clock/work');print(json.dumps(status(root),indent=2));bring_up(root);print(f'Open http://localhost:8091 and {root / "TASKS.md"}')
    elif args.action=='status':print(json.dumps(status(root),indent=2))
    elif args.action=='submit':submit(root)
    else:
        result=check(root);return 2 if result['evidence'].get('infrastructure_failure') else int(any(result['evidence'][k] for k in ['api_exit','ui_exit','service_exit']))
    return 0


if __name__=='__main__':
    try:sys.exit(main())
    except (RuntimeError,FileNotFoundError,subprocess.TimeoutExpired) as exc:print('INFRASTRUCTURE:',exc);sys.exit(2)
