import { Link } from "@tanstack/react-router";

export function Logo() {
  return (
    <Link to="/" className="flex items-center gap-2 group">
      <div className="relative">
        <div className="absolute inset-0 rounded-lg blur-md opacity-60 group-hover:opacity-100 transition-opacity bg-white/20" />
        <div className="relative w-10 h-10 flex items-center justify-center">
          <img 
            src="/images/LOGO.jpg" 
            alt="VeritasAI Logo" 
            className="w-full h-full object-contain transition-transform group-hover:scale-110 drop-shadow-lg"
          />
        </div>
      </div>
      <span className="font-display font-bold text-lg tracking-tight">
        Veritas<span className="gradient-text">AI</span>
      </span>
    </Link>
  );
}
