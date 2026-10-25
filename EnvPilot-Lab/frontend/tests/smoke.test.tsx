import {render,screen,fireEvent,cleanup,waitFor,act} from '@testing-library/react';
import {afterEach,beforeEach,expect,test,vi} from 'vitest';
import Home from '../app/page';

vi.mock('../components/Dashboard',()=>({default:({role,organization,token}:{role:string;organization:number;token:string})=><section aria-label="Active workspace">{role}:{organization}:{token}</section>}));
const preferences='envpilot.demo-selection.v1';
const memberships=[{organization:1,name:'Team Alpha',role:'developer'},{organization:2,name:'Team Beta',role:'developer'}];
function session(role:string){return {ok:true,json:async()=>({username:role,token:role+'-token',memberships:role==='outsider'?[]:role==='dual'?memberships:[{organization:1,name:'Team Alpha',role}]})};}
let fetcher:ReturnType<typeof vi.fn>;
beforeEach(()=>{localStorage.clear();fetcher=vi.fn().mockImplementation((_url,init)=>Promise.resolve(session(JSON.parse(init.body).role)));vi.stubGlobal('fetch',fetcher);});
afterEach(()=>{cleanup();vi.unstubAllGlobals();});
test('opens as owner without login and explains the first task',async()=>{
  render(<Home/>);
  expect(screen.queryByLabelText('Password')).toBeNull();
  expect(screen.queryByRole('button',{name:'Sign in'})).toBeNull();
  expect(screen.getByRole('heading',{name:'Your first task: investigate the running system'})).toBeDefined();
  expect(screen.getByRole('link',{name:'Start Day 1 →'}).getAttribute('href')).toBe('/guide/day-1');
  expect((screen.getByRole('combobox',{name:'Role'}) as HTMLSelectElement).value).toBe('owner');
  expect((await screen.findByRole('region',{name:'Active workspace'})).textContent).toBe('owner:1:owner-token');
});
test('role and organization survive remount without storing credentials',async()=>{
  const view=render(<Home/>);await screen.findByRole('region',{name:'Active workspace'});
  fireEvent.change(screen.getByRole('combobox',{name:'Role'}),{target:{value:'dual'}});
  await waitFor(()=>expect(screen.getAllByRole('option').some(option=>option.textContent==='Team Beta · developer')).toBe(true));
  fireEvent.change(screen.getByRole('combobox',{name:'Organization'}),{target:{value:'2'}});
  expect(JSON.parse(localStorage.getItem(preferences)!)).toEqual({role:'dual',organization:2});
  view.unmount();render(<Home/>);
  await waitFor(()=>expect(screen.getByRole('region',{name:'Active workspace'}).textContent).toBe('developer:2:dual-token'));
  expect(localStorage.getItem(preferences)).not.toContain('token');
});
test('late role response cannot replace the new selection',async()=>{
  let old!:(value:unknown)=>void;
  fetcher.mockReturnValueOnce(new Promise(resolve=>{old=resolve;}));
  render(<Home/>);
  fireEvent.change(screen.getByRole('combobox',{name:'Role'}),{target:{value:'viewer'}});
  await screen.findByRole('region',{name:'Active workspace'});
  await act(async()=>{old(session('owner'));});
  expect(screen.getByRole('region',{name:'Active workspace'}).textContent).toBe('viewer:1:viewer-token');
});
test('failed connection offers retry and outsider has no workspace',async()=>{
  fetcher.mockRejectedValueOnce(new Error('offline'));
  render(<Home/>);await screen.findByRole('alert');
  fireEvent.click(screen.getByRole('button',{name:'Retry'}));
  await screen.findByRole('region',{name:'Active workspace'});
  expect(screen.queryByRole('alert')).toBeNull();
  fireEvent.change(screen.getByRole('combobox',{name:'Role'}),{target:{value:'outsider'}});
  await screen.findByText('This demo account has no organization memberships. Select another role to explore a workspace.');
  expect(screen.queryByRole('region',{name:'Active workspace'})).toBeNull();
});
test('invalid saved selection falls back to owner',async()=>{
  localStorage.setItem(preferences,'invalid-json');render(<Home/>);
  expect((await screen.findByRole('region',{name:'Active workspace'})).textContent).toBe('owner:1:owner-token');
});
test('glossary remains available',async()=>{
  render(<Home/>);await screen.findByRole('region',{name:'Active workspace'});
  fireEvent.click(screen.getByText('What do the dashboard controls mean?'));
  expect(screen.getByText(/No real VM or cloud account is used/)).toBeDefined();
});
