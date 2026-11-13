# Lab 8 Predict First

## 2 Supplier variable

Prediction: Both products should still show the supplier after `del supplier`. That only deletes the variable, and the products still have a reference to the same supplier.

What happened: Both printed Music Shop and its email. They still shared the same supplier object. Matched, so nothing to change.

## 3 Removing a product from inventory

Prediction: The product should still work after I remove it from Inventory A. The inventory just holds a reference, so my product variable should still work.

What happened: I could update its stock to 8 and add that exact same object to Inventory B. Matched, so nothing to change.

## 4 Same product in two orders

Prediction: Two order lines, but just one shared product for those lines. Each order makes its own line and both lines point to the same product.

What happened: Comparing the lines with `is` gave False, and comparing their products gave True. Matched, so nothing to change. Adding the music product afterwards made three lines and two products overall.

## 7 Fulfilment messages

Prediction: The physical product should print "This product requires physical shipping." The digital one should print "This product is delivered digitally by download."

What happened: Both printed those messages from the same loop. Matched, so nothing to change.

## LSP check

Both products inherit `update_stock()`, so giving either one a valid stock quantity sets its stock to that number. The same `show_product_details(product)` function also works for both, with each product printing its own details and fulfilment message.

The proposed digital `update_stock()` breaks LSP because code expecting a Product would suddenly get an error. I'd keep the inherited stock behaviour for this lab. If digital products really had no stock, I'd move stock operations into a separate capability and rethink what belongs in Product.
