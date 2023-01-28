

Recall and precision for top k result evaluation. 
We will define two functions named recall, precision that takes lists of actual conditions and predicted conditions, a K value, and returns a recall@K, precision@K score.

``` Python
# recall@k function
def recall(actual, predicted, k):
    act_set = set(actual)
    pred_set = set(predicted[:k])
    result = round(len(act_set & pred_set) / float(len(act_set)), 2)
    return result
```

``` Python
# precesion@k function
def precision(actual, predicted, k):
    act_set = set(actual)
    pred_set = set(predicted[:k])
    result = round(len(act_set & pred_set) / float(len(pred_set)), 2)
    return result
```
    
https://www.pinecone.io/learn/offline-evaluation/
    
