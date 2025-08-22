import { test, expect } from '@playwright/test';

test.describe('Restaurant Listing and Navigation', () => {
  test('should display restaurants with titles on index page', async ({ page }) => {
    await page.goto('/');
    
    // Wait for the restaurants to load
    await page.waitForSelector('[data-testid="restaurants-grid"]', { timeout: 10000 });
    
    // Check that restaurants are displayed
    const restaurantCards = page.locator('[data-testid="restaurant-card"]');
    
    // Wait for at least one restaurant card to be visible
    await expect(restaurantCards.first()).toBeVisible();
    
    // Check that we have at least one restaurant
    const restaurantCount = await restaurantCards.count();
    expect(restaurantCount).toBeGreaterThan(0);
    
    // Check that each restaurant card has a title
    const firstRestaurantCard = restaurantCards.first();
    await expect(firstRestaurantCard.locator('[data-testid="restaurant-title"]')).toBeVisible();
    
    // Verify that restaurant titles are not empty
    const restaurantTitle = await firstRestaurantCard.locator('[data-testid="restaurant-title"]').textContent();
    expect(restaurantTitle?.trim()).toBeTruthy();
  });

  test('should navigate to correct restaurant details page when clicking on a restaurant', async ({ page }) => {
    await page.goto('/');
    
    // Wait for restaurants to load
    await page.waitForSelector('[data-testid="restaurants-grid"]', { timeout: 10000 });
    
    // Get the first restaurant card and its data attributes
    const firstRestaurantCard = page.locator('[data-testid="restaurant-card"]').first();
    const restaurantId = await firstRestaurantCard.getAttribute('data-restaurant-id');
    const restaurantTitle = await firstRestaurantCard.getAttribute('data-restaurant-title');
    
    // Click on the first restaurant
    await firstRestaurantCard.click();
    
    // Verify we're on the correct restaurant details page
    await expect(page).toHaveURL(`/restaurant/${restaurantId}`);
    
    // Verify the restaurant details page loads
    await page.waitForSelector('[data-testid="restaurant-details"]', { timeout: 10000 });
    
    // Verify the title matches what we clicked on
    const detailsTitle = page.locator('[data-testid="restaurant-details-title"]');
    await expect(detailsTitle).toHaveText(restaurantTitle || '');
  });

  test('should display restaurant details with all required information', async ({ page }) => {
    // Navigate to a specific restaurant (we'll use restaurant ID 1 as an example)
    await page.goto('/restaurant/1');
    
    // Wait for restaurant details to load
    await page.waitForSelector('[data-testid="restaurant-details"]', { timeout: 10000 });
    
    // Check that the restaurant title is present and not empty
    const restaurantTitle = page.locator('[data-testid="restaurant-details-title"]');
    await expect(restaurantTitle).toBeVisible();
    const titleText = await restaurantTitle.textContent();
    expect(titleText?.trim()).toBeTruthy();
    
    // Check that the restaurant description is present and not empty
    const restaurantDescription = page.locator('[data-testid="restaurant-details-description"]');
    await expect(restaurantDescription).toBeVisible();
    const descriptionText = await restaurantDescription.textContent();
    expect(descriptionText?.trim()).toBeTruthy();
    
    // Check that either publisher or category (or both) are present
    const publisherExists = await page.locator('[data-testid="restaurant-details-publisher"]').isVisible();
    const categoryExists = await page.locator('[data-testid="restaurant-details-category"]').isVisible();
    expect(publisherExists && categoryExists).toBeTruthy();
    
    // If publisher exists, check it has content
    if (publisherExists) {
      const publisherText = await page.locator('[data-testid="restaurant-details-publisher"]').textContent();
      expect(publisherText?.trim()).toBeTruthy();
    }
    
    // If category exists, check it has content
    if (categoryExists) {
      const categoryText = await page.locator('[data-testid="restaurant-details-category"]').textContent();
      expect(categoryText?.trim()).toBeTruthy();
    }
  });

  test('should display a button to save to favorite', async ({ page }) => {
    await page.goto('/restaurant/1');
    
    // Wait for restaurant details to load
    await page.waitForSelector('[data-testid="restaurant-details"]', { timeout: 10000 });
    
    // Check that the back restaurant button is present
    const backButton = page.locator('[data-testid="back-restaurant-button"]');
    await expect(backButton).toBeVisible();
    await expect(backButton).toContainText('Save to favorite');
    
    // Verify the button is clickable
    await expect(backButton).toBeEnabled();
  });

  test('should be able to navigate back to home from restaurant details', async ({ page }) => {
    await page.goto('/restaurant/1');
    
    // Wait for the page to load
    await page.waitForSelector('[data-testid="restaurant-details"]', { timeout: 10000 });
    
    // Find and click the back to all restaurants link
    const backLink = page.locator('a:has-text("Back to all restaurants")');
    await expect(backLink).toBeVisible();
    await backLink.click();
    
    // Verify we're back on the home page
    await expect(page).toHaveURL('/');
    await page.waitForSelector('[data-testid="restaurants-grid"]', { timeout: 10000 });
  });

  test('should handle navigation to non-existent restaurant gracefully', async ({ page }) => {
    // Navigate to a restaurant that doesn't exist
    await page.goto('/restaurant/99999');
    
    // The page should load without crashing
    // Check if there's an error message or if it handles gracefully
    await page.waitForTimeout(3000);
    
    // The page should either show an error or handle it gracefully
    // We expect the page to not crash and still have a valid title
    await expect(page).toHaveTitle(/Restaurant Details - Kuwait Fine Dining/);
  });
});
