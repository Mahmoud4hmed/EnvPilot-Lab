import {act,cleanup,fireEvent,render,screen} from '@testing-library/react';
import {afterEach,expect,test,vi} from 'vitest';
import MemoEditor from '../components/MemoEditor';
afterEach(()=>{cleanup();vi.unstubAllGlobals();});
test('failed save retains draft and confirmed heading',async()=>{
  vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:false}));
  render(<MemoEditor initial={{id:1,title:'Original',archived_at:null}} token="a"/>);
  fireEvent.change(screen.getByRole('textbox'),{target:{value:'My draft'}});fireEvent.click(screen.getByRole('button',{name:'Save'}));
  await screen.findByRole('alert');expect((screen.getByRole('textbox') as HTMLInputElement).value).toBe('My draft');expect(screen.getByRole('heading').textContent).toBe('Original');
});
test('pending save is single flight and success commits confirmed value',async()=>{
  let resolve!:(value:unknown)=>void;const fetcher=vi.fn().mockReturnValue(new Promise(r=>{resolve=r;}));vi.stubGlobal('fetch',fetcher);
  render(<MemoEditor initial={{id:1,title:'Original',archived_at:null}} token="a"/>);
  fireEvent.change(screen.getByRole('textbox'),{target:{value:'Changed'}});const button=screen.getByRole('button',{name:'Save'});fireEvent.click(button);fireEvent.click(button);
  expect(fetcher).toHaveBeenCalledTimes(1);expect(screen.getByRole('heading').textContent).toBe('Original');
  await act(async()=>{resolve({ok:true,json:async()=>({id:1,title:'Changed',archived_at:null})});});
  expect(screen.getByRole('heading').textContent).toBe('Changed');expect((button as HTMLButtonElement).disabled).toBe(false);
});
