from ...account.models import User
from ...product.models import Category, Product
from ...profile.models import Company
from ..core.dataloaders import DataLoader


class UserByIdLoader(DataLoader):
    context_key = "user_by_id"

    def batch_load(self, keys):
        user = User.objects.in_bulk(keys)
        return [user.get(user_id) for user_id in keys]


class CategoryByIdLoader(DataLoader):
    context_key = "category_by_id"

    def batch_load(self, keys):
        category = Category.objects.in_bulk(keys)
        return [category.get(category_id) for category_id in keys]


class CompanyByIdLoader(DataLoader):
    context_key = "company_by_id"

    def batch_load(self, keys):
        company = Company.objects.in_bulk(keys)
        return [company.get(company_id) for company_id in keys]


class ProductByIdLoader(DataLoader):
    context_key = "product_by_id"

    def batch_load(self, keys):
        product = Product.objects.in_bulk(keys)
        return [product.get(product_id) for product_id in keys]
