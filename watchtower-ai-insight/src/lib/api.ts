/** API client for Watchtower AML Platform */

import type { BatchTransactionResponse, HealthCheckResponse, ApiError } from "@/types/api";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

/**
 * Check if API is available
 */
export async function healthCheck(): Promise<HealthCheckResponse> {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error(`API health check failed: ${response.statusText}`);
  }
  
  return response.json();
}

/**
 * Upload CSV file and get fraud predictions
 * @param file CSV file to analyze
 * @param modelType Model to use ('dqn' or 'rf'), defaults to 'dqn'
 * @returns Batch prediction results
 */
export async function predictBatch(
  file: File,
  modelType: string = "dqn"
): Promise<BatchTransactionResponse> {
  // Create FormData for file upload
  const formData = new FormData();
  formData.append("file", file);

  // Build URL with query parameter
  const url = new URL(`${API_BASE_URL}/predict/batch`);
  url.searchParams.append("model_type", modelType);

  try {
    const response = await fetch(url.toString(), {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      // Try to parse error response
      let errorMessage = `API request failed: ${response.statusText}`;
      
      try {
        const errorData: ApiError = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch {
        // If JSON parsing fails, use status text
      }
      
      throw new Error(errorMessage);
    }

    const data: BatchTransactionResponse = await response.json();
    return data;
  } catch (error) {
    // Handle network errors
    if (error instanceof TypeError && error.message.includes("fetch")) {
      throw new Error(
        `Unable to connect to API at ${API_BASE_URL}. Please ensure the API server is running.`
      );
    }
    
    // Re-throw other errors
    throw error;
  }
}

/**
 * Get API base URL (for debugging)
 */
export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

