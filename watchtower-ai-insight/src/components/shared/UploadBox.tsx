import { Upload, CheckCircle2, XCircle } from "lucide-react";
import { Card } from "@/components/ui/card";
import { useState } from "react";
import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";

interface UploadBoxProps {
  title: string;
  description: string;
  onFileSelect?: (file: File) => void;
  acceptedFormats?: string;
  maxSizeMB?: number;
}

export const UploadBox = ({
  title,
  description,
  onFileSelect,
  acceptedFormats = ".csv",
  maxSizeMB = 10,
}: UploadBoxProps) => {
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState<string>("");
  const [fileSize, setFileSize] = useState<number>(0);
  const [validationError, setValidationError] = useState<string>("");

  const validateFile = (file: File): string | null => {
    // Check file type
    if (!file.name.toLowerCase().endsWith('.csv')) {
      return "File must be a CSV file";
    }

    // Check file size (default 10MB)
    const maxSizeBytes = maxSizeMB * 1024 * 1024;
    if (file.size > maxSizeBytes) {
      return `File size exceeds ${maxSizeMB}MB limit`;
    }

    if (file.size === 0) {
      return "File is empty";
    }

    return null;
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const handleFile = (file: File) => {
    const error = validateFile(file);
    if (error) {
      setValidationError(error);
      setFileName("");
      setFileSize(0);
      return;
    }

    setValidationError("");
    setFileName(file.name);
    setFileSize(file.size);
    onFileSelect?.(file);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      handleFile(file);
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFile(file);
    }
  };

  return (
    <Card
      className={`p-8 border-2 border-dashed transition-all duration-200 ${
        isDragging
          ? "border-primary bg-primary/5"
          : "border-border hover:border-primary/50"
      }`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <motion.div
        whileHover={{ scale: 1.02 }}
        className="flex flex-col items-center justify-center text-center"
      >
        <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-4">
          <Upload className="w-8 h-8 text-primary" />
        </div>
        <h3 className="text-lg font-semibold text-foreground mb-2">{title}</h3>
        <p className="text-sm text-muted-foreground mb-4">{description}</p>
        
        {fileName && !validationError && (
          <div className="mb-3 p-3 bg-success/10 border border-success/20 rounded-lg">
            <div className="flex items-center gap-2 text-success">
              <CheckCircle2 className="w-4 h-4" />
              <span className="text-sm font-medium">File selected</span>
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {fileName} ({formatFileSize(fileSize)})
            </p>
          </div>
        )}

        {validationError && (
          <div className="mb-3 p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
            <div className="flex items-center gap-2 text-destructive">
              <XCircle className="w-4 h-4" />
              <span className="text-sm font-medium">{validationError}</span>
            </div>
          </div>
        )}

        <label className="cursor-pointer">
          <span className="inline-block px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
            Browse Files
          </span>
          <input
            type="file"
            className="hidden"
            accept={acceptedFormats}
            onChange={handleFileInput}
          />
        </label>
        <p className="text-xs text-muted-foreground mt-2">
          Accepted formats: {acceptedFormats} (Max {maxSizeMB}MB)
        </p>
      </motion.div>
    </Card>
  );
};
