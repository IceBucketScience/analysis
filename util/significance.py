import numpy as np
from scipy.stats import ttest_ind, ks_2samp, mannwhitneyu, shapiro, t

def test_significance(d1, d2):
    print '[D1] size:', d1.size, '; mean:', d1.mean(), '; median:', d1.median(), 'normality:', shapiro(d1.values)
    print '[D2] size:', d2.size, '; mean:', d2.mean(), '; median:', d2.median(), 'normality:', shapiro(d2.values)

    print 't-test:', ttest_ind(d1.values, d2.values, equal_var=False)
    print 'ks-test:', ks_2samp(d1.values, d2.values)

    mann_whitney = mannwhitneyu(d1.values, d2.values)
    print 'mann-whitney-u:', (mann_whitney[0], mann_whitney[1] * 2)

    print '% difference (mean):', (d2.mean() - d1.mean())/float(d1.mean()), '; % difference (median):', (d2.median() - d1.median())/float(d1.median())

    df = ((var_size_ratio(d1) + var_size_ratio(d2))**2)/((var_size_ratio(d1)**2)/(float(d1.size) - 1) + (var_size_ratio(d2)**2)/(float(d2.size) - 1))
    t_val = t.ppf(0.05, df)
    delta = d2.mean() - d1.mean()
    conf_delta = t_val * np.sqrt(d1.var()/float(d1.size) + d2.var()/float(d2.size))
    print '95% conf int:', ((delta - conf_delta)/d1.mean(), (delta + conf_delta)/d1.mean())

def var_size_ratio(d):
    return d.var()/float(d.size)