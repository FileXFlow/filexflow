export const metadata = { title: "FilexFlow", description: "Simple PDF ↔ Office conversions" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (<html lang="en"><body className="min-h-screen">{children}</body></html>);
}