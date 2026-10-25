import { render, screen, fireEvent, waitFor, act, cleanup } from '@testing-library/react';
import { afterEach, beforeEach, expect, test, vi } from 'vitest';
import Dashboard from '../components/Dashboard';

const row = (id: number, name: string, status = 'pending') => ({id, name, status, project_name: 'Platform', latest_event: 'Accepted', provider_id: '', project: 1, organization: 1});
const ok = (results: unknown[]) => ({ok: true, json: async () => ({count: results.length, results})});
let fetcher: ReturnType<typeof vi.fn>;
beforeEach(() => {fetcher = vi.fn(); vi.stubGlobal('fetch', fetcher);});
afterEach(() => {cleanup(); vi.unstubAllGlobals(); vi.useRealTimers();});
test('loading then empty feedback', async () => {
  let resolve!: (value: unknown) => void;
  fetcher.mockReturnValue(new Promise(r => {resolve = r;}));
  render(<Dashboard token="a" organization={1} role="owner"/>);
  expect(screen.getByRole('status').textContent).toMatch(/loading/i);
  await act(async () => {resolve(ok([]));});
  expect(screen.getByText(/no environments/i)).toBeDefined();
});
test('late response cannot replace current organization', async () => {
  let older!: (value: unknown) => void;
  fetcher.mockReturnValueOnce(new Promise(r => {older = r;})).mockResolvedValueOnce(ok([row(2, 'Team Beta')]));
  const view = render(<Dashboard token="a" organization={1} role="owner"/>);
  view.rerender(<Dashboard token="a" organization={2} role="owner"/>);
  await screen.findByText('Team Beta');
  await act(async () => {older(ok([row(1, 'Team Alpha')]));});
  expect(screen.queryByText('Team Alpha')).toBeNull();
  expect(screen.getByText('Team Beta')).toBeDefined();
});
test('refresh recovers from errors and clears stale error', async () => {
  fetcher.mockRejectedValueOnce(new Error('offline')).mockResolvedValue(ok([row(1, 'Recovered')]));
  render(<Dashboard token="a" organization={1} role="owner"/>);
  await screen.findByRole('alert');
  fireEvent.click(screen.getByRole('button', {name: 'Refresh'}));
  await screen.findByText('Recovered');
  expect(screen.queryByRole('alert')).toBeNull();
});
test('request aborts on unmount', () => {
  fetcher.mockReturnValue(new Promise(() => {}));
  const view = render(<Dashboard token="a" organization={1} role="owner"/>);
  const init = fetcher.mock.calls[0][1];
  expect(init.signal).toBeDefined(); view.unmount(); expect(init.signal.aborted).toBe(true);
});
test('token changes trigger a request with current credentials', async () => {
  fetcher.mockResolvedValue(ok([row(1, 'Current')]));
  const view = render(<Dashboard token="old" organization={1} role="owner"/>);
  await screen.findByText('Current');
  view.rerender(<Dashboard token="new" organization={1} role="owner"/>);
  await waitFor(() => expect(fetcher.mock.calls.some(call => call[1].headers.Authorization === 'Token new')).toBe(true));
});
test('unmount stops polling requests', async () => {
  vi.useFakeTimers(); fetcher.mockResolvedValue(ok([row(1, 'Current')]));
  const view = render(<Dashboard token="a" organization={1} role="owner"/>);
  await act(async () => {await Promise.resolve();});
  view.unmount(); const before = fetcher.mock.calls.length;
  await act(async () => {await vi.advanceTimersByTimeAsync(5000);});
  expect(fetcher.mock.calls.length).toBe(before);
});
test('accepted operation is truthful and eventually refreshed', async () => {
  fetcher.mockResolvedValueOnce(ok([row(1, 'Sandbox')])).mockResolvedValueOnce({ok: true, json: async () => ({id: 1, status: 'queued'})}).mockResolvedValue(ok([row(1, 'Sandbox', 'ready')]));
  render(<Dashboard token="a" organization={1} role="owner"/>);
  fireEvent.click(await screen.findByRole('button', {name: 'Provision Sandbox'}));
  await waitFor(() => expect(fetcher.mock.calls.length).toBeGreaterThanOrEqual(2));
  expect(screen.queryByText('Environment ready')).toBeNull();
  await waitFor(() => expect(fetcher.mock.calls.length).toBeGreaterThan(2), {timeout: 5000});
});
test('small feature: environment name filter', async () => {
  fetcher.mockResolvedValue(ok([row(1, 'alpha'), row(2, 'beta')]));
  render(<Dashboard token="a" organization={1} role="owner"/>);
  await screen.findByText('alpha');
  fireEvent.change(screen.getByRole('textbox', {name: /search/i}), {target: {value: 'BETA'}});
  expect(screen.queryByText('alpha')).toBeNull(); expect(screen.getByText('beta')).toBeDefined();
});
