import { test, expect } from '@playwright/test';


test('test - content - post - pagination', async ({ page }) => {
  await page.goto('http://localhost:8008/');

  await expect(page.locator('h1')).toContainText('simple_social_network');
  await page.getByRole('link', { name: 'content' }).last().click();

  await expect(page.locator('h1')).toContainText('content');
  await page.getByRole('link', { name: 'post' }).click();
  await expect(page.getByRole('heading')).toContainText('post');

  const fields = ['id', 'user_id', 'content'];
  for (const field of fields) {
    await expect(page.locator('th', {hasText: field}).first()).toBeVisible();
  }

  // await page.getByRole('button', { name: '>>>' }).click();
  // await page.getByRole('button', { name: '<<<' }).click();
  await page.getByRole('button', { name: 'refresh' }).click();
});


test('test - content - post - instance', async ({ page }) => {

    //
    // create user and login because post requires auth
    //

    const testEmail = `test-post-${Math.random()}-${Date.now()}@example.com`;
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
    await page.goto('http://localhost:8008/template-module/post/create');



    //
    // test post
    //

    const textToContain = []

    // create item

    await page.goto('http://localhost:8008/content/post');
    await page.getByRole('button', { name: 'create' }).click();
    
    // content
    await page.locator('input[name="content"]').click();
    await page.locator('input[name="content"]').fill('one');
    textToContain.push('one');



    
    await page.getByRole('button', { name: 'submit' }).click();

    await expect(page.locator('#create-post-status')).toContainText('success');

    const createdItem = await page.locator('#created-post');
    const createdItemId = await createdItem.innerText();
    textToContain.push(createdItemId);
    
    await createdItem.click();

    for (const text of textToContain) {
        await expect(page.locator('#post-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'edit' }).click();
    await page.getByRole('button', { name: 'save' }).click();
    await page.getByRole('link', { name: createdItemId }).click();
    
    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'no, cancel' }).click();
    await page.getByRole('link', { name: 'post' }).click();
    
    await page.getByPlaceholder('post id').click();
    await page.getByPlaceholder('post id').fill(createdItemId);
    await page.getByRole('button', { name: 'get' }).click();

    for (const text of textToContain) {
        await expect(page.locator('#post-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'yes, please delete' }).click();
    await expect(page.locator('#post-not-found')).toContainText('item not found');
});

test('test - content - post - create random', async ({ page }) => {
    //
    // create user and login because post requires auth
    //

    const testEmail = `test-post-${Math.random()}-${Date.now()}@example.com`;
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
    await page.goto('http://localhost:8008/template-module/post/create');


  //
  // test create random post
  //

  await page.goto('http://localhost:8008/content/post/create');
  
  await page.getByRole('button', { name: 'random' }).click();
  await page.getByRole('button', { name: 'submit' }).click();

  await expect(page.locator('#create-post-status')).toBeVisible();
  await expect(page.locator('#create-post-status')).toContainText('success');
});