import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

exercise, folder, exit_code = sys.argv[1:]
folder = Path(folder)
weights = {'1':20,'2':12,'3':25,'4':12,'5':14,'6':7,'7':10}
path = folder / f'ex{exercise}.xml'
criteria = []
if path.exists():
    for case in ET.parse(path).iter('testcase'):
        failure = case.find('failure')
        error = case.find('error')
        skipped = case.find('skipped')
        status = 'fail' if failure is not None else 'infrastructure_error' if error is not None else 'skipped' if skipped is not None else 'pass'
        evidence = failure if failure is not None else error
        criteria.append({'criterion':case.get('name'),'status':status,'evidence':evidence.get('message','') if evidence is not None else ''})
infrastructure = int(exit_code) not in [0,1] or any(c['status']=='infrastructure_error' for c in criteria) or (exercise in ['1','2','3','5','7'] and not criteria)
if exercise=='3' and (folder/'worker.json').exists():
    for result in json.loads((folder/'worker.json').read_text()):
        criteria.append({'criterion':'real-worker '+result['scenario'],'status':'pass' if result['passed'] else 'fail','evidence':result.get('evidence','')})
report = {'exercise':exercise,'weight':weights[exercise],'exit_code':int(exit_code),'classification':'INFRASTRUCTURE FAILURE' if infrastructure else 'EXPECTED TRAINING FAILURE' if int(exit_code) else 'PASS', 'criteria':criteria, 'automatic_partial_credit':f"{sum(c['status']=='pass' for c in criteria)}/{len(criteria)} criteria" if criteria else 'See command evidence; no XML result for this exercise.', 'manual_review':'Engineering notes, tests added, maintainability, and explanation require review using RUBRIC.md.'}
(folder / f'ex{exercise}.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
sys.exit(2 if infrastructure else 0)
