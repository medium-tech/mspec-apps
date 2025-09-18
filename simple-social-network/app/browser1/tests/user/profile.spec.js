import { test, expect } from '@playwright/test';


test('test - user - profile - pagination', async ({ page }) => {
  await page.goto('http://localhost:8008/');

  await expect(page.locator('h1')).toContainText('simple_social_network');
  await page.getByRole('link', { name: 'user' }).last().click();

  await expect(page.locator('h1')).toContainText('user');
  await page.getByRole('link', { name: 'profile' }).click();
  await expect(page.getByRole('heading')).toContainText('profile');

  const fields = ['id', 'user_id', 'username', 'bio'];
  for (const field of fields) {
    await expect(page.locator('th', {hasText: field}).first()).toBeVisible();
  }

  // await page.getByRole('button', { name: '>>>' }).click();
  // await page.getByRole('button', { name: '<<<' }).click();
  await page.getByRole('button', { name: 'refresh' }).click();
});


test('test - user - profile - instance', async ({ page }) => {

    //
    // create user and login because profile requires auth
    //

    const testEmail = `test-profile-${Math.random()}-${Date.now()}@example.com`;
    const testPassword = 'testpassword123';
    const testName = 'Test User';

    // Step 1: Create User
    await page.goto('http://localhost:8008/');
    await page.getByRole('button', { name: 'Create User' }).click();

    await expect(page.locator('h1')).toContainText('Create User - simple_social_network');

    // Fill out the create user form
    await page.locator('input[name="name"]').fill(testName);
    await page.locator('input[name="email"]').fill(testEmail);
    await page.locator('input[name="password1"]').fill(testPassword);
    await page.locator('input[name="password2"]').fill(testPassword);

    // Submit the form
    await page.getByRole('button', { name: 'Create User' }).click();

    // Wait for success message
    await expect(page.locator('#message')).toContainText('User created successfully');

    // Step 2: Login
    await page.getByRole('link', { name: 'Login' }).click();

    await expect(page.locator('h1')).toContainText('Login - simple_social_network');

    // Fill out the login form
    await page.locator('input[name="email"]').fill(testEmail);
    await page.locator('input[name="password"]').fill(testPassword);

    // Submit the login form
    await page.getByRole('button', { name: 'Login' }).click();

    // Wait for success message and redirect
    await expect(page.locator('#message')).toContainText('Login successful');

    // Wait for redirect to home page
    await page.waitForURL('http://localhost:8008/');

    // Create random multi model item
    await page.goto('http://localhost:8008/template-module/profile/create');



    //
    // test profile
    //

    const textToContain = []

    // create item

    await page.goto('http://localhost:8008/user/profile');
    await page.getByRole('button', { name: 'create' }).click();
    
    // username
    await page.locator('input[name="username"]').click();
    await page.locator('input[name="username"]').fill('one');
    textToContain.push('one');


    // bio
    await page.locator('input[name="bio"]').click();
    await page.locator('input[name="bio"]').fill('one');
    textToContain.push('one');



    
    await page.getByRole('button', { name: 'submit' }).click();

    await expect(page.locator('#create-profile-status')).toContainText('success');

    const createdItem = await page.locator('#created-profile');
    const createdItemId = await createdItem.innerText();
    textToContain.push(createdItemId);
    
    await createdItem.click();

    for (const text of textToContain) {
        await expect(page.locator('#profile-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'edit' }).click();
    await page.getByRole('button', { name: 'save' }).click();
    await page.getByRole('link', { name: createdItemId }).click();
    
    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'no, cancel' }).click();
    await page.getByRole('link', { name: 'profile' }).click();
    
    await page.getByPlaceholder('profile id').click();
    await page.getByPlaceholder('profile id').fill(createdItemId);
    await page.getByRole('button', { name: 'get' }).click();

    for (const text of textToContain) {
        await expect(page.locator('#profile-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'yes, please delete' }).click();
    await expect(page.locator('#profile-not-found')).toContainText('item not found');
});

test('test - user - profile - create random', async ({ page }) => {
    //
    // create user and login because profile requires auth
    //

    const testEmail = `test-profile-${Math.random()}-${Date.now()}@example.com`;
    const testPassword = 'testpassword123';
    const testName = 'Test User';

    // Step 1: Create User
    await page.goto('http://localhost:8008/');
    await page.getByRole('button', { name: 'Create User' }).click();

    await expect(page.locator('h1')).toContainText('Create User - simple_social_network');

    // Fill out the create user form
    await page.locator('input[name="name"]').fill(testName);
    await page.locator('input[name="email"]').fill(testEmail);
    await page.locator('input[name="password1"]').fill(testPassword);
    await page.locator('input[name="password2"]').fill(testPassword);

    // Submit the form
    await page.getByRole('button', { name: 'Create User' }).click();

    // Wait for success message
    await expect(page.locator('#message')).toContainText('User created successfully');

    // Step 2: Login
    await page.getByRole('link', { name: 'Login' }).click();

    await expect(page.locator('h1')).toContainText('Login - simple_social_network');

    // Fill out the login form
    await page.locator('input[name="email"]').fill(testEmail);
    await page.locator('input[name="password"]').fill(testPassword);

    // Submit the login form
    await page.getByRole('button', { name: 'Login' }).click();

    // Wait for success message and redirect
    await expect(page.locator('#message')).toContainText('Login successful');

    // Wait for redirect to home page
    await page.waitForURL('http://localhost:8008/');

    // Create random multi model item
    await page.goto('http://localhost:8008/template-module/profile/create');


  //
  // test create random profile
  //

  await page.goto('http://localhost:8008/user/profile/create');
  
  await page.getByRole('button', { name: 'random' }).click();
  await page.getByRole('button', { name: 'submit' }).click();

  await expect(page.locator('#create-profile-status')).toBeVisible();
  await expect(page.locator('#create-profile-status')).toContainText('success');
});