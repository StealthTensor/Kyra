"use client";

import Link from "next/link";
import { ArrowRight } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 text-center bg-zinc-950 space-y-8">
      <div className="space-y-4 max-w-lg">
        <h1 className="text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-zinc-500">
          Kyra AI
        </h1>
        <p className="text-zinc-400 text-lg">
          The B2B Native AI Email Operating System.
          <br />
          Reclaim your inbox, automate your workflow.
        </p>
      </div>

      <div className="flex flex-col gap-4 w-full max-w-sm">
        <Link href="/auth/login">
          <button className="w-full bg-white text-zinc-950 font-medium py-3 px-4 rounded-xl flex items-center justify-center gap-2 hover:bg-zinc-200 transition-colors">
            Login
            <ArrowRight size={18} />
          </button>
        </Link>
        <div className="text-xs text-zinc-600">
          By logging in, you agree to our Terms of Service.
        </div>
      </div>
    </div>
  );
}
