import './style.css';
export const metadata = {title: 'EnvPilot Lab', description: 'Local engineering practice'};
export default function RootLayout({children}: {children: React.ReactNode}) {return <html lang="en"><body>{children}</body></html>;}
