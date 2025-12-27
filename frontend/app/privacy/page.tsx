"use client";

import { motion } from "framer-motion";
import { ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function PrivacyPolicy() {
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
                    <h1 className="text-4xl font-bold text-white tracking-tight">Privacy Policy for Kyra</h1>
                    <p className="text-zinc-500">Last Updated: December 26, 2025</p>
                </motion.div>

                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.1 }}
                    className="prose prose-invert prose-zinc max-w-none space-y-8"
                >
                    <p>
                        At StealthTensor ("we," "our," or "us"), your privacy is our primary engineering constraint.
                        This Privacy Policy explains how Kyra (the "Service") collects, uses, and protects your information,
                        specifically regarding your Gmail and Google Calendar data.
                    </p>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">1. Information We Collect</h2>

                        <h3 className="text-lg font-medium text-white mt-4 mb-2">A. Google User Data</h3>
                        <p>When you authorize Kyra via Google OAuth, we access:</p>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li><strong>Email Address:</strong> To identify your account.</li>
                            <li><strong>Email Metadata:</strong> Subject lines, sender/recipient info, timestamps, and thread IDs.</li>
                            <li><strong>Email Content:</strong> Cleaned text from your emails to enable AI classification, summarization, and RAG (Retrieval-Augmented Generation).</li>
                            <li><strong>Calendar Data:</strong> To detect deadlines and schedule events at your command.</li>
                        </ul>

                        <h3 className="text-lg font-medium text-white mt-4 mb-2">B. Agent Memory & Interaction Data</h3>
                        <p>To improve the "Intelligence Layer," we store:</p>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li><strong>Interaction Logs:</strong> Whether you opened, ignored, or replied to a specific email.</li>
                            <li><strong>Preference Memory:</strong> Structured rules you teach the agent (e.g., "Always mark professor emails as urgent").</li>
                            <li><strong>Vector Embeddings:</strong> Mathematical representations of your emails stored in our vector database (pgvector) to provide context for AI queries.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">2. How We Use Your Information</h2>
                        <p>We use your data strictly to provide the "Personal Email Operating System" experience:</p>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li><strong>AI Classification:</strong> Categorizing mail into Priority, Informational, or Promotional buckets.</li>
                            <li><strong>Contextual Retrieval:</strong> Searching your history to answer questions like "Why is this urgent?"</li>
                            <li><strong>Draft Generation:</strong> Creating suggested replies based on thread context.</li>
                            <li><strong>Proactive Nudges:</strong> Identifying upcoming deadlines from your email content.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">3. Data Sharing and Third Parties</h2>

                        <h3 className="text-lg font-medium text-white mt-4 mb-2">A. LLM Providers</h3>
                        <p>To process your requests, Kyra sends cleaned email text to Large Language Model providers (e.g., Google Gemini, OpenAI).</p>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li><strong>Privacy-Respecting Mode:</strong> We strive to send only the minimum context required.</li>
                            <li><strong>No Training:</strong> We specifically use API tiers that do not use customer data to train their foundational models.</li>
                        </ul>

                        <h3 className="text-lg font-medium text-white mt-4 mb-2">B. No Sale of Data</h3>
                        <p>We never sell your email content, metadata, or personal information to third parties or advertisers.</p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">4. Google API Limited Use Disclosure</h2>
                        <p>
                            Kyra's use and transfer to any other app of information received from Google APIs will adhere to the
                            <a href="https://developers.google.com/terms/api-services-user-data-policy" target="_blank" className="text-indigo-400 hover:text-indigo-300 mx-1">
                                Google API Services User Data Policy
                            </a>, including the Limited Use requirements. We do not use Google user data to serve advertisements or for any purpose other than providing and improving the Service's core functionality.
                        </p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">5. Data Retention and Deletion</h2>
                        <ul className="list-disc pl-5 space-y-1 text-zinc-400">
                            <li><strong>Storage:</strong> Data is stored in our secured PostgreSQL database and vector store.</li>
                            <li><strong>Deletion:</strong> You may disconnect your Google accounts at any time. Upon request for account deletion, we will purge your email metadata, cleaned text, and vector embeddings from our active databases within 30 days.</li>
                        </ul>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">6. Security</h2>
                        <p>We implement industry-standard encryption for data at rest (AES-256) and data in transit (TLS 1.2+). OAuth tokens are stored in encrypted database fields.</p>
                    </section>

                    <section>
                        <h2 className="text-xl font-semibold text-white mb-3">7. Contact</h2>
                        <p>For privacy-related inquiries, reach out to StealthTensor at: <a href="mailto:rayabharaputrinai@gmail.com" className="text-indigo-400 hover:text-indigo-300">rayabharaputrinai@gmail.com</a></p>
                    </section>
                </motion.div>
            </div>
        </div>
    );
}
