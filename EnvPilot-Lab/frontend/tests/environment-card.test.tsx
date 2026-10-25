import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, expect, test, vi } from 'vitest';
import EnvironmentCard from '../components/EnvironmentCard';
import type { Environment } from '../lib/api';

const environment: Environment = {
  id: 12, name: 'dev-platform-12', project: 3, project_name: 'Platform', organization: 1,
  organization_name: 'Team Alpha', status: 'pending', provider_id: '', latest_event: 'Request accepted',
  created_at: '2026-10-25T08:00:00Z', updated_at: '2026-10-25T09:30:00Z',
};
afterEach(cleanup);

test('record context and timestamps are labeled, and provision acts on the displayed record', () => {
  const provision = vi.fn();
  render(<EnvironmentCard environment={environment} role="owner" onProvision={provision}/>);
  expect(screen.getByRole('article', {name: environment.name})).toBeDefined();
  for (const text of ['Project', 'Platform', 'Organization', 'Team Alpha', 'Latest recorded event', 'Request accepted', 'What to do next']) {
    expect(screen.getByText(text)).toBeDefined();
  }
  expect(screen.getByText('25 Oct 2026, 09:30 UTC').getAttribute('datetime')).toBe(environment.updated_at);
  expect(screen.getByText('/api/environments/12/')).toBeDefined();
  fireEvent.click(screen.getByRole('button', {name: 'Provision dev-platform-12'}));
  expect(provision).toHaveBeenCalledWith(environment);
});

test('viewer receives read-only guidance without a provisioning action', () => {
  render(<EnvironmentCard environment={environment} role="viewer" onProvision={vi.fn()}/>);
  expect(screen.queryByRole('button')).toBeNull();
  expect(screen.getByText(/Viewer access is read-only/)).toBeDefined();
});

test.each([
  ['provisioning', 'Creation in progress', /Use Refresh/],
  ['ready', 'Reported as ready', /Compare the reported status/],
  ['failed', 'Creation failed', /Inspect the event and operation history/],
] as const)('%s has specific guidance and does not offer to provision again', (status, title, guidance) => {
  render(<EnvironmentCard environment={{...environment, status, provider_id: 'vm-123'}} role="developer" onProvision={vi.fn()}/>);
  expect(screen.getByRole('heading', {name: title})).toBeDefined();
  expect(screen.getByText(guidance)).toBeDefined();
  expect(screen.getByText('vm-123')).toBeDefined();
  expect(screen.queryByRole('button')).toBeNull();
  if (status === 'failed') expect(screen.getByRole('link', {name: /Read the API contract/}).getAttribute('href')).toBe('/guide/api');
});

test('missing evidence is explicit rather than inventing a successful resource or event', () => {
  render(<EnvironmentCard environment={{...environment, status: 'ready', latest_event: null, created_at: '', updated_at: 'invalid'}} role="owner" onProvision={vi.fn()}/>);
  expect(screen.getByText('No resource reference recorded')).toBeDefined();
  expect(screen.getByText('No event has been recorded for this environment.')).toBeDefined();
  expect(screen.getAllByText('Not recorded')).toHaveLength(3);
});

test('sample names become readable titles while preserving the exact name and callback record', () => {
  const sample = {...environment, name: 'dev-4-060', provider_id: 'seed-1-3-59'};
  const provision = vi.fn();
  render(<EnvironmentCard environment={sample} role="owner" onProvision={provision}/>);
  expect(screen.getByRole('heading', {name: 'Sample development workspace 60'})).toBeDefined();
  expect(screen.getByText(/Example workspace 60 in sample project 4/)).toBeDefined();
  expect(screen.getByText('Preloaded sample resource')).toBeDefined();
  expect(screen.getByTestId('environment-name').closest('details')).not.toBeNull();
  expect(screen.getByText('seed-1-3-59').closest('details')).not.toBeNull();
  expect(screen.getByTestId('environment-name').textContent).toBe(sample.name);
  fireEvent.click(screen.getByRole('button', {name: 'Provision Sample development workspace 60'}));
  expect(provision).toHaveBeenCalledWith(sample);
});

test('diagnostic workspaces explain their purpose and keep the random suffix in details', () => {
  const name = 'check-f37c904214a940eda4d135e906a5cbbd';
  render(<EnvironmentCard environment={{...environment, name}} role="viewer" onProvision={vi.fn()}/>);
  expect(screen.getByRole('heading', {name: 'System check workspace'})).toBeDefined();
  expect(screen.getByText(/diagnostic evidence, not a training assignment/)).toBeDefined();
  expect(screen.getByText(name).closest('details')).not.toBeNull();
});

test.each(['check-my-project', 'dev-platform-12', 'dev-4-release'])('custom name %s stays unchanged', name => {
  render(<EnvironmentCard environment={{...environment, name}} role="viewer" onProvision={vi.fn()}/>);
  expect(screen.getByRole('heading', {name})).toBeDefined();
  expect(screen.queryByText('Automated lab check')).toBeNull();
  expect(screen.queryByText('Preloaded practice data')).toBeNull();
});
