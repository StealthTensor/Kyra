"use client";

import { motion } from "framer-motion";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function TermsOfService() {
    return (
        <div className="min-h-screen bg-zinc-950 text-zinc-300 p-6 md:p-12">
            <div className="max-w-3xl mx-auto space-y-8">
                {/* Header */}
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="space-y-4"
                >
                    <Link href="/" className="inline-flex items-center text-sm text-zinc-500 hover:text-white transition-colors gap-2">
                        <ArrowLeft size={16} /> Back to Home
                    </Link>
                    <h1 className="text-4xl font-bold text-white tracking-tight">Terms of Service for Kyra</h1>
                    <p className="text-zinc-500">Effective Date: December 26, 2025</p>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className="prose prose-invert prose-zinc max-w-none space-y-8"
                >
                    <p>
                        Welcome to Kyra. By using our "Personal Email Operating System," you agree to the following terms.
                        If you do not agree, do not authorize the Service to access your accounts.
                    </p>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">1. Description of Service</h2>
                        <p>
                            Kyra is an AI-driven agent framework that interacts with your Google Workspace (Gmail/Calendar).
                            It provides email classification, summarization, RAG-based search, and drafting capabilities.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">2. Eligibility and Account Security</h2>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li><strong>Age:</strong> You must be at least 18 years old.</li>
                            <li><strong>Authority:</strong> You represent that you have the legal right to grant Kyra access to the Google accounts you connect.</li>
                            <li><strong>Responsibility:</strong> You are responsible for all activity that occurs under your Kyra account.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">3. AI Disclaimer and "Hallucinations"</h2>
                        <p>Kyra utilizes Large Language Models (LLMs) to process information.</p>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li><strong>Accuracy:</strong> You acknowledge that AI-generated summaries, classifications, and drafts may contain errors, inaccuracies, or "hallucinations."</li>
                            <li><strong>Human-in-the-loop:</strong> You are solely responsible for reviewing any AI-generated drafts before sending them. Kyra is not liable for the content of emails sent through the Service.</li>
                            <li><strong>No Professional Advice:</strong> Kyra is a productivity tool, not a legal, financial, or medical advisor.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">4. User Conduct and Prohibitions</h2>
                        <p>You agree not to:</p>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li>Use Kyra for any illegal purpose or to send spam.</li>
                            <li>Attempt to reverse engineer the Kyra "Three Brain" architecture.</li>
                            <li>Bypass any security measures or rate limits implemented on our API.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">5. Intellectual Property</h2>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li><strong>Our Stuff:</strong> StealthTensor retains all rights to the Kyra software, UI design, brand, and proprietary agent prompts.</li>
                            <li><strong>Your Stuff:</strong> You retain all ownership of the email content and data processed by the Service. You grant us a limited license to process this data solely to provide the Service to you.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">6. Limitation of Liability</h2>
                        <p>TO THE MAXIMUM EXTENT PERMITTED BY LAW, STEALTHTENSOR SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING BUT NOT LIMITED TO:</p>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li>Loss of data or emails.</li>
                            <li>Missed deadlines or scheduling errors.</li>
                            <li>Inaccurate AI interpretations of urgent matters.</li>
                            <li>Unauthorized access to your Google account resulting from your failure to secure your login credentials.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">7. Termination</h2>
                        <p>We reserve the right to suspend or terminate your access to Kyra at any time, with or without cause, especially for violations of these Terms.</p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">8. Modifications</h2>
                        <p>We may update these Terms as the Service evolves (e.g., moving from MVP to Phase 8). Continued use of the Service after changes constitute acceptance of the new Terms.</p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">9. Governing Law</h2>
                        <p>These Terms are governed by the laws of the jurisdiction in which StealthTensor is registered, without regard to conflict of law principles.</p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">10. Contact</h2>
                        <p>Questions? Reach out: <a href="mailto:rayabharaputrinai@gmail.com" className="text-indigo-400 hover:text-indigo-300">rayabharaputrinai@gmail.com</a></p>
                    </section>
                </motion.div>
            </div>
        </div>
    );
}
