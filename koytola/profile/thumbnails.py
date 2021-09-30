from ..celeryconf import app
from ..core.utils import create_thumbnails
from .models import Company


@app.task
def create_company_logo_thumbnails(company_id):
    """Create thumbnails for company company logo."""
    create_thumbnails(
        pk=company_id, model=Company, size_set="company_logos", image_attr="logo"
    )
