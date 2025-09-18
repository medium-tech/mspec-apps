import { test, expect } from '@playwright/test';


test('test - store - customers - pagination', async ({ page }) => {
  await page.goto('http://localhost:7007/');

  await expect(page.locator('h1')).toContainText('my_sample_store');
  await page.getByRole('link', { name: 'store' }).last().click();

  await expect(page.locator('h1')).toContainText('store');
  await page.getByRole('link', { name: 'customers' }).click();
  await expect(page.getByRole('heading')).toContainText('customers');

  const fields = ['id', 'customer_name', 'email', 'phone_number'];
  for (const field of fields) {
    await expect(page.locator('th', {hasText: field}).first()).toBeVisible();
  }

  // await page.getByRole('button', { name: '>>>' }).click();
  // await page.getByRole('button', { name: '<<<' }).click();
  await page.getByRole('button', { name: 'refresh' }).click();
});


test('test - store - customers - instance', async ({ page }) => {



    //
    // test customers
    //

    const textToContain = []

    // create item

    await page.goto('http://localhost:7007/store/customers');
    await page.getByRole('button', { name: 'create' }).click();
    
    // customer_name
    await page.locator('input[name="customer_name"]').click();
    await page.locator('input[name="customer_name"]').fill('one');
    textToContain.push('one');


    // email
    await page.locator('input[name="email"]').click();
    await page.locator('input[name="email"]').fill('one');
    textToContain.push('one');


    // phone_number
    await page.locator('input[name="phone_number"]').click();
    await page.locator('input[name="phone_number"]').fill('one');
    textToContain.push('one');



    
    await page.getByRole('button', { name: 'submit' }).click();

    await expect(page.locator('#create-customers-status')).toContainText('success');

    const createdItem = await page.locator('#created-customers');
    const createdItemId = await createdItem.innerText();
    textToContain.push(createdItemId);
    
    await createdItem.click();

    for (const text of textToContain) {
        await expect(page.locator('#customers-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'edit' }).click();
    await page.getByRole('button', { name: 'save' }).click();
    await page.getByRole('link', { name: createdItemId }).click();
    
    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'no, cancel' }).click();
    await page.getByRole('link', { name: 'customers' }).click();
    
    await page.getByPlaceholder('customers id').click();
    await page.getByPlaceholder('customers id').fill(createdItemId);
    await page.getByRole('button', { name: 'get' }).click();

    for (const text of textToContain) {
        await expect(page.locator('#customers-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'yes, please delete' }).click();
    await expect(page.locator('#customers-not-found')).toContainText('item not found');
});

test('test - store - customers - create random', async ({ page }) => {

  //
  // test create random customers
  //

  await page.goto('http://localhost:7007/store/customers/create');
  
  await page.getByRole('button', { name: 'random' }).click();
  await page.getByRole('button', { name: 'submit' }).click();

  await expect(page.locator('#create-customers-status')).toBeVisible();
  await expect(page.locator('#create-customers-status')).toContainText('success');
});