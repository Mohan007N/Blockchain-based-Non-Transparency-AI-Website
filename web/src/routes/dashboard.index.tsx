import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Upload, FileText, CheckCircle, XCircle, Clock, TrendingUp, AlertCircle, Lock, Sparkles } from "lucide-react";
import { toast } from "sonner";

export const Route = createFileRoute("/dashboard/")({
  component: DashboardPage,
});

function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const [applications, setApplications] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [activeTab, setActiveTab] = useState("all");

  useEffect(() => {
    const userData = localStorage.getItem("user");
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      
      if (parsedUser.role === "manager" || parsedUser.role === "admin") {
        fetchManagerApplications();
        fetchManagerStats();
      } else {
        fetchMyApplications();
      }
    }
  }, []);

  const fetchMyApplications = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/api/loans/applications", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.success) {
        setApplications(data.applications);
      }
    } catch (error) {
      toast.error("Failed to fetch applications");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchManagerApplications = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/api/manager/all", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.success) {
        setApplications(data.applications);
      }
    } catch (error) {
      toast.error("Failed to fetch applications");
    } finally {
      setIsLoading(false);
    }
  };

  const fetchManagerStats = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/api/manager/stats", {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.success) {
        setStats(data.stats);
      }
    } catch (error) {
      console.error("Failed to fetch stats");
    }
  };

  const handleApplyLoan = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsUploading(true);

    const formData = new FormData(e.currentTarget);
    const token = localStorage.getItem("token");

    try {
      const response = await fetch("http://localhost:5000/api/loans/apply", {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        toast.success(data.message);
        fetchMyApplications();
        (e.target as HTMLFormElement).reset();
      } else {
        toast.error(data.detail || "Application failed");
      }
    } catch (error) {
      toast.error("Connection error. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleManagerAction = async (applicationId: string, action: string) => {
    const comment = prompt(`Enter comment for ${action}:`);
    if (!comment) return;

    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/api/manager/approve", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ application_id: applicationId, action, comment }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success(data.message);
        fetchManagerApplications();
        fetchManagerStats();
      } else {
        toast.error(data.detail || "Action failed");
      }
    } catch (error) {
      toast.error("Connection error. Please try again.");
    }
  };

  const isManager = user?.role === "manager" || user?.role === "admin";

  const filteredApplications = applications.filter((app) => {
    if (activeTab === "all") return true;
    if (activeTab === "pending") return app.status === "pending_manager_approval";
    if (activeTab === "approved") return app.status === "approved";
    if (activeTab === "rejected") return app.status === "rejected";
    return true;
  });

  return (
    <div className="space-y-8">
      {/* Welcome Banner (Client Only) */}
      {!isManager && (
        <div className="relative bg-gradient-to-r from-blue-600 via-cyan-600 to-purple-600 rounded-2xl p-8 text-white shadow-2xl shadow-blue-500/50 overflow-hidden group hover:shadow-blue-500/70 transition-all duration-500">
          <div className="absolute inset-0 bg-grid-white/10"></div>
          <div className="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-full blur-3xl group-hover:scale-150 transition-transform duration-700"></div>
          <div className="relative z-10">
            <h2 className="text-3xl font-bold mb-2 flex items-center gap-3">
              Welcome, {user?.name}! 
              <Sparkles className="h-6 w-6 animate-spin" style={{ animationDuration: '3s' }} />
            </h2>
            <p className="text-blue-100 text-lg">
              Apply for a loan securely with our AI-powered verification system
            </p>
          </div>
        </div>
      )}

      {/* Statistics Cards (Manager Only) */}
      {isManager && stats && (
        <div>
          <h2 className="text-3xl font-bold text-white mb-6 flex items-center gap-3">
            Dashboard Overview
            <div className="h-3 w-3 bg-green-400 rounded-full animate-pulse"></div>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <StatCard
              title="Total Applications"
              value={stats.total}
              icon={<FileText className="h-5 w-5" />}
              color="blue"
              subtitle="All time"
            />
            <StatCard
              title="Pending Review"
              value={stats.pending}
              icon={<Clock className="h-5 w-5" />}
              color="yellow"
              subtitle="Awaiting approval"
            />
            <StatCard
              title="Approved"
              value={stats.approved}
              icon={<CheckCircle className="h-5 w-5" />}
              color="green"
              subtitle="Approved"
            />
            <StatCard
              title="Rejected"
              value={stats.rejected}
              icon={<XCircle className="h-5 w-5" />}
              color="red"
              subtitle="Not approved"
            />
          </div>
        </div>
      )}

      {/* Application Form (Client Only) */}
      {!isManager && (
        <Card className="bg-slate-800/50 backdrop-blur-xl border-white/10 shadow-2xl shadow-blue-500/20 hover:shadow-blue-500/40 transition-all duration-500">
          <CardHeader className="border-b border-white/10 bg-gradient-to-r from-blue-900/50 to-purple-900/50">
            <CardTitle className="text-2xl text-white flex items-center gap-2">
              <Upload className="h-6 w-6 text-cyan-400" />
              Apply for Loan
            </CardTitle>
            <CardDescription className="text-slate-300">
              Upload your income certificate for secure verification
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <form onSubmit={handleApplyLoan} className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <Label htmlFor="loan_type" className="font-semibold text-slate-300">Loan Type</Label>
                  <select
                    id="loan_type"
                    name="loan_type"
                    className="flex h-11 w-full rounded-lg border bg-slate-700/50 border-slate-600 text-white px-4 py-2 text-sm mt-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50 transition-all"
                    required
                  >
                    <option value="personal">Personal Loan (5x salary)</option>
                    <option value="home">Home Loan (60x salary)</option>
                    <option value="auto">Auto Loan (10x salary)</option>
                    <option value="business">Business Loan (8x salary)</option>
                    <option value="education">Education Loan (12x salary)</option>
                  </select>
                </div>
                <div>
                  <Label htmlFor="loan_amount" className="font-semibold text-slate-300">Loan Amount (₹)</Label>
                  <Input
                    id="loan_amount"
                    name="loan_amount"
                    type="number"
                    placeholder="200000"
                    required
                    min="10000"
                    className="mt-2 h-11 bg-slate-700/50 border-slate-600 text-white placeholder:text-slate-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/50"
                  />
                </div>
              </div>
              <div>
                <Label htmlFor="income_certificate" className="font-semibold text-slate-300">
                  Income Certificate (PDF/JPEG/PNG)
                </Label>
                <Input
                  id="income_certificate"
                  name="income_certificate"
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  required
                  className="mt-2 h-11 bg-slate-700/50 border-slate-600 text-white file:text-white cursor-pointer hover:border-blue-500 transition-colors"
                />
                <p className="text-xs text-slate-400 mt-2 flex items-center gap-2">
                  <Lock className="h-3.5 w-3.5 text-green-400" />
                  Your salary is processed securely and never stored
                </p>
              </div>
              <Button 
                type="submit" 
                disabled={isUploading} 
                className="w-full h-12 bg-gradient-to-r from-blue-600 via-cyan-600 to-purple-600 hover:from-blue-700 hover:via-cyan-700 hover:to-purple-700 text-white shadow-lg shadow-blue-500/50 hover:shadow-xl hover:shadow-blue-500/70 transition-all duration-300 hover:scale-105"
              >
                {isUploading ? (
                  <>
                    <Upload className="mr-2 h-5 w-5 animate-spin" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload className="mr-2 h-5 w-5" />
                    Submit Application
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Applications List */}
      <Card className="bg-slate-800/50 backdrop-blur-xl border-white/10 shadow-2xl shadow-blue-500/20">
        <CardHeader className="border-b border-white/10 bg-gradient-to-r from-slate-900/50 to-blue-900/50">
          <CardTitle className="text-2xl text-white">{isManager ? "Loan Applications" : "My Applications"}</CardTitle>
          <CardDescription className="text-slate-300">
            {isManager
              ? "Review and manage loan applications"
              : "Track your loan application status"}
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-6">
          {isManager ? (
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-4 mb-6 bg-slate-700/50 p-1.5">
                <TabsTrigger 
                  value="all"
                  className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-cyan-600 data-[state=active]:text-white text-slate-300"
                >
                  All ({applications.length})
                </TabsTrigger>
                <TabsTrigger 
                  value="pending"
                  className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-yellow-600 data-[state=active]:to-orange-600 data-[state=active]:text-white text-slate-300"
                >
                  Pending ({applications.filter(a => a.status === "pending_manager_approval").length})
                </TabsTrigger>
                <TabsTrigger 
                  value="approved"
                  className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-green-600 data-[state=active]:to-emerald-600 data-[state=active]:text-white text-slate-300"
                >
                  Approved ({applications.filter(a => a.status === "approved").length})
                </TabsTrigger>
                <TabsTrigger 
                  value="rejected"
                  className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-red-600 data-[state=active]:to-pink-600 data-[state=active]:text-white text-slate-300"
                >
                  Rejected ({applications.filter(a => a.status === "rejected").length})
                </TabsTrigger>
              </TabsList>

              <TabsContent value={activeTab}>
                {isLoading ? (
                  <div className="text-center py-16">
                    <div className="inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
                    <p className="mt-4 text-slate-300 text-lg">Loading...</p>
                  </div>
                ) : filteredApplications.length === 0 ? (
                  <div className="text-center py-16">
                    <AlertCircle className="h-16 w-16 text-slate-500 mx-auto mb-4" />
                    <p className="text-slate-300 text-lg">No applications found</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {filteredApplications.map((app) => (
                      <ApplicationCard
                        key={app.id}
                        app={app}
                        isManager={isManager}
                        onAction={handleManagerAction}
                      />
                    ))}
                  </div>
                )}
              </TabsContent>
            </Tabs>
          ) : (
            <>
              {isLoading ? (
                <div className="text-center py-16">
                  <div className="inline-block h-12 w-12 animate-spin rounded-full border-4 border-solid border-blue-600 border-r-transparent"></div>
                  <p className="mt-4 text-slate-300 text-lg">Loading...</p>
                </div>
              ) : applications.length === 0 ? (
                <div className="text-center py-16">
                  <AlertCircle className="h-16 w-16 text-slate-500 mx-auto mb-4" />
                  <p className="text-slate-300 text-lg">No applications yet</p>
                  <p className="text-sm text-slate-400 mt-2">Submit your first application above</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {applications.map((app) => (
                    <ApplicationCard
                      key={app.id}
                      app={app}
                      isManager={isManager}
                      onAction={handleManagerAction}
                    />
                  ))}
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function StatCard({ title, value, icon, color, subtitle }: {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: string;
  subtitle: string;
}) {
  const colorClasses: Record<string, { bg: string; text: string; glow: string }> = {
    blue: { bg: "from-blue-600 to-cyan-600", text: "text-blue-400", glow: "shadow-blue-500/50" },
    yellow: { bg: "from-yellow-600 to-orange-600", text: "text-yellow-400", glow: "shadow-yellow-500/50" },
    green: { bg: "from-green-600 to-emerald-600", text: "text-green-400", glow: "shadow-green-500/50" },
    red: { bg: "from-red-600 to-pink-600", text: "text-red-400", glow: "shadow-red-500/50" },
  };

  const colors = colorClasses[color];

  return (
    <Card className={`bg-slate-800/50 backdrop-blur-xl border-white/10 hover:border-white/30 transition-all duration-500 hover:scale-105 hover:-translate-y-1 shadow-xl ${colors.glow} hover:shadow-2xl group`}>
      <CardContent className="pt-6">
        <div className="flex items-center justify-between mb-4">
          <div className={`p-3 rounded-xl bg-gradient-to-br ${colors.bg} ${colors.text} shadow-lg group-hover:scale-110 transition-transform duration-300`}>
            {icon}
          </div>
        </div>
        <div>
          <p className="text-sm text-slate-400 mb-2">{title}</p>
          <p className={`text-4xl font-bold ${colors.text} mb-1`}>{value}</p>
          <p className="text-xs text-slate-500">{subtitle}</p>
        </div>
      </CardContent>
    </Card>
  );
}

function ApplicationCard({ app, isManager, onAction }: any) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-xl border border-white/10 rounded-xl p-6 hover:border-white/30 hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:scale-[1.02] group">
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-4 flex-1">
          {/* User Info (Manager View) */}
          {isManager && app.user && (
            <div className="flex items-center gap-3 pb-4 border-b border-white/10">
              <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-lg shadow-lg group-hover:scale-110 transition-transform duration-300">
                {app.user.name.charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="font-bold text-white text-lg">{app.user.name}</p>
                <p className="text-sm text-slate-400">{app.user.email}</p>
              </div>
            </div>
          )}

          {/* Loan Details */}
          <div className="flex items-center gap-6 flex-wrap">
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-blue-400" />
              <span className="font-semibold capitalize text-white">{app.loan_type} Loan</span>
            </div>
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-cyan-400" />
              <span className="text-xl font-bold text-white">₹{app.loan_amount?.toLocaleString()}</span>
            </div>
            <StatusBadge status={app.status} />
          </div>

          {/* Verification Details */}
          {app.verification_result && (
            <div className="grid grid-cols-2 gap-4 p-4 bg-slate-700/50 rounded-xl border border-white/10">
              <div>
                <p className="text-xs text-slate-400 mb-1">Max Eligible</p>
                <p className="font-bold text-white text-lg">
                  ₹{app.verification_result.max_eligible_loan?.toLocaleString()}
                </p>
              </div>
              <div>
                <p className="text-xs text-slate-400 mb-1">Utilization</p>
                <p className="font-bold text-white text-lg">
                  {app.verification_result.utilization_percent}%
                </p>
              </div>
            </div>
          )}

          {/* Reason/Comment */}
          {app.reason && (
            <div className="p-4 bg-blue-500/20 border-l-4 border-blue-500 rounded-lg">
              <p className="text-sm text-slate-200">{app.reason}</p>
            </div>
          )}

          {/* Blockchain Hash */}
          {app.blockchain_hash && (
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <Lock className="h-4 w-4 text-green-400" />
              <span>Blockchain:</span>
              <code className="font-mono bg-slate-700/50 px-3 py-1 rounded-lg border border-white/10">
                {app.blockchain_hash.substring(0, 20)}...
              </code>
            </div>
          )}

          {/* Timestamp */}
          {app.created_at && (
            <p className="text-xs text-slate-500">
              Applied on {new Date(app.created_at).toLocaleString()}
            </p>
          )}
        </div>

        {/* Action Buttons (Manager View - Pending Only) */}
        {isManager && app.status === "pending_manager_approval" && (
          <div className="flex flex-col gap-3">
            <Button
              size="sm"
              onClick={() => onAction(app.application_id, "approve")}
              className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white shadow-lg shadow-green-500/50 hover:shadow-xl hover:shadow-green-500/70 transition-all duration-300 hover:scale-105"
            >
              <CheckCircle className="h-4 w-4 mr-1" />
              Approve
            </Button>
            <Button
              size="sm"
              onClick={() => onAction(app.application_id, "reject")}
              className="bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white shadow-lg shadow-red-500/50 hover:shadow-xl hover:shadow-red-500/70 transition-all duration-300 hover:scale-105"
            >
              <XCircle className="h-4 w-4 mr-1" />
              Reject
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const variants: Record<string, { color: string; icon: React.ReactNode; label: string }> = {
    pending_manager_approval: {
      color: "bg-gradient-to-r from-yellow-600 to-orange-600 text-white shadow-lg shadow-yellow-500/50",
      icon: <Clock className="h-4 w-4" />,
      label: "Pending"
    },
    approved: {
      color: "bg-gradient-to-r from-green-600 to-emerald-600 text-white shadow-lg shadow-green-500/50",
      icon: <CheckCircle className="h-4 w-4" />,
      label: "Approved"
    },
    rejected: {
      color: "bg-gradient-to-r from-red-600 to-pink-600 text-white shadow-lg shadow-red-500/50",
      icon: <XCircle className="h-4 w-4" />,
      label: "Rejected"
    },
  };

  const variant = variants[status] || variants.pending_manager_approval;

  return (
    <Badge className={`${variant.color} flex items-center gap-2 px-3 py-1.5 text-sm font-semibold border-0`}>
      {variant.icon}
      {variant.label}
    </Badge>
  );
}
