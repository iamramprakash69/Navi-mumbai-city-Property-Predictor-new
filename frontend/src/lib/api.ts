export type RealEstateRequest = {
  location: "airoli" | "belapur" | "cbd belapur" | "ghansoli" | "kharghar" | "nerul" | "panvel" | "ulwe" | "vashi";
  area_sqft: number;
  bhk: number;
  bathrooms: number;
  floor: number;
  total_floors: number;
  age_of_property: number;
  parking: boolean;
  lift: boolean;
};

export type RealEstateResponse = {
  predicted_price: number;
  price_per_sqft: number;
  market_status: "Below Market" | "Average" | "Above Market";
};

// Use the environment variable for API URL or default to localhost for development
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetchWithRetry(url: string, options: RequestInit, retries = 3, delay = 2000): Promise<Response> {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
      if (response.status >= 500) throw new Error(`Server error: ${response.status}`);
      return response;
    } catch (err) {
      if (i === retries - 1) throw err;
      console.warn(`Attempt ${i + 1} failed. Retrying...`);
      await new Promise(res => setTimeout(res, delay));
    }
  }
  throw new Error("Failed to connect to backend after several attempts.");
}

export async function predictRealEstate(
  payload: RealEstateRequest
): Promise<RealEstateResponse> {
  const response = await fetchWithRetry(`${API_URL}/predict/real-estate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
    cache: "no-store",
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(errorData.detail || `Prediction failed with status ${response.status}`);
  }

  return response.json();
}
