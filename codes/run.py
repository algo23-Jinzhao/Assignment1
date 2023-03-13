from getFactors import get_factors
from getOrders import get_orders
from getResults import get_results

if __name__ == '__main__':
    get_factors('./data', './factors')
    get_orders('./factors', './orders', 'vnsp_llt')
    get_results('./orders', './figures', 'vnsp_llt')