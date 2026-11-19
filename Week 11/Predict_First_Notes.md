# Week 11 Lab 9 Predict First Notes

INF1103 Programming with DevOps

Phone Myat Pyae Sone

This lab continues the Week 10 Lab 8 inventory system. The predictions below cover all eight Predict First prompts in Sections 2 to 5. The runnable checks are in `demo_predict_first.py` and `tests/test_lab9.py`.

## Starting diagnosis from Section 1.5

- Behaviour choices: `main.add_product()` selects physical or digital input, `InventoryStorage.load()` selects a product type, and `InventoryStorage.save()` selects a JSON representation. Week 10 has no discount logic yet; the discount if/elif in the PDF is a proposed example, not existing project code.
- Direct construction: Week 10 has two constructor calls in `main.add_product()`, two in `InventoryStorage.load()`, two in `demo_relationships.main()`, and two in `InventoryTests.setUp()`. That is eight calls across four functions, including the test fixture; production has four calls across two functions.
- Bad input: `int(input(...))` for stock can raise ValueError. Week 10 already catches it at the menu loop. Its JSON loader already handles a missing file by returning an empty inventory, and startup reports invalid JSON without overwriting it. The new CSV loader needs its own missing-file and per-row handling.
- Existing validation: stock is a non-negative whole number and order quantity is a positive whole number. Week 10 accepts a zero price; Lab 9 now requires a strictly positive price.

## 1 Adding a student discount

**Prompt:** Without Strategy, which class and method must change for a 5% student discount? What changes with Strategy?

**Prediction:** In the PDF's if/elif design, `Order.calculate_total()` must gain a student branch. With Strategy, add `StudentDiscount.apply()` and supply that strategy to an order. `Order.calculate_total()` stays the same. A menu may still need a new option so a user can select it.

**Observed:** The fourth strategy returns 237.5 for an order subtotal of 250. Order delegates to `self.discount.apply(total)` and never imports StudentDiscount. A test-local fifth strategy also works without changing Order.

**Difference and changes:** The prediction matched. The implementation adds StudentDiscount and a menu selection; Order contains no discount-type branching.

## 2 Changing the strategy on an existing order

**Prompt:** An order has lines totalling 250. Predict BulkDiscount(200, 20), then PercentageDiscount(10).

**Prediction:** Bulk gives 250 - 20 = 230. After `set_discount(PercentageDiscount(10))`, the same order gives 250 x 0.90 = 225. The second calculation starts with the line subtotal, not the already discounted 230.

**Observed:** The demo prints `Bulk: 230.0` and `Percentage: 225.0`. The order still contains the original product and quantity.

**Difference and changes:** Matched; no corrective change was needed.

## 3 Order and DiscountStrategy relationship

**Prompt:** Is this association, aggregation or composition? Give multiplicities and consider a shared strategy.

**Prediction:** Association: an order uses a discount strategy. The strategy can exist independently and can be shared by multiple orders. At the DiscountStrategy end the multiplicity is 1: each Order has exactly one active strategy, including the default NoDiscount. At the Order end it is 0..*: a strategy can serve zero or many orders.

**Observed:** Two orders given the same PercentageDiscount object have identical strategy references. Replacing the first order's strategy leaves the second using the shared object. The demo prints True for both checks. Omitting the constructor argument creates a NoDiscount object.

**Difference and changes:** Matched. The constructor argument is optional, but the active relationship is still 1 because None is replaced immediately.

## 4 Unknown product type

**Prompt:** What happens for `ProductFactory.create("service", ...)`? Which line raises and what happens if uncaught?

**Prediction:** The final branch in `ProductFactory.create()` executes `raise ValueError(f"Unknown product type: {product_type}")`. The message is `Unknown product type: service`. Without a handler the exception propagates, prints a traceback and terminates the script with a nonzero exit code.

**Observed:** The demo catches the exception and prints `ValueError: Unknown product type: service` so later checks can run. A separate subprocess test deliberately leaves it uncaught and checks the nonzero exit code and traceback pointing to ProductFactory.py.

