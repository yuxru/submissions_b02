# Preston Stover - BERN02 - 04.09.2026
import csv
import math
import random

# extract data
x = []
y = []
with open("bird_count.csv", mode="r") as file:
    # Turn rows of csv into Python dictionaries. Top row are keys and each row below have data appended to each key.
    var_Dicts = csv.DictReader(file)
    for row in var_Dicts:
        # read year and bird count into two lists
        y.append(float(row["count"]))
        # move year mean to x=0 at mean(x) of years in data to avoid expected 10^29 bird count at year 0
        x.append(float(row["yr"]) - 2005.6923)

# initialize parameter vector (matrix?)
b0 = 0.0
b1 = 0.0
betas = (b0, b1)

# optimize parameters using Newton-Raphnison iteration approach
loops = 16
for j in range(loops):
    # initialize/reset variables:
    # gradient matrix (vector?)
    g0 = 0.0
    g1 = 0.0
    gradients = (g0, g1)
    # hessian matrix
    h00 = 0.0
    h01 = 0.0
    h10 = 0.0
    h11 = 0.0

    for i in range(len(x)):
        # lambda(x_i): expected intensity for point x_i
        lam = math.exp(b0 + b1 * x[i])

        # GRADIENT VECTOR
        # partial first derivatives of beta 0 and beta 1 from likelihood function for Poisson GLM in lecture notes
        # L = log l(y|bo,b1,x) -> partial dL / d(b0 or b1):
        g0 += y[i] - lam
        g1 += x[i] * (y[i] - lam) 

        # HESSIAN MATRIX
        # partial second derivatives for b0 and b1 (2 x 2)
        h00 += -lam
        h01 += -x[i] * lam
        h10 += -x[i] * lam
        h11 += -(x[i]**2) * lam
    # calculate inverted Hessian
    determinate = (h00 * h11) - (h01 * h10)
    inv_h00 = h11 / determinate
    inv_h01 = -h01 / determinate
    inv_h10 = -h10 / determinate
    inv_h11 = h00 / determinate

    # update parameter vector with: -= H^(-1) * g
    # inverse Hessian * gradient = 2 x 1 matrix values which are subtracted from b0 and b1
    b0 -= (inv_h00 * g0 + inv_h01 * g1)
    b1 -= (inv_h10 * g0 + inv_h11 * g1)
    print('iteration:', j+1, b0, b1)

print('Final B_0, B_1:', b0, b1)

# generate new data points
new_years = [1996, 2026, 2100]
new_counts = []
knuth_loop = 0
for year in new_years:
    # expected intensity per new year
    lam = math.exp(b0 + b1 * (year - 2005.6923))
    # generate bird count integer based on Poisson distribution Po(lam(x_0))
    # wanted to make Poisson distribution without using NumPy library
    # used Knuth's Algorithm approach
    p = 1.0
    k = 0
    while p > (math.exp(-lam)):
        k += 1
        # best practice to use .random (uses C) instead of .uniform(uses Python) for speed, doesn't matter here though
        # .random returns float in range [0,1.0)
        p *= random.random()
        knuth_loop += 1
    new_counts.append(k - 1)
print('Knuth loops:', knuth_loop)
print('New data points - year and bird count:')
for year, count in zip(new_years, new_counts):
    print(f"{year} | {count}")

with open('bird_poisson_gen.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['year', 'bird count'])
    for row in range(len(new_years)):
        writer.writerow((new_years[row], new_counts[row]))