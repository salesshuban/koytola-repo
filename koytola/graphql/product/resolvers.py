import graphene
from django.db.models import Q, Count, Subquery, Avg, Value, IntegerField, CharField, F
from django.db.models.functions import Coalesce
from ...blog import models
import requests, csv, json, io, os, sys
import urllib
from django_countries.fields import Country
from django.db.models.expressions import RawSQL
from ...product.models import (
    Category,
    Product,
    ProductImage,
    ProductVideo,
    HSCodeAndProduct,
    Offers,
    PortDeals,
    PortProductGallery,
    ProductReviews,
    ProductQuery,
    OpenExchange,
    User,
    Company,
    Industry,
    SuccessStory,
    CertificateType,
    Certificate,
    Contact,
    SocialResponsibility,
    Brochure,
    Images,
    Address,
    Representative,
    Video
)
from ...core.exceptions import PermissionDenied
from ...core.permissions import ProductPermissions
from ..core.validators import validate_one_of_args_is_in_query
from ..utils.filters import filter_by_query_param
from ...profile.models import Roetter, CertificateType
from datetime import datetime

CATEGORY_SEARCH_FIELDS = ("name",)


def resolve_category(info, category_id=None, slug=None):
    validate_one_of_args_is_in_query("id", category_id, "slug", slug)

    if category_id:
        _model, category_pk = graphene.Node.from_global_id(category_id)
        return Category.objects.filter(id=category_pk).first()
    if slug:
        return Category.objects.filter(slug=slug).first()


def resolve_currency_exchange(info, base, **kwargs):
    return OpenExchange.objects.filter(base=base).first()


def resolve_categories(info, query, **_kwargs):
    qs = Category.objects.filter(parent=None)
    return filter_by_query_param(qs, query, CATEGORY_SEARCH_FIELDS)


def resolve_product(info, product_id=None, slug=None):
    assert product_id or slug, "No product ID or slug provided."
    user = info.context.user
    if slug is not None:
        if user.is_authenticated and not user.is_buyer:
            return Product.objects.filter(slug=slug).first()
        else:
            return Product.objects.filter(slug=slug, is_published=True, company__is_published=True).first()
    else:
        _model, product_pk = graphene.Node.from_global_id(product_id)
        if product_id is not None:
            if user.is_authenticated and not user.is_buyer:
                return Product.objects.filter(pk=product_pk, ).first()
            else:
                product = Product.objects.filter(
                    Q(company__user=user) & Q(pk=product_pk), is_published=True, company__is_published=True
                ).first()
                if product:
                    return product
    raise PermissionDenied()


def resolve_products(info, company_id=None, **_kwargs):
    user = info.context.user
    if company_id:
        _model, company_pk = graphene.Node.from_global_id(company_id)
        return Product.objects.filter(company__pk=company_pk).order_by("name")
    if user and not user.is_anonymous and not user.is_superuser:
        return Product.objects.filter(company__user=user).order_by("name")
    elif user.is_superuser:
        return Product.objects.filter().order_by("-creation_date")
    else:
        return Product.objects.filter(is_published=True, company__is_published=True).order_by("name")


