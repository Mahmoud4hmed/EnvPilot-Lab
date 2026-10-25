export type Environment = {
  id: number; name: string; project: number; project_name: string; organization: number;
  organization_name: string; status: 'pending' | 'provisioning' | 'ready' | 'failed';
  provider_id: string; latest_event: string | null; created_at: string; updated_at: string;
};
export type Page = {count: number; results: Environment[]};
export type Operation = {id: number; environment: number; kind: string; key: string; status: 'queued' | 'running' | 'retrying' | 'succeeded' | 'failed'; attempts: number; error: string};
export type Membership = {organization: number; name: string; role: 'owner' | 'developer' | 'viewer'};
export async function api<T>(path: string, token: string, init: RequestInit = {}): Promise<T> {
  const response = await fetch(path, {...init, headers: {'Content-Type': 'application/json', Authorization: `Token ${token}`, ...init.headers}});
  const body = await response.json();
  if (!response.ok) throw new Error(JSON.stringify(body.error || body));
  return body as T;
}
