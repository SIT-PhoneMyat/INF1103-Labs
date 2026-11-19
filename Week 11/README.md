# Week 11 Lab 9

This is a standalone continuation of the Week 10 Lab 8 inventory system.

From this folder, run:

```powershell
python main.py
python demo_predict_first.py
python demo_relationships.py
python -m unittest discover -s tests -v
```

Python 3.10 or later is required. The application and tests use only the standard library.

`Predict_First_Notes.md` contains all eight predictions, observed results and explanations. The Word version is `Lab9_Predict_First_Notes.docx`; its layout has been reviewed and accepted.

New source files implement DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount, ProductFactory, the positive-price helper, and the CSV loader. The previous relationship model and JSON persistence remain in use. The menu adds option 13 to change an order discount and option 14 to import CSV products. Orders and their discounts remain session-only.

`products.csv` matches the lab sample, including two deliberately invalid rows. Importing it into an empty inventory loads three products and reports the two skipped rows. Reimporting skips duplicate IDs. Its five-column schema omits weight and download size, so the factory uses 0.0 for those fields. JSON and menu creation retain explicit values.

`UML_Class_Diagram.drawio` is an editable diagrams.net document with two pages: the domain and design patterns, and supporting persistence dependencies. Open it in draw.io or diagrams.net using File > Open From > Device. The main page includes association multiplicities, aggregation, composition, inheritance, interface realization, and the factory's dashed `creates` dependency.

Git/Docker workflow screenshots remain to complete the lab submission.

PNG image copies are also available: `UML_Class_Diagram.png` (main diagram) and `UML_Persistence_Dependencies.png` (supporting page). The `.drawio` file remains the editable source.
