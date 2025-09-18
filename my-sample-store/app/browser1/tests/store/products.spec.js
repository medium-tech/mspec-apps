import { test, expect } from '@playwright/test';


test('test - store - products - pagination', async ({ page }) => {
  await page.goto('http://localhost:7007/');

  await expect(page.locator('h1')).toContainText('my_sample_store');
  await page.getByRole('link', { name: 'store' }).last().click();

  await expect(page.locator('h1')).toContainText('store');
  await page.getByRole('link', { name: 'products' }).click();
  await expect(page.getByRole('heading')).toContainText('products');

  const fields = ['id', 'product_name', 'price', 'in_stock'];
  for (const field of fields) {
    await expect(page.locator('th', {hasText: field}).first()).toBeVisible();
  }

  // await page.getByRole('button', { name: '>>>' }).click();
  // await page.getByRole('button', { name: '<<<' }).click();
  await page.getByRole('button', { name: 'refresh' }).click();
});


test('test - store - products - instance', async ({ page }) => {



    //
    // test products
    //

    const textToContain = []

    // create item

    await page.goto('http://localhost:7007/store/products');
    await page.getByRole('button', { name: 'create' }).click();
    
    // product_name
    await page.locator('input[name="product_name"]').click();
    await page.locator('input[name="product_name"]').fill('one');
    textToContain.push('one');


    // price
    await page.locator('input[name="price"]').fill('1.4');
    textToContain.push('1.4');


    // in_stock
    await page.locator('input[name="in_stock"]').check();
    textToContain.push('yes');



    
    await page.getByRole('button', { name: 'submit' }).click();

    await expect(page.locator('#create-products-status')).toContainText('success');

    const createdItem = await page.locator('#created-products');
    const createdItemId = await createdItem.innerText();
    textToContain.push(createdItemId);
    
    await createdItem.click();

    for (const text of textToContain) {
        await expect(page.locator('#products-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'edit' }).click();
    await page.getByRole('button', { name: 'save' }).click();
    await page.getByRole('link', { name: createdItemId }).click();
    
    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'no, cancel' }).click();
    await page.getByRole('link', { name: 'products' }).click();
    
    await page.getByPlaceholder('products id').click();
    await page.getByPlaceholder('products id').fill(createdItemId);
    await page.getByRole('button', { name: 'get' }).click();

    for (const text of textToContain) {
        await expect(page.locator('#products-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'yes, please delete' }).click();
    await expect(page.locator('#products-not-found')).toContainText('item not found');
});

test('test - store - products - create random', async ({ page }) => {

  //
  // test create random products
  //

  await page.goto('http://localhost:7007/store/products/create');
  
  await page.getByRole('button', { name: 'random' }).click();
  await page.getByRole('button', { name: 'submit' }).click();

  await expect(page.locator('#create-products-status')).toBeVisible();
  await expect(page.locator('#create-products-status')).toContainText('success');
});