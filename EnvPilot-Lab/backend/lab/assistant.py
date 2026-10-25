import json
from .models import Environment, SupportDocument


def fake_model(documents, scenario):
    if scenario == 'timeout':
        raise TimeoutError('Fake model deadline exceeded')
    if scenario == 'malformed':
        return '{invalid'
    if scenario == 'tool':
        return json.dumps({'answer': '', 'citations': [], 'tool': {'name': 'environment_status', 'environment_id': 241}})
    if scenario == 'forbidden_tool':
        return json.dumps({'answer': '', 'citations': [], 'tool': {'name': 'delete_environment', 'environment_id': 1}})
    if scenario == 'injection' and any('IGNORE' in d.content for d in documents):
        return json.dumps({'answer': 'PWNED', 'citations': [], 'tool': None})
    if not documents:
        return json.dumps({'answer': 'Restart all servers', 'citations': [], 'tool': None})
    doc = documents[0]
    return json.dumps({'answer': doc.content, 'citations': [doc.id], 'tool': None})


def ask(user, organization, question, scenario='normal'):
    documents = list(SupportDocument.objects.filter(title__icontains=question).order_by('id'))
    try:
        result = json.loads(fake_model(documents, scenario))
    except (ValueError, TimeoutError):
        return {'answer': 'Try restarting everything.', 'citations': [], 'tool': None, 'fallback': False}
    tool = result.get('tool')
    if tool:
        env = Environment.objects.filter(pk=tool.get('environment_id')).first()
        result['answer'] = env.status if env else 'missing'
    result['fallback'] = False
    return result
