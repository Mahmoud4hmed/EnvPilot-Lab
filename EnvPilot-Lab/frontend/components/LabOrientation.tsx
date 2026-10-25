import Link from 'next/link';

export default function LabOrientation() {
  return <section className="lab-orientation" aria-labelledby="mission-title">
    <div className="mission-heading"><div><p className="eyebrow">START HERE · DAY 1 / 30 MINUTES</p><h2 id="mission-title">Your first task: investigate the running system</h2></div><Link className="primary-link" href="/guide/day-1">Start Day 1 →</Link></div>
    <p className="orientation-description">This dashboard belongs to a fictional platform for temporary development environments. Your role is to understand its behavior, reproduce problems, repair the code, and verify your work with tests. Open the lab guide for each exercise's instructions.</p>
    <ol className="mission-steps">
      <li><span className="step-number">01</span><div><h3>Read the task</h3><p>Open the Day 1 checklist and the <Link href="/guide/api">API contract</Link>. Record what the system should do.</p></div></li>
      <li><span className="step-number">02</span><div><h3>Observe this dashboard</h3><p>Inspect one environment, switch accounts, and trace a request from the browser to the database.</p></div></li>
      <li><span className="step-number">03</span><div><h3>Work in your editor</h3><p>Run <code>python lab.py check smoke</code>, save your notes, then open <Link href="/guide/exercise-1">Exercise 1</Link>.</p></div></li>
    </ol>
    <details className="dashboard-explainer"><summary>What do the dashboard controls mean?</summary><div className="explainer-body">
      <p><strong>Organization</strong> is a fictional team. Team Alpha and Team Beta are separate tenants. Accounts have a role in each team.</p>
      <p><strong>Environment</strong> is a temporary development workspace belonging to a project. Each card labels its project, organization, reported lifecycle, latest event, provider resource, and creation/update times. Read <strong>What to do next</strong> for guidance, or expand <strong>Technical details</strong> to find the API endpoint and record IDs.</p>
      <p><strong>Provision</strong> asks a background worker to create a resource in the local fake provider. No real VM or cloud account is used.</p>
      <dl className="state-legend"><div><dt>pending</dt><dd>Waiting for provisioning</dd></div><div><dt>provisioning</dt><dd>Background work in progress</dd></div><div><dt>ready</dt><dd>Provisioning completed</dd></div><div><dt>failed</dt><dd>Inspect operation and event evidence</dd></div></dl>
      <p><strong>Refresh / Status</strong> reload the list or filter it by lifecycle. Names starting with <code>dev-</code> are seeded examples; <code>check-</code> records are created by diagnostic checks.</p>
      <p className="training-note">This starter deliberately contains exercise defects. Use the issue cards and checks to evaluate behavior; styling and the number of cards are not your assignment.</p>
    </div></details>
    <div className="orientation-links"><Link href="/guide">Browse all exercises</Link><Link href="/guide/commands">Terminal commands</Link><Link href="/guide/notes">Notes template</Link></div>
  </section>;
}
