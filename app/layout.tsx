import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Project Udyam Digital | Accel Business B2B Onboarding',
  description: 'Zero-Trust & High-Assurance Self-Service Digital Acquisition Platform for Indian MSMEs',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-100 text-slate-900 antialiased selection:bg-red-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}