def resolve_search_hscode_and_product(info, key, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        return HSCodeAndProduct.objects.filter(Q(hs_code__contains=key) | Q(product_name__contains=key))
    raise PermissionDenied()


def resolve_product_image(info, product_image_id=None):
    assert product_image_id, "No product image ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, product_image_pk = graphene.Node.from_global_id(product_image_id)
        if product_image_id is not None:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                return ProductImage.objects.filter(pk=product_image_pk).first()
            else:
                product_image = ProductImage.objects.filter(pk=product_image_pk).first()
                if product_image.product.company.is_published and product_image.product.company.is_active:
                    return product_image
    raise PermissionDenied()


def resolve_product_images(info, **_kwargs):
    product_id = _kwargs.get("product_id")
    user = info.context.user
    if user and not user.is_anonymous:
        if not product_id:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                return ProductImage.objects.all().order_by("index")
        else:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                model, product_pk = graphene.Node.from_global_id(product_id)
                product = Product.objects.filter(pk=product_pk).order_by("index").first()
                return product.images
            else:
                model, product_pk = graphene.Node.from_global_id(product_id)
                product = Product.objects.filter(Q(company__user=user) & Q(pk=product_pk)).order_by("index").first()
                if product.company.is_published and product.company.is_active:
                    return product.images
    raise PermissionDenied()


def resolve_product_video(info, product_video_id=None):
    assert product_video_id, "No product video ID provided."
    user = info.context.user
    if user and not user.is_anonymous:
        _model, product_video_pk = graphene.Node.from_global_id(product_video_id)
        if product_video_id is not None:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                return ProductVideo.objects.filter(pk=product_video_pk).first()
            else:
                product_video = ProductImage.objects.filter(pk=product_video_pk).first()
                if product_video.product.company.is_published and product_video.product.company.is_active:
                    return product_video
    raise PermissionDenied()


def resolve_product_videos(info, **_kwargs):
    product_id = _kwargs.get("product_id")
    user = info.context.user
    if user and not user.is_anonymous:
        if not product_id:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                return ProductVideo.objects.all()
        else:
            if user.has_perms([ProductPermissions.MANAGE_PRODUCTS]):
                model, product_pk = graphene.Node.from_global_id(product_id)
                product = Product.objects.filter(pk=product_pk).first()
                return product.videos
            else:
                model, product_pk = graphene.Node.from_global_id(product_id)
                product = Product.objects.filter(Q(company__user=user) & Q(pk=product_pk)).first()
                if product.company.is_published and product.company.is_active:
                    return product.videos
    raise PermissionDenied()


def resolve_offer(info, offer_id=None, slug=None):
    assert offer_id or slug, "No product ID or slug provided."
    if slug is not None:
        return Offers.objects.filter(slug=slug, is_active=True).first()
    else:
        _model, offer_pk = graphene.Node.from_global_id(offer_id)
        return Offers.objects.filter(id=offer_pk, is_active=True).first()


def resolve_offers(info, company_id=None, **_kwargs):
    if company_id is not None:
        _model, company_pk = graphene.Node.from_global_id(company_id)
        return Offers.objects.filter(company__id=company_pk, is_active=True, end_date__gte=datetime.now()).order_by(
            "-created_at")
    if info.context.user.is_anonymous or info.context.user.is_superuser:
        return Offers.objects.filter(is_active=True, end_date__gte=datetime.now()).order_by("-created_at")
    else:
        return Offers.objects.filter(company__user=info.context.user, is_active=True,
                                     end_date__gte=datetime.now()).order_by("-created_at")


def resolve_port_deal(info, id=None, slug=None):
    assert id or slug, "No product ID or slug provided."
    if slug is not None:
        return PortDeals.objects.filter(slug=slug).first()
    else:
        _model, offer_pk = graphene.Node.from_global_id(id)
        return PortDeals.objects.filter(id=offer_pk).first()


def resolve_port_deals(info, company_id=None, **_kwargs):
    PortDeals.objects.filter(end_date__lte=datetime.now(), is_expire=False).update(is_expire=True)
    if company_id is not None:
        _model, company_pk = graphene.Node.from_global_id(company_id)
        return PortDeals.objects.filter(company__id=company_pk).order_by("-created_at")
    if info.context.user.is_anonymous or info.context.user.is_superuser:
        return PortDeals.objects.filter(is_active=True, end_date__gte=datetime.now()).order_by("-created_at")
    else:
        return PortDeals.objects.filter(company__user=info.context.user).order_by("-created_at")


def resolve_search_product(info, key, **kwargs):
    if Product.objects.filter(Q(hs_code__icontains=key) | Q(name__icontains=key)).exists():
        field = 'hs_code' if key.isnumeric() else 'name'
        table = Product.objects.model._meta.db_table
        if not info.context.user.is_anonymous and not info.context.user.is_superuser and info.context.user.is_seller:
            query = f"SELECT MAX(id)  FROM {table} WHERE company_id=%s AND {field} iLIKE %s GROUP By {field}"
            return Product.objects.filter(id__in=RawSQL(query, (info.context.user.companies.id, f'%{key}%',)),
                                          is_published=True, company__is_published=True)
        else:
            query = f"SELECT MAX(id)  FROM {table} WHERE {field} iLIKE %s GROUP By {field}"
            return Product.objects.filter(id__in=RawSQL(query, (f'%{key}%',)), is_published=True,
                                          company__is_published=True)
    else:
        return []


def resolve_search_port_deals(info, key, **kwargs):
    return PortDeals.objects.filter(
        Q(slug__contains=key) |
        Q(location__contains=key) |
        Q(company__name__contains=key) |
        Q(product_name__contains=key) |
        Q(hs_code__contains=key) |
        Q(name__contains=key) |
        Q(certificate__contains=key) |
        Q(start_date__contains=key) |
        Q(end_date__contains=key)
    ).annotate(dcount=Count('id')).order_by()


def resolve_product_reviews(info, product_id, **kwargs):
    return ProductReviews.objects.filter(product__id=product_id)


def resolve_product_rosetters(info, **_kwargs):
    return Roetter.objects.filter(type="Product", is_active=True)


def resolve_product_certificate_type(info, **_kwargs):
    return CertificateType.objects.filter(type="Product", is_active=True)


def resolve_product_queries(info, company_id=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        if company_id is not None:
            _model, company_pk = graphene.Node.from_global_id(company_id)
            return ProductQuery.objects.filter(product__company__id=company_pk)
        else:
            return ProductQuery.objects.filter(user=user)
    return PermissionDenied()


def resolve_product_query(info, id=None, **_kwargs):
    user = info.context.user
    if user and not user.is_anonymous:
        _model, product_query_pk = graphene.Node.from_global_id(id)
        return ProductQuery.objects.filter(id=product_query_pk).first()
    return PermissionDenied()


def resolve_port_product_gallery(info, port_deal_id=None, **_kwargs):
    _model, port_deal_pk = graphene.Node.from_global_id(port_deal_id)
    return PortProductGallery.objects.filter(product__id=port_deal_pk)


def blog_data_create():
    blog_csv_reader = list(csv.reader((open('./././filenameblog.csv', 'r'))))
    for i in blog_csv_reader[1:]:
        if not models.Blog.objects.filter(title=i[9]).exists():
            print(i[1], i[2], i[3])
            blog = {'seo_title': i[4], 'seo_description': i[5], 'category': i[6],
                    'user': models.User.objects.filter(is_superuser=True).first(), 'slug': i[8], 'is_published': i[15],
                    'title': i[9], 'short_description': i[11], 'description': i[12], 'tags': i[13], 'is_active': i[14]}
            obj = models.Blog.objects.create(**blog)
            img_file = open('./././bs/' + i[10], 'rb')
            image = io.BytesIO(img_file.read())
            obj.image.save(i[10], image)
            obj.save()


def success_story_data_insert():
    ss_csv_reader = list(csv.reader((open('./././filenamesuccess story.csv', 'r'))))
    for j in ss_csv_reader[1:]:

        if not SuccessStory.objects.filter(title=j[1]).exists():
            success_story = {'title': j[1], 'name': j[2], 'description': j[3], 'location': j[5],
                             'company_name': j[6], 'slug': j[7], 'tags': j[8], 'is_active': j[9], 'is_published': j[10]}
            obj = SuccessStory.objects.create(**success_story)
            img_file = open('./././bs/' + j[4], 'rb')
            image = io.BytesIO(img_file.read())
            obj.image.save(j[10], image)
            obj.save()


def user_data_insert():
    ss_csv_reader = list(csv.reader((open('./././filenameuser.csv', 'r'))))
    for j in ss_csv_reader[1:]:
        if not User.objects.filter(email=j[6]).exists():
            user = {'email': j[6], 'first_name': j[7], 'last_name': j[9], 'phone': j[10], 'is_seller': j[12],
                    'is_staff': j[13], 'is_superuser': j[3], 'note': j[14]}
        else:
            obj = User.objects.get(email=j[6])
            if j[6] == "admin@koytola.com":
                obj.set_password('@Koytola!Admin#')
            else:
                obj.set_password('koytola')
            obj.save()


def company_data_insert():
    ss_csv_reader = list(csv.reader((open('./././filenameCompany.csv', 'r'))))
    for j in ss_csv_reader[1:]:
        user = User.objects.filter(email=j[7]).first()
        if not Company.objects.filter(user=user).exists():
            company = {'user': user, 'is_published': eval(j[4]), 'seo_title': j[5], 'seo_description': j[6],
                       'slug': j[8], 'name': j[9], 'website': j[10], 'phone': j[11], 'founded_year': j[15],
                       'no_of_employees': j[16], 'content': json.loads(j[19]) if j[19] else {},
                       'content_plaintext': j[18], 'vision': j[19],
                       'brands': j[20], 'membership': j[21], 'is_brand': eval(j[22]), 'is_verified': eval(j[32]),
                       'industry': Industry.objects.filter(name=j[23]).first(), 'export_countries': eval(j[24]),
                       'size': j[25], 'type': j[26], 'organic_products': eval(j[27]),
                       'private_label': eval(j[28]), 'female_leadership': eval(j[29]), 'branded_value': eval(j[30]),
                       'is_active': eval(j[31])
                       }
            Company.objects.create(**company)


def product_data_insert():
    ss_csv_reader = list(csv.reader((open('./././filenameproduct.csv', 'r'))))
    for j in ss_csv_reader[1:]:
        if not Product.objects.filter(slug=j[10]).exists():
            company = Company.objects.filter(name=j[8]).first()
            category = Category.objects.filter(name=j[14]).first()
            product = {
                'company': company, 'name': j[9], 'slug': j[10], 'description': eval(j[11]) if j[11] else {},
                'description_plaintext': j[12],
                'hs_code': j[13], 'category': category, 'unit_number': j[15], 'unit': j[16], 'unit_price': j[17],
                'currency': j[18], 'minimum_order_quantity': j[19], 'quantity_unit': j[20], 'organic': eval(j[21]),
                'private_label': eval(j[22]), 'is_active': eval(j[23]), 'is_published': eval(j[24]),
                'is_brand': eval(j[25]), 'brand': j[26], 'tags': j[27], 'packaging': j[28], 'delivery': j[29],
                'delivery_time_option': j[30], 'delivery_time': j[31],
            }
            Product(**product).save()
        else:
            product = Product.objects.get(slug=j[10])
            product.description = eval(j[11]) if j[11] else {}
            product.save()


def model_data_insert(obj, filename):
    try:
        ss_csv_reader = list(csv.reader((open(f'./././{filename}', 'r'))))
        for j in ss_csv_reader[1:]:
            data = {i.replace(' ', '_'): '' for i in ss_csv_reader[0]}

            for index, key in enumerate(data):
                if key == "company":
                    data[key] = Company.objects.filter(name=j[index]).first()
                elif key == "product":
                    data[key] = Product.objects.filter(slug=j[index]).first()
                elif key == "category":
                    data[key] = Category.objects.filter(name=j[index]).first()
                elif key == "export_countries":
                    data[key] = eval(j[index])
                # elif key == "type":
                #     data[key] = CertificateType.objects.filter(name=j[index]).first()
                else:
                    data[key] = j[index]
            # if Company.objects.filter(slug=data['slug']).exists():
            #     continue
            if data['product'] is None:
                continue
            # if not data['product']:
            #     continue
            data.pop('ID')
            # data.pop('user')

            # data.pop('creation_date')
            # data.pop('update_date')
            # data.pop('publication_date')
            # if data['content']:
            #     data['content'] = eval(data['content'])
            data.pop('ppoi')
            # data.pop('address')
            # data.pop('industry')
            files = []
            for k in ("image", 'photo', 'avatar', 'video', 'background_image', 'logo', 'certificate'):
                if k in data:
                    files.append(("https://testing-backend.koytola.com/media/" + data[k], k))
                    data.pop(k)
            if data['index'] == '' or not data['index']:
                data['index'] = None

            obj_save = obj(**data)
            print(data)
            if any(files):
                for file in files:
                    try:
                        img_file = urllib.request.urlopen(file[0]).read()
                        image = io.BytesIO(img_file)
                        if file[1] == 'image':
                            obj_save.image.save(file[0].split('/')[-1], image)
                        if file[1] == 'photo':
                            obj_save.photo.save(file[0].split('/')[-1], image)
                        if file[1] == 'avatar':
                            obj_save.avatar.save(file[0].split('/')[-1], image)
                        if file[1] == 'video':
                            obj_save.video.save(file[0].split('/')[-1], image)
                        if file[1] == 'background_image':
                            obj_save.background_image.save(file[0].split('/')[-1], image)
                        if file[1] == 'logo':
                            obj_save.logo.save(file[0].split('/')[-1], image)
                        if file[1] == 'certificate':
                            obj_save.certificate.save(file[0].split('/')[-1], image)
                    except Exception as e:
                        print(e)
                        continue
            obj_save.save()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        return f'{e, exc_type, fname, exc_tb.tb_lineno}'


def resolve_data_insert(info, **_kwargs):
    product_data_insert()
    # r = model_data_insert(ProductImage, 'filenameproduct image.csv')
    return "Done"
