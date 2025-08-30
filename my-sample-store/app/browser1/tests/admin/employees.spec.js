import { test, expect } from '@playwright/test';


test('test - admin - employees - pagination', async ({ page }) => {
  await page.goto('http://localhost:7007/');

  await expect(page.locator('h1')).toContainText('my_sample_store');
  await page.getByRole('link', { name: 'admin' }).last().click();

  await expect(page.locator('h1')).toContainText('admin');
  await page.getByRole('link', { name: 'employees' }).click();
  await expect(page.getByRole('heading')).toContainText('employees');

  const fields = ['id', 'employee_name', 'position', 'hire_date', 'email', 'phone_number', 'salary'];
  for (const field of fields) {
    await expect(page.locator('th', {hasText: field}).first()).toBeVisible();
  }

  // await page.getByRole('button', { name: '>>>' }).click();
  // await page.getByRole('button', { name: '<<<' }).click();
  await page.getByRole('button', { name: 'refresh' }).click();
});


test('test - admin - employees - instance', async ({ page }) => {

    const textToContain = []

    // create item

    await page.goto('http://localhost:7007/admin/employees');
    await page.getByRole('button', { name: 'create' }).click();
    
    // employee_name
    await page.locator('input[name="employee_name"]').click();
    await page.locator('input[name="employee_name"]').fill('one');
    textToContain.push('one');


    // position
    await page.locator('select[name="position"]').selectOption('Manager');
    textToContain.push('Manager');


    // hire_date
    await page.locator('input[name="hire_date"]').click();
    await page.locator('input[name="hire_date"]').fill('one');
    textToContain.push('one');


    // email
    await page.locator('input[name="email"]').click();
    await page.locator('input[name="email"]').fill('one');
    textToContain.push('one');


    // phone_number
    await page.locator('input[name="phone_number"]').click();
    await page.locator('input[name="phone_number"]').fill('one');
    textToContain.push('one');


    // salary
    await page.locator('input[name="salary"]').fill('1.4');
    textToContain.push('1.4');



    
    await page.getByRole('button', { name: 'submit' }).click();

    await expect(page.locator('#create-employees-status')).toContainText('success');

    const createdItem = await page.locator('#created-employees');
    const createdItemId = await createdItem.innerText();
    textToContain.push(createdItemId);
    
    await createdItem.click();

    for (const text of textToContain) {
        await expect(page.locator('#employees-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'edit' }).click();
    await page.getByRole('button', { name: 'save' }).click();
    await page.getByRole('link', { name: createdItemId }).click();
    
    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'no, cancel' }).click();
    await page.getByRole('link', { name: 'employees' }).click();
    
    await page.getByPlaceholder('employees id').click();
    await page.getByPlaceholder('employees id').fill(createdItemId);
    await page.getByRole('button', { name: 'get' }).click();

    for (const text of textToContain) {
        await expect(page.locator('#employees-read-tbody')).toContainText(text);
    }

    await page.getByRole('button', { name: 'delete' }).click();
    await page.getByRole('button', { name: 'yes, please delete' }).click();
    await expect(page.locator('#employees-not-found')).toContainText('item not found');
});

test('test - admin - employees - create random', async ({ page }) => {
  await page.goto('http://localhost:7007/admin/employees/create');
  
  await page.getByRole('button', { name: 'random' }).click();
  await page.getByRole('button', { name: 'submit' }).click();

  await expect(page.locator('#create-employees-status')).toBeVisible();
  await expect(page.locator('#create-employees-status')).toContainText('success');
});