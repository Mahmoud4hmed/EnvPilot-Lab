import type { Environment } from '../lib/api';

const lifecycle = {
  pending: {title: 'Waiting to be created', description: 'This record is waiting for a provisioning request.'},
  provisioning: {title: 'Creation in progress', description: 'The background worker is processing this environment.'},
  ready: {title: 'Reported as ready', description: 'The API reports this environment as ready. Review the resource and latest event below.'},
  failed: {title: 'Creation failed', description: 'The API reports a failure. Review the latest event and operation history.'},
};

function describeName(row: Environment) {
  const sample = /^dev-([1-9]\d*)-(\d{3,})$/.exec(row.name);
  if (sample) return {
    title: `Sample development workspace ${Number(sample[2])}`,
    category: 'Preloaded practice data',
    description: `Example workspace ${Number(sample[2])} in sample project ${Number(sample[1])}. Use it to explore the application during training.`,
    nameMeaning: 'dev means development; the next number is the sample project number and the final number is the workspace sequence within that project.',
  };
  if (/^check-[a-f\d]{32}$/i.test(row.name)) return {
    title: 'System check workspace',
    category: 'Automated lab check',
    description: 'Created by an automated lab check to verify resource provisioning. This record is diagnostic evidence, not a training assignment.',
    nameMeaning: 'check marks an automated diagnostic record. The random suffix keeps check names unique; it does not describe a project or task.',
  };
  return {
    title: row.name,
    category: 'Development workspace',
    description: 'A temporary development workspace belonging to the project below.',
    nameMeaning: 'This is the name recorded by the application. Use the exact value when tracing API requests or logs.',
  };
}

function describeResource(id: string) {
  if (!id) return {label: 'No resource reference recorded', description: 'The API has not recorded a provider resource ID for this environment.'};
  if (id.startsWith('seed-')) return {label: 'Preloaded sample resource', description: 'A reference included with the initial practice data; it does not identify a live VM.'};
  return {label: 'Simulated provider resource', description: 'A reference used by the local fake provider. It does not identify a real VM or a public URL.'};
}

function Timestamp({value}: {value: string}) {
  const date = new Date(value);
  if (!Number.isFinite(date.getTime())) return <>Not recorded</>;
  return <time dateTime={value}>{new Intl.DateTimeFormat('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'UTC',
  }).format(date)} UTC</time>;
}

export default function EnvironmentCard({environment: row, role, onProvision}: {
  environment: Environment; role: string; onProvision: (environment: Environment) => void;
}) {
  const state = lifecycle[row.status];
  const identity = describeName(row);
  const resource = describeResource(row.provider_id);
  const canProvision = role !== 'viewer';
  const nextStep = row.status === 'pending'
    ? canProvision
      ? 'Select Provision to ask the local fake provider to create a resource.'
      : 'Viewer access is read-only. Choose Owner or Developer to request provisioning.'
    : row.status === 'provisioning'
      ? 'Use Refresh to check for a newer status or event from the worker.'
      : row.status === 'failed'
        ? 'Inspect the event and operation history using the API contract before investigating the failure.'
        : 'Compare the reported status, latest event, and provider resource when investigating this record.';

  return <article className="environment-card" aria-labelledby={`environment-${row.id}-name`}>
    <div className="environment-card-top"><span className={'badge ' + row.status}>{row.status}</span><span className="environment-id">Environment #{row.id}</span></div>
    <p className="environment-category">{identity.category}</p>
    <h3 id={`environment-${row.id}-name`} data-testid={identity.title === row.name ? 'environment-name' : undefined}>{identity.title}</h3>
    <p className="environment-purpose">{identity.description}</p>
    <dl className="environment-context">
      <div><dt>Project</dt><dd>{row.project_name}</dd></div>
      <div><dt>Organization</dt><dd>{row.organization_name}</dd></div>
    </dl>
    <div className="environment-state"><h4>{state.title}</h4><p>{state.description}</p></div>
    <div className="environment-event"><h4>Latest recorded event</h4><p>{row.latest_event || 'No event has been recorded for this environment.'}</p></div>
    <dl className="environment-facts">
      <div><dt>Provider resource</dt><dd>{resource.label}</dd></div>
      <div><dt>Created</dt><dd><Timestamp value={row.created_at}/></dd></div>
      <div><dt>Last updated</dt><dd><Timestamp value={row.updated_at}/></dd></div>
    </dl>
    <div className="environment-next-step"><h4>What to do next</h4><p>{nextStep}</p>
      {row.status === 'pending' && canProvision && <button onClick={() => onProvision(row)}>Provision {identity.title}</button>}
      {row.status === 'failed' && <a href="/guide/api">Read the API contract →</a>}
    </div>
    <details className="environment-technical"><summary>Technical details</summary>
      <dl className="environment-facts">
        {identity.title !== row.name && <div><dt>Technical environment name</dt><dd><code data-testid="environment-name">{row.name}</code></dd></div>}
        <div><dt>Provider resource ID</dt><dd>{row.provider_id ? <code>{row.provider_id}</code> : 'Not recorded'}</dd></div>
        <div><dt>Project ID</dt><dd>{row.project}</dd></div><div><dt>Organization ID</dt><dd>{row.organization}</dd></div>
      </dl>
      <p>{identity.nameMeaning}</p><p>{resource.description}</p>
      <p>Authenticated API endpoint</p><code>/api/environments/{row.id}/</code>
      <p>Resources are simulated locally. This lab does not create a real VM or a public environment URL.</p>
    </details>
  </article>;
}
