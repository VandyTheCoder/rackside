import type { APIRoute } from "astro";
import { saveProduct } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { parseProductForm } from "@/lib/forms";

export const POST: APIRoute = async ({ request, cookies, redirect, params }) => {
  const token = getToken(cookies);
  if (!token) {
    return redirect("/admin/login", 303);
  }

  const body = parseProductForm(await request.formData());
  const ok = await saveProduct(token, body, params.id);
  return redirect(ok ? "/admin" : `/admin/products/${params.id}/edit?error=1`, 303);
};
