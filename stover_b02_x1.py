# Preston Stover - BERN02 Exercise 1 - 01 Sep 2026
import csv
import math

def local_points(x, y, x_0, k):
    '''takes two variable lists x and y, target point x_0, and number of closest points k as inputs
    processes variable lists to calculate x - x_0 distance squared and returns two lists 
    of x and y values for the k closest points and generates distance weights w'''

    xsq_distances = []
    # for every point x_i, calculate squared distance from x_0 and append to three-item list inlcuding x and y pair
    for i in range(len(x)):
        xsq_dist = (x[i] - x_0)**2
        xsq_distances.append((xsq_dist, x[i], y[i]))
    # sort the (dist, x, y) data point list with lowest xsq_dist first
    xsq_distances.sort()

    # pull out x and y pairs from k data points with smallest xsq_dist
    # x is second variable and y is third variable in listed three-dimension points
    x_local = [point[1] for point in xsq_distances[:k]]
    y_local = [point[2] for point in xsq_distances[:k]]
    # add K_i,0 weight values based on inverse distance with small positive value to avoid /0
    w_local = [1.0 / (point[0] + 1.0) for point in xsq_distances[:k]]

    return x_local, y_local, w_local


def local_lin(x, y, x_0, k, w):
    ''' given x and y variable lists, returns slope, intercept, and variance
    using sum of squared errors methods '''
    sum_w = sum(w)
    # calculate means based on equation given in LOESS lecture
    # dividing by sum_w scales the weighted proportions to sum=1
    mx = (sum(x[i] * w[i] for i in range(k)) / sum_w)
    my = (sum(y[i] * w[i] for i in range(k)) / sum_w)
    # loop through all x and y to calculate sum squared err values
    sxx = 0
    sxy = 0
    syy = 0
    sse = 0
    for i in range(k):
        sxx += (w[i] * (x[i] - mx)**2)
        sxy += (w[i] * (x[i] - mx) * (y[i] - my))
        syy += (w[i] * (y[i] - my)**2)

    # calculate slope and intercept using sq errs
    slope = sxy / sxx
    intercept = my - (slope * mx)
    # calculate residual var with sq errs: var = SSE / (n-2)
    # using slope = sxy / sxx and SSE = syy - 2*slope*sxy + sxx*slope**2:
    # had to change this for the weighted approach, iterating through list to add individual weights
    for i in range(k):
        sse += (w[i] * (y[i] - (intercept + slope * x[i]))**2)
    sigma_hat_sq = sse / (k - 2)

    # predictions for y_hat at x_0
    y_pred = (intercept + slope * x_0)
    # predicted value variance equation from lecture material:
    v_pred = sigma_hat_sq * ((1/k) + (((x_0 - mx)**2) / sxx))
    alpha = 0.05
    # use dof(=k-2) and alpha to look up t-score threshold using scipy library
    # this was used to calculate margin of error at first before I switched to sd
    # lambda_alpha = t.ppf(1 - alpha / 2, k - 2)
    # +/- confidence interval
    y_sd = math.sqrt(v_pred)

    return float(y_pred), float(y_sd)


def local_reg(x, y, x_0, k):
    se = []
    pred = []
    for i in range(len(x_0)):
        xl, yl, wl = local_points(x, y, x_0[i], k)
        y_pred, y_se = local_lin(xl, yl, x_0[i], k, wl)
        pred.append(y_pred)
        se.append(y_se)
    return pred, se


#---------------------------------------

# Read variable data to lists
x = []
y = []
with open("pollution_cleaneddata.csv", mode="r") as file:
    # Turn rows of csv into Python dictionaries. Top row are keys and each row below have data appended to each key.
    var_Dicts = csv.DictReader(file)
    for row in var_Dicts:
        # response variable: MORT - Total age-adjusted mortality rate per 100,000
        y.append(float(row["MORT"]))
        # predictor variable: POOR - % of families with income < $3000
        x.append(float(row["POOR"]))

# predict for POOR = 10, 18, and 25 percent
x_0 = 10.0, 18.0, 25.0
# loop k values closest to x_0 and rerturn prediction and sdt dev x_0:
pred, se = local_reg(x, y, x_0, k=12)
print(f"{'x_0 '} | Predicted +/- SE")
print('----------------------------')
for i in range(len(pred)):
    print(f"{x_0[i]} | {pred[i]:.0f} +/- {se[i]:.0f}")