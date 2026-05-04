def simple_linear_regression(x, y):
    """
    Computes simple linear regression y = mx + b
    Returns (m, b)
    """
    n = len(x)
    if n == 0:
        return 0, 0
    if n == 1:
        return 0, y[0]
        
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_sq = sum(xi*xi for xi in x)
    sum_xy = sum(x[i]*y[i] for i in range(n))
    
    denominator = (n * sum_x_sq - sum_x**2)
    if denominator == 0:
        return 0, sum_y / n
        
    m = (n * sum_xy - sum_x * sum_y) / denominator
    b = (sum_y - m * sum_x) / n
    return m, b

def moving_average(y, window=3):
    """
    Computes the moving average array
    """
    if len(y) < window:
        return y
    res = []
    for i in range(len(y) - window + 1):
        res.append(sum(y[i:i+window]) / window)
    return res

def forecast_next_days(historical_sales, days_to_predict=7):
    """
    historical_sales: list of daily sale totals (chronological, oldest to newest)
    Returns list of predicted next `days_to_predict` daily sale totals.
    """
    if not historical_sales:
        return [0] * days_to_predict
        
    # X values: 0, 1, 2, ...
    x = list(range(len(historical_sales)))
    y = historical_sales
    
    m, b = simple_linear_regression(x, y)
    
    predictions = []
    start_x = len(x)
    for i in range(days_to_predict):
        pred_val = m * (start_x + i) + b
        # Let's not have negative sales
        predictions.append(max(0, pred_val))
        
    return predictions
