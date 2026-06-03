import type { APIRoute } from "astro";
import { saveProduct } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { parseProductForm } from "@/lib/forms";

export const POST: APIRoute = async ({ request, cookies, redirect }) => {
  const token = getToken(cookies);
  if (!token) {
    return redirect("/admin/login", 303);
  }

  const body = parseProductForm(await request.formData());
  const ok = await saveProduct(token, body);
  return redirect(ok ? "/admin" : "/admin/products/new?error=1", 303);
};
