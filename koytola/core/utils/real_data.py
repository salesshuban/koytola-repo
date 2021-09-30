from ...profile.models import (
    SocialChannel,
    SocialChannelUrlFormat,
    LinkWidget
)

link_widgets_data = [
    {
        "name": "Spotify",
        "description": "Spotify song play widget. Enter your song url to",
        "parameters": {},
        "is_active": True,
    },
    {
        "name": "Shopify",
        "description": "Enter your product url to display your product properties",
        "parameters": {},
        "is_active": True,
    },
]

social_channels_data = [
    {
        "name": "Amazon",
        "url_schema": "",
        "is_active": True,
        "url_format": ["amazon.com"],
    },
    {
        "name": "Apple Music",
        "url_schema": "",
        "is_active": True,
        "url_format": ["music.apple.com"],
    },
    {
        "name": "Behance",
        "url_schema": "https://www.behance.net/{username}",
        "is_active": True,
        "url_format": ["behance.net"]
    },
    {
        "name": "CashApp",
        "url_schema": "https://cash.app/${username}",
        "is_active": True,
        "url_format": ["cash.app"]
    },
    {
        "name": "Discord",
        "url_schema": "https://discordapp.com/users/{username}",
        "is_active": True,
        "url_format": ["discord.com", "discordapp.com"]
    },
    {
        "name": "Facebook",
        "url_schema": "https://www.facebook.com/{username}",
        "is_active": True,
        "url_format": ["facebook.com", "fb.com"]
    },
    {
        "name": "Flickr",
        "url_schema": "https://www.flickr.com/people/{username}",
        "is_active": True,
        "url_format": ["flickr.com"]
    },
    {
        "name": "GitHub",
        "url_schema": "https://github.com/{username}",
        "is_active": True,
        "url_format": ["github.com"]
    },
    {
        "name": "Instagram",
        "url_schema": "https://www.instagram.com/{username}/",
        "is_active": True,
        "url_format": ["instagram.com"]
    },
    {
        "name": "Line",
        "url_schema": "https://line.me/R/ti/p/{username}",
        "is_active": True,
        "url_format": ["line.me"]
    },
    {
        "name": "Linkedin",
        "url_schema": "https://www.linkedin.com/in/{username}",
        "is_active": True,
        "url_format": ["linkedin.com"]
    },
    {
        "name": "Medium",
        "url_schema": "https://{username}.medium.com/",
        "is_active": True,
        "url_format": ["medium.com"]
    },
    {
        "name": "Messenger",
        "url_schema": "",
        "is_active": False,
        "url_format": ["messenger.com"],
    },
    {
        "name": "Pinterest",
        "url_schema": "https://www.pinterest.com/{username}",
        "is_active": True,
        "url_format": ["pinterest.com"]
    },
    {
        "name": "Quora",
        "url_schema": "https://www.quora.com/{username}",
        "is_active": True,
        "url_format": ["quora.com"]
    },
    {
        "name": "Reddit",
        "url_schema": "https://www.reddit.com/r/{username}",
        "is_active": True,
        "url_format": ["reddit.com"]
    },
    {
        "name": "Skype",
        "url_schema": "",
        "is_active": True,
        "url_format": ["skype.com", "join.skype.com"]
    },
    {
        "name": "Slack",
        "url_schema": "https://{username}.slack.com/",
        "is_active": True,
        "url_format": ["slack.com", "join.slack.com"]
    },
    {
        "name": "Snapchat",
        "url_schema": "https://snapchat.com/add/{username}",
        "is_active": True,
        "url_format": ["snapchat.com"]
    },
    {
        "name": "Spotify",
        "url_schema": "",
        "is_active": True,
        "url_format": ["spotify.com", "open.spotify.com"]
    },
    {
        "name": "Telegram",
        "url_schema": "https://t.me/{username}",
        "is_active": True,
        "url_format": ["telegram.org", "t.me"]
    },
    {
        "name": "TikTok",
        "url_schema": "https://www.tiktok.com/@{username}",
        "is_active": True,
        "url_format": ["tiktok.com"]
    },
    {
        "name": "Tumblr",
        "url_schema": "https://{username}.tumblr.com/",
        "is_active": True,
        "url_format": ["tumblr.com"]
    },
    {
        "name": "Twitch",
        "url_schema": "https://www.twitch.tv/{username}",
        "is_active": True,
        "url_format": ["twitch.tv"]
    },
    {
        "name": "Twitter",
        "url_schema": "https://twitter.com/{username}",
        "is_active": True,
        "url_format": ["twitter.com"]
    },
    {
        "name": "QQ",
        "url_schema": "",
        "is_active": False,
        "url_format": ["qq.com"]
    },
    {
        "name": "QZone",
        "url_schema": "",
        "is_active": False,
        "url_format": ["qzone.qq.com"]
    },
    {
        "name": "WeChat",
        "url_schema": "",
        "is_active": False,
        "url_format": ["wechat.com"]
    },
    {
        "name": "WhatsApp",
        "url_schema": "https://wa.me/{username}",
        "is_active": True,
        "url_format": ["whatsapp.com", "wa.me"]
    },
    {
        "name": "Venmo",
        "url_schema": "https://venmo.com/{username}",
        "is_active": True,
        "url_format": ["venmo.com"]
    },
    {
        "name": "VK",
        "url_schema": "https://vk.com/{username}",
        "is_active": True,
        "url_format": ["vk.com"]
    },
    {
        "name": "VSCO",
        "url_schema": "https://vsco.co/{username}",
        "is_active": True,
        "url_format": ["vsco.co"]
    },
    {
        "name": "Youtube",
        "url_schema": "https://www.youtube.com/user/{username}",
        "is_active": True,
        "url_format": ["youtube.com", "youtu.be"]
    },
]


def create_link_widgets(save=True):
    for data in link_widgets_data:
        link_widget = LinkWidget(
            name=data["name"],
            description=data["description"],
            parameters=data["parameters"],
            is_active=data["is_active"],
        )

        if save:
            link_widget.save()

        yield f"Social Channel: {link_widget.name} generated."


def create_social_channels(save=True):
    for data in social_channels_data:
        social_channel = SocialChannel(
            name=data["name"],
            url_schema=data["url_schema"],
            is_active=data["is_active"],
        )

        if save:
            social_channel.save()

        for url_format in data["url_format"]:
            format = SocialChannelUrlFormat(
                url=url_format,
                social_channel_id=social_channel.id
            )

            if save:
                format.save()

            yield f"Social Channel Url Format: {format.url} generated."
        yield f"Social Channel: {social_channel.name} generated."
