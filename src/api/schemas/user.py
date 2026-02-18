from pydantic import (
    BaseModel,
    EmailStr,
    SecretStr,
    field_validator,
    ConfigDict,
    model_validator,
)
from typing import Optional
from pydantic_core.core_schema import FieldValidationInfo
from uuid import UUID


class UserBaseModel(BaseModel):
    user_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserBaseModel):
    user_name: str
    email: EmailStr
    phone: str
    password_1: SecretStr
    password_2: SecretStr

    @field_validator("password_1")
    @classmethod
    def password_validation(cls, v: SecretStr):
        if not v.get_secret_value():
            raise ValueError("Password is required")
        if len(v.get_secret_value()) < 12:
            raise ValueError("Password length must be 12 character")
        return v

    @field_validator("password_2")
    @classmethod
    def passwords_match(cls, v, info: FieldValidationInfo):

        if (
            "password_1" in info.data
            and v.get_secret_value() != info.data["password_1"].get_secret_value()
        ):
            raise ValueError("passwords do not match")
        return v


class UserUpdate(BaseModel):
    old_password: Optional[SecretStr]
    new_password: Optional[SecretStr]

    @model_validator(mode="after")
    def check_old_password_exis(self):
        if self.new_password and not self.old_password:
            raise ValueError("Old password is required to set a new password")
        return self


# TODO NEED TO FINISH THE PASSWORD UODATE RULE AND CREATE A VALIDATION FOR CREATINF A NEW PASSWORD


class UserLogin(BaseModel):
    user_name: str
    password: SecretStr
