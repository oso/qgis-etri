from .types import Categories, Category
from .types import CategoriesProfiles, CategoryProfile
from .types import Limits

def generate_categories(number, prefix='cat'):
    cats = Categories()
    for i in range(number):
        c = Category()
        c.id = "%s%d" % (prefix, i+1)
        c.rank = i+1
        cats.append(c)
    return cats

def generate_categories_profiles(cats, prefix='b'):
    cat_ids = cats.get_ordered_categories()
    cps = CategoriesProfiles()
    for i in range(len(cats)-1):
        l = Limits(cat_ids[i], cat_ids[i+1])
        cp = CategoryProfile("%s%d" % (prefix, i+1), l)
        cps.append(cp)
    return cps
