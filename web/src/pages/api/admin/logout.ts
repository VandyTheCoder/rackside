import type { APIRoute } from "astro";
import { clearToken } from "@/lib/auth";

export const POST: APIRoute = async ({ cookies, redirect }) => {
  clearToken(cookies);
  return redirect("/admin/login", 303);
};
