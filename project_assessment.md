### Project Assessment

To assess your project work, you should be able to answer the following questions:

+ For classifying product names to categories:


+  **What precision (P@1) were you able to achieve?**
	+ The result of my best attempt with data pruned by `--min_products  200`

    	N       10000
		P@1     0.887
		R@1     0.887
    


- **What fastText parameters did you use?**
	+ In my early attempts after manual experiments I used an approach similar to grid search with the following parameters
	
    ` dim=(10, 20, 50, 100) lr=(0.1, 0.15, 0.3)  wordNgrams=(1 2 3) epoch=(25, 50, 100)`

	but then I used fasttext **autotune** feature to get the best model.


- **How did you transform the product names?**
	1. Lowercase() and strip() text
	2. New line chars removed
	3. Punctuation removed
	4. Accented chars normalized
	5. Stemming with SnowballStemmer


- **How did you prune infrequent category labels, and how did that affect your precision?**
	+ I took advantage of Pandas to remove infrequent labels.
	+ without pruning infrequent category labels the best `P@1` I could get was **0.608** .
	+ with `--min_products 50` I got :  **0.728**
	+ with `--min_products 100` I got :  **0.812**
	+ with `--min_products 200` I got :  **0.887**

-** How did you prune the category tree, and how did that affect your precision?**
+ I just added a new switch called `--cat_granularity_level` which basically recieves the number of backward steps from the leaf depth to select the right leaf ancestor and use it as a category label.