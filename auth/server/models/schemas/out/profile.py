from server.models.schemas.base.users import ProfileBase, UserBase


class ProfileResponse(ProfileBase):
    user_account: UserBase