**Difference and changes:** Matched. The demo's handler deliberately allows the remaining demonstrations to continue; the subprocess verifies the uncaught case.

## 5 Adding BundleProduct and counting changes

**Prompt:** Count the places that need changes before and after Factory. Why does the factory still break OCP?

**Prediction:** Before Factory there are two production functions that construct concrete products: `main.add_product()` and `InventoryStorage.load()` (four calls). Including the relationship demo and test setup gives four functions (eight calls). After Factory, construction decisions live in one method, `ProductFactory.create()`, which has the two concrete constructor calls. Existing callers use the factory.

**Observed:** Code inspection confirms these counts. The Week 11 menu, JSON loader, CSV loader, demos and test fixtures request products through ProductFactory. The factory still needs a new branch for BundleProduct, so it is not closed to modification. Centralising this small decision is a reasonable trade-off compared with a plugin registry.

**Difference and changes:** The count describes construction, not every feature needed to support bundles. A complete BundleProduct feature also needs its new class, menu input, JSON read/write schema, and tests. Factory does not remove those responsibilities. The menu and JSON loader still select which fields to pass; the JSON serializer still knows concrete types. No BundleProduct is implemented in this lab.

## 6 LSP and digital stock validation

**Prompt:** Can DigitalProduct skip or change Product's rule against negative stock?

**Prediction:** No. Code using a Product must be able to rely on the same stock contract for either subclass. Both PhysicalProduct and DigitalProduct must reject negative stock; a subtype must not silently allow an invalid state. It must also avoid rejecting otherwise valid Product operations by strengthening preconditions.

**Observed:** Both inherit Product's validation. Setting stock to -1 raises `ValueError: Stock must be a non-negative whole number.` for each type. Zero stock is accepted. Constructor, setter and update-method checks use the same rule.

**Difference and changes:** Matched. The existing inherited rule was retained. Price validation was tightened separately to satisfy this week's requirement.

## 7 Positive price input

**Prompt:** The user enters abc, then -5, then 12.50. Predict the exact messages and return value.

**Prediction:** With the prompt `Price: `, the interaction is:

```text
Price: abc
Please enter a valid number, e.g. 12.50
Price: -5
Please enter a number greater than zero.
Price: 12.50
```

The function returns the float 12.5. It prints no success message. The input entries shown after the prompts are user input echoed by the terminal.

**Observed:** Mocked input verifies three requests, those two error messages in that order, and the returned value 12.5. The demo prints `Returned: 12.5` outside the helper. Mocking input suppresses the prompt and keyboard echo.

**Difference and changes:** Matched. A finite-value check also rejects nan and infinity, which float() accepts but which are unsuitable prices.

## 8 CSV loading and a missing file

**Prompt:** How many sample products load, which messages print, and in which order? What happens after the CSV is renamed?

**Prediction:** Three products load: P001, D001 and P003. Row numbers include the header as row 1. The output is:

```text
Skipping row 4: Unknown product type: service
Skipping row 5: could not convert string to float: 'abc'
3 products loaded.
Load attempt finished.
```

The successful outer try opens the file; else reads the rows. Each bad row runs its own except ValueError and loading continues. Finally runs last. If the file is renamed, the outer except FileNotFoundError runs, else is skipped, and finally still runs. For the checked missing path:

```text
Products file not found: products_missing.csv
Load attempt finished.
```

There is no products-loaded summary in the missing-file case.

**Observed:** The demo and automated tests reproduce these messages and confirm the three product IDs. The missing-file check uses a nonexistent filename, which exercises the same branch as renaming products.csv without changing the supplied sample file.

**Difference and changes:** Matched. The factory supplies 0.0 for weight or download size when the five-column lab CSV omits them. Explicit values from the menu and JSON remain supported. Invalid headers, malformed rows, duplicate IDs and invalid model values are also reported without adding a partial product.
