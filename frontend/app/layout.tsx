import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import MobileLayout from "@/components/layout/MobileLayout";
import AuthSync from "@/components/AuthSync";
import { Toaster } from "@/components/ui/sonner";
import { ErrorBoundary } from "@/components/ErrorBoundary";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: "#09090b",
};

export const metadata: Metadata = {
  title: "Kyra AI | Enterprise Agent",
  description: "The B2B Native AI Email OS.",
  manifest: "/manifest.json",
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://kyra.ai",
    title: "Kyra AI - The Future of Work",
    description: "Automate your inbox with a personal AI agent.",
    siteName: "Kyra AI",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-zinc-950 text-white`}
      >
        <ErrorBoundary>
          <AuthSync>
            {children}
            <Toaster />
          </AuthSync>
        </ErrorBoundary>
      </body>
    </html>
  );
}
