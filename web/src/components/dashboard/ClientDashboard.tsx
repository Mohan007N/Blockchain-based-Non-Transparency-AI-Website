import { useState, useCallback, useEffect } from "react";
import { useDropzone } from "react-dropzone";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import {
  Upload, FileText, Sparkles, CheckCircle2, XCircle, Loader2, X,
  History, Image as ImageIcon, ShieldCheck, Clock, DollarSign, Briefcase, TrendingUp,
} from "lucide-react";

type Status = "idle" | "uploading" | "extracting" | "verified" | "failed";

interface ExtractedField { label: string; value: string; }
interface HistoryItem {
  id: string;
  name: string;
  type: string;
  date: string;
  status: "verified" | "failed";
  claim: string;
  loanAmount?: string;
  loanPurpose?: string;
}

type LoanPurpose = "personal" | "home" | "auto" | "education" | "business";

const SAMPLE_HISTORY: HistoryItem[] = [
  { id: "1", name: "Salary_Certificate.pdf", type: "Income", date: "2 days ago", status: "verified", claim: "Monthly income ≥ ₹50,000", loanAmount: "₹5,00,000", loanPurpose: "personal" },
  { id: "2", name: "Bank_Statement.pdf", type: "Financial", date: "5 days ago", status: "verified", claim: "Account active ≥ 6 months", loanAmount: "₹10,00,000", loanPurpose: "home" },
  { id: "3", name: "ITR_2024.pdf", type: "Tax", date: "1 week ago", status: "verified", claim: "Annual income ≥ ₹6,00,000", loanAmount: "₹15,00,000", loanPurpose: "business" },
  { id: "4", name: "OldID.png", type: "Identity", date: "2 weeks ago", status: "failed", claim: "Tampering detected", loanAmount: "₹3,00,000", loanPurpose: "education" },
];

