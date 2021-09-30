from ..celeryconf import app
from ..core.utils import create_thumbnails
from .models import Category, ProductImage


@app.task
def create_product_thumbnails(image_id: str):
    """Take a ProductImage model and create thumbnails for it."""
    create_thumbnails(pk=image_id, model=ProductImage, size_set="products")


@app.task
def create_category_background_image_thumbnails(category_id: str):
    """Take a Product model and create the background image thumbnails for it."""
    create_thumbnails(
        pk=category_id,
        model=Category,
        size_set="background_images",
        image_attr="background_image",
    )
