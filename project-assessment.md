##Project Assessment - week 4

**For query classification:**

1. How many unique categories did you see in your rolled up training data when you set the minimum number of queries per category to 100? To 1000?
   1. with --min_queries **100**:
      - number of unique queries: `407`
   2. with --min_queries **1000**:
      - `74`
2. What values did you achieve for P@1, R@3, and R@5? You should have tried at least a few different models, varying the minimum number of queries per category as well as trying different fastText parameters or query normalization. Report at least 3 of your runs.
   1. I trained my model with fasttext _autotune_
      1. with --min_queries **1000**
         1. **P@1** = `0.578` ,
         2. **P@3** = `0.257`  , **R@3** = `0.772`
         3. **P@5** = `0.167`  , **R@5** = `0.833`
      2. with --min_queries **100**
         1. **P@1** = `0.523`,
         2. **P@3** = `0.235`  , **R@3** = `0.706`
         3. **P@5** = `0.153`  , **R@5** = `0.766`
3. For integrating query classification with search:
   1. Give 2 or 3 examples of queries where you saw a dramatic positive change in the results because of filtering. Make sure to include the classifier output for those queries.
      1. iphone 4 -> `pcmcat209400050001`
      2. ps3 -> `abcat0703001`
      3. laptops -> `pcmcat247400050000`
      4. dr dre beats -> `pcmcat144700050004`
      5. sony tv -> `abcat0101001`
   2. Given 2 or 3 examples of queries where filtering hurt the results, either because the classifier was wrong or for some other reason. Again, include the classifier output for those queries.
      1. microsoft office -> `pcmcat245100050028`
      2. logitech webcam -> `abcat0403000`
      3. r kelly -> `cat02015`