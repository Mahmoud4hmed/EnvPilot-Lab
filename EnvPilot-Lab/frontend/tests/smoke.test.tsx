import { render, screen, cleanup } from '@testing-library/react';
import { afterEach, expect, test } from 'vitest';
import Home from '../app/page';
afterEach(cleanup);
test('working sign-in navigation', () => {render(<Home/>); expect(screen.getByRole('heading', {name: 'Welcome back'})).toBeDefined(); expect(screen.getByRole('button', {name: 'Sign in'})).toBeDefined();});