export function ClientDashboard() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [status, setStatus] = useState<Status>("idle");
  const [progress, setProgress] = useState(0);
  const [extracted, setExtracted] = useState<ExtractedField[]>([]);
  
  // Loan application state
  const [loanAmount, setLoanAmount] = useState("");
  const [loanPurpose, setLoanPurpose] = useState<LoanPurpose>("personal");
  const [monthlyIncome, setMonthlyIncome] = useState("");
  const [applicationStatus, setApplicationStatus] = useState<"none" | "pending" | "approved" | "rejected">("none");
  const [applicationId, setApplicationId] = useState<string | null>(null);

  const onDrop = useCallback((accepted: File[]) => {
    const f = accepted[0];
    if (!f) return;
    setFile(f);
    setStatus("idle");
    setExtracted([]);
    setProgress(0);
    if (f.type.startsWith("image/")) {
      setPreviewUrl(URL.createObjectURL(f));
    } else {
      setPreviewUrl(null);
    }
    toast.success("File ready", { description: f.name });
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [], "application/pdf": [] },
    maxFiles: 1,
  });

  const startVerification = async () => {
    if (!file) return;
    
    // Validate loan amount is entered
    if (!loanAmount) {
      toast.error("Please enter loan amount", { description: "Loan amount is required to apply" });
      return;
    }
    
    setStatus("uploading");
    setProgress(0);
    // simulate upload
    for (let p = 0; p <= 60; p += 10) {
      await new Promise((r) => setTimeout(r, 120));
      setProgress(p);
    }
    setStatus("extracting");
    for (let p = 60; p <= 100; p += 10) {
      await new Promise((r) => setTimeout(r, 150));
      setProgress(p);
    }
    
    // Generate application ID
    const appId = "LN-" + Math.random().toString(36).substring(2, 8).toUpperCase();
    setApplicationId(appId);
    
    // mock extracted data - now includes income verification for loan
    setExtracted([
      { label: "Document type", value: "Salary Certificate / Income Proof" },
      { label: "Applicant name", value: "Current User" },
      { label: "Monthly income", value: monthlyIncome || "Not specified" },
      { label: "Loan amount", value: loanAmount },
      { label: "Loan purpose", value: loanPurpose.charAt(0).toUpperCase() + loanPurpose.slice(1) + " Loan" },
      { label: "AI Verification", value: "Income verified via document" },
    ]);
    
    const ok = Math.random() > 0.15;
    setStatus(ok ? "verified" : "failed");
    
    // Set application status
    if (ok) {
      setApplicationStatus("pending");
      toast.success("Application submitted", { description: `Application ${appId} submitted for AI review` });
    } else {
      toast.error("Verification failed", { description: "Document could not be verified" });
    }
  };

  const reset = () => {
    setFile(null);
    setPreviewUrl(null);
    setStatus("idle");
    setProgress(0);
    setExtracted([]);
    setApplicationStatus("none");
    setApplicationId(null);
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="font-display text-3xl font-bold">Client workspace</h1>
        <p className="text-muted-foreground mt-1">Apply for a loan with AI-powered document verification.</p>
      </div>

      {/* Loan Application Form */}
      <div className="glass rounded-2xl p-6">
        <h2 className="font-semibold mb-4 flex items-center gap-2">
          <DollarSign className="w-4 h-4 text-accent" />
          Loan Application
        </h2>
        
        <div className="grid md:grid-cols-3 gap-4">
          {/* Loan Amount */}
          <div className="space-y-2">
            <Label htmlFor="loanAmount" className="text-xs text-muted-foreground">Loan Amount Needed</Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">₹</span>
              <Input
                id="loanAmount"
                type="text"
                placeholder="e.g., 5,00,000"
                value={loanAmount}
                onChange={(e) => {
                  const value = e.target.value.replace(/[^\d]/g, "");
                  const formatted = value ? `₹${parseInt(value).toLocaleString("en-IN")}` : "";
                  setLoanAmount(formatted);
                }}
                className="pl-7 bg-white/5 border-white/10"
                disabled={status !== "idle"}
              />
            </div>
          </div>

          {/* Loan Purpose */}
          <div className="space-y-2">
            <Label htmlFor="loanPurpose" className="text-xs text-muted-foreground">Loan Purpose</Label>
            <select
              id="loanPurpose"
              value={loanPurpose}
              onChange={(e) => setLoanPurpose(e.target.value as LoanPurpose)}
              disabled={status !== "idle"}
              className="w-full h-10 px-3 rounded-lg bg-white/5 border border-white/10 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
              <option value="personal">Personal Loan</option>
              <option value="home">Home Loan</option>
              <option value="auto">Auto Loan</option>
              <option value="education">Education Loan</option>
              <option value="business">Business Loan</option>
            </select>
          </div>

          {/* Monthly Income */}
          <div className="space-y-2">
            <Label htmlFor="monthlyIncome" className="text-xs text-muted-foreground">Monthly Income</Label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">₹</span>
              <Input
                id="monthlyIncome"
                type="text"
                placeholder="e.g., 50,000"
                value={monthlyIncome}
                onChange={(e) => {
                  const value = e.target.value.replace(/[^\d]/g, "");
                  const formatted = value ? `₹${parseInt(value).toLocaleString("en-IN")}` : "";
                  setMonthlyIncome(formatted);
                }}
                className="pl-7 bg-white/5 border-white/10"
                disabled={status !== "idle"}
              />
            </div>
          </div>
        </div>

        {/* Eligibility Indicator */}
        {loanAmount && monthlyIncome && (
          <div className="mt-4 p-4 rounded-xl bg-white/5 border border-white/10">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-accent" />
                <span className="text-sm">Estimated Eligibility</span>
              </div>
              <span className="text-sm font-medium text-success">
                Based on your income, you may qualify for loans up to ₹{Math.min(parseInt(monthlyIncome.replace(/[^\d]/g, "") || "0") * 60, parseInt(loanAmount.replace(/[^\d]/g, "") || "0")).toLocaleString("en-IN")}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Application Status */}
      {applicationStatus !== "none" && (
        <div className={`glass rounded-2xl p-6 border ${
          applicationStatus === "approved" ? "bg-success/10 border-success/30" :
          applicationStatus === "rejected" ? "bg-destructive/10 border-destructive/30" :
          "bg-amber-400/10 border-amber-400/30"
        }`}>
          <div className="flex items-center gap-3">
            {applicationStatus === "pending" && <Clock className="w-6 h-6 text-amber-300" />}
            {applicationStatus === "approved" && <CheckCircle2 className="w-6 h-6 text-success" />}
            {applicationStatus === "rejected" && <XCircle className="w-6 h-6 text-destructive" />}
            <div>
              <div className="font-semibold">
                {applicationStatus === "pending" && "Application Under Review"}
                {applicationStatus === "approved" && "Loan Approved!"}
                {applicationStatus === "rejected" && "Application Not Approved"}
              </div>
              <div className="text-xs text-muted-foreground">
                Application ID: {applicationId} • AI is reviewing your documents
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Upload + preview */}
        <div className="glass rounded-2xl p-6">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <Upload className="w-4 h-4 text-accent" />
            Upload document
          </h2>

          {!file ? (
            <div
              {...getRootProps()}
              className={`relative rounded-2xl border-2 border-dashed transition-all cursor-pointer p-10 text-center ${
                isDragActive ? "border-primary bg-primary/5 shadow-glow-violet" : "border-white/15 hover:border-white/30 hover:bg-white/[0.02]"
              }`}
            >
              <input {...getInputProps()} />
              <div className="w-14 h-14 mx-auto rounded-2xl bg-gradient-primary/20 border border-white/10 flex items-center justify-center mb-4">
                <Upload className="w-6 h-6 text-primary" />
              </div>
              <div className="font-medium">{isDragActive ? "Drop it here" : "Drag & drop your file"}</div>
              <div className="text-xs text-muted-foreground mt-1">PDF, PNG, JPG up to 20MB</div>
              <Button type="button" variant="outline" size="sm" className="mt-4 bg-white/5 border-white/10">
                Browse files
              </Button>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="rounded-2xl overflow-hidden border border-white/10 bg-black/30 aspect-[4/3] flex items-center justify-center relative">
                {previewUrl ? (
                  <img src={previewUrl} alt={file.name} className="w-full h-full object-contain" />
                ) : (
                  <div className="text-center">
                    <FileText className="w-16 h-16 text-muted-foreground mx-auto mb-2" />
                    <div className="text-sm text-muted-foreground">PDF preview</div>
                  </div>
                )}
                {status === "extracting" && (
                  <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/30 to-transparent animate-shimmer" />
                )}
              </div>

              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-2 min-w-0">
                  {file.type.startsWith("image/") ? (
                    <ImageIcon className="w-4 h-4 text-accent shrink-0" />
                  ) : (
                    <FileText className="w-4 h-4 text-accent shrink-0" />
                  )}
                  <div className="min-w-0">
                    <div className="text-sm font-medium truncate">{file.name}</div>
                    <div className="text-xs text-muted-foreground">{(file.size / 1024).toFixed(1)} KB</div>
                  </div>
                </div>
                <Button variant="ghost" size="icon" onClick={reset}>
                  <X className="w-4 h-4" />
                </Button>
              </div>

              {(status === "uploading" || status === "extracting") && (
                <div>
                  <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
                    <span className="flex items-center gap-1.5">
                      <Loader2 className="w-3 h-3 animate-spin" />
                      {status === "uploading" ? "Encrypting & uploading…" : "AI extracting fields…"}
                    </span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-1.5" />
                </div>
              )}

              {status === "idle" && (
                <Button
                  onClick={startVerification}
                  className="w-full h-11 bg-gradient-primary text-primary-foreground border-0 shadow-glow-violet hover:opacity-90"
                >
                  <Sparkles className="w-4 h-4 mr-2" />
                  Start Verification
                </Button>
              )}
            </div>
          )}
        </div>

        {/* Result */}
        <div className="glass rounded-2xl p-6 min-h-[400px]">
          <h2 className="font-semibold mb-4 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-accent" />
            Extracted data & verification
          </h2>

          <AnimatePresence mode="wait">
            {extracted.length === 0 ? (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full flex flex-col items-center justify-center text-center text-muted-foreground py-16"
              >
                <Sparkles className="w-10 h-10 mb-3 opacity-40" />
                <div className="text-sm">Results will appear here</div>
              </motion.div>
            ) : (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-4"
              >
                {/* Status banner */}
                <div
                  className={`rounded-xl p-4 border flex items-center gap-3 ${
                    status === "verified"
                      ? "bg-success/10 border-success/30"
                      : "bg-destructive/10 border-destructive/30"
                  }`}
                >
                  {status === "verified" ? (
                    <CheckCircle2 className="w-6 h-6 text-success" />
                  ) : (
                    <XCircle className="w-6 h-6 text-destructive" />
                  )}
                  <div>
                    <div className="font-semibold">
                      {status === "verified" ? "Verified" : "Not verified"}
                    </div>
                    <div className="text-xs text-muted-foreground">
                      {status === "verified"
                        ? "Zero-knowledge proof generated successfully"
                        : "Document signature could not be validated"}
                    </div>
                  </div>
                </div>

                {/* Extracted fields */}
                <div className="space-y-1">
                  {extracted.map((f, i) => (
                    <motion.div
                      key={f.label}
                      initial={{ opacity: 0, x: -10 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.04 }}
                      className="flex justify-between items-center py-2.5 px-3 rounded-lg hover:bg-white/5"
                    >
                      <span className="text-xs text-muted-foreground">{f.label}</span>
                      <span className="text-sm font-medium">{f.value}</span>
                    </motion.div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* History */}
      <div className="glass rounded-2xl p-6">
        <h2 className="font-semibold mb-4 flex items-center gap-2">
          <History className="w-4 h-4 text-accent" />
          Loan Application History
        </h2>
        <div className="space-y-1">
          {SAMPLE_HISTORY.map((h) => (
            <div
              key={h.id}
              className="flex items-center justify-between gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors"
            >
              <div className="flex items-center gap-3 min-w-0">
                <div className="w-9 h-9 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center shrink-0">
                  <Briefcase className="w-4 h-4 text-muted-foreground" />
                </div>
                <div className="min-w-0">
                  <div className="text-sm font-medium truncate">{h.name}</div>
                  <div className="text-xs text-muted-foreground flex items-center gap-2">
                    <Clock className="w-3 h-3" />
                    {h.date} · {h.type}
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                {h.loanAmount && (
                  <span className="text-xs font-medium text-accent">{h.loanAmount}</span>
                )}
                <span className="text-xs text-muted-foreground hidden sm:block">{h.claim}</span>
                {h.status === "verified" ? (
                  <Badge className="bg-success/15 text-success border-success/30 hover:bg-success/20">
                    <CheckCircle2 className="w-3 h-3 mr-1" /> Verified
                  </Badge>
                ) : (
                  <Badge className="bg-destructive/15 text-destructive border-destructive/30 hover:bg-destructive/20">
                    <XCircle className="w-3 h-3 mr-1" /> Failed
                  </Badge>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
