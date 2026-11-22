import { test, expect } from "@playwright/test";

test("landing is usable without horizontal overflow", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toContainText("Mais clareza");
  await expect(page.getByRole("link", { name: "Entrar" })).toBeVisible();
  await expect(page.getByRole("link", { name: /Começar agora/ })).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(overflow, "The public landing should not scroll horizontally").toBe(false);
});

test("user can navigate to the login screen on each viewport", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: "Entrar" }).click();
  await expect(page).toHaveURL(/\/login$/);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.getByRole("textbox", { name: "E-mail" })).toBeVisible();
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
  expect(overflow, "The login screen should not scroll horizontally").toBe(false);
});
