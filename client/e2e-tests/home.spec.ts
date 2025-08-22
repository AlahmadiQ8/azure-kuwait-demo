import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should display the correct title', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page title is correct
    await expect(page).toHaveTitle('Kuwait Fine Dining - Find your new favorite restaurant!');
  });

  test('should display the main heading', async ({ page }) => {
    await page.goto('/');
    
    // Check that the main heading is present
    const mainHeading = page.locator('h1').first();
    await expect(mainHeading).toHaveText('Kuwait Fine Dining');
  });

  test('should display the welcome message', async ({ page }) => {
    await page.goto('/');
    
    // Check that the welcome message is present
    const welcomeMessage = page.locator('p').first();
    await expect(welcomeMessage).toHaveText('Find your next restaurant in Kuwait!');
  });
});
