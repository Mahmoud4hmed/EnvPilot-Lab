import { render, screen, cleanup, fireEvent } from '@testing-library/react';
import { afterEach, expect, test } from 'vitest';
import Home from '../app/page';
afterEach(cleanup);
test('working sign-in navigation', () => {render(<Home/>); expect(screen.getByRole('heading', {name: 'Welcome back'})).toBeDefined(); expect(screen.getByRole('button', {name: 'Sign in'})).toBeDefined();});
test('generic owner and a visible first task help learners get started', () => {
  render(<Home/>);
  expect((screen.getByRole('textbox',{name:'Username'}) as HTMLInputElement).value).toBe('owner');
  expect(screen.getByRole('heading',{name:'Your first task: investigate the running system'})).toBeDefined();
  expect(screen.getByRole('link',{name:'Start Day 1 →'}).getAttribute('href')).toBe('/guide/day-1');
  expect(screen.getByRole('link',{name:'Exercise 1'}).getAttribute('href')).toBe('/guide/exercise-1');
});
test('dashboard glossary explains the organization, environment, and fake provider', () => {
  render(<Home/>);
  fireEvent.click(screen.getByText('What do the dashboard controls mean?'));
  expect(screen.getByText(/No real VM or cloud account is used/)).toBeDefined();
  expect(screen.getByText(/Team Alpha and Team Beta are separate tenants/)).toBeDefined();
});
