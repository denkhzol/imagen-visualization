import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import "../public/styles/bootstrap.min.css"
import ReduxProvider from './reduxprovider';
import { Buffer } from 'buffer';

if (typeof window !== 'undefined') {
  globalThis.Buffer = Buffer;
}

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "Imagen Interactive Dashboard",
  description: "",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
         <ReduxProvider>
         {children}
         </ReduxProvider>
         
      </body>
    </html>
  );
}