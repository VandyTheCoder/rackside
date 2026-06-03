export function parseProductForm(form: FormData): Record<string, unknown> {
  const price = Number(form.get("price"));
  const imageUrl = String(form.get("image_url") ?? "").trim();
  return {
    name: String(form.get("name") ?? "").trim(),
    slug: String(form.get("slug") ?? "").trim(),
    description: String(form.get("description") ?? "").trim(),
    price_cents: Number.isFinite(price) ? Math.round(price * 100) : 0,
    category: String(form.get("category") ?? "").trim(),
    stock: Number(form.get("stock") ?? 0),
    image_url: imageUrl === "" ? null : imageUrl,
    active: form.get("active") === "on",
  };
}
