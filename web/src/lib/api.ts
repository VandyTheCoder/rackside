import { API_URL } from "astro:env/server";
import type { Order, Product } from "@/lib/types";

async function request(path: string, init?: RequestInit): Promise<Response> {
  return fetch(`${API_URL}${path}`, init);
}

export async function getProducts(): Promise<Product[]> {
  const response = await request("/api/products");
  if (!response.ok) {
    return [];
  }
  return response.json();
}

export async function getProduct(slug: string): Promise<Product | null> {
  const response = await request(`/api/products/${slug}`);
  return response.ok ? response.json() : null;
}

export async function login(
  email: string,
  password: string,
): Promise<string | null> {
  const response = await request("/api/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!response.ok) {
    return null;
  }
  const data = await response.json();
  return data.access_token ?? null;
}

export async function createCheckout(
  items: { slug: string; quantity: number }[],
): Promise<string | null> {
  const response = await request("/api/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  });
  if (!response.ok) {
    return null;
  }
  const data = await response.json();
  return data.url ?? null;
}

function authHeaders(token: string): HeadersInit {
  return { Authorization: `Bearer ${token}`, "Content-Type": "application/json" };
}

export async function getAdminProducts(token: string): Promise<Product[] | null> {
  const response = await request("/api/admin/products", {
    headers: authHeaders(token),
  });
  return response.ok ? response.json() : null;
}

export async function getAdminProduct(
  token: string,
  id: string,
): Promise<Product | null> {
  const products = await getAdminProducts(token);
  return products?.find((product) => product.id === id) ?? null;
}

export async function getAdminOrders(token: string): Promise<Order[] | null> {
  const response = await request("/api/admin/orders", {
    headers: authHeaders(token),
  });
  return response.ok ? response.json() : null;
}

export async function saveProduct(
  token: string,
  body: Record<string, unknown>,
  id?: string,
): Promise<boolean> {
  const response = await request(
    id ? `/api/admin/products/${id}` : "/api/admin/products",
    {
      method: id ? "PUT" : "POST",
      headers: authHeaders(token),
      body: JSON.stringify(body),
    },
  );
  return response.ok;
}

export async function deleteProduct(token: string, id: string): Promise<boolean> {
  const response = await request(`/api/admin/products/${id}`, {
    method: "DELETE",
    headers: authHeaders(token),
  });
  return response.ok;
}
