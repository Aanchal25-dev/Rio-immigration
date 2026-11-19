# Migration Notes for Accounting App Refactoring

## Summary
The accounting app has been refactored to use `rio.Applicant` and `rio.Services` directly instead of separate `Customer` and `ProductService` models.

## Changes Made to Models

### Removed Models
- `Customer` - Now using `rio.Applicant` directly
- `ProductService` - Now using `rio.Services` directly

### Updated Models
- `Invoice.customer` → `Invoice.applicant` (ForeignKey to `rio.Applicant`)
- `InvoiceItem.product_service` → `InvoiceItem.service` (ForeignKey to `rio.Services`, nullable)
- `Payment.customer` → `Payment.applicant` (ForeignKey to `rio.Applicant`)

## Migrations Required

When you run `python manage.py makemigrations` on the server, Django will detect:

1. **Removal of Customer model** - Will create a migration to:
   - Drop the `accounting_customer` table
   - Remove the foreign key from `Invoice.customer` to `Customer`
   - Remove the foreign key from `Payment.customer` to `Customer`

2. **Removal of ProductService model** - Will create a migration to:
   - Drop the `accounting_productservice` table
   - Remove the foreign key from `InvoiceItem.product_service` to `ProductService`

3. **New Foreign Keys** - Will create migrations to:
   - Add `Invoice.applicant` (ForeignKey to `rio.Applicant`)
   - Add `InvoiceItem.service` (ForeignKey to `rio.Services`, nullable)
   - Add `Payment.applicant` (ForeignKey to `rio.Applicant`)

## Data Migration Considerations

⚠️ **IMPORTANT**: If you have existing data in the `Customer` and `ProductService` tables:

1. **Customer → Applicant Migration**:
   - Existing `Invoice.customer` records need to be migrated to `Invoice.applicant`
   - If a Customer was linked to an Applicant (via `Customer.applicant`), use that relationship
   - If not linked, you may need to create Applicants or handle orphaned invoices

2. **ProductService → Services Migration**:
   - Existing `InvoiceItem.product_service` records need to be migrated to `InvoiceItem.service`
   - Match ProductService names to Services names, or handle orphaned items

## Recommended Migration Strategy

1. **Before running migrations**, create a data migration script to:
   - Map existing Customer records to Applicant records
   - Map existing ProductService records to Services records
   - Update all Invoice, InvoiceItem, and Payment records accordingly

2. **Run makemigrations** on the server to generate the schema changes

3. **Review the generated migrations** and add data migration steps if needed

4. **Test on a staging environment** before applying to production

## Files Modified (No Migration Files Changed)

- `rio_imm/accounting/models.py` - Model definitions updated
- `rio_imm/accounting/views.py` - Views updated to use Applicant/Services, customer/product-service management views commented out
- `rio_imm/accounting/urls.py` - Customer/product-service URLs commented out
- `rio_imm/templates/accounting/add_invoice.html` - Template updated to use applicants/services

## Commented Out Views

The following views have been commented out (not deleted) in case you need to reference them:
- `customers()` - List customers
- `create_customer()` - Create customer
- `edit_customer()` - Edit customer
- `products_services()` - List products/services
- `create_product_service()` - Create product/service
- `edit_product_service()` - Edit product/service

These views are no longer accessible via URLs, but the code is preserved in comments.
