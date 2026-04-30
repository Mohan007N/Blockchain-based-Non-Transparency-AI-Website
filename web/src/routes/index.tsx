import { createFileRoute, Link } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";
import { Shield, CheckCircle, Lock, Zap, TrendingUp, Users, ArrowRight, Award, BarChart3, FileCheck, Sparkles, ChevronRight, Star, Globe, Building2, Clock, Target, Briefcase } from "lucide-react";
import { useState, useEffect } from "react";

export const Route = createFileRoute("/")({
  component: HomePage,
});

function HomePage() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="min-h-screen bg-black">
      {/* Sophisticated Grid Background */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#0a0a0a_1px,transparent_1px),linear-gradient(to_bottom,#0a0a0a_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_0%,#000_70%,transparent_110%)]"></div>
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-blue-600/5 rounded-full blur-[150px] animate-pulse"></div>
        <div className="absolute bottom-0 right-1/4 w-[600px] h-[600px] bg-cyan-600/5 rounded-full blur-[150px] animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      {/* Premium Header */}
      <header className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-black/90 backdrop-blur-2xl transition-all duration-300">
        <div className="container mx-auto px-6 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 group cursor-pointer">
              <div className="relative">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-xl blur-lg opacity-50 group-hover:opacity-100 transition-opacity"></div>
                <div className="relative bg-gradient-to-br from-blue-600 to-cyan-600 p-2.5 rounded-xl">
                  <Shield className="h-6 w-6 text-white" />
                </div>
              </div>
              <div>
                <span className="text-2xl font-bold bg-gradient-to-r from-white via-blue-100 to-cyan-100 bg-clip-text text-transparent">Verity AI</span>
                <p className="text-[10px] text-gray-600 -mt-0.5 tracking-wider uppercase">Secure Lending Platform</p>
              </div>
            </div>
            
            <nav className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-sm text-gray-400 hover:text-white transition-colors font-medium">Features</a>
              <a href="#how-it-works" className="text-sm text-gray-400 hover:text-white transition-colors font-medium">How It Works</a>
              <a href="#security" className="text-sm text-gray-400 hover:text-white transition-colors font-medium">Security</a>
              <a href="#stats" className="text-sm text-gray-400 hover:text-white transition-colors font-medium">About</a>
            </nav>

            <div className="flex items-center gap-3">
              <Link to="/auth">
                <Button variant="ghost" className="text-gray-300 hover:text-white hover:bg-white/5">
                  Sign In
                </Button>
              </Link>
              <Link to="/auth">
                <Button className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white shadow-lg shadow-blue-600/30 hover:shadow-blue-600/50 transition-all duration-300">
                  Get Started
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-16 items-center">
              {/* Left Content */}
              <div className="space-y-8" style={{ transform: `translateY(${scrollY * 0.1}px)` }}>
                <div className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600/10 to-cyan-600/10 backdrop-blur-xl border border-blue-500/20 rounded-full">
                  <div className="h-2 w-2 bg-green-400 rounded-full animate-pulse"></div>
                  <span className="text-sm text-blue-300 font-medium">Trusted by 10,000+ Customers</span>
                </div>
                
                <h1 className="text-6xl md:text-7xl font-bold leading-[1.1]">
                  <span className="text-white">Smart Lending</span>
                  <br />
                  <span className="bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-400 bg-clip-text text-transparent bg-[length:200%_auto] animate-gradient">
                    Made Simple
                  </span>
                </h1>
                
                <p className="text-xl text-gray-400 leading-relaxed max-w-xl">
                  Experience the future of loan verification with AI-powered document analysis, 
                  blockchain security, and instant approvals. Your financial journey starts here.
                </p>

                <div className="flex flex-wrap gap-6 pt-4">
                  <div className="flex items-center gap-3">
                    <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-blue-600/10 to-cyan-600/10 border border-blue-500/20 flex items-center justify-center">
                      <CheckCircle className="h-6 w-6 text-blue-400" />
                    </div>
                    <div>
                      <p className="text-white font-semibold">Instant Approval</p>
                      <p className="text-sm text-gray-500">Within 24 hours</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="h-12 w-12 rounded-xl bg-gradient-to-br from-cyan-600/10 to-blue-600/10 border border-cyan-500/20 flex items-center justify-center">
                      <Lock className="h-6 w-6 text-cyan-400" />
                    </div>
                    <div>
                      <p className="text-white font-semibold">Bank-Grade Security</p>
                      <p className="text-sm text-gray-500">256-bit encryption</p>
                    </div>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-4 pt-4">
                  <Link to="/auth">
                    <Button size="lg" className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white px-8 h-14 text-base font-semibold shadow-2xl shadow-blue-600/40 hover:shadow-blue-600/60 transition-all duration-300 hover:scale-105 group">
                      Apply Now
                      <ArrowRight className="ml-2 h-5 w-5 group-hover:translate-x-1 transition-transform" />
                    </Button>
                  </Link>
                  <Button size="lg" variant="outline" className="border-2 border-gray-800 bg-gray-900/50 text-white hover:bg-gray-800 hover:border-gray-700 px-8 h-14 text-base font-semibold backdrop-blur-xl">
                    Watch Demo
                  </Button>
                </div>

                {/* Trust Badges */}
                <div className="flex items-center gap-6 pt-6 border-t border-gray-900">
                  <div className="flex items-center gap-2">
                    <Star className="h-5 w-5 text-yellow-400 fill-yellow-400" />
                    <Star className="h-5 w-5 text-yellow-400 fill-yellow-400" />
                    <Star className="h-5 w-5 text-yellow-400 fill-yellow-400" />
                    <Star className="h-5 w-5 text-yellow-400 fill-yellow-400" />
                    <Star className="h-5 w-5 text-yellow-400 fill-yellow-400" />
                  </div>
                  <p className="text-sm text-gray-400">
                    <span className="text-white font-semibold">4.9/5</span> from 2,500+ reviews
                  </p>
                </div>
              </div>

              {/* Right Content - Interactive Card */}
              <div className="relative" style={{ transform: `translateY(${scrollY * -0.05}px)` }}>
                <div className="relative">
                  {/* Glow Effect */}
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-3xl blur-3xl opacity-10"></div>
                  
                  {/* Main Card */}
                  <div className="relative bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-3xl p-8 shadow-2xl">
                    <div className="space-y-6">
                      {/* Header */}
                      <div className="flex items-center justify-between pb-6 border-b border-gray-800">
                        <div>
                          <p className="text-sm text-gray-500 mb-1">Loan Application</p>
                          <p className="text-2xl font-bold text-white">₹5,00,000</p>
                        </div>
                        <div className="h-14 w-14 rounded-2xl bg-gradient-to-br from-blue-600 to-cyan-600 flex items-center justify-center">
                          <FileCheck className="h-7 w-7 text-white" />
                        </div>
                      </div>

                      {/* Progress Steps */}
                      <div className="space-y-4">
                        <StepItem icon={<FileCheck className="h-5 w-5" />} title="Document Upload" status="completed" />
                        <StepItem icon={<Zap className="h-5 w-5" />} title="AI Verification" status="processing" />
                        <StepItem icon={<CheckCircle className="h-5 w-5" />} title="Approval" status="pending" />
                      </div>

                      {/* Stats */}
                      <div className="grid grid-cols-3 gap-4 pt-6 border-t border-gray-800">
                        <div>
                          <p className="text-2xl font-bold text-white">98%</p>
                          <p className="text-xs text-gray-500">Approval Rate</p>
                        </div>
                        <div>
                          <p className="text-2xl font-bold text-white">24h</p>
                          <p className="text-xs text-gray-500">Avg. Time</p>
                        </div>
                        <div>
                          <p className="text-2xl font-bold text-white">100%</p>
                          <p className="text-xs text-gray-500">Secure</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Floating Elements */}
                  <div className="absolute -top-6 -right-6 h-24 w-24 bg-gradient-to-br from-blue-600 to-cyan-600 rounded-2xl opacity-10 blur-2xl animate-pulse"></div>
                  <div className="absolute -bottom-6 -left-6 h-24 w-24 bg-gradient-to-br from-cyan-600 to-blue-600 rounded-2xl opacity-10 blur-2xl animate-pulse" style={{ animationDelay: '1s' }}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Logo Marquee */}
      <section className="relative py-16 border-y border-gray-900">
        <div className="container mx-auto px-6">
          <p className="text-center text-sm text-gray-600 mb-8 uppercase tracking-wider">Trusted by Leading Financial Institutions</p>
          <div className="flex items-center justify-center gap-16 opacity-30">
            <Building2 className="h-10 w-10 text-gray-700" />
            <Globe className="h-10 w-10 text-gray-700" />
            <Shield className="h-10 w-10 text-gray-700" />
            <Award className="h-10 w-10 text-gray-700" />
            <BarChart3 className="h-10 w-10 text-gray-700" />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative py-32 bg-gradient-to-b from-black to-gray-950">
        <div className="container mx-auto px-6">
          <div className="text-center mb-20">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600/10 border border-blue-500/20 rounded-full mb-6">
              <Sparkles className="h-4 w-4 text-blue-400" />
              <span className="text-sm text-blue-300 font-medium">Features</span>
            </div>
            <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">
              Everything You Need
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Advanced technology meets privacy-first design for secure lending
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
            <FeatureCard
              icon={<Lock className="h-8 w-8" />}
              title="Zero-Knowledge Privacy"
              description="Your salary is never stored or exposed. Only eligibility results are shared using advanced cryptographic proofs."
              gradient="from-blue-600 to-cyan-600"
            />
            <FeatureCard
              icon={<FileCheck className="h-8 w-8" />}
              title="AI-Powered OCR"
              description="Automatic extraction and verification of income certificates using state-of-the-art AI technology."
              gradient="from-cyan-600 to-blue-600"
            />
            <FeatureCard
              icon={<Zap className="h-8 w-8" />}
              title="Instant Processing"
              description="Get immediate eligibility results with blockchain verification and streamlined approval workflow."
              gradient="from-blue-600 to-purple-600"
            />
            <FeatureCard
              icon={<Shield className="h-8 w-8" />}
              title="Blockchain Security"
              description="Every transaction is recorded on blockchain for immutability and complete transparency."
              gradient="from-purple-600 to-blue-600"
            />
            <FeatureCard
              icon={<Clock className="h-8 w-8" />}
              title="24/7 Availability"
              description="Apply anytime, anywhere. Our system works round the clock to process your application."
              gradient="from-cyan-600 to-purple-600"
            />
            <FeatureCard
              icon={<Target className="h-8 w-8" />}
              title="Smart Eligibility"
              description="Intelligent loan matching based on your income and loan type for optimal approval chances."
              gradient="from-blue-600 to-cyan-600"
            />
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="relative py-32 bg-gradient-to-b from-gray-950 to-black">
        <div className="container mx-auto px-6">
          <div className="text-center mb-20">
            <div className="inline-flex items-center gap-2 px-4 py-2 bg-cyan-600/10 border border-cyan-500/20 rounded-full mb-6">
              <ChevronRight className="h-4 w-4 text-cyan-400" />
              <span className="text-sm text-cyan-300 font-medium">Process</span>
            </div>
            <h2 className="text-5xl md:text-6xl font-bold text-white mb-6">How It Works</h2>
            <p className="text-xl text-gray-400">Simple, secure, and fast in 4 easy steps</p>
          </div>

          <div className="grid md:grid-cols-4 gap-8 max-w-6xl mx-auto">
            <ProcessStep 
              number="01" 
              title="Upload Document" 
              description="Securely upload your income certificate through our encrypted platform"
              icon={<FileCheck className="h-6 w-6" />}
            />
            <ProcessStep 
              number="02" 
              title="AI Extraction" 
              description="Our AI extracts salary information privately without storing sensitive data"
              icon={<Zap className="h-6 w-6" />}
            />
            <ProcessStep 
              number="03" 
              title="Blockchain Verify" 
              description="Eligibility verified and recorded on blockchain for immutability"
              icon={<Shield className="h-6 w-6" />}
            />
            <ProcessStep 
              number="04" 
              title="Manager Approval" 
              description="Final approval from authorized manager with complete audit trail"
              icon={<CheckCircle className="h-6 w-6" />}
            />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section id="stats" className="relative py-32 bg-gradient-to-b from-black to-gray-950">
        <div className="container mx-auto px-6">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-4 gap-8">
              <StatCard number="10K+" label="Active Users" icon={<Users className="h-6 w-6" />} />
              <StatCard number="98%" label="Approval Rate" icon={<TrendingUp className="h-6 w-6" />} />
              <StatCard number="24h" label="Avg. Processing" icon={<Clock className="h-6 w-6" />} />
              <StatCard number="100%" label="Secure" icon={<Lock className="h-6 w-6" />} />
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-32 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 via-cyan-600/10 to-blue-600/10"></div>
        <div className="container mx-auto px-6 text-center relative z-10">
          <h2 className="text-5xl md:text-6xl font-bold mb-6 text-white">Ready to Get Started?</h2>
          <p className="text-xl md:text-2xl mb-10 text-gray-400 max-w-2xl mx-auto">
            Join thousands of users who trust Verity AI for secure loan verification
          </p>
          <Link to="/auth">
            <Button 
              size="lg" 
              className="bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white text-lg px-12 h-16 shadow-2xl shadow-blue-600/40 hover:shadow-blue-600/60 transition-all duration-300 hover:scale-105 font-semibold"
            >
              Apply Now
              <ArrowRight className="ml-2 h-6 w-6" />
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative border-t border-gray-900 bg-black py-16">
        <div className="container mx-auto px-6">
          <div className="grid md:grid-cols-4 gap-12 mb-12">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="bg-gradient-to-br from-blue-600 to-cyan-600 p-2 rounded-lg">
                  <Shield className="h-5 w-5 text-white" />
                </div>
                <span className="font-bold text-white text-lg">Verity AI</span>
              </div>
              <p className="text-gray-500 text-sm">
                Secure loan verification powered by AI and blockchain technology.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-gray-500">
                <li><a href="#" className="hover:text-white transition-colors">Features</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Security</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Pricing</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-gray-500">
                <li><a href="#" className="hover:text-white transition-colors">About</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Careers</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-500">
                <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Compliance</a></li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-gray-900 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-gray-500 text-sm">© 2026 Verity AI. All rights reserved.</p>
            <div className="flex gap-6">
              <a href="#" className="text-gray-500 hover:text-white transition-colors">
                <Globe className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-500 hover:text-white transition-colors">
                <Building2 className="h-5 w-5" />
              </a>
              <a href="#" className="text-gray-500 hover:text-white transition-colors">
                <Shield className="h-5 w-5" />
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function StepItem({ icon, title, status }: { icon: React.ReactNode; title: string; status: string }) {
  const statusColors = {
    completed: "bg-green-600 border-green-500",
    processing: "bg-blue-600 border-blue-500 animate-pulse",
    pending: "bg-gray-800 border-gray-700"
  };

  return (
    <div className="flex items-center gap-4">
      <div className={`h-10 w-10 rounded-xl ${statusColors[status as keyof typeof statusColors]} border flex items-center justify-center text-white`}>
        {icon}
      </div>
      <div>
        <p className="text-white font-medium">{title}</p>
        <p className="text-xs text-gray-500 capitalize">{status}</p>
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, description, gradient }: { 
  icon: React.ReactNode; 
  title: string; 
  description: string;
  gradient: string;
}) {
  return (
    <div className="group relative bg-gradient-to-br from-gray-900 to-black border border-gray-800 hover:border-gray-700 p-8 rounded-2xl transition-all duration-500 hover:scale-105 cursor-pointer">
      <div className={`absolute inset-0 bg-gradient-to-br ${gradient} opacity-0 group-hover:opacity-5 rounded-2xl transition-opacity duration-500`}></div>
      
      <div className="relative z-10">
        <div className={`mb-6 text-white bg-gradient-to-br ${gradient} p-3 rounded-xl inline-block group-hover:scale-110 transition-transform duration-500`}>
          {icon}
        </div>
        <h3 className="text-xl font-bold mb-4 text-white group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:bg-clip-text group-hover:from-blue-400 group-hover:to-cyan-400 transition-all duration-300">
          {title}
        </h3>
        <p className="text-gray-400 leading-relaxed group-hover:text-gray-300 transition-colors duration-300">
          {description}
        </p>
      </div>
    </div>
  );
}

