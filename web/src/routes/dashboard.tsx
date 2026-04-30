import { createFileRoute, Outlet, useNavigate, Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Shield, LogOut, FileText, BarChart3, Sparkles } from "lucide-react";

export const Route = createFileRoute("/dashboard")({
  component: DashboardLayout,
});

function DashboardLayout() {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const userData = localStorage.getItem("user");

    if (!token || !userData) {
      navigate({ to: "/auth" });
      return;
    }

    setUser(JSON.parse(userData));
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate({ to: "/" });
  };

  if (!user) return null;

  const isManager = user.role === "manager" || user.role === "admin";

  return (
    <div className="min-h-screen bg-black">
      {/* Sophisticated Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#0a0a0a_1px,transparent_1px),linear-gradient(to_bottom,#0a0a0a_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]"></div>
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/5 rounded-full blur-[120px] animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-cyan-600/5 rounded-full blur-[120px] animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      {/* Header */}
      <header className="relative border-b border-gray-900 bg-black/90 backdrop-blur-2xl sticky top-0 z-50 shadow-2xl">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo and Navigation */}
            <div className="flex items-center gap-8">
              <Link to="/" className="flex items-center gap-3 group">
                <div className="relative">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl blur-lg opacity-50 group-hover:opacity-100 transition-opacity"></div>
                  <div className="relative bg-gradient-to-br from-blue-600 to-cyan-600 p-2 rounded-xl">
                    <Shield className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div>
                  <span className="text-xl font-bold bg-gradient-to-r from-white via-blue-100 to-cyan-100 bg-clip-text text-transparent">
                    Verity AI
                  </span>
                  <p className="text-[10px] text-gray-600 -mt-0.5 tracking-wider uppercase">Dashboard</p>
                </div>
              </Link>
              
              <nav className="hidden md:flex gap-2">
                <Link
                  to="/dashboard"
                  className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-blue-600/10 text-gray-400 hover:text-blue-400 font-medium transition-all duration-300 border border-transparent hover:border-blue-600/20"
                >
                  <FileText className="h-4 w-4" />
                  {isManager ? "Applications" : "My Applications"}
                </Link>
                {isManager && (
                  <Link
                    to="/dashboard"
                    className="flex items-center gap-2 px-4 py-2 rounded-lg hover:bg-cyan-600/10 text-gray-400 hover:text-cyan-400 font-medium transition-all duration-300 border border-transparent hover:border-cyan-600/20"
                  >
                    <BarChart3 className="h-4 w-4" />
                    Analytics
                  </Link>
                )}
              </nav>
            </div>

            {/* User Info and Logout */}
            <div className="flex items-center gap-4">
              <div className="hidden sm:flex items-center gap-3 px-4 py-2 bg-gray-900/50 backdrop-blur-xl border border-gray-800 rounded-lg">
                <div className="h-10 w-10 rounded-lg bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center text-white font-bold shadow-lg">
                  {user.name.charAt(0).toUpperCase()}
                </div>
                <div className="text-right">
                  <p className="font-semibold text-white">{user.name}</p>
                  <p className="text-xs text-gray-500 capitalize flex items-center gap-1.5">
                    <span className={`h-2 w-2 rounded-full ${isManager ? 'bg-cyan-400' : 'bg-blue-400'} animate-pulse`}></span>
                    {user.role}
                  </p>
                </div>
              </div>
              <Button 
                variant="ghost" 
                size="icon" 
                onClick={handleLogout}
                className="hover:bg-red-600/10 hover:text-red-400 text-gray-400 transition-all duration-300 border border-transparent hover:border-red-600/20"
              >
                <LogOut className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="relative container mx-auto px-6 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="relative border-t border-gray-900 bg-black/90 backdrop-blur-xl py-6 mt-12">
        <div className="container mx-auto px-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Shield className="h-5 w-5 text-blue-400" />
            <span className="font-bold text-white">Verity AI</span>
          </div>
          <p className="text-sm text-gray-500">© 2026 Verity AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
