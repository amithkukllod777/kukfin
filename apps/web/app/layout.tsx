import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'KukFin — AI Market Intelligence',
  description: 'AI-powered research, portfolio intelligence, backtesting and paper trading by Kuklabs.'
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
