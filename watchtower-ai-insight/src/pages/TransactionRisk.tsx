import { useState } from "react";
import { MainLayout } from "@/components/layout/MainLayout";
import { MetricCard } from "@/components/shared/MetricCard";
import { DataTable } from "@/components/shared/DataTable";
import { UploadBox } from "@/components/shared/UploadBox";
import { Button } from "@/components/ui/button";
import { AlertTriangle, TrendingUp, Target, Activity, Loader2 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";
import { predictBatch } from "@/lib/api";
import type { BatchTransactionResponse, TransactionResponse } from "@/types/api";
import { useToast } from "@/hooks/use-toast";

interface TransactionRow {
  id: string;
  amount: string;
  risk: number;
  isFraud: boolean;
  fraudProbability: number;
}

export default function TransactionRisk() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [predictions, setPredictions] = useState<BatchTransactionResponse | null>(null);
  const [csvData, setCsvData] = useState<any[]>([]);
  const { toast } = useToast();

  const getRiskBadge = (risk: number) => {
    if (risk >= 70) return <Badge className="bg-destructive text-destructive-foreground">High Risk</Badge>;
    if (risk >= 40) return <Badge className="bg-warning text-warning-foreground">Medium Risk</Badge>;
    return <Badge className="bg-success text-success-foreground">Low Risk</Badge>;
  };

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setError("");
    setPredictions(null);
    setCsvData([]);
    
    // Read CSV to get data for display (Amount column)
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const text = e.target?.result as string;
        if (!text || text.trim().length === 0) {
          console.warn("CSV file is empty");
          return;
        }
        
        const lines = text.split('\n').filter(line => line.trim());
        if (lines.length === 0) {
          console.warn("No data in CSV file");
          return;
        }
        
        const headers = lines[0].split(',').map(h => h.trim());
        const data = lines.slice(1).map((line, index) => {
          const values = line.split(',');
          const row: any = { index };
          headers.forEach((header, i) => {
            row[header] = values[i]?.trim() || '';
          });
          return row;
        });
        setCsvData(data);
      } catch (err) {
        console.error("Error reading CSV:", err);
        // Don't block file selection if CSV reading fails
      }
    };
    reader.onerror = () => {
      console.error("Error reading file");
    };
    reader.readAsText(file);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError("Please select a CSV file first");
      toast({
        title: "No file selected",
        description: "Please upload a CSV file before analyzing",
        variant: "destructive",
      });
      return;
    }

    setIsLoading(true);
    setError("");
    setPredictions(null);

    try {
      const response = await predictBatch(selectedFile, "dqn");
      setPredictions(response);
      
      toast({
        title: "Analysis complete",
        description: `Analyzed ${response.total_transactions} transactions. Found ${response.fraud_count} fraud cases.`,
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An error occurred during analysis";
      setError(errorMessage);
      toast({
        title: "Analysis failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Transform API predictions to table format
  const transformPredictionsToTable = (): TransactionRow[] => {
    if (!predictions) return [];

    return predictions.predictions.map((pred: TransactionResponse, index: number) => {
      const csvRow = csvData[index] || {};
      let amount = "N/A";
      
      // Try to get amount from CSV data
      if (csvRow.Amount) {
        const amountValue = parseFloat(csvRow.Amount);
        if (!isNaN(amountValue)) {
          amount = `$${amountValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        }
      }
      
      return {
        id: `TX${String(index + 1001).padStart(4, '0')}`,
        amount,
        risk: Math.round(pred.risk_score),
        isFraud: pred.is_fraud,
        fraudProbability: pred.fraud_probability,
      };
    });
  };

  // Calculate metrics from predictions
  const calculateMetrics = () => {
    if (!predictions) {
      return {
        highRiskCount: 0,
        highRiskPercent: "0%",
        totalVolume: "$0",
        anomaliesDetected: 0,
        avgRiskScore: 0,
        riskDistribution: { high: 0, medium: 0, low: 0 },
      };
    }

    const highRiskCount = predictions.predictions.filter(p => p.risk_score >= 70).length;
    const highRiskPercent = ((highRiskCount / predictions.total_transactions) * 100).toFixed(1);
    
    // Calculate total volume from CSV data
    const totalAmount = csvData.reduce((sum, row) => {
      const amount = parseFloat(row.Amount || row.amount || '0') || 0;
      return sum + amount;
    }, 0);
    let totalVolume = "$0";
    if (totalAmount > 0) {
      if (totalAmount >= 1000000) {
        totalVolume = `$${(totalAmount / 1000000).toFixed(2)}M`;
      } else if (totalAmount >= 1000) {
        totalVolume = `$${(totalAmount / 1000).toFixed(1)}K`;
      } else {
        totalVolume = `$${totalAmount.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
      }
    }

    const anomaliesDetected = predictions.fraud_count;
    const avgRiskScore = predictions.predictions.reduce((sum, p) => sum + p.risk_score, 0) / predictions.total_transactions;

    // Calculate risk distribution
    const high = predictions.predictions.filter(p => p.risk_score >= 70).length;
    const medium = predictions.predictions.filter(p => p.risk_score >= 40 && p.risk_score < 70).length;
    const low = predictions.predictions.filter(p => p.risk_score < 40).length;
    const total = predictions.total_transactions;

    return {
      highRiskCount,
      highRiskPercent: `${highRiskPercent}%`,
      totalVolume,
      anomaliesDetected,
      avgRiskScore: avgRiskScore.toFixed(1),
      riskDistribution: {
        high: (high / total) * 100,
        medium: (medium / total) * 100,
        low: (low / total) * 100,
      },
    };
  };

  const metrics = calculateMetrics();
  const tableData = transformPredictionsToTable();

  const columns = [
    { key: "id", label: "Transaction ID" },
    { key: "amount", label: "Amount" },
    {
      key: "risk",
      label: "Risk Score",
      render: (value: number, row: TransactionRow) => (
        <div className="flex items-center gap-2">
          <span className="font-semibold">{value}%</span>
          {getRiskBadge(value)}
          {row.isFraud && (
            <Badge className="bg-destructive text-destructive-foreground ml-2">Fraud</Badge>
          )}
        </div>
      ),
    },
    {
      key: "fraudProbability",
      label: "Fraud Probability",
      render: (value: number) => (
        <span className="text-sm text-muted-foreground">
          {(value * 100).toFixed(2)}%
        </span>
      ),
    },
  ];

  return (
    <MainLayout title="Transaction Risk Scoring">
      <div className="space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h3 className="text-2xl font-bold text-foreground mb-2">
            Detect Suspicious Transactions
          </h3>
          <p className="text-muted-foreground">
            Upload transaction data to identify high-risk patterns using AI-powered analysis
          </p>
        </motion.div>

        <UploadBox
          title="Upload Transaction Data"
          description="Drag and drop your CSV file or click to browse"
          acceptedFormats=".csv"
          onFileSelect={handleFileSelect}
        />

        {error && (
          <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-sm text-destructive font-medium">{error}</p>
          </div>
        )}

        <div className="flex justify-center">
          <Button
            size="lg"
            onClick={handleAnalyze}
            disabled={!selectedFile || isLoading}
            className="px-8"
          >
            {isLoading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Activity className="w-5 h-5 mr-2" />
                Analyze Risk
              </>
            )}
          </Button>
        </div>

        {predictions && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <MetricCard
                title="High-Risk Transactions"
                value={metrics.highRiskPercent}
                icon={AlertTriangle}
                variant="destructive"
                trend={`${metrics.highRiskCount} transactions flagged`}
              />
              <MetricCard
                title="Total Volume"
                value={metrics.totalVolume}
                icon={TrendingUp}
                trend={`Analyzed ${predictions.total_transactions} transactions`}
              />
              <MetricCard
                title="Anomalies Detected"
                value={metrics.anomaliesDetected.toString()}
                icon={Target}
                variant="warning"
                trend="Requires manual review"
              />
              <MetricCard
                title="Avg Risk Score"
                value={metrics.avgRiskScore}
                icon={Activity}
                trend="Across all transactions"
              />
            </div>

            <DataTable
              title="Transaction Analysis Results"
              columns={columns}
              data={tableData}
            />

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
                <h4 className="text-lg font-semibold mb-4">Summary</h4>
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                    <span>Total Transactions</span>
                    <span className="font-semibold">{predictions.total_transactions}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                    <span>Fraud Detected</span>
                    <Badge className="bg-destructive text-destructive-foreground">
                      {predictions.fraud_count}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-muted rounded-lg">
                    <span>Fraud Rate</span>
                    <span className="font-semibold">{predictions.fraud_rate}%</span>
                  </div>
                </div>
              </div>

              <div className="bg-card p-6 rounded-lg shadow-sm border border-border">
                <h4 className="text-lg font-semibold mb-4">Risk Distribution</h4>
                <div className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>High Risk</span>
                      <span className="font-semibold">{metrics.riskDistribution.high.toFixed(1)}%</span>
                    </div>
                    <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-destructive" 
                        style={{ width: `${metrics.riskDistribution.high}%` }} 
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Medium Risk</span>
                      <span className="font-semibold">{metrics.riskDistribution.medium.toFixed(1)}%</span>
                    </div>
                    <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-warning" 
                        style={{ width: `${metrics.riskDistribution.medium}%` }} 
                      />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span>Low Risk</span>
                      <span className="font-semibold">{metrics.riskDistribution.low.toFixed(1)}%</span>
                    </div>
                    <div className="w-full h-3 bg-muted rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-success" 
                        style={{ width: `${metrics.riskDistribution.low}%` }} 
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
    </MainLayout>
  );
}
