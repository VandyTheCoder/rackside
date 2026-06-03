import type { APIRoute } from "astro";
import { login } from "@/lib/api";
import { setToken } from "@/lib/auth";

export const POST: APIRoute = async ({ request, cookies, redirect }) => {
  const form = await request.formData();
  const email = String(form.get("email") ?? "");
  const password = String(form.get("password") ?? "");

  const token = await login(email, password);
  if (!token) {
    return redirect("/admin/login?error=1", 303);
  }

  setToken(cookies, token);
  return redirect("/admin", 303);
};
