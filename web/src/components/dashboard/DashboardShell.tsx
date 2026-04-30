import { ReactNode } from "react";
import { Logo } from "@/components/site/Logo";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";
import { LogOut, User, Briefcase } from "lucide-react";

export function DashboardShell({ children }: { children: ReactNode }) {
  const { user, role, signOut } = useAuth();

  // Get role icon based on actual user role
  const RoleIcon = role === "manager" ? Briefcase : User;
  const roleLabel = role === "manager" ? "Manager" : "Client";

  return (
    <div className="min-h-screen">
      {/* Top bar */}
      <header className="sticky top-0 z-40 glass-strong border-b border-white/5">
        <div className="mx-auto max-w-7xl px-6 py-3 flex items-center justify-between gap-4">
          <Logo />

          {/* Show current role (read-only) */}
          <div className="hidden md:flex items-center gap-1 p-1 bg-white/5 border border-white/10 rounded-xl">
            <div className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-lg ${
              role === "manager"
                ? "bg-amber-500/20 text-amber-300 border border-amber-500/30"
                : "bg-primary/20 text-primary border border-primary/30"
            }`}>
              <RoleIcon className="w-3.5 h-3.5" />
              {roleLabel}
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-right hidden sm:block">
              <div className="text-sm font-medium">{user?.user_metadata?.full_name ?? user?.email?.split("@")[0]}</div>
              <div className="text-xs text-muted-foreground capitalize">{roleLabel}</div>
            </div>
            <div className="w-9 h-9 rounded-full bg-gradient-primary flex items-center justify-center text-sm font-bold text-primary-foreground">
              {(user?.email?.[0] ?? "U").toUpperCase()}
            </div>
            <Button variant="ghost" size="icon" onClick={() => signOut()}>
              <LogOut className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">{children}</main>
    </div>
  );
}
