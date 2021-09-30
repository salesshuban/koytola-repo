import graphene
from ....profile import models
from ...core.mutations import ModelDeleteMutation, ModelMutation
from ...core.types import Upload
from ...core.types.common import ProfileError
from ...profile.types import Company, Video
from ..utils import company_permission
from ...core.fields import FilterInputConnectionField


class VideoInput(graphene.InputObjectType):
    video = Upload(description="Company video file.", required=False)
    youtube_url = graphene.String(description="The youtube url of company video.")
    description = graphene.String(description="The description of company video.")
    sort_order = graphene.Int(description="The order of your video.")


class VideoCreate(ModelMutation):
    videos = FilterInputConnectionField(Video, description="A created video.")

    class Arguments:
        company_id = graphene.ID(
            required=True, description="ID of a company to add video."
        )
        input = VideoInput(
            required=True, description="Fields required to create a video."
        )

    class Meta:
        description = "Creates a new video."
        model = models.Video
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, company_id, **data):
        company = cls.get_node_or_error(
            info, company_id, only_type=Company, field="company_id"
        )
        company_permission(info, company)
        instance = cls.get_instance(info, **data)
        instance.company = company
        cleaned_input = cls.clean_input(info, instance, data.get("input"))
        instance = cls.construct_instance(instance, cleaned_input)
        cls.clean_instance(info, instance)
        cls.save(info, instance, cleaned_input)
        return VideoCreate(videos=models.Video.objects.filter(company=company))

    @classmethod
    def get_type_for_model(cls):
        return Video


class VideoUpdate(ModelMutation):
    videos = FilterInputConnectionField(Video, description="A created video.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a video to update."
        )
        input = VideoInput(
            required=True, description="Fields required to update a video."
        )

    class Meta:
        description = "Updates an existing ticket."
        model = models.Video
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        video = cls.get_node_or_error(
            info, id, only_type=Video, field="id"
        )
        company_permission(info, video.company)
        cleaned_input = cls.clean_input(info, video, data.get("input"))
        contact = cls.construct_instance(video, cleaned_input)
        cls.clean_instance(info, contact)
        cls.save(info, contact, cleaned_input)
        return VideoUpdate(videos=models.Video.objects.filter(company=company))

    @classmethod
    def get_type_for_model(cls):
        return Video


class VideoDelete(ModelDeleteMutation):
    videos = FilterInputConnectionField(Video, description="A created video.")

    class Arguments:
        id = graphene.ID(
            required=True, description="ID of a video to delete."
        )

    class Meta:
        description = "Deletes a video."
        model = models.Video
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, id, **data):
        video = cls.get_node_or_error(
            info, id, only_type=Video, field="id"
        )
        company_permission(info, video.company)
        company = video.company
        video.delete()
        return VideoDelete(videos=models.Video.objects.filter(company=company))


class VideoIndexUpdate(ModelMutation):
    videos = FilterInputConnectionField(Video, description="An updated video.")

    class Arguments:
        ids = graphene.List(graphene.ID, required=True, description="Company Video.")

    class Meta:
        description = "Video index update."
        model = models.Video
        error_type_class = ProfileError
        error_type_field = "profile_errors"

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, root, info, ids, **data):
        video_list = []
        for index, id in enumerate(ids):
            video = cls.get_node_or_error(info, id, only_type=Video, field="id")
            company_permission(info, video.company)
            video.index = index
            video.save()
            video_list.append(video)
        return VideoIndexUpdate(videos=video_list)
