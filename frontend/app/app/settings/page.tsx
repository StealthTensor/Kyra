"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuthStore } from "@/store/useAuthStore";
import { api } from "@/lib/api";
import { Settings, User, Mail, Bell, Shield, LogOut, ArrowLeft } from "lucide-react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function SettingsPage() {
    const { user, logout } = useAuthStore();
    const router = useRouter();
    const [activeTab, setActiveTab] = useState<"profile" | "accounts" | "notifications" | "organization">("profile");

    const handleLogout = () => {
        logout();
        router.push("/auth/login");
    };

    return (
        <div className="min-h-screen bg-zinc-950 p-4 pb-24">
            <div className="max-w-2xl mx-auto space-y-6">
                <div className="flex items-center gap-4 mb-6">
                    <Link href="/app/dashboard">
                        <Button variant="ghost" size="icon" className="text-zinc-400 hover:text-white">
                            <ArrowLeft className="h-5 w-5" />
                        </Button>
                    </Link>
                    <h1 className="text-2xl font-bold text-white">Settings</h1>
                </div>

                <div className="grid grid-cols-4 gap-2 mb-6">
                    <Button
                        variant={activeTab === "profile" ? "default" : "outline"}
                        onClick={() => setActiveTab("profile")}
                        className="flex flex-col items-center gap-1 h-auto py-3"
                    >
                        <User className="h-4 w-4" />
                        <span className="text-xs">Profile</span>
                    </Button>
                    <Button
                        variant={activeTab === "accounts" ? "default" : "outline"}
                        onClick={() => setActiveTab("accounts")}
                        className="flex flex-col items-center gap-1 h-auto py-3"
                    >
                        <Mail className="h-4 w-4" />
                        <span className="text-xs">Accounts</span>
                    </Button>
                    <Button
                        variant={activeTab === "notifications" ? "default" : "outline"}
                        onClick={() => setActiveTab("notifications")}
                        className="flex flex-col items-center gap-1 h-auto py-3"
                    >
                        <Bell className="h-4 w-4" />
                        <span className="text-xs">Notify</span>
                    </Button>
                    <Button
                        variant={activeTab === "organization" ? "default" : "outline"}
                        onClick={() => setActiveTab("organization")}
                        className="flex flex-col items-center gap-1 h-auto py-3"
                    >
                        <Shield className="h-4 w-4" />
                        <span className="text-xs">Org</span>
                    </Button>
                </div>

                {activeTab === "profile" && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        <Card className="border-zinc-800 bg-zinc-900/50">
                            <CardHeader>
                                <CardTitle className="text-lg">Profile Information</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="space-y-2">
                                    <label className="text-sm text-zinc-400">Name</label>
                                    <Input
                                        value={user?.name || ""}
                                        className="bg-zinc-950 border-zinc-800 text-white"
                                        readOnly
                                    />
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm text-zinc-400">Email</label>
                                    <Input
                                        value={user?.email || ""}
                                        className="bg-zinc-950 border-zinc-800 text-white"
                                        readOnly
                                    />
                                </div>
                                <Button className="w-full bg-indigo-600 hover:bg-indigo-700">
                                    Save Changes
                                </Button>
                            </CardContent>
                        </Card>
                    </motion.div>
                )}

                {activeTab === "accounts" && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        <Card className="border-zinc-800 bg-zinc-900/50">
                            <CardHeader>
                                <CardTitle className="text-lg">Email Accounts</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="p-4 bg-zinc-950 rounded-lg border border-zinc-800">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="font-medium text-white">{user?.email}</p>
                                            <p className="text-xs text-zinc-400">Gmail • Connected</p>
                                        </div>
                                        <Button variant="outline" size="sm" className="border-zinc-800">
                                            Manage
                                        </Button>
                                    </div>
                                </div>
                                <Button variant="outline" className="w-full border-zinc-800">
                                    Add Account
                                </Button>
                            </CardContent>
                        </Card>
                    </motion.div>
                )}

                {activeTab === "notifications" && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        <Card className="border-zinc-800 bg-zinc-900/50">
                            <CardHeader>
                                <CardTitle className="text-lg">Notification Preferences</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="font-medium text-white">Email Notifications</p>
                                        <p className="text-xs text-zinc-400">Receive notifications for urgent emails</p>
                                    </div>
                                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                                </div>
                                <div className="flex items-center justify-between">
                                    <div>
                                        <p className="font-medium text-white">Daily Digest</p>
                                        <p className="text-xs text-zinc-400">Receive daily briefing emails</p>
                                    </div>
                                    <input type="checkbox" className="w-5 h-5 rounded" defaultChecked />
                                </div>
                                <Button className="w-full bg-indigo-600 hover:bg-indigo-700">
                                    Save Preferences
                                </Button>
                            </CardContent>
                        </Card>
                    </motion.div>
                )}

                {activeTab === "organization" && (
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                    >
                        <Card className="border-zinc-800 bg-zinc-900/50">
                            <CardHeader>
                                <CardTitle className="text-lg">Organization</CardTitle>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <p className="text-sm text-zinc-400">
                                    Manage your organization settings, members, and permissions.
                                </p>
                                <Link href="/app/settings/organization">
                                    <Button className="w-full bg-indigo-600 hover:bg-indigo-700">
                                        Manage Organization
                                    </Button>
                                </Link>
                            </CardContent>
                        </Card>
                    </motion.div>
                )}

                <Card className="border-zinc-800 bg-zinc-900/50">
                    <CardContent className="pt-6">
                        <Button
                            variant="outline"
                            className="w-full border-red-500/20 text-red-400 hover:bg-red-500/10"
                            onClick={handleLogout}
                        >
                            <LogOut className="mr-2 h-4 w-4" />
                            Sign Out
                        </Button>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}

