import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Polaris — OSINT Workbench",
  description: "Source-backed open-source intelligence workbench.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}