function ProcessStep({ number, title, description, icon }: { 
  number: string; 
  title: string; 
  description: string;
  icon: React.ReactNode;
}) {
  return (
    <div className="text-center group hover:scale-105 transition-all duration-500 cursor-pointer">
      <div className="relative w-20 h-20 bg-gradient-to-br from-blue-600 to-cyan-600 text-white rounded-2xl flex items-center justify-center text-2xl font-bold mx-auto mb-6 shadow-2xl group-hover:shadow-blue-600/50 transition-all duration-500">
        <div className="absolute inset-0 bg-white/10 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-500"></div>
        <span className="relative z-10">{number}</span>
      </div>
      <div className="mb-4 text-blue-400 flex items-center justify-center">
        {icon}
      </div>
      <h3 className="font-bold text-lg mb-3 text-white group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:bg-clip-text group-hover:from-blue-400 group-hover:to-cyan-400 transition-all duration-300">
        {title}
      </h3>
      <p className="text-sm text-gray-500 leading-relaxed group-hover:text-gray-400 transition-colors duration-300">
        {description}
      </p>
    </div>
  );
}

function StatCard({ number, label, icon }: { number: string; label: string; icon: React.ReactNode }) {
  return (
    <div className="text-center p-8 bg-gradient-to-br from-gray-900 to-black border border-gray-800 rounded-2xl hover:border-gray-700 transition-all duration-300 hover:scale-105 cursor-pointer group">
      <div className="text-blue-400 mb-4 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <p className="text-4xl font-bold text-white mb-2">{number}</p>
      <p className="text-gray-500 text-sm">{label}</p>
    </div>
  );
}
