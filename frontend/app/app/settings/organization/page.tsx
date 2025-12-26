"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuthStore } from "@/store/useAuthStore";
import { api } from "@/lib/api";
import { ArrowLeft, UserPlus, Crown, Shield, User, Eye } from "lucide-react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { toast } from "sonner";

interface Organization {
    id: string;
    name: string;
    plan_type: string;
    role: string;
}

interface Member {
    user_id: string;
    email: string;
    name: string;
    role: string;
    joined_at: string;
}

const roleIcons = {
    owner: Crown,
    admin: Shield,
    member: User,
    viewer: Eye
};

const roleColors = {
    owner: "text-yellow-400",
    admin: "text-purple-400",
    member: "text-blue-400",
    viewer: "text-zinc-400"
};

export default function OrganizationPage() {
    const { user } = useAuthStore();
    const router = useRouter();
    const [organizations, setOrganizations] = useState<Organization[]>([]);
    const [selectedOrg, setSelectedOrg] = useState<Organization | null>(null);
    const [members, setMembers] = useState<Member[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [inviteEmail, setInviteEmail] = useState("");

    useEffect(() => {
        if (!user?.email) return;
        fetchOrganizations();
    }, [user?.email]);

    useEffect(() => {
        if (selectedOrg) {
            fetchMembers(selectedOrg.id);
        }
    }, [selectedOrg]);

    const fetchOrganizations = async () => {
        try {
            setIsLoading(true);
            const response = await api.get("/organizations/");
            setOrganizations(response.data);
            if (response.data.length > 0) {
                setSelectedOrg(response.data[0]);
            }
        } catch (error) {
            console.error("Failed to fetch organizations:", error);
            toast.error("Failed to load organizations");
        } finally {
            setIsLoading(false);
        }
    };

    const fetchMembers = async (orgId: string) => {
        try {
            const response = await api.get(`/organizations/${orgId}/members`);
            setMembers(response.data);
        } catch (error) {
            console.error("Failed to fetch members:", error);
            toast.error("Failed to load members");
        }
    };

    const handleInvite = async () => {
        if (!selectedOrg || !inviteEmail) return;

        try {
            const response = await api.post(`/organizations/${selectedOrg.id}/members`, {
                user_id: inviteEmail,
                role: "member"
            });
            toast.success("Member invited");
            setInviteEmail("");
            fetchMembers(selectedOrg.id);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || "Failed to invite member");
        }
    };

    const handleRoleChange = async (userId: string, newRole: string) => {
        if (!selectedOrg) return;

        try {
            await api.patch(`/organizations/${selectedOrg.id}/members/${userId}`, {
                role: newRole
            });
            toast.success("Role updated");
            fetchMembers(selectedOrg.id);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || "Failed to update role");
        }
    };

    const handleRemoveMember = async (userId: string) => {
        if (!selectedOrg) return;

        try {
            await api.delete(`/organizations/${selectedOrg.id}/members/${userId}`);
            toast.success("Member removed");
            fetchMembers(selectedOrg.id);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || "Failed to remove member");
        }
    };

    return (
        <div className="min-h-screen bg-zinc-950 p-4 pb-24">
            <div className="max-w-3xl mx-auto space-y-6">
                <div className="flex items-center gap-4 mb-6">
                    <Link href="/app/settings">
                        <Button variant="ghost" size="icon" className="text-zinc-400 hover:text-white">
                            <ArrowLeft className="h-5 w-5" />
                        </Button>
                    </Link>
                    <h1 className="text-2xl font-bold text-white">Organization Management</h1>
                </div>

                {isLoading ? (
                    <div className="text-center text-zinc-400 py-8">Loading...</div>
                ) : organizations.length === 0 ? (
                    <Card className="border-zinc-800 bg-zinc-900/50">
                        <CardContent className="pt-6 text-center">
                            <p className="text-zinc-400 mb-4">No organizations found</p>
                            <Button className="bg-indigo-600 hover:bg-indigo-700">
                                Create Organization
                            </Button>
                        </CardContent>
                    </Card>
                ) : (
                    <>
                        <Card className="border-zinc-800 bg-zinc-900/50">
                            <CardHeader>
                                <CardTitle className="text-lg">Select Organization</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-2">
                                    {organizations.map((org) => (
                                        <Button
                                            key={org.id}
                                            variant={selectedOrg?.id === org.id ? "default" : "outline"}
                                            className="w-full justify-start"
                                            onClick={() => setSelectedOrg(org)}
                                        >
                                            {org.name} <span className="ml-2 text-xs opacity-70">({org.role})</span>
                                        </Button>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>

                        {selectedOrg && (
                            <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                            >
                                <Card className="border-zinc-800 bg-zinc-900/50">
                                    <CardHeader>
                                        <CardTitle className="text-lg flex items-center justify-between">
                                            <span>Members</span>
                                            {(selectedOrg.role === "owner" || selectedOrg.role === "admin") && (
                                                <Button size="sm" className="bg-indigo-600 hover:bg-indigo-700">
                                                    <UserPlus className="mr-2 h-4 w-4" />
                                                    Invite
                                                </Button>
                                            )}
                                        </CardTitle>
                                    </CardHeader>
                                    <CardContent className="space-y-4">
                                        {(selectedOrg.role === "owner" || selectedOrg.role === "admin") && (
                                            <div className="flex gap-2">
                                                <Input
                                                    placeholder="Email address"
                                                    value={inviteEmail}
                                                    onChange={(e) => setInviteEmail(e.target.value)}
                                                    className="bg-zinc-950 border-zinc-800 text-white"
                                                />
                                                <Button onClick={handleInvite} className="bg-indigo-600 hover:bg-indigo-700">
                                                    Invite
                                                </Button>
                                            </div>
                                        )}

                                        <div className="space-y-2">
                                            {members.map((member) => {
                                                const RoleIcon = roleIcons[member.role as keyof typeof roleIcons] || User;
                                                const roleColor = roleColors[member.role as keyof typeof roleColors] || "text-zinc-400";
                                                const isCurrentUser = member.email === user?.email;

                                                return (
                                                    <div
                                                        key={member.user_id}
                                                        className="flex items-center justify-between p-3 bg-zinc-950 rounded-lg border border-zinc-800"
                                                    >
                                                        <div className="flex items-center gap-3">
                                                            <div className={`w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white text-xs font-semibold`}>
                                                                {member.name?.charAt(0)?.toUpperCase() || member.email.charAt(0).toUpperCase()}
                                                            </div>
                                                            <div>
                                                                <p className="text-sm font-medium text-white">
                                                                    {member.name || member.email}
                                                                    {isCurrentUser && <span className="ml-2 text-xs text-zinc-400">(You)</span>}
                                                                </p>
                                                                <p className="text-xs text-zinc-400">{member.email}</p>
                                                            </div>
                                                        </div>
                                                        <div className="flex items-center gap-2">
                                                            <RoleIcon className={`h-4 w-4 ${roleColor}`} />
                                                            <span className={`text-xs font-medium ${roleColor}`}>
                                                                {member.role}
                                                            </span>
                                                            {(selectedOrg.role === "owner" || selectedOrg.role === "admin") && !isCurrentUser && (
                                                                <div className="flex gap-1">
                                                                    <select
                                                                        value={member.role}
                                                                        onChange={(e) => handleRoleChange(member.user_id, e.target.value)}
                                                                        className="text-xs bg-zinc-900 border-zinc-800 rounded px-2 py-1 text-zinc-300"
                                                                    >
                                                                        <option value="viewer">Viewer</option>
                                                                        <option value="member">Member</option>
                                                                        <option value="admin">Admin</option>
                                                                        {selectedOrg.role === "owner" && <option value="owner">Owner</option>}
                                                                    </select>
                                                                    <Button
                                                                        variant="ghost"
                                                                        size="sm"
                                                                        className="text-red-400 hover:text-red-300"
                                                                        onClick={() => handleRemoveMember(member.user_id)}
                                                                    >
                                                                        Remove
                                                                    </Button>
                                                                </div>
                                                            )}
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </CardContent>
                                </Card>
                            </motion.div>
                        )}
                    </>
                )}
            </div>
        </div>
    );
}